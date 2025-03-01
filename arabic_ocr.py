# -*- coding: utf-8 -*-
"""arabic_ocr.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1i-fz-mV1Gw7utIkVid9OqlcyKhHHepPm
"""









"""https://huggingface.co/spaces/MohamedRashad/Arabic-Nougat/blob/main/book_page1.jpeg

https://huggingface.co/MohamedRashad/arabic-small-nougat
"""

!pip install python-Levenshtein

from PIL import Image
import torch
from transformers import NougatProcessor, VisionEncoderDecoderModel

# Load the model and processor
processor = NougatProcessor.from_pretrained("MohamedRashad/arabic-small-nougat")
model = VisionEncoderDecoderModel.from_pretrained("MohamedRashad/arabic-small-nougat")
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

context_length = 2048

def predict(img_path):
    # prepare PDF image for the model
    image = Image.open(img_path)
    pixel_values = processor(image, return_tensors="pt").pixel_values

    # generate transcription
    outputs = model.generate(
        pixel_values.to(device),
        min_length=1,
        max_new_tokens=context_length,
        bad_words_ids=[[processor.tokenizer.unk_token_id]],
    )

    page_sequence = processor.batch_decode(outputs, skip_special_tokens=True)[0]
    page_sequence = processor.post_process_generation(page_sequence, fix_markdown=False)
    return page_sequence

print(predict("/content/book_page1.jpeg"))

"""# مقدمة

قبل أن يظهر كتاب الأستاذ محمد حسنين هيكل المشهور «خريف الغضب» في الأسواق، نُشر على هيئة سلسلة من المقالات في صحيفة «الوطن» الكويتية، وطوال الوقت الذي كانت تُتشر فيه هذه المقالات، كانت سلسلةٌ أخرى من الأفكار تتفاعل في ذهني وتتبلور يومًا بعد يوم. كان كتاب هيكل، بغير شك، هو السبب المباشر في إثارة هذه الأفكار، ومع ذلك فقد كانت أصولها أبعد من ذلك وأعمق بكثير؛ إذ كانت في نهاية المطاف تأملات في تلك الأزمة العقلية الشاملة التي شوَّهت تفكيرنا، حُكامًا ومحكومين، في النصف الثاني من القرن العشرين. وحين اطلعت على ردود الفعل التي أثارها كتاب هيكل، أو ما نُشر منه، في الأوساط الرسمية والإعلامية والثقافية المصرية، والطريقة التي استجاب بها الناس له، ما بين موافقٍ ومخالف، ازدادت الأمور في ذهني وضوحًا، وتبيَّن لي أن المناخ السائد، الذي تولَّدت عنه هذه الأزمة العقلية، يلف الجميع، من مؤيدين ومعارضين، مهما بدا من اختلاف ردود أفعالهم في الظاهر، وكانت المهمة التي أخذتها على عاتقي هي أن أُحدِّد أبعاد هذه الأزمة، وأثبت أن المشكلة ليست مشكلة هيكل وحده، أو مشكلة التضاد بين هيكل وتلك القوى التي وقفت تحتُجٌ وتعترض عليه، وإنما هي أوسع من ذلك وأخطر، فقد تشوَّهت أشياءٌ كثيرة في عقولنا، بفعل فترة القمع الطويلة التي لم تسمح لفكرنا بأن ينمو ويتطوَّر بحرية، وإذا كان هذا التشويه قد ظهر بوضوحٍ كامل في معركة «خريف الغضب»، بين أنصار هيكل وخصومه، فإن هذه المعركة لم تكن في الواقع إلا مظهرًا واحدًا لداءٍ أصبح مُتأصِّلًا في عقولنا، ولطريقةٍ في التفكير فرضت نفسها على مختلف أطراف الصراع السياسي والاجتماعي الراهن.


"""



from PIL import Image
import matplotlib.pyplot as plt

image = Image.open("/content/book_page1.jpeg")  # استبدل المسار بمسار الصورة

plt.imshow(image)
plt.axis('off')  # لإخفاء المحاور
plt.show()

import requests
from io import BytesIO

image_url = "رابط الصورة"
response = requests.get(image_url)
image = Image.open(BytesIO(response.content))

plt.imshow(image)
plt.axis('off')
plt.show()









!pip install pymupdf

from PIL import Image
import torch
from transformers import NougatProcessor, VisionEncoderDecoderModel
import fitz  # PyMuPDF للتعامل مع ملفات PDF
import os

# Load the model and processor
processor = NougatProcessor.from_pretrained("MohamedRashad/arabic-small-nougat")
model = VisionEncoderDecoderModel.from_pretrained("MohamedRashad/arabic-small-nougat")
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

context_length = 2048

def process_pdf(pdf_path, output_dir="temp_images"):
    # إنشاء مجلد مؤقت لتخزين الصور إذا لم يكن موجودًا
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # فتح ملف PDF
    pdf_document = fitz.open(pdf_path)
    all_text = ""

    # حلقة على جميع الصفحات
    for page_num in range(len(pdf_document)):
        # تحويل الصفحة إلى صورة
        page = pdf_document.load_page(page_num)
        pix = page.get_pixmap()

        # حفظ الصورة مؤقتًا
        img_path = os.path.join(output_dir, f"page_{page_num + 1}.png")
        pix.save(img_path)

        # معالجة الصورة واستخراج النص
        try:
            text = predict(img_path)
            all_text += f"\n\n--- صفحة {page_num + 1} ---\n\n{text}"
            print(f"تم معالجة صفحة {page_num + 1}")
        except Exception as e:
            print(f"خطأ في معالجة صفحة {page_num + 1}: {e}")

        # حذف الصورة المؤقتة لتوفير المساحة
        os.remove(img_path)

    # إغلاق ملف PDF
    pdf_document.close()
    return all_text

def predict(img_path):
    # تحميل وتحضير الصورة للنموذج
    image = Image.open(img_path)
    pixel_values = processor(image, return_tensors="pt").pixel_values

    # توليد النص
    outputs = model.generate(
        pixel_values.to(device),
        min_length=1,
        max_new_tokens=context_length,
        bad_words_ids=[[processor.tokenizer.unk_token_id]],
    )

    page_sequence = processor.batch_decode(outputs, skip_special_tokens=True)[0]
    page_sequence = processor.post_process_generation(page_sequence, fix_markdown=False)
    return page_sequence

# استخدام الكود
pdf_path = "/content/arabic_book.pdf"  # استبدل هذا بمسار ملف PDF الخاص بك
extracted_text = process_pdf(pdf_path)

# حفظ النص في ملف (اختياري)
with open("extracted_text.txt", "w", encoding="utf-8") as f:
    f.write(extracted_text)

print("تم استخراج النص من الكتاب بنجاح!")

from PIL import Image
import torch
from transformers import NougatProcessor, VisionEncoderDecoderModel
import fitz  # PyMuPDF للتعامل مع ملفات PDF
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

# Load the model and processor
processor = NougatProcessor.from_pretrained("MohamedRashad/arabic-small-nougat")
model = VisionEncoderDecoderModel.from_pretrained("MohamedRashad/arabic-small-nougat")
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

context_length = 2048

def predict(img_path):
    # تحميل وتحضير الصورة للنموذج
    image = Image.open(img_path)
    pixel_values = processor(image, return_tensors="pt").pixel_values

    # توليد النص
    outputs = model.generate(
        pixel_values.to(device),
        min_length=1,
        max_new_tokens=context_length,
        bad_words_ids=[[processor.tokenizer.unk_token_id]],
    )

    page_sequence = processor.batch_decode(outputs, skip_special_tokens=True)[0]
    page_sequence = processor.post_process_generation(page_sequence, fix_markdown=False)
    return page_sequence

def process_page(page_num, page, output_dir):
    # تحويل الصفحة إلى صورة
    pix = page.get_pixmap()
    img_path = os.path.join(output_dir, f"page_{page_num + 1}.png")
    pix.save(img_path)

    # استخراج النص
    try:
        text = predict(img_path)
        os.remove(img_path)  # حذف الصورة بعد المعالجة
        return page_num, text
    except Exception as e:
        os.remove(img_path)  # حذف الصورة حتى في حالة الخطأ
        return page_num, f"خطأ في معالجة صفحة {page_num + 1}: {e}"

def process_pdf(pdf_path, output_dir="temp_images", max_workers=4):
    # إنشاء مجلد مؤقت لتخزين الصور إذا لم يكن موجودًا
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # فتح ملف PDF
    pdf_document = fitz.open(pdf_path)
    pages = len(pdf_document)
    all_text = [""] * pages  # لتخزين النصوص حسب ترتيب الصفحات

    # معالجة الصفحات باستخدام ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # إرسال المهام للمعالجة المتوازية
        future_to_page = {
            executor.submit(process_page, i, pdf_document.load_page(i), output_dir): i
            for i in range(pages)
        }

        # جمع النتائج مع تقدم المعالجة
        for future in as_completed(future_to_page):
            page_num, text = future.result()
            all_text[page_num] = f"\n\n--- صفحة {page_num + 1} ---\n\n{text}"
            print(f"تم معالجة صفحة {page_num + 1}")

    # إغلاق ملف PDF
    pdf_document.close()

    # دمج النصوص في نص واحد
    final_text = "".join(all_text)
    return final_text

# استخدام الكود
pdf_path = "/content/arabic_book.pdf"  # استبدل هذا بمسار ملف PDF الخاص بك
extracted_text = process_pdf(pdf_path, max_workers=4)  # يمكنك تعديل عدد العاملين حسب جهازك

# حفظ النص في ملف (اختياري)
with open("extracted_text.txt", "w", encoding="utf-8") as f:
    f.write(extracted_text)

print("تم استخراج النص من الكتاب بنجاح!")





"""الكود المحسن بالمعالجة المتوازية مع ضمان أن النصوص من جميع الصفحات يتم جمعها وحفظها"""

from PIL import Image
import torch
from transformers import NougatProcessor, VisionEncoderDecoderModel
import fitz  # PyMuPDF للتعامل مع ملفات PDF
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

# Load the model and processor
processor = NougatProcessor.from_pretrained("MohamedRashad/arabic-small-nougat")
model = VisionEncoderDecoderModel.from_pretrained("MohamedRashad/arabic-small-nougat")
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

context_length = 2048

def predict(img_path):
    # تحميل وتحضير الصورة للنموذج
    image = Image.open(img_path)
    pixel_values = processor(image, return_tensors="pt").pixel_values

    # توليد النص
    outputs = model.generate(
        pixel_values.to(device),
        min_length=1,
        max_new_tokens=context_length,
        bad_words_ids=[[processor.tokenizer.unk_token_id]],
    )

    page_sequence = processor.batch_decode(outputs, skip_special_tokens=True)[0]
    page_sequence = processor.post_process_generation(page_sequence, fix_markdown=False)
    return page_sequence

def process_page(page_num, page, output_dir):
    # تحويل الصفحة إلى صورة
    pix = page.get_pixmap()
    img_path = os.path.join(output_dir, f"page_{page_num + 1}.png")
    pix.save(img_path)

    # استخراج النص
    try:
        text = predict(img_path)
        os.remove(img_path)  # حذف الصورة بعد المعالجة
        return page_num, text
    except Exception as e:
        os.remove(img_path)  # حذف الصورة حتى في حالة الخطأ
        return page_num, f"خطأ في معالجة صفحة {page_num + 1}: {e}"

def process_pdf(pdf_path, output_dir="temp_images", max_workers=4):
    # إنشاء مجلد مؤقت لتخزين الصور إذا لم يكن موجودًا
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # فتح ملف PDF
    pdf_document = fitz.open(pdf_path)
    pages = len(pdf_document)
    all_text = [""] * pages  # لتخزين النصوص حسب ترتيب الصفحات

    # معالجة الصفحات باستخدام ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # إرسال المهام للمعالجة المتوازية
        future_to_page = {
            executor.submit(process_page, i, pdf_document.load_page(i), output_dir): i
            for i in range(pages)
        }

        # جمع النتائج مع تقدم المعالجة
        for future in as_completed(future_to_page):
            page_num, text = future.result()
            all_text[page_num] = f"\n\n--- صفحة {page_num + 1} ---\n\n{text}"
            print(f"تم معالجة صفحة {page_num + 1}")

    # إغلاق ملف PDF
    pdf_document.close()

    # دمج النصوص في نص واحد
    final_text = "".join(all_text)
    return final_text

# استخدام الكود
pdf_path = "/content/arabic_book.pdf"  # استبدل هذا بمسار ملف PDF الخاص بك
extracted_text = process_pdf(pdf_path, max_workers=4)  # يمكنك تعديل عدد العاملين حسب جهازك

# حفظ النص في ملف
with open("extracted_text.txt", "w", encoding="utf-8") as f:
    f.write(extracted_text)

print("تم استخراج النص من الكتاب بنجاح!")







"""تحسين دمج الدفعات"""

from PIL import Image
import torch
from transformers import NougatProcessor, VisionEncoderDecoderModel
import fitz  # PyMuPDF للتعامل مع ملفات PDF
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

# Load the model and processor
processor = NougatProcessor.from_pretrained("MohamedRashad/arabic-small-nougat")
model = VisionEncoderDecoderModel.from_pretrained("MohamedRashad/arabic-small-nougat")
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

context_length = 2048
batch_size = 4  # يمكنك تعديل حجم الدفعة حسب سعة GPU الخاص بك

def predict_batch(image_paths):
    # تحميل وتحضير دفعة من الصور
    images = [Image.open(img_path) for img_path in image_paths]
    pixel_values = processor(images, return_tensors="pt").pixel_values  # معالجة الدفعة بأكملها

    # نقل البيانات إلى GPU والتوليد
    outputs = model.generate(
        pixel_values.to(device),
        min_length=1,
        max_new_tokens=context_length,
        bad_words_ids=[[processor.tokenizer.unk_token_id]],
    )

    # فك التشفير ومعالجة النصوص
    page_sequences = processor.batch_decode(outputs, skip_special_tokens=True)
    page_sequences = [processor.post_process_generation(seq, fix_markdown=False) for seq in page_sequences]
    return page_sequences

def process_page(page_num, page, output_dir):
    # تحويل الصفحة إلى صورة
    pix = page.get_pixmap()
    img_path = os.path.join(output_dir, f"page_{page_num + 1}.png")
    pix.save(img_path)
    return page_num, img_path  # نرجع مسار الصورة لمعالجتها لاحقًا في دفعات

def process_pdf(pdf_path, output_dir="temp_images", max_workers=4):
    # إنشاء مجلد مؤقت لتخزين الصور إذا لم يكن موجودًا
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # فتح ملف PDF
    pdf_document = fitz.open(pdf_path)
    pages = len(pdf_document)
    all_text = [""] * pages  # لتخزين النصوص حسب ترتيب الصفحات

    # معالجة الصفحات لتحويلها إلى صور باستخدام ThreadPoolExecutor
    image_paths = [""] * pages
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_page = {
            executor.submit(process_page, i, pdf_document.load_page(i), output_dir): i
            for i in range(pages)
        }
        for future in as_completed(future_to_page):
            page_num, img_path = future.result()
            image_paths[page_num] = img_path
            print(f"تم تحويل صفحة {page_num + 1} إلى صورة")

    # معالجة الصور في دفعات
    for i in range(0, pages, batch_size):
        batch_paths = image_paths[i:i + batch_size]
        try:
            batch_texts = predict_batch(batch_paths)
            for j, text in enumerate(batch_texts):
                page_num = i + j
                all_text[page_num] = f"\n\n--- صفحة {page_num + 1} ---\n\n{text}"
                print(f"تم استخراج النص من صفحة {page_num + 1}")
        except Exception as e:
            for j in range(len(batch_paths)):
                page_num = i + j
                all_text[page_num] = f"\n\n--- صفحة {page_num + 1} ---\n\nخطأ: {e}"
                print(f"خطأ في معالجة صفحة {page_num + 1}: {e}")

        # حذف الصور المؤقتة بعد معالجة الدفعة
        for img_path in batch_paths:
            os.remove(img_path)

    # إغلاق ملف PDF
    pdf_document.close()

    # دمج النصوص في نص واحد
    final_text = "".join(all_text)
    return final_text

# استخدام الكود
pdf_path = "/content/arabic_book.pdf"  # استبدل هذا بمسار ملف PDF الخاص بك
extracted_text = process_pdf(pdf_path, max_workers=4)

# حفظ النص في ملف
with open("extracted_text.txt", "w", encoding="utf-8") as f:
    f.write(extracted_text)

print("تم استخراج النص من الكتاب بنجاح!")



from PIL import Image
import torch
from transformers import NougatProcessor, VisionEncoderDecoderModel
import fitz  # PyMuPDF للتعامل مع ملفات PDF
import os

# Load the model and processor
processor = NougatProcessor.from_pretrained("MohamedRashad/arabic-small-nougat")
model = VisionEncoderDecoderModel.from_pretrained("MohamedRashad/arabic-small-nougat")
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

context_length = 2048
batch_size = 4  # يمكنك تعديل حجم الدفعة حسب سعة GPU

def predict_batch(image_paths):
    # تحميل وتحضير دفعة من الصور
    images = [Image.open(img_path) for img_path in image_paths]
    pixel_values = processor(images, return_tensors="pt").pixel_values

    # توليد النصوص للدفعة
    outputs = model.generate(
        pixel_values.to(device),
        min_length=1,
        max_new_tokens=context_length,
        bad_words_ids=[[processor.tokenizer.unk_token_id]],
    )

    # فك التشفير ومعالجة النصوص
    page_sequences = processor.batch_decode(outputs, skip_special_tokens=True)
    page_sequences = [processor.post_process_generation(seq, fix_markdown=False) for seq in page_sequences]
    return page_sequences

def process_pdf(pdf_path, output_dir="temp_images"):
    # إنشاء مجلد مؤقت لتخزين الصور
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # فتح ملف PDF
    pdf_document = fitz.open(pdf_path)
    total_pages = len(pdf_document)
    all_text = [""] * total_pages  # قائمة لتخزين النصوص حسب ترتيب الصفحات
    image_paths = []

    # تحويل جميع الصفحات إلى صور
    for page_num in range(total_pages):
        page = pdf_document.load_page(page_num)
        pix = page.get_pixmap()
        img_path = os.path.join(output_dir, f"page_{page_num + 1}.png")
        pix.save(img_path)
        image_paths.append(img_path)
        print(f"تم تحويل صفحة {page_num + 1} إلى صورة")

    # معالجة الصور في دفعات
    for i in range(0, total_pages, batch_size):
        batch_paths = image_paths[i:i + batch_size]
        try:
            batch_texts = predict_batch(batch_paths)
            for j, text in enumerate(batch_texts):
                page_num = i + j
                all_text[page_num] = f"\n\n--- صفحة {page_num + 1} ---\n\n{text}"
                print(f"تم استخراج النص من صفحة {page_num + 1}: {text[:50]}...")  # عرض أول 50 حرف للتحقق
        except Exception as e:
            for j in range(len(batch_paths)):
                page_num = i + j
                all_text[page_num] = f"\n\n--- صفحة {page_num + 1} ---\n\nخطأ: {e}"
                print(f"خطأ في معالجة صفحة {page_num + 1}: {e}")

        # حذف الصور المؤقتة بعد معالجة الدفعة
        for img_path in batch_paths:
            os.remove(img_path)

    # إغلاق ملف PDF
    pdf_document.close()

    # دمج النصوص في نص واحد
    final_text = "".join(all_text)
    return final_text

# استخدام الكود
pdf_path = "/content/arabic_book.pdf"  # استبدل بمسار ملف PDF الخاص بك
extracted_text = process_pdf(pdf_path)

# حفظ النص في ملف
output_file = "extracted_text.txt"
with open(output_file, "w", encoding="utf-8") as f:
    f.write(extracted_text)

# التحقق من المحتوى
print(f"تم استخراج النص من الكتاب بنجاح! تم حفظ النص في {output_file}")
print(f"عدد الأحرف في النص النهائي: {len(extracted_text)}")
with open(output_file, "r", encoding="utf-8") as f:
    print("أول 200 حرف من الملف النهائي:")
    print(f.read()[:200])

!rm -rf /content/temp_images

"""### aشغال كتاب كامل 10 صفحات استخرج النص صح"""

from PIL import Image
import torch
from transformers import NougatProcessor, VisionEncoderDecoderModel
import fitz  # PyMuPDF للتعامل مع ملفات PDF
import os

# Load the model and processor
processor = NougatProcessor.from_pretrained("MohamedRashad/arabic-small-nougat")
model = VisionEncoderDecoderModel.from_pretrained("MohamedRashad/arabic-small-nougat")
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

context_length = 2048
batch_size = 2  # قللنا الحجم لتسهيل الاختبار، يمكنك زيادته لاحقًا

def predict_batch(image_paths):
    print(f"معالجة دفعة تحتوي على {len(image_paths)} صورة")
    images = [Image.open(img_path) for img_path in image_paths]
    pixel_values = processor(images, return_tensors="pt").pixel_values

    outputs = model.generate(
        pixel_values.to(device),
        min_length=1,
        max_new_tokens=context_length,
        bad_words_ids=[[processor.tokenizer.unk_token_id]],
    )

    page_sequences = processor.batch_decode(outputs, skip_special_tokens=True)
    page_sequences = [processor.post_process_generation(seq, fix_markdown=False) for seq in page_sequences]
    for i, seq in enumerate(page_sequences):
        print(f"نص الصفحة في الدفعة {i + 1}: {seq[:50]}...")  # طباعة جزء من النص للتحقق
    return page_sequences

def process_pdf(pdf_path, output_dir="temp_images"):
    # إنشاء مجلد مؤقت
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # فتح ملف PDF
    pdf_document = fitz.open(pdf_path)
    total_pages = len(pdf_document)
    print(f"إجمالي عدد الصفحات في الملف: {total_pages}")
    all_texts = []  # استخدام قائمة ديناميكية بدلاً من تحديد الحجم مسبقًا
    image_paths = []

    # تحويل الصفحات إلى صور
    for page_num in range(total_pages):
        page = pdf_document.load_page(page_num)
        pix = page.get_pixmap()
        img_path = os.path.join(output_dir, f"page_{page_num + 1}.png")
        pix.save(img_path)
        image_paths.append(img_path)
        print(f"تم تحويل الصفحة {page_num + 1} إلى صورة: {img_path}")

    # معالجة الصور في دفعات
    for i in range(0, total_pages, batch_size):
        batch_paths = image_paths[i:i + batch_size]
        try:
            batch_texts = predict_batch(batch_paths)
            all_texts.extend(batch_texts)  # إضافة النصوص مباشرة إلى القائمة
            for j, text in enumerate(batch_texts):
                page_num = i + j + 1
                print(f"تم استخراج النص من الصفحة {page_num}: {text[:50]}...")
        except Exception as e:
            for j in range(len(batch_paths)):
                page_num = i + j + 1
                all_texts.append(f"خطأ في الصفحة {page_num}: {e}")
                print(f"خطأ في معالجة الصفحة {page_num}: {e}")

        # حذف الصور المؤقتة
        for img_path in batch_paths:
            os.remove(img_path)
            print(f"تم حذف الصورة: {img_path}")

    # إغلاق ملف PDF
    pdf_document.close()

    # دمج النصوص مع فواصل
    final_text = ""
    for page_num, text in enumerate(all_texts, 1):
        final_text += f"\n\n--- صفحة {page_num} ---\n\n{text}"
    print(f"النص النهائي يحتوي على {len(all_texts)} صفحة")

    return final_text

# استخدام الكود
pdf_path = "/content/a.pdf"  # استبدل بمسار ملف PDF الخاص بك
extracted_text = process_pdf(pdf_path)

# حفظ النص في ملف
output_file = "extracted_text.txt"
with open(output_file, "w", encoding="utf-8") as f:
    f.write(extracted_text)

# التحقق النهائي
print(f"تم استخراج النص من الكتاب بنجاح! تم حفظ النص في {output_file}")
print(f"عدد الأحرف في النص النهائي: {len(extracted_text)}")
with open(output_file, "r", encoding="utf-8") as f:
    content = f.read()
    print("أول 200 حرف من الملف النهائي:")
    print(content[:200])

from PIL import Image
import torch
from transformers import NougatProcessor, VisionEncoderDecoderModel
import fitz  # PyMuPDF للتعامل مع ملفات PDF
import os

# Load the model and processor
processor = NougatProcessor.from_pretrained("MohamedRashad/arabic-small-nougat")
model = VisionEncoderDecoderModel.from_pretrained("MohamedRashad/arabic-small-nougat")
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

context_length = 2048
batch_size = 2  # قللنا الحجم لتسهيل الاختبار، يمكنك زيادته لاحقًا

def predict_batch(image_paths):
    print(f"معالجة دفعة تحتوي على {len(image_paths)} صورة")
    images = [Image.open(img_path) for img_path in image_paths]
    pixel_values = processor(images, return_tensors="pt").pixel_values

    outputs = model.generate(
        pixel_values.to(device),
        min_length=1,
        max_new_tokens=context_length,
        bad_words_ids=[[processor.tokenizer.unk_token_id]],
    )

    page_sequences = processor.batch_decode(outputs, skip_special_tokens=True)
    page_sequences = [processor.post_process_generation(seq, fix_markdown=False) for seq in page_sequences]
    for i, seq in enumerate(page_sequences):
        print(f"نص الصفحة في الدفعة {i + 1}: {seq[:50]}...")  # طباعة جزء من النص للتحقق
    return page_sequences

def process_pdf(pdf_path, output_dir="temp_images"):
    # إنشاء مجلد مؤقت
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # فتح ملف PDF
    pdf_document = fitz.open(pdf_path)
    total_pages = len(pdf_document)
    print(f"إجمالي عدد الصفحات في الملف: {total_pages}")
    all_texts = []  # استخدام قائمة ديناميكية بدلاً من تحديد الحجم مسبقًا
    image_paths = []

    # تحويل الصفحات إلى صور
    for page_num in range(total_pages):
        page = pdf_document.load_page(page_num)
        pix = page.get_pixmap()
        img_path = os.path.join(output_dir, f"page_{page_num + 1}.png")
        pix.save(img_path)
        image_paths.append(img_path)
        print(f"تم تحويل الصفحة {page_num + 1} إلى صورة: {img_path}")

    # معالجة الصور في دفعات
    for i in range(0, total_pages, batch_size):
        batch_paths = image_paths[i:i + batch_size]
        try:
            batch_texts = predict_batch(batch_paths)
            all_texts.extend(batch_texts)  # إضافة النصوص مباشرة إلى القائمة
            for j, text in enumerate(batch_texts):
                page_num = i + j + 1
                print(f"تم استخراج النص من الصفحة {page_num}: {text[:50]}...")
        except Exception as e:
            for j in range(len(batch_paths)):
                page_num = i + j + 1
                all_texts.append(f"خطأ في الصفحة {page_num}: {e}")
                print(f"خطأ في معالجة الصفحة {page_num}: {e}")

        # حذف الصور المؤقتة
        for img_path in batch_paths:
            os.remove(img_path)
            print(f"تم حذف الصورة: {img_path}")

    # إغلاق ملف PDF
    pdf_document.close()

    # دمج النصوص مع فواصل
    final_text = ""
    for page_num, text in enumerate(all_texts, 1):
        final_text += f"\n\n--- صفحة {page_num} ---\n\n{text}"
    print(f"النص النهائي يحتوي على {len(all_texts)} صفحة")

    return final_text

# استخدام الكود
pdf_path = "/content/a.pdf"  # استبدل بمسار ملف PDF الخاص بك
extracted_text = process_pdf(pdf_path)

# حفظ النص في ملف
output_file = "extracted_text.txt"
with open(output_file, "w", encoding="utf-8") as f:
    f.write(extracted_text)

# التحقق النهائي
print(f"تم استخراج النص من الكتاب بنجاح! تم حفظ النص في {output_file}")
print(f"عدد الأحرف في النص النهائي: {len(extracted_text)}")
with open(output_file, "r", encoding="utf-8") as f:
    content = f.read()
    print("أول 200 حرف من الملف النهائي:")
    print(content[:200])