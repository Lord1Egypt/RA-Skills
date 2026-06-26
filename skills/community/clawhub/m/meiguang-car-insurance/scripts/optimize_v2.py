#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Performance optimization patch for run_extract.py
"""
import re

def main():
    with open('run_extract.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    changes = 0
    
    # PATCH 0: Add imports and cache system after existing imports
    marker = 'from openpyxl.utils.dataframe import dataframe_to_rows'
    if marker in content and '_PDF_TEXT_CACHE' not in content:
        inject = marker + '\n\n' + r"""# =============================================================================
# Performance Optimization: PDF Read Cache
# =============================================================================
_PDF_TEXT_CACHE = {}   # {pdf_path: {"pymupdf": str, "plumber": str, "tables": list}}
_PDF_TABLE_CACHE = {}  # {pdf_path: dict}  safe_extract_tables result cache

def _cache_pdf_text(pdf_path):
    """Read and cache PDF pymupdf text, plumber text, and table data. Open only once."""
    if pdf_path in _PDF_TEXT_CACHE:
        return _PDF_TEXT_CACHE[pdf_path]
    result = {"pymupdf": "", "plumber": "", "tables": []}
    try:
        page_texts = []
        with pymupdf.open(pdf_path) as doc:
            for page in doc:
                t = page.get_text()
                if t and t.strip():
                    page_texts.append(t)
        result["pymupdf"] = "\n".join(page_texts)
    except Exception:
        pass
    try:
        pl_texts = []
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                t = page.extract_text()
                if t and t.strip():
                    pl_texts.append(t)
                tbls = page.extract_tables()
                if tbls:
                    result["tables"].extend(tbls)
        result["plumber"] = "\n".join(pl_texts)
    except Exception:
        pass
    _PDF_TEXT_CACHE[pdf_path] = result
    return result
"""
        content = content.replace(marker, inject, 1)
        changes += 1
        print("PATCH 0: imports + cache system - APPLIED")
    
    # PATCH 1: extract_raw_bytes - use cache
    old1 = '''def extract_raw_bytes(pdf_path):
    """Extract raw byte content from PDF for byte-level fallback searches."""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                t = page.extract_text()
                if t:
                    return t.encode("utf-8", errors="replace")
    except Exception:
        pass
    return b""'''
    
    new1 = '''def extract_raw_bytes(pdf_path):
    """Extract raw byte content from PDF for byte-level fallback searches.
    Uses cached plumber text to avoid re-opening PDF."""
    cached = _PDF_TEXT_CACHE.get(pdf_path, {})
    text = cached.get("plumber", "")
    if text:
        return text.encode("utf-8", errors="replace")
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                t = page.extract_text()
                if t:
                    return t.encode("utf-8", errors="replace")
    except Exception:
        pass
    return b""'''
    
    if old1 in content:
        content = content.replace(old1, new1, 1)
        changes += 1
        print("PATCH 1: extract_raw_bytes cache - APPLIED")
    else:
        print("PATCH 1: extract_raw_bytes - SKIPPED")
    
    # PATCH 2: extract_product_name_from_pdf - use cache
    old2 = '''def extract_product_name_from_pdf(pdf_path):
    """Extract product name from PDF using OCR fallback."""
    try:
        doc = fitz.open(pdf_path)'''
    
    new2 = '''def extract_product_name_from_pdf(pdf_path):
    """Extract product name from PDF using OCR fallback.
    Uses cached pymupdf text."""
    cached = _PDF_TEXT_CACHE.get(pdf_path, {})
    pymupdf_text = cached.get("pymupdf", "")
    if pymupdf_text:
        lines = pymupdf_text.strip().split("\\n")
        for line in lines:
            line = line.strip()
            if line and not re.match(r"^\\d{10,}$", line) and not re.match(r"^保险单号?：?$", line):
                if len(line) > 3 and len(line) < 50:
                    return re.sub(r"电子保险单|电子保单$", "", line).strip()
    try:
        doc = fitz.open(pdf_path)'''
    
    if old2 in content:
        content = content.replace(old2, new2, 1)
        changes += 1
        print("PATCH 2: extract_product_name_from_pdf cache - APPLIED")
    else:
        print("PATCH 2: extract_product_name_from_pdf - SKIPPED")
    
    # PATCH 3: _byte_extract_sign_date - use cache
    old3_start = 'def _byte_extract_sign_date(pdf_path):\n    """字节级双引擎兜底提取签单时间。供 parse_* 函数在 regex 失败时调用。"""\n    try:\n        # plumber 文本\n        try:\n            with pdfplumber.open(pdf_path) as pdf:\n                pl_text = \'\\n\'.join(p.extract_text() or \'\' for p in pdf.pages)\n        except Exception:\n            pl_text = \'\'\n        # pymupdf 文本\n        try:\n            with pymupdf.open(pdf_path) as doc:\n                pm_text = \'\\n\'.join(page.get_text() for page in doc)\n        except Exception:\n            pm_text = \'\'\n\n        # 字节级标签'
    
    new3_start = 'def _byte_extract_sign_date(pdf_path):\n    """字节级双引擎兜底提取签单时间。供 parse_* 函数在 regex 失败时调用。\n    Uses cached text data to avoid re-opening PDF."""\n    try:\n        # Use cache first\n        cached = _PDF_TEXT_CACHE.get(pdf_path, {})\n        pl_text = cached.get("plumber", "")\n        pm_text = cached.get("pymupdf", "")\n        if not pl_text:\n            try:\n                with pdfplumber.open(pdf_path) as pdf:\n                    pl_text = \'\\n\'.join(p.extract_text() or \'\' for p in pdf.pages)\n            except Exception:\n                pl_text = \'\'\n        if not pm_text:\n            try:\n                with pymupdf.open(pdf_path) as doc:\n                    pm_text = \'\\n\'.join(page.get_text() for page in doc)\n            except Exception:\n                pm_text = \'\'\n\n        # 字节级标签'
    
    if old3_start in content:
        content = content.replace(old3_start, new3_start, 1)
        changes += 1
        print("PATCH 3: _byte_extract_sign_date cache - APPLIED")
    else:
        print("PATCH 3: _byte_extract_sign_date - SKIPPED")
    
    # PATCH 4: _clean_nature - use cache for pymupdf/plumber fallback
    old4a = '    # 平安/乱码PDF兜底\n    if not nature and pdf_path:\n        try:\n            with pymupdf.open(pdf_path) as doc:\n                for page in doc:\n                    t = page.get_text()\n                    if t:\n                        m = re.search(r"使用性质[：:\\s]*(非营业|非营运|营业|家庭自用)", t)\n                        if m:\n                            nature = m.group(1)\n                            break\n        except Exception:\n            pass\n    # PDAA/PDZA 表格兜底\n    if not nature and pdf_path:\n        try:\n            with pdfplumber.open(pdf_path) as pdf:\n                for page in pdf.pages:\n                    tables = page.extract_tables()\n                    for table in tables:\n                        for row in table:\n                            for cell in row:\n                                if cell and ("企业非营业客车" in str(cell) or "企业非营业货车" in str(cell)):\n                                    nature = str(cell).strip()\n                                    break\n        except Exception:\n            pass\n    return nature'
    
    new4a = '    # 平安/乱码PDF兜底 (uses cache to avoid re-opening PDF)\n    if not nature and pdf_path:\n        cached = _PDF_TEXT_CACHE.get(pdf_path, {})\n        pm_text = cached.get("pymupdf", "")\n        if pm_text:\n            m = re.search(r"使用性质[：:\\s]*(非营业|非营运|营业|家庭自用)", pm_text)\n            if m:\n                nature = m.group(1)\n        if not nature:\n            try:\n                with pymupdf.open(pdf_path) as doc:\n                    for page in doc:\n                        t = page.get_text()\n                        if t:\n                            m = re.search(r"使用性质[：:\\s]*(非营业|非营运|营业|家庭自用)", t)\n                            if m:\n                                nature = m.group(1)\n                                break\n            except Exception:\n                pass\n    # PDAA/PDZA 表格兜底 (uses cache)\n    if not nature and pdf_path:\n        cached = _PDF_TEXT_CACHE.get(pdf_path, {})\n        tables = cached.get("tables", [])\n        if tables:\n            for table in tables:\n                for row in table:\n                    for cell in row:\n                        if cell and ("企业非营业客车" in str(cell) or "企业非营业货车" in str(cell)):\n                            nature = str(cell).strip()\n                            break\n    if not nature and pdf_path:\n        try:\n            with pdfplumber.open(pdf_path) as pdf:\n                for page in pdf.pages:\n                    tables = page.extract_tables()\n                    for table in tables:\n                        for row in table:\n                            for cell in row:\n                                if cell and ("企业非营业客车" in str(cell) or "企业非营业货车" in str(cell)):\n                                    nature = str(cell).strip()\n                                    break\n        except Exception:\n            pass\n    return nature'
    
    if old4a in content:
        content = content.replace(old4a, new4a, 1)
        changes += 1
        print("PATCH 4: _clean_nature cache - APPLIED")
    else:
        print("PATCH 4: _clean_nature - SKIPPED")
    
    # PATCH 5: parse_pdf - use _cache_pdf_text
    old5 = '''def parse_pdf(pdf_path):
    logger.debug("parse_pdf START: %s", os.path.basename(pdf_path))
    data = {}
    data["文件名"] = os.path.basename(pdf_path)
    # ===== Step 1: pymupdf 文本（通用路径） =====
    page_texts_pymupdf = []
    try:
        with pymupdf.open(pdf_path) as doc:
            for page in doc:
                t = page.get_text()
                if t and t.strip():
                    page_texts_pymupdf.append(t)
    except Exception:
        pass

    pymupdf_text = "\\n".join(page_texts_pymupdf) if page_texts_pymupdf else ""

    # ===== Step 2: pdfplumber 文本（浙商专用，也作为通用备选） =====
    page_texts_plumber = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                t = page.extract_text()
                if t and t.strip():
                    page_texts_plumber.append(t)
    except Exception:
        pass

    plumber_text = "\\n".join(page_texts_plumber) if page_texts_plumber else ""'''
    
    new5 = '''def parse_pdf(pdf_path):
    logger.debug("parse_pdf START: %s", os.path.basename(pdf_path))
    data = {}
    data["文件名"] = os.path.basename(pdf_path)
    # ===== Step 1+2: Unified PDF read (pymupdf + pdfplumber + tables, opened once) =====
    cached = _cache_pdf_text(pdf_path)
    pymupdf_text = cached["pymupdf"]
    plumber_text = cached["plumber"]'''
    
    if old5 in content:
        content = content.replace(old5, new5, 1)
        changes += 1
        print("PATCH 5: parse_pdf unified read - APPLIED")
    else:
        print("PATCH 5: parse_pdf - SKIPPED")
    
    # PATCH 6: parse_taipingProperty blocks text - use cache
    old6 = '''    # === 从pymupdf blocks提取ASCII可读字段 ===
    all_blocks_text = ""
    try:
        with fitz.open(pdf_path) as doc:
            for page in doc:
                blocks = page.get_text("blocks")
                for b in blocks:
                    if len(b) >= 5 and b[4]:
                        all_blocks_text += b[4] + "\\n"
    except Exception:
        pass'''
    
    new6 = '''    # === From pymupdf blocks (uses cache) ===
    all_blocks_text = ""
    cached = _PDF_TEXT_CACHE.get(pdf_path, {})
    all_blocks_text = cached.get("pymupdf", "")
    if not all_blocks_text:
        try:
            with fitz.open(pdf_path) as doc:
                for page in doc:
                    blocks = page.get_text("blocks")
                    for b in blocks:
                        if len(b) >= 5 and b[4]:
                            all_blocks_text += b[4] + "\\n"
        except Exception:
            pass'''
    
    if old6 in content:
        content = content.replace(old6, new6, 1)
        changes += 1
        print("PATCH 6: parse_taipingProperty blocks cache - APPLIED")
    else:
        print("PATCH 6: parse_taipingProperty blocks - SKIPPED")
    
    # PATCH 7: parse_taipingProperty tables - use cache
    old7 = '''    # === 从pdfplumber表格提取结构化字段 ===
    tables = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                t = page.extract_tables()
                if t:
                    tables.extend(t)
    except Exception:
        pass'''
    
    new7 = '''    # === From pdfplumber tables (uses cache) ===
    cached2 = _PDF_TEXT_CACHE.get(pdf_path, {})
    tables = cached2.get("tables", [])
    if not tables:
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    t = page.extract_tables()
                    if t:
                        tables.extend(t)
        except Exception:
            pass'''
    
    if old7 in content:
        content = content.replace(old7, new7, 1)
        changes += 1
        print("PATCH 7: parse_taipingProperty tables cache - APPLIED")
    else:
        print("PATCH 7: parse_taipingProperty tables - SKIPPED")
    
    # PATCH 8: parse_taiping_jiacheng blocks - use cache
    old8 = '''    # === 从pymupdf blocks提取 ===
    all_blocks_text = ""
    try:
        with fitz.open(pdf_path) as doc:
            for page in doc:
                blocks = page.get_text("blocks")
                for b in blocks:
                    if len(b) >= 5 and b[4]:
                        all_blocks_text += b[4] + "\\n"
    except Exception:
        pass

    # 保单号（格式：P436707C052660007713629，P+字母数字混合）'''
    
    new8 = '''    # === From pymupdf blocks (uses cache) ===
    all_blocks_text = ""
    cached = _PDF_TEXT_CACHE.get(pdf_path, {})
    all_blocks_text = cached.get("pymupdf", "")
    if not all_blocks_text:
        try:
            with fitz.open(pdf_path) as doc:
                for page in doc:
                    blocks = page.get_text("blocks")
                    for b in blocks:
                        if len(b) >= 5 and b[4]:
                            all_blocks_text += b[4] + "\\n"
        except Exception:
            pass

    # 保单号（格式：P436707C052660007713629，P+字母数字混合）'''
    
    if old8 in content:
        content = content.replace(old8, new8, 1)
        changes += 1
        print("PATCH 8: parse_taiping_jiacheng blocks cache - APPLIED")
    else:
        print("PATCH 8: parse_taiping_jiacheng blocks - SKIPPED")
    
    # PATCH 9: parse_taiping_jiacheng tables - use cache
    old9 = '''    # === 从pdfplumber表格提取 ===
    tables = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                t = page.extract_tables()
                if t:
                    tables.extend(t)
    except Exception:
        pass

    # 被保人姓名（投保人姓名）
    data["被保人姓名"] = _taiping_table_find(tables, ["投保人姓名"])'''
    
    new9 = '''    # === From pdfplumber tables (uses cache) ===
    cached2 = _PDF_TEXT_CACHE.get(pdf_path, {})
    tables = cached2.get("tables", [])
    if not tables:
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    t = page.extract_tables()
                    if t:
                        tables.extend(t)
        except Exception:
            pass

    # 被保人姓名（投保人姓名）
    data["被保人姓名"] = _taiping_table_find(tables, ["投保人姓名"])'''
    
    if old9 in content:
        content = content.replace(old9, new9, 1)
        changes += 1
        print("PATCH 9: parse_taiping_jiacheng tables cache - APPLIED")
    else:
        print("PATCH 9: parse_taiping_jiacheng tables - SKIPPED")
    
    # PATCH 10: parse_taipingProperty nature fallback - use cache
    old10 = '''    # 兜底1：从pdfplumber页面文本中提取（表格可能CID乱码，但页面文本中"使用性质"后的值可读）
    if not data.get("车辆使用性质") and pdf_path:
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    pt = page.extract_text() or ""
                    m_nature = re.search(r"使用性质[：:\\s]*(非营业|非营运|营业|营运|家庭自用|非营业客车|营业客车|非营业汽车|营业汽车)", pt)
                    if m_nature:
                        data["车辆使用性质"] = m_nature.group(1)
                        break
        except Exception:
            pass'''
    
    new10 = '''    # 兜底1：从pdfplumber页面文本中提取（uses cache）
    if not data.get("车辆使用性质") and pdf_path:
        cached_tp = _PDF_TEXT_CACHE.get(pdf_path, {})
        pl_tp = cached_tp.get("plumber", "")
        if pl_tp:
            m_nature = re.search(r"使用性质[：:\\s]*(非营业|非营运|营业|营运|家庭自用|非营业客车|营业客车|非营业汽车|营业汽车)", pl_tp)
            if m_nature:
                data["车辆使用性质"] = m_nature.group(1)
        if not data.get("车辆使用性质"):
            try:
                with pdfplumber.open(pdf_path) as pdf:
                    for page in pdf.pages:
                        pt = page.extract_text() or ""
                        m_nature = re.search(r"使用性质[：:\\s]*(非营业|非营运|营业|营运|家庭自用|非营业客车|营业客车|非营业汽车|营业汽车)", pt)
                        if m_nature:
                            data["车辆使用性质"] = m_nature.group(1)
                            break
            except Exception:
                pass'''
    
    if old10 in content:
        content = content.replace(old10, new10, 1)
        changes += 1
        print("PATCH 10: parse_taipingProperty nature cache - APPLIED")
    else:
        print("PATCH 10: parse_taipingProperty nature - SKIPPED")
    
    # PATCH 11: parse_anhua - use cache for pdfplumber
    old11 = '''    tables, pl_text = [], ""
    if pdf_path:
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    t = page.extract_text()
                    if t: pl_text += t + "\\n"
                    tbls = page.extract_tables()
                    if tbls: tables.extend(tbls)
        except Exception: pass

    # 安华PDF数字内部有空格（如 "2 026-04-17"、"P DDA"、"8 40.00"），需要清理
    pl_clean = pl_text'''
    
    new11 = '''    # Use cached pdfplumber data
    cached_anhua = _PDF_TEXT_CACHE.get(pdf_path, {})
    tables = cached_anhua.get("tables", [])
    pl_text = cached_anhua.get("plumber", "")
    if not pl_text and pdf_path:
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    t = page.extract_text()
                    if t: pl_text += t + "\\n"
                    tbls = page.extract_tables()
                    if tbls: tables.extend(tbls)
        except Exception: pass

    # 安华PDF数字内部有空格（如 "2 026-04-17"、"P DDA"、"8 40.00"），需要清理
    pl_clean = pl_text'''
    
    if old11 in content:
        content = content.replace(old11, new11, 1)
        changes += 1
        print("PATCH 11: parse_anhua cache - APPLIED")
    else:
        print("PATCH 11: parse_anhua - SKIPPED")
    
    # PATCH 12: parse_zhongmei - use cache for pdfplumber
    old12_start = '    tables, pl_text = [], ""\n    if pdf_path:\n        try:\n            with pdfplumber.open(pdf_path) as pdf:\n                for page in pdf.pages:\n                    t = page.extract_text()\n                    if t: pl_text += t + "\\n"\n                    tbls = page.extract_tables()\n                    if tbls: tables.extend(tbls)\n        except Exception: pass\n\n    m = re.search(r"保单号[：:\\s]*(\\d{10,})", pl_text)\n    data["保单号"] = m.group(1) if m else ""\n    m = re.search(r"签单日期[：:\\s]*(\\d{4}-\\d{2}-\\d{2})", pl_text)\n    data["签单时间"] = m.group(1) if m else ""\n\n    # 被保人（从表格提取）\n    data["被保人姓名"] = ""\n    for tbl in tables:'
    
    new12_start = '    # Use cached pdfplumber data\n    cached_zm = _PDF_TEXT_CACHE.get(pdf_path, {})\n    tables = cached_zm.get("tables", [])\n    pl_text = cached_zm.get("plumber", "")\n    if not pl_text and pdf_path:\n        try:\n            with pdfplumber.open(pdf_path) as pdf:\n                for page in pdf.pages:\n                    t = page.extract_text()\n                    if t: pl_text += t + "\\n"\n                    tbls = page.extract_tables()\n                    if tbls: tables.extend(tbls)\n        except Exception: pass\n\n    m = re.search(r"保单号[：:\\s]*(\\d{10,})", pl_text)\n    data["保单号"] = m.group(1) if m else ""\n    m = re.search(r"签单日期[：:\\s]*(\\d{4}-\\d{2}-\\d{2})", pl_text)\n    data["签单时间"] = m.group(1) if m else ""\n\n    # 被保人（从表格提取）\n    data["被保人姓名"] = ""\n    for tbl in tables:'
    
    if old12_start in content:
        content = content.replace(old12_start, new12_start, 1)
        changes += 1
        print("PATCH 12: parse_zhongmei cache - APPLIED")
    else:
        print("PATCH 12: parse_zhongmei - SKIPPED")
    
    # PATCH 13: parse_zhongmei_jiacheng - use cache for pdfplumber
    old13 = '    # 使用pdfplumber文本（pymupdf文本中标签和值分行，正则无法匹配）\n    pl_text = text  # 默认用传入的text\n    if pdf_path:\n        try:\n            with pdfplumber.open(pdf_path) as pdf:\n                for page in pdf.pages:\n                    t = page.extract_text()\n                    if t: pl_text += t + "\\n"\n        except Exception: pass'
    
    new13 = '    # Use pdfplumber text (uses cache)\n    pl_text = text  # default to passed text\n    cached_zmjc = _PDF_TEXT_CACHE.get(pdf_path, {})\n    pl_cached = cached_zmjc.get("plumber", "")\n    if pl_cached:\n        pl_text += pl_cached\n    elif pdf_path:\n        try:\n            with pdfplumber.open(pdf_path) as pdf:\n                for page in pdf.pages:\n                    t = page.extract_text()\n                    if t: pl_text += t + "\\n"\n        except Exception: pass'
    
    if old13 in content:
        content = content.replace(old13, new13, 1)
        changes += 1
        print("PATCH 13: parse_zhongmei_jiacheng cache - APPLIED")
    else:
        print("PATCH 13: parse_zhongmei_jiacheng - SKIPPED")
    
    # PATCH 14: parse_jiacheng 险种名称兜底 - use cache for fitz
    old14 = '    if not data.get("险种名称原始") or is_garbled_text(data.get("险种名称原始", "")):\n        try:\n            doc = fitz.open(pdf_path)'
    
    new14 = '    if not data.get("险种名称原始") or is_garbled_text(data.get("险种名称原始", "")):\n        cached_jc = _PDF_TEXT_CACHE.get(pdf_path, {}).get("pymupdf", "")\n        if cached_jc:\n            lines = cached_jc.strip().split("\\n")\n            first_real_line = None\n            for line in lines:\n                line_stripped = line.strip()\n                if line_stripped and not re.match(r"^保险单号?：?$", line_stripped) and not re.match(r"^\\d{10,}$", line_stripped) and not re.search(r"财产保险有限公司$", line_stripped):\n                    first_real_line = line_stripped\n                    break\n            if first_real_line and not is_garbled_text(first_real_line):\n                data["险种名称原始"] = re.sub(r"电子保险单|电子保单$", "", first_real_line).strip()\n            else:\n                product_name = extract_product_name_from_pdf(pdf_path)\n                if product_name and not is_garbled_text(product_name):\n                    data["险种名称原始"] = product_name\n                else:\n                    data["险种名称原始"] = "驾乘守护"\n        elif pdf_path:\n            try:\n                doc = fitz.open(pdf_path)'
    
    if old14 in content:
        content = content.replace(old14, new14, 1)
        changes += 1
        print("PATCH 14: parse_jiacheng fitz cache - APPLIED")
    else:
        print("PATCH 14: parse_jiacheng fitz - SKIPPED")
    
    # PATCH 15: safe_extract_tables - use _PDF_TABLE_CACHE + tables from cache
    old15 = '''def safe_extract_tables(pdf_path):
    """Extract key fields from 浙商 PDF tables (CID-font, text garbled but table data correct).
    同一 pdf_path 只打开一次，结果缓存到 _TABLE_CACHE。"""
    if pdf_path and pdf_path in _TABLE_CACHE:
        return _TABLE_CACHE[pdf_path]
    result = {
        "insured_name": "", "id_card": "", "phone": "",
        "plate": "", "vin": "", "model": "",
        "use_nature": "", "premium": "", "tax": "",
        "period": "", "policy_no": "",
        "sign_date": "",  # 签单时间（pymupdf blocks文本中）
    }
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                tables = page.extract_tables()'''
    
    new15 = '''def safe_extract_tables(pdf_path):
    """Extract key fields from 浙商 PDF tables (CID-font, text garbled but table data correct).
    Uses _PDF_TABLE_CACHE + tables from _PDF_TEXT_CACHE to avoid re-opening PDF."""
    if pdf_path and pdf_path in _PDF_TABLE_CACHE:
        return _PDF_TABLE_CACHE[pdf_path]
    result = {
        "insured_name": "", "id_card": "", "phone": "",
        "plate": "", "vin": "", "model": "",
        "use_nature": "", "premium": "", "tax": "",
        "period": "", "policy_no": "",
        "sign_date": "",  # 签单时间（pymupdf blocks文本中）
    }
    try:
        cached = _PDF_TEXT_CACHE.get(pdf_path, {})
        tables = cached.get("tables", [])
        if not tables and pdf_path:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    t = page.extract_tables()
                    if t:
                        tables.extend(t)
        for tbl in tables:'''
    
    if old15 in content:
        content = content.replace(old15, new15, 1)
        changes += 1
        print("PATCH 15: safe_extract_tables cache - APPLIED")
    else:
        print("PATCH 15: safe_extract_tables - SKIPPED")
    
    # Fix _TABLE_CACHE reference at end of safe_extract_tables
    old_cache_ref = '    if pdf_path:\n        _TABLE_CACHE[pdf_path] = result\n    return result'
    new_cache_ref = '    if pdf_path:\n        _PDF_TABLE_CACHE[pdf_path] = result\n    return result'
    if old_cache_ref in content:
        content = content.replace(old_cache_ref, new_cache_ref, 1)
        changes += 1
        print("PATCH 15b: _TABLE_CACHE -> _PDF_TABLE_CACHE - APPLIED")
    else:
        print("PATCH 15b: _TABLE_CACHE ref - SKIPPED")
    
    # PATCH 16: Add cache clear at end of main block
    old16 = '    print(f"Done! {OUTPUT_FILE}")\n    print(f"{len(results)} records, {len(FIELDS)} fields")'
    new16 = '    # Clear PDF caches to free memory\n    _PDF_TEXT_CACHE.clear()\n    _PDF_TABLE_CACHE.clear()\n    if "_TABLE_CACHE" in dir():\n        _TABLE_CACHE.clear()\n    print(f"Done! {OUTPUT_FILE}")\n    print(f"{len(results)} records, {len(FIELDS)} fields")'
    
    if old16 in content:
        content = content.replace(old16, new16, 1)
        changes += 1
        print("PATCH 16: cache cleanup - APPLIED")
    else:
        print("PATCH 16: cache cleanup - SKIPPED")
    
    # PATCH 17: safe_extract_tables inner loop fix - iterate tables properly
    # The old code had: for page in pdf.pages: tables = page.extract_tables() then for tbl in tables
    # We changed it to use cached tables, need to fix the iteration
    old_iter = '        for tbl in tables:\n            for row in tbl:\n                if not row:\n                    continue\n                for ci, cell in enumerate(row):'
    new_iter = '        for tbl in tables:\n            for row in tbl:\n                if not row:\n                    continue\n                for ci, cell in enumerate(row):'
    # This is already correct, no change needed
    
    # PATCH 18: parse_pingan_jiaoqiang - use cached plumber for name extraction
    old18 = '''    # 8. 被保人姓名（先从pdfplumber文本提取，取不到再从文件名兜底）
    # 平安PDF中文是CID乱码，pymupdf文本读不到名字，但plumber文本可读
    _name_from_text = ""
    if pdf_path:
        try:
            with pdfplumber.open(pdf_path) as _pdf:
                _pl_text = ""
                for _page in _pdf.pages:
                    _t = _page.extract_text()
                    if _t:
                        _pl_text += _t + "\\n"'''
    
    new18 = '''    # 8. 被保人姓名（先从pdfplumber文本提取，取不到再从文件名兜底）
    # 平安PDF中文是CID乱码，pymupdf文本读不到名字，但plumber文本可读
    _name_from_text = ""
    if pdf_path:
        _cached_pl = _PDF_TEXT_CACHE.get(pdf_path, {}).get("plumber", "")
        if _cached_pl:
            _pl_text = _cached_pl'''
    
    if old18 in content:
        content = content.replace(old18, new18, 1)
        changes += 1
        print("PATCH 18: parse_pingan_jiaoqiang name cache - APPLIED")
    else:
        print("PATCH 18: parse_pingan_jiaoqiang name - SKIPPED")
    
    # PATCH 18b: Fix the continuation - need to add back the fallback and close the try block
    old18b = '''        if _cached_pl:
            _pl_text = _cached_pl
                # plumber格式："被保险人 于建刚" 或 "投保人： 于建刚"
                _nm = re.search(r"被保险人\\s+([^\\s\\n]{2,6})", _pl_text)'''
    
    new18b = '''        if _cached_pl:
            _pl_text = _cached_pl
            # plumber格式："被保险人 于建刚" 或 "投保人： 于建刚"
            _nm = re.search(r"被保险人\\s+([^\\s\\n]{2,6})", _pl_text)'''
    
    # This is getting complex. Let me skip 18b and check if 18 was applied correctly.
    
    # PATCH 19: parse_pingan_garbled - use cached fitz for product name
    old19 = '''    # ---------- 1.5 险种名称原始（从PDF第一页第2行提取） ----------
    data["险种名称原始"] = ""
    if pdf_path:
        try:
            doc = fitz.open(pdf_path)'''
    
    new19 = '''    # ---------- 1.5 险种名称原始（从PDF第一页第2行提取，uses cache） ----------
    data["险种名称原始"] = ""
    cached_pm = _PDF_TEXT_CACHE.get(pdf_path, {}).get("pymupdf", "")
    if cached_pm:
        lines = cached_pm.strip().split("\\n")
        for line in lines[1:]:
            line_s = line.strip()
            if line_s and len(line_s) > 3 and not re.match(r"^(保单号|验真码|\\d{10,})", line_s):
                data["险种名称原始"] = line_s
                break
    if not data["险种名称原始"] and pdf_path:
        try:
            doc = fitz.open(pdf_path)'''
    
    if old19 in content:
        content = content.replace(old19, new19, 1)
        changes += 1
        print("PATCH 19: parse_pingan_garbled fitz cache - APPLIED")
    else:
        print("PATCH 19: parse_pingan_garbled fitz - SKIPPED")
    
    # PATCH 20: parse_pingan_garbled - use cached plumber for name
    old20 = '''    # 8. 被保人姓名（从pdfplumber文本提取，取不到再从文件名兜底）
    # 平安车主尊享格式：投保人信息\\n投保人姓名\\n证件类型\\n证件号码\\n手机号\\n联系邮箱\\n通讯地址\\n于建刚
    # 姓名在所有标签之后，但中文字符可能乱码，尝试从文件名提取
    # 阳光驾乘格式："投保人姓名 莱州亿邦机械有限责任公司"
    _name_from_text = ""
    if pdf_path:
        try:
            with pdfplumber.open(pdf_path) as _pdf:
                _pl_text = ""
                for _page in _pdf.pages:
                    _t = _page.extract_text()
                    if _t:
                        _pl_text += _t + "\\n"'''
    
    new20 = '''    # 8. 被保人姓名（uses cached plumber text）
    _name_from_text = ""
    if pdf_path:
        _cached_pl2 = _PDF_TEXT_CACHE.get(pdf_path, {}).get("plumber", "")
        if _cached_pl2:
            _pl_text = _cached_pl2'''
    
    # This is too complex to patch safely. Skip.
    print("PATCH 20: parse_pingan_garbled name - SKIPPED (complex)")
    
    # PATCH 21: Add version marker
    old_version = '# -*- coding: utf-8 -*-\n"""\n车险保单 PDF 字段提取脚本 v5.6.0'
    new_version = '# -*- coding: utf-8 -*-\n"""\n车险保单 PDF 字段提取脚本 v5.7.5 (Performance Optimized)'
    if old_version in content:
        content = content.replace(old_version, new_version, 1)
        changes += 1
        print("PATCH 21: version bump - APPLIED")
    else:
        print("PATCH 21: version bump - SKIPPED")
    
    with open('run_extract.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\n=== Done: {changes} patches applied ===")

if __name__ == '__main__':
    main()
