#!/usr/bin/env python3
"""
تحويل الأرقام الإنجليزية (0-9) إلى أرقام عربية هندية (٠-٩) في النصوص العربية.

المنطق:
- document.xml: تحويل الأرقام في الفقرات التي تحتوي على نص عربي فقط
  (الفقرات الإنجليزية البحتة مثل المراجع الإنجليزية تُترك كما هي)
- header*.xml / footer*.xml: تحويل جميع الأرقام (أرقام الصفحات)
"""
import sys
import re
import zipfile
import shutil
from lxml import etree

W_NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
W = f'{{{W_NS}}}'

# نطاق الأحرف العربية في اليونيكود
ARABIC_RE = re.compile(r'[\u0600-\u06FF\u0750-\u077F\uFB50-\uFDFF\uFE70-\uFEFF]')

# الأرقام العربية الهندية ٠-٩
ARABIC_DIGITS = '٠١٢٣٤٥٦٧٨٩'


def to_arabic_indic(text):
    """تحويل الأرقام الإنجليزية 0-9 إلى أرقام عربية ٠-٩"""
    result = []
    for c in text:
        if '0' <= c <= '9':
            result.append(ARABIC_DIGITS[ord(c) - ord('0')])
        else:
            result.append(c)
    return ''.join(result)


def process_body_xml(xml_bytes):
    """
    معالجة document.xml:
    تحويل الأرقام في الفقرات التي تحتوي نصاً عربياً.
    الفقرات الإنجليزية البحتة تُترك كما هي (مراجع إنجليزية، DOIs، إلخ).
    """
    root = etree.fromstring(xml_bytes)
    converted_count = 0

    for p in root.iter(f'{W}p'):
        # جمع كل النص في الفقرة
        para_text = ''
        for t in p.iter(f'{W}t'):
            if t.text:
                para_text += t.text

        # إذا احتوت الفقرة نصاً عربياً، حوّل جميع الأرقام فيها
        if ARABIC_RE.search(para_text):
            for t in p.iter(f'{W}t'):
                if t.text and any('0' <= c <= '9' for c in t.text):
                    new_text = to_arabic_indic(t.text)
                    if new_text != t.text:
                        t.text = new_text
                        converted_count += 1

    result = etree.tostring(
        root, xml_declaration=True, encoding='UTF-8', standalone=True
    )
    return result, converted_count


def process_header_footer_xml(xml_bytes):
    """
    معالجة ملفات الترويسة/التذييل:
    تحويل جميع الأرقام (أرقام الصفحات في حقول PAGE/NUMPAGES).
    """
    root = etree.fromstring(xml_bytes)
    converted_count = 0

    for t in root.iter(f'{W}t'):
        if t.text and any('0' <= c <= '9' for c in t.text):
            new_text = to_arabic_indic(t.text)
            if new_text != t.text:
                t.text = new_text
                converted_count += 1

    result = etree.tostring(
        root, xml_declaration=True, encoding='UTF-8', standalone=True
    )
    return result, converted_count


def process_docx(docx_path):
    """معالجة ملف docx: استخراج، تحويل، إعادة ضغط"""
    temp_path = docx_path + '.tmp'
    total_converted = 0

    with zipfile.ZipFile(docx_path, 'r') as zin:
        with zipfile.ZipFile(temp_path, 'w', zipfile.ZIP_DEFLATED) as zout:
            for item in zin.namelist():
                data = zin.read(item)

                if item == 'word/document.xml':
                    data, cnt = process_body_xml(data)
                    total_converted += cnt
                elif (item.startswith('word/header') or
                      item.startswith('word/footer')) and item.endswith('.xml'):
                    data, cnt = process_header_footer_xml(data)
                    total_converted += cnt

                zout.writestr(item, data)

    shutil.move(temp_path, docx_path)
    return total_converted


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("الاستخدام: python convert_arabic_numerals.py <docx_path>")
        sys.exit(1)

    docx_path = sys.argv[1]
    count = process_docx(docx_path)
    print(f"✓ تم تحويل الأرقام في: {docx_path}")
    print(f"  عدد عناصر النص المُحوّلة: {count}")
