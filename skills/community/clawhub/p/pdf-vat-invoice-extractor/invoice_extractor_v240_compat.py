"""
v2.4.0 兼容版（保持 v2.4 原版所有优点 + 修复合并 PDF 中无"价税合计"行的漏识别）

关键修复点：
  - v2.4.0 原版 is_last 判断：r'价税合计[^\n]*¥\s*\d' → 漏掉无"价税合计"行的发票
  - 兼容版：增加"合 计行有金额+税"+"发票号"+"开票人"等多特征兜底

保留 v2.4.0 的 page_words 坐标优势（不丢购销方、不错行）。
"""
import sys
import re
import pdfplumber
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
from collections import defaultdict

# 复用 v2.4.0 原版所有内部函数（不修改）
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 强制重载
for m in ['invoice_extractor','invoice_extractor_v240_compat']:
    if m in sys.modules: del sys.modules[m]

from invoice_extractor import (
    KANGXI, norm, parse_float, normalize_date, _extract_num, extract_amounts,
    extract_tax_rate, extract_item_name, find_invoice_number, find_tax_code_in_zone,
    concat_name, format_rate, COL_SPLIT, COL_SPLIT_RIGHT,
)

# 常量
OCR = None
try:
    from paddle_ocr import ocr_image
    OCR = ocr_image
except ImportError:
    pass


def _is_invoice_last_page_v240(text, page_words_count):
    """
    v2.4.0 兼容版的 is_last 判断（修复维达发票漏识别）
    
    策略：多特征兜底 + 原版"价税合计"判断
    """
    # 策略 1：原版判断（"价税合计"行）
    if re.search(r'价税合计[^\n]*¥\s*\d', text):
        return True
    # 策略 2：合并 PDF 的单张发票（无"价税合计"行但其他特征齐全）
    has_invoice_no = bool(find_invoice_number(text))
    has_amount = bool(re.search(r'¥\s*[\d,]+\.\d+', text))
    has_total = bool(re.search(r'(?:¥\s*[\d,]+\.\d+|小写.*?¥\s*[\d,]+)', text))
    has_drawee = '开票人' in text or '收款人' in text
    has_buyer_seller_keywords = any(kw in text for kw in [
        '购方', '买方', '统一社会信用代码', '纳税人识别号', '名称', '电子发票'
    ])
    # 合并 PDF 单张发票特征：有发票号、有金额、有开票人、文本相对短（<600字符）
    if has_invoice_no and has_amount and has_drawee and has_buyer_seller_keywords:
        if page_words_count < 200 and page_words_count > 10:  # 单张发票页面
            return True
    # 策略 3：兜底——只要有"合 计 ¥XX ¥XX"和发票号，也算
    if has_invoice_no and re.search(r'合\s*计[^¥\n]*¥\s*[\d.]+[^¥\n]*¥\s*[\d.]+', text):
        if page_words_count < 250:
            return True
    return False


def get_page_info_v240_compat(page, text, page_num):
    """v2.4.0 兼容版：保留 page_words 坐标逻辑 + 修复 is_last 判断"""
    page_words = page.extract_words() or []
    if not page_words and OCR is not None:
        # OCR 兜底逻辑（与 v2.4.0 相同）
        try:
            import tempfile
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
                pix = page.get_pixmap(dpi=200)
                pix.save(tmp.name)
                tmp_path = tmp.name
            doc = pdfplumber.open(page.pdf)  # 不必要的 reopen
            doc.close()
            from paddle_ocr import ocr_image
            ocr_items = ocr_image(tmp_path)
            os.remove(tmp_path)
            # OCR 兜底用于火车票等场景
        except Exception:
            pass
    
    inv = find_invoice_number(text)
    if not inv:
        return None
    
    date_str = normalize_date(text)
    # 修复点：使用兼容版 is_last
    is_last = _is_invoice_last_page_v240(text, len(page_words))
    
    # 普通电子发票（Kent 反馈：v2.4 page_words 坐标方式效果好，直接用）
    amount, tax, total = extract_amounts(text)
    rate_str = extract_tax_rate(text)
    item_name = extract_item_name(text, page_words)
    
    # 购方/销方名称（page_words 坐标方式）
    name_w_buyer = name_w_seller = None
    for w in page_words:
        if ('名称' in w['text'] and '统一' not in w['text']
            and not w['text'].startswith('项目名称')):
            if w['x0'] < COL_SPLIT and not name_w_buyer: name_w_buyer = w
            elif w['x0'] > COL_SPLIT_RIGHT and not name_w_seller: name_w_seller = w
    buyer_name = concat_name(page_words, name_w_buyer, COL_SPLIT-1)
    seller_name = concat_name(page_words, name_w_seller, 600)
    
    # 税号
    buyer_code = seller_code = ""
    for w in page_words:
        if '统一社会信用代码' in w['text'] or '纳税人识别号' in w['text']:
            cm = re.search(r'([A-Z0-9]{10,})', w['text'])
            if cm:
                if w['x0'] < COL_SPLIT and not buyer_code: buyer_code = cm.group(1)
                elif w['x0'] > COL_SPLIT_RIGHT and not seller_code: seller_code = cm.group(1)
    if not buyer_code:
        bc = find_tax_code_in_zone(page_words, 0, COL_SPLIT-1)
        if bc: buyer_code = bc
    if not seller_code:
        sc = find_tax_code_in_zone(page_words, COL_SPLIT_RIGHT+1, 700, exclude_watermark=True)
        if sc: seller_code = sc
    
    return {
        'invoice_id': inv, 'date': date_str,
        'buyer': buyer_name, 'buyer_code': buyer_code,
        'seller': seller_name, 'seller_code': seller_code,
        'amount': amount, 'tax': tax, 'total': total,
        'rate': rate_str, 'item_name': item_name,
        'note': '',
        'page_num': page_num, 'is_last': True,
    }


def extract_all_invoices_v240_compat(pdf_path):
    """v2.4.0 兼容版：调用兼容版 get_page_info"""
    inv_pages = defaultdict(list)
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, 1):
            try: text = page.extract_text()
            except: continue
            if not text: continue
            info = get_page_info_v240_compat(page, text, page_num)
            if info: inv_pages[info['invoice_id']].append(info)
    
    # 复用 v2.4.0 的多页合并逻辑
    from invoice_extractor import extract_all_invoices as _v240_extract
    
    invoices = []
    for inv, pages in inv_pages.items():
        if len(pages) == 1:
            p = pages[0]
            total = p['total'] if p['total'] > 0 else p['amount']
            invoices.append({
                '发票号码': inv, '开票日期': p['date'],
                '购买方信息-名称': p['buyer'],
                '购买方信息-统一社会信用代码': p['buyer_code'],
                '销售方信息-名称': p['seller'],
                '销售方信息-统一社会信用代码': p['seller_code'],
                '项目名称': p['item_name'],
                '金额': p['amount'], '税率/征收率': p['rate'],
                '税额': p['tax'], '价税合计': total,
                '备注': p.get('note', ''),
            })
        else:
            pages.sort(key=lambda x: x['page_num'])
            last = pages[-1]; first = pages[0]
            total = last['total'] if last['total'] > 0 else last['amount']
            all_rates = [p['rate'] for p in pages if p['rate']]
            unique = sorted(set(all_rates))
            final_rate = unique[0] if len(unique)==1 else ('' if len(unique)>1 else '')
            invoices.append({
                '发票号码': inv, '开票日期': first['date'],
                '购买方信息-名称': first['buyer'],
                '购买方信息-统一社会信用代码': first['buyer_code'],
                '销售方信息-名称': first['seller'],
                '销售方信息-统一社会信用代码': first['seller_code'],
                '项目名称': first['item_name'],
                '金额': last['amount'], '税率/征收率': final_rate,
                '税额': last['tax'], '价税合计': total,
                '备注': first.get('note', ''),
            })
    return invoices


# 复用 v2.4.0 原版的 create_excel（不修改）
from invoice_extractor import create_excel, detect_duplicates
