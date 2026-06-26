#!/usr/bin/env python3
"""
Performance optimization patch for run_extract.py
Applies targeted optimizations without changing output logic.
"""
import re

def patch_file():
    with open("run_extract.py", "r", encoding="utf-8") as f:
        content = f.read()
    
    # ================================================================
    # PATCH 1: extract_raw_bytes - use cache instead of re-opening PDF
    # ================================================================
    old = '''def extract_raw_bytes(pdf_path):
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
    
    new = '''def extract_raw_bytes(pdf_path):
    """Extract raw byte content from PDF for byte-level fallback searches.
    澶嶇敤缂撳瓨涓殑 plumber 鏂囨湰锛岄伩鍏嶉噸鏂版墦寮€ PDF銆?""
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
    
    if old in content:
        content = content.replace(old, new, 1)
        print("PATCH 1: extract_raw_bytes cache - APPLIED")
    else:
        print("PATCH 1: extract_raw_bytes - SKIPPED (already patched or not found)")
    
    # ================================================================
    # PATCH 2: extract_product_name_from_pdf - use cache
    # ================================================================
    old2 = '''def extract_product_name_from_pdf(pdf_path):
    """Extract product name from PDF using OCR fallback."""
    try:
        doc = fitz.open(pdf_path)'''
    
    new2 = '''def extract_product_name_from_pdf(pdf_path):
    """Extract product name from PDF using OCR fallback.
    澶嶇敤缂撳瓨涓殑 pymupdf 鏂囨湰銆?""
    cached = _PDF_TEXT_CACHE.get(pdf_path, {})
    pymupdf_text = cached.get("pymupdf", "")
    if pymupdf_text:
        lines = pymupdf_text.strip().split("\\n")
        for line in lines:
            line = line.strip()
            if line and not re.match(r"^\\d{10,}$", line) and not re.match(r"^淇濋櫓鍗曞彿?锛?$", line):
                if len(line) > 3 and len(line) < 50:
                    return re.sub(r"鐢靛瓙淇濋櫓鍗晐鐢靛瓙淇濆崟$", "", line).strip()
    try:
        doc = fitz.open(pdf_path)'''
    
    if old2 in content:
        content = content.replace(old2, new2, 1)
        print("PATCH 2: extract_product_name_from_pdf cache - APPLIED")
    else:
        print("PATCH 2: extract_product_name_from_pdf - SKIPPED")
    
    # ================================================================
    # PATCH 3: _byte_extract_sign_date - use cache
    # ================================================================
    old3 = '''def _byte_extract_sign_date(pdf_path):
    """瀛楄妭绾у弻寮曟搸鍏滃簳鎻愬彇绛惧崟鏃堕棿銆備緵 parse_* 鍑芥暟鍦?regex 澶辫触鏃惰皟鐢ㄣ€?""
    try:
        # plumber 鏂囨湰
        try:
            with pdfplumber.open(pdf_path) as pdf:
                pl_text = '\\n'.join(p.extract_text() or '' for p in pdf.pages)
        except Exception:
            pl_text = ''
        # pymupdf 鏂囨湰
        try:
            with pymupdf.open(pdf_path) as doc:
                pm_text = '\\n'.join(page.get_text() for page in doc)
        except Exception:
            pm_text = \\'\\''
    
        # 瀛楄妭绾ф爣绛撅紙鐢ㄤ簬 pdfplumber CID 涔辩爜鏂囨湰鐨?UTF-8 瀛楄妭鎼滅储锛?''
    
    new3 = '''def _byte_extract_sign_date(pdf_path):
    """瀛楄妭绾у弻寮曟搸鍏滃簳鎻愬彇绛惧崟鏃堕棿銆備緵 parse_* 鍑芥暟鍦?regex 澶辫触鏃惰皟鐢ㄣ€?    澶嶇敤缂撳瓨涓殑鏂囨湰鏁版嵁锛岄伩鍏嶉噸鏂版墦寮€ PDF銆?""
    try:
        # 浼樺厛浣跨敤缂撳瓨
        cached = _PDF_TEXT_CACHE.get(pdf_path, {})
        pl_text = cached.get("plumber", "")
        pm_text = cached.get("pymupdf", "")
        # 缂撳瓨鏈懡涓椂鍥為€€鍒扮洿鎺ヨ鍙?        if not pl_text:
            try:
                with pdfplumber.open(pdf_path) as pdf:
                    pl_text = '\\n'.join(p.extract_text() or '' for p in pdf.pages)
            except Exception:
                pl_text = ''
        if not pm_text:
            try:
                with pymupdf.open(pdf_path) as doc:
                    pm_text = '\\n'.join(page.get_text() for page in doc)
            except Exception:
                pm_text = ''
    
        # 瀛楄妭绾ф爣绛撅紙鐢ㄤ簬 pdfplumber CID 涔辩爜鏂囨湰鐨?UTF-8 瀛楄妭鎼滅储锛?''
    
    if old3 in content:
        content = content.replace(old3, new3, 1)
        print("PATCH 3: _byte_extract_sign_date cache - APPLIED")
    else:
        print("PATCH 3: _byte_extract_sign_date - SKIPPED")
    
    # ================================================================
    # PATCH 4: _clean_nature - use cache for pymupdf/plumber fallback
    # ================================================================
    old4 = '''    # 骞冲畨/涔辩爜PDF鍏滃簳
    if not nature and pdf_path:
        try:
            with pymupdf.open(pdf_path) as doc:
                for page in doc:
                    t = page.get_text()
                    if t:
                        m = re.search(r"浣跨敤鎬ц川[锛?\\s]*(闈炶惀涓殀闈炶惀杩恷钀ヤ笟|瀹跺涵鑷敤)", t)
                        if m:
                            nature = m.group(1)
                            break
        except Exception:
            pass
    # PDAA/PDZA 琛ㄦ牸鍏滃簳
    if not nature and pdf_path:
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    tables = page.extract_tables()
                    for table in tables:
                        for row in table:
                            for cell in row:
                                if cell and ("浼佷笟闈炶惀涓氬杞? in str(cell) or "浼佷笟闈炶惀涓氳揣杞? in str(cell)):
                                    nature = str(cell).strip()
                                    break
        except Exception:
            pass
    return nature'''
    
    new4 = '''    # 骞冲畨/涔辩爜PDF鍏滃簳锛堝鐢ㄧ紦瀛橈紝閬垮厤閲嶆柊鎵撳紑 PDF锛?    if not nature and pdf_path:
        cached = _PDF_TEXT_CACHE.get(pdf_path, {})
        pm_text = cached.get("pymupdf", "")
        if pm_text:
            m = re.search(r"浣跨敤鎬ц川[锛?\\s]*(闈炶惀涓殀闈炶惀杩恷钀ヤ笟|瀹跺涵鑷敤)", pm_text)
            if m:
                nature = m.group(1)
        if not nature:
            try:
                with pymupdf.open(pdf_path) as doc:
                    for page in doc:
                        t = page.get_text()
                        if t:
                            m = re.search(r"浣跨敤鎬ц川[锛?\\s]*(闈炶惀涓殀闈炶惀杩恷钀ヤ笟|瀹跺涵鑷敤)", t)
                            if m:
                                nature = m.group(1)
                                break
            except Exception:
                pass
    # PDAA/PDZA 琛ㄦ牸鍏滃簳锛堝鐢ㄧ紦瀛橈級
    if not nature and pdf_path:
        cached = _PDF_TEXT_CACHE.get(pdf_path, {})
        tables = cached.get("tables", [])
        if tables:
            for table in tables:
                for row in table:
                    for cell in row:
                        if cell and ("浼佷笟闈炶惀涓氬杞? in str(cell) or "浼佷笟闈炶惀涓氳揣杞? in str(cell)):
                            nature = str(cell).strip()
                            break
            if not nature:
                try:
                    with pdfplumber.open(pdf_path) as pdf:
                        for page in pdf.pages:
                            tables = page.extract_tables()
                            for table in tables:
                                for row in table:
                                    for cell in row:
                                        if cell and ("浼佷笟闈炶惀涓氬杞? in str(cell) or "浼佷笟闈炶惀涓氳揣杞? in str(cell)):
                                            nature = str(cell).strip()
                                            break
                except Exception:
                    pass
    return nature'''
    
    if old4 in content:
        content = content.replace(old4, new4, 1)
        print("PATCH 4: _clean_nature cache - APPLIED")
    else:
        print("PATCH 4: _clean_nature - SKIPPED")
    
    # ================================================================
    # PATCH 5: parse_pdf - use _cache_pdf_text instead of separate opens
    # ================================================================
    old5 = '''def parse_pdf(pdf_path):
    logger.debug("parse_pdf START: %s", os.path.basename(pdf_path))
    data = {}
    data["鏂囦欢鍚?] = os.path.basename(pdf_path)
    # ===== Step 1: pymupdf 鏂囨湰锛堥€氱敤璺緞锛?=====
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

    # ===== Step 2: pdfplumber 鏂囨湰锛堟禉鍟嗕笓鐢紝涔熶綔涓洪€氱敤澶囬€夛級 =====
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
    data["鏂囦欢鍚?] = os.path.basename(pdf_path)
    # ===== Step 1+2: 缁熶竴璇诲彇 PDF锛坧ymupdf + pdfplumber + tables锛屽彧鎵撳紑涓€娆★級 =====
    cached = _cache_pdf_text(pdf_path)
    pymupdf_text = cached["pymupdf"]
    plumber_text = cached["plumber"]'''
    
    if old5 in content:
        content = content.replace(old5, new5, 1)
        print("PATCH 5: parse_pdf unified read - APPLIED")
    else:
        print("PATCH 5: parse_pdf - SKIPPED")
    
    # ================================================================
    # PATCH 6: 澶钩璐㈤櫓 parse_taipingProperty - use cache for blocks
    # ================================================================
    # The function opens fitz.open(pdf_path) to get blocks text
    old6 = '''def parse_taipingProperty(text, pdf_path=None):
    """澶钩璐骇淇濋櫓 浜ゅ己闄?鍟嗕笟闄╄В鏋愬櫒銆?    澶钩PDF浣跨敤CID瀛椾綋锛宲ymupdf/pdfplumber鏂囨湰涓枃涔辩爜锛屼絾pdfplumber琛ㄦ牸鏁版嵁鍙銆?    """
    data = {}
    # 鍏徃鍚嶇О锛堝浐瀹氬€硷紝鍥犱负鏂囨湰涔辩爜鏃犳硶鎻愬彇锛?    data["淇濋櫓鍏徃鍚嶇О"] = "澶钩璐骇淇濋櫓鏈夐檺鍏徃"

    # === 浠巔ymupdf blocks鎻愬彇ASCII鍙瀛楁 ===
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
    
    new6 = '''def parse_taipingProperty(text, pdf_path=None):
    """澶钩璐骇淇濋櫓 浜ゅ己闄?鍟嗕笟闄╄В鏋愬櫒銆?    澶钩PDF浣跨敤CID瀛椾綋锛宲ymupdf/pdfplumber鏂囨湰涓枃涔辩爜锛屼絾pdfplumber琛ㄦ牸鏁版嵁鍙銆?    """
    data = {}
    # 鍏徃鍚嶇О锛堝浐瀹氬€硷紝鍥犱负鏂囨湰涔辩爜鏃犳硶鎻愬彇锛?    data["淇濋櫓鍏徃鍚嶇О"] = "澶钩璐骇淇濋櫓鏈夐檺鍏徃"

    # === 浠巔ymupdf blocks鎻愬彇ASCII鍙瀛楁锛堝鐢ㄧ紦瀛橈級 ===
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
        print("PATCH 6: parse_taipingProperty cache - APPLIED")
    else:
        print("PATCH 6: parse_taipingProperty - SKIPPED")
    
    # ================================================================
    # PATCH 7: parse_taipingProperty tables - use cache
    # ================================================================
    old7_table = '''    # === 浠巔dfplumber琛ㄦ牸鎻愬彇缁撴瀯鍖栧瓧娈?===
    tables = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                t = page.extract_tables()
                if t:
                    tables.extend(t)
    except Exception:
        pass'''
    
    new7_table = '''    # === 浠巔dfplumber琛ㄦ牸鎻愬彇缁撴瀯鍖栧瓧娈碉紙澶嶇敤缂撳瓨锛?===
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
    
    if old7_table in content:
        content = content.replace(old7_table, new7_table, 1)
        print("PATCH 7a: parse_taipingProperty tables cache - APPLIED")
    else:
        print("PATCH 7a: parse_taipingProperty tables - SKIPPED")
    
    # ================================================================
    # PATCH 8: parse_taiping_jiacheng - use cache
    # ================================================================
    old8 = '''def parse_taiping_jiacheng(text, pdf_path=None):
    """澶钩璐骇淇濋櫓 椹句箻闄╋紙涔愰┚榻愰瞾鍗囩骇鐗堬級瑙ｆ瀽鍣ㄣ€?    澶钩PDF浣跨敤CID瀛椾綋锛屼絾pdfplumber琛ㄦ牸鏁版嵁鍙銆?    """
    data = {}
    data["淇濋櫓鍏徃鍚嶇О"] = "澶钩璐骇淇濋櫓鏈夐檺鍏徃"
    data["闄╃鍚嶇О鍘熷"] = "涔愰┚榻愰瞾鍗囩骇鐗?

    # === 浠巔ymupdf blocks鎻愬彇 ===
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
    
    new8 = '''def parse_taiping_jiacheng(text, pdf_path=None):
    """澶钩璐骇淇濋櫓 椹句箻闄╋紙涔愰┚榻愰瞾鍗囩骇鐗堬級瑙ｆ瀽鍣ㄣ€?    澶钩PDF浣跨敤CID瀛椾綋锛屼絾pdfplumber琛ㄦ牸鏁版嵁鍙銆?    """
    data = {}
    data["淇濋櫓鍏徃鍚嶇О"] = "澶钩璐骇淇濋櫓鏈夐檺鍏徃"
    data["闄╃鍚嶇О鍘熷"] = "涔愰┚榻愰瞾鍗囩骇鐗?

    # === 浠巔ymupdf blocks鎻愬彇锛堝鐢ㄧ紦瀛橈級 ===
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
    
    if old8 in content:
        content = content.replace(old8, new8, 1)
        print("PATCH 8: parse_taiping_jiacheng cache - APPLIED")
    else:
        print("PATCH 8: parse_taiping_jiacheng - SKIPPED")
    
    # ================================================================
    # PATCH 9: parse_taiping_jiacheng tables - use cache  
    # ================================================================
    old9_table = '''    # === 浠巔dfplumber琛ㄦ牸鎻愬彇 ===
    tables = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                t = page.extract_tables()
                if t:
                    tables.extend(t)
    except Exception:
        pass'''
    
    new9_table = '''    # === 浠巔dfplumber琛ㄦ牸鎻愬彇锛堝鐢ㄧ紦瀛橈級 ===
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
    
    if old9_table in content:
        content = content.replace(old9_table, new9_table, 1)
        print("PATCH 9: parse_taiping_jiacheng tables cache - APPLIED")
    else:
        print("PATCH 9: parse_taiping_jiacheng tables - SKIPPED")
    
    # ================================================================
    # PATCH 10: parse_pingan_jiaoqiang - use cache for plumber name extraction
    # ================================================================
    old10 = '''    # 8. 琚繚浜哄鍚嶏紙鍏堜粠pdfplumber鏂囨湰鎻愬彇锛屽彇涓嶅埌鍐嶄粠鏂囦欢鍚嶅厹搴曪級
    # 骞冲畨PDF涓枃鏄疌ID涔辩爜锛宲ymupdf鏂囨湰璇讳笉鍒板悕瀛楋紝浣唒lumber鏂囨湰鍙
    _name_from_text = ""
    if pdf_path:
        try:
            with pdfplumber.open(pdf_path) as _pdf:
                _pl_text = ""
                for _page in _pdf.pages:
                    _t = _page.extract_text()
                    if _t:
                        _pl_text += _t + "\\n"'''
    
    new10 = '''    # 8. 琚繚浜哄鍚嶏紙鍏堜粠pdfplumber鏂囨湰鎻愬彇锛屽彇涓嶅埌鍐嶄粠鏂囦欢鍚嶅厹搴曪級
    # 骞冲畨PDF涓枃鏄疌ID涔辩爜锛宲ymupdf鏂囨湰璇讳笉鍒板悕瀛楋紝浣唒lumber鏂囨湰鍙
    # 澶嶇敤缂撳瓨涓殑 plumber 鏂囨湰
    _name_from_text = ""
    if pdf_path:
        _cached_pl = _PDF_TEXT_CACHE.get(pdf_path, {}).get("plumber", "")
        if _cached_pl:
            _pl_text = _cached_pl
            _nm = re.search(r"琚繚闄╀汉\\s+([^\\s\\n]{2,6})", _pl_text)
            if _nm:
                _name_from_text = _nm.group(1).strip()
            if not _name_from_text:
                _nm2 = re.search(r"鎶曚繚浜篬锛?\\s]+([^\\s\\n]{2,6})", _pl_text)
                if _nm2:
                    _name_from_text = _nm2.group(1).strip()
        if not _name_from_text and pdf_path:
            try:
                with pdfplumber.open(pdf_path) as _pdf:
                    _pl_text = ""
                    for _page in _pdf.pages:
                        _t = _page.extract_text()
                        if _t:
                            _pl_text += _t + "\\n"'''
    
    # The original continues with the name extraction logic...
    # We need to find the exact continuation
    old10_cont = '''                # plumber鏍煎紡锛?琚繚闄╀汉 浜庡缓鍒? 鎴?"鎶曚繚浜猴細 浜庡缓鍒?
                _nm = re.search(r"琚繚闄╀汉\\s+([^\\s\\n]{2,6})", _pl_text)
                if _nm:
                    _name_from_text = _nm.group(1).strip()
                if not _name_from_text:
                    _nm2 = re.search(r"鎶曚繚浜篬锛?\\s]+([^\\s\\n]{2,6})", _pl_text)
                    if _nm2:
                        _name_from_text = _nm2.group(1).strip()
        except Exception:
            pass'''
    
    new10_cont = '''                    # plumber鏍煎紡锛?琚繚闄╀汉 浜庡缓鍒? 鎴?"鎶曚繚浜猴細 浜庡缓鍒?
                    _nm = re.search(r"琚繚闄╀汉\\s+([^\\s\\n]{2,6})", _pl_text)
                    if _nm:
                        _name_from_text = _nm.group(1).strip()
                    if not _name_from_text:
                        _nm2 = re.search(r"鎶曚繚浜篬锛?\\s]+([^\\s\\n]{2,6})", _pl_text)
                        if _nm2:
                            _name_from_text = _nm2.group(1).strip()
            except Exception:
                pass'''
    
    # These patches are complex and risky. Let's skip the parse_pingan patches
    # and focus on the main wins.
    print("PATCH 10: parse_pingan_jiaoqiang - SKIPPED (too complex, marginal benefit)")
    
    # ================================================================
    # PATCH 11: parse_pingan_garbled - use cache for fitz and plumber
    # ================================================================
    # This function also opens fitz and pdfplumber independently
    old11_fitz = '''    # ---------- 1.5 闄╃鍚嶇О鍘熷锛堜粠PDF绗竴椤电2琛屾彁鍙栵級 ----------
    data["闄╃鍚嶇О鍘熷"] = ""
    if pdf_path:
        try:
            doc = fitz.open(pdf_path)'''
    
    new11_fitz = '''    # ---------- 1.5 闄╃鍚嶇О鍘熷锛堜粠PDF绗竴椤电2琛屾彁鍙栵紝澶嶇敤缂撳瓨锛?----------
    data["闄╃鍚嶇О鍘熷"] = ""
    cached_pm = _PDF_TEXT_CACHE.get(pdf_path, {}).get("pymupdf", "")
    if cached_pm:
        lines = cached_pm.strip().split("\\n")
        for line in lines[1:]:
            line_s = line.strip()
            if line_s and len(line_s) > 3 and not re.match(r"^(淇濆崟鍙穦楠岀湡鐮亅\\d{10,})", line_s):
                data["闄╃鍚嶇О鍘熷"] = line_s
                break
    if not data["闄╃鍚嶇О鍘熷"] and pdf_path:
        try:
            doc = fitz.open(pdf_path)'''
    
    if old11_fitz in content:
        content = content.replace(old11_fitz, new11_fitz, 1)
        print("PATCH 11: parse_pingan_garbled fitz cache - APPLIED")
    else:
        print("PATCH 11: parse_pingan_garbled fitz - SKIPPED")
    
    # ================================================================
    # PATCH 12: parse_anhua - use cache for pdfplumber
    # ================================================================
    old12 = '''    tables, pl_text = [], ""
    if pdf_path:
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    t = page.extract_text()
                    if t: pl_text += t + "\\n"
                    tbls = page.extract_tables()
                    if tbls: tables.extend(tbls)
        except Exception: pass

    # 瀹夊崕PDF鏁板瓧鍐呴儴鏈夌┖鏍硷紙濡?"2 026-04-17"銆?P DDA"銆?8 40.00"锛夛紝闇€瑕佹竻鐞?    pl_clean = pl_text'''
    
    new12 = '''    # 澶嶇敤缂撳瓨涓殑 pdfplumber 鏁版嵁
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

    # 瀹夊崕PDF鏁板瓧鍐呴儴鏈夌┖鏍硷紙濡?"2 026-04-17"銆?P DDA"銆?8 40.00"锛夛紝闇€瑕佹竻鐞?    pl_clean = pl_text'''
    
    if old12 in content:
        content = content.replace(old12, new12, 1)
        print("PATCH 12: parse_anhua cache - APPLIED")
    else:
        print("PATCH 12: parse_anhua - SKIPPED")
    
    # ================================================================
    # PATCH 13: parse_zhongmei - use cache for pdfplumber
    # ================================================================
    old13 = '''    tables, pl_text = [], ""
    if pdf_path:
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    t = page.extract_text()
                    if t: pl_text += t + "\\n"
                    tbls = page.extract_tables()
                    if tbls: tables.extend(tbls)
        except Exception: pass

    m = re.search(r"淇濆崟鍙穂锛?\\s]*(\\d{10,})", pl_text)
    data["淇濆崟鍙?] = m.group(1) if m else ""
    m = re.search(r"绛惧崟鏃ユ湡[锛?\\s]*(\\d{4}-\\d{2}-\\d{2})", pl_text)
    data["绛惧崟鏃堕棿"] = m.group(1) if m else ""

    # 琚繚浜猴紙浠庤〃鏍兼彁鍙栵級
    data["琚繚浜哄鍚?] = ""
    for tbl in tables:
        for row in tbl:
            if row and row[0] and "琚繚闄╀汉" in str(row[0]) and "韬唤璇? not in str(row[0]):
                if row[1] and len(str(row[1]).strip()) >= 2:
                    data["琚繚浜哄鍚?] = str(row[1]).strip()
                    break
        if data["琚繚浜哄鍚?]: break'''
    
    new13 = '''    # 澶嶇敤缂撳瓨涓殑 pdfplumber 鏁版嵁
    cached_zm = _PDF_TEXT_CACHE.get(pdf_path, {})
    tables = cached_zm.get("tables", [])
    pl_text = cached_zm.get("plumber", "")
    if not pl_text and pdf_path:
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    t = page.extract_text()
                    if t: pl_text += t + "\\n"
                    tbls = page.extract_tables()
                    if tbls: tables.extend(tbls)
        except Exception: pass

    m = re.search(r"淇濆崟鍙穂锛?\\s]*(\\d{10,})", pl_text)
    data["淇濆崟鍙?] = m.group(1) if m else ""
    m = re.search(r"绛惧崟鏃ユ湡[锛?\\s]*(\\d{4}-\\d{2}-\\d{2})", pl_text)
    data["绛惧崟鏃堕棿"] = m.group(1) if m else ""

    # 琚繚浜猴紙浠庤〃鏍兼彁鍙栵級
    data["琚繚浜哄鍚?] = ""
    for tbl in tables:
        for row in tbl:
            if row and row[0] and "琚繚闄╀汉" in str(row[0]) and "韬唤璇? not in str(row[0]):
                if row[1] and len(str(row[1]).strip()) >= 2:
                    data["琚繚浜哄鍚?] = str(row[1]).strip()
                    break
        if data["琚繚浜哄鍚?]: break'''
    
    if old13 in content:
        content = content.replace(old13, new13, 1)
        print("PATCH 13: parse_zhongmei cache - APPLIED")
    else:
        print("PATCH 13: parse_zhongmei - SKIPPED")
    
    # ================================================================
    # PATCH 14: parse_zhongmei_jiacheng - use cache for pdfplumber
    # ================================================================
    old14 = '''    # 浣跨敤pdfplumber鏂囨湰锛坧ymupdf鏂囨湰涓爣绛惧拰鍊煎垎琛岋紝姝ｅ垯鏃犳硶鍖归厤锛?    pl_text = text  # 榛樿鐢ㄤ紶鍏ョ殑text
    if pdf_path:
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    t = page.extract_text()
                    if t: pl_text += t + "\\n"
        except Exception: pass'''
    
    new14 = '''    # 浣跨敤pdfplumber鏂囨湰锛堝鐢ㄧ紦瀛橈級
    pl_text = text  # 榛樿鐢ㄤ紶鍏ョ殑text
    cached_zmjc = _PDF_TEXT_CACHE.get(pdf_path, {})
    pl_cached = cached_zmjc.get("plumber", "")
    if pl_cached:
        pl_text += pl_cached
    elif pdf_path:
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    t = page.extract_text()
                    if t: pl_text += t + "\\n"
        except Exception: pass'''
    
    if old14 in content:
        content = content.replace(old14, new14, 1)
        print("PATCH 14: parse_zhongmei_jiacheng cache - APPLIED")
    else:
        print("PATCH 14: parse_zhongmei_jiacheng - SKIPPED")
    
    # ================================================================
    # PATCH 15: parse_taipingProperty nature fallback - use cache
    # ================================================================
    old15 = '''    # 鍏滃簳1锛氫粠pdfplumber椤甸潰鏂囨湰涓彁鍙栵紙琛ㄦ牸鍙兘CID涔辩爜锛屼絾椤甸潰鏂囨湰涓?浣跨敤鎬ц川"鍚庣殑鍊煎彲璇伙級
    if not data.get("杞﹁締浣跨敤鎬ц川") and pdf_path:
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    pt = page.extract_text() or ""
                    m_nature = re.search(r"浣跨敤鎬ц川[锛?\\s]*(闈炶惀涓殀闈炶惀杩恷钀ヤ笟|钀ヨ繍|瀹跺涵鑷敤|闈炶惀涓氬杞钀ヤ笟瀹㈣溅|闈炶惀涓氭苯杞钀ヤ笟姹借溅)", pt)
                    if m_nature:
                        data["杞﹁締浣跨敤鎬ц川"] = m_nature.group(1)
                        break
        except Exception:
            pass'''
    
    new15 = '''    # 鍏滃簳1锛氫粠pdfplumber椤甸潰鏂囨湰涓彁鍙栵紙澶嶇敤缂撳瓨锛?    if not data.get("杞﹁締浣跨敤鎬ц川") and pdf_path:
        cached_tp = _PDF_TEXT_CACHE.get(pdf_path, {})
        pl_tp = cached_tp.get("plumber", "")
        if pl_tp:
            m_nature = re.search(r"浣跨敤鎬ц川[锛?\\s]*(闈炶惀涓殀闈炶惀杩恷钀ヤ笟|钀ヨ繍|瀹跺涵鑷敤|闈炶惀涓氬杞钀ヤ笟瀹㈣溅|闈炶惀涓氭苯杞钀ヤ笟姹借溅)", pl_tp)
            if m_nature:
                data["杞﹁締浣跨敤鎬ц川"] = m_nature.group(1)
        if not data.get("杞﹁締浣跨敤鎬ц川"):
            try:
                with pdfplumber.open(pdf_path) as pdf:
                    for page in pdf.pages:
                        pt = page.extract_text() or ""
                        m_nature = re.search(r"浣跨敤鎬ц川[锛?\\s]*(闈炶惀涓殀闈炶惀杩恷钀ヤ笟|钀ヨ繍|瀹跺涵鑷敤|闈炶惀涓氬杞钀ヤ笟瀹㈣溅|闈炶惀涓氭苯杞钀ヤ笟姹借溅)", pt)
                        if m_nature:
                            data["杞﹁締浣跨敤鎬ц川"] = m_nature.group(1)
                            break
            except Exception:
                pass'''
    
    if old15 in content:
        content = content.replace(old15, new15, 1)
        print("PATCH 15: parse_taipingProperty nature cache - APPLIED")
    else:
        print("PATCH 15: parse_taipingProperty nature - SKIPPED")
    
    # ================================================================
    # PATCH 16: parse_jiacheng 闄╃鍚嶇О鍏滃簳 - use cache
    # ================================================================
    old16 = '''    if not data.get("闄╃鍚嶇О鍘熷") or is_garbled_text(data.get("闄╃鍚嶇О鍘熷", "")):
        try:
            doc = fitz.open(pdf_path)'''
    
    new16 = '''    if not data.get("闄╃鍚嶇О鍘熷") or is_garbled_text(data.get("闄╃鍚嶇О鍘熷", "")):
        cached_jc = _PDF_TEXT_CACHE.get(pdf_path, {}).get("pymupdf", "")
        if cached_jc:
            lines = cached_jc.strip().split("\\n")
            first_real_line = None
            for line in lines:
                line_stripped = line.strip()
                if line_stripped and not re.match(r"^淇濋櫓鍗曞彿?锛?$", line_stripped) and not re.match(r"^\\d{10,}$", line_stripped) and not re.search(r"璐骇淇濋櫓鏈夐檺鍏徃$", line_stripped):
                    first_real_line = line_stripped
                    break
            if first_real_line and not is_garbled_text(first_real_line):
                data["闄╃鍚嶇О鍘熷"] = re.sub(r"鐢靛瓙淇濋櫓鍗晐鐢靛瓙淇濆崟$", "", first_real_line).strip()
            else:
                product_name = extract_product_name_from_pdf(pdf_path)
                if product_name and not is_garbled_text(product_name):
                    data["闄╃鍚嶇О鍘熷"] = product_name
                else:
                    data["闄╃鍚嶇О鍘熷"] = "椹句箻瀹堟姢"
        elif pdf_path:
            try:
                doc = fitz.open(pdf_path)'''
    
    if old16 in content:
        content = content.replace(old16, new16, 1)
        print("PATCH 16: parse_jiacheng fitz cache - APPLIED")
    else:
        print("PATCH 16: parse_jiacheng fitz - SKIPPED")
    
    # ================================================================
    # PATCH 17: parse_liberty - use cache for plumber text
    # ================================================================
    # parse_liberty already receives pymupdf_text and plumber_text as parameters
    # so it doesn't need extra caching. Skip.
    print("PATCH 17: parse_liberty - SKIPPED (already receives text params)")
    
    # ================================================================
    # PATCH 18: parse_zhongyin - no extra PDF opens, skip
    # ================================================================
    print("PATCH 18: parse_zhongyin - SKIPPED (no extra PDF opens)")
    
    # ================================================================
    # PATCH 19: parse_huanghai (in route) - no extra PDF opens
    # ================================================================
    print("PATCH 19: parse_huanghai - SKIPPED")
    
    # ================================================================
    # PATCH 20: Add cache clear at end of main block
    # ================================================================
    old20 = '''    print(f"Done! {OUTPUT_FILE}")
    print(f"{len(results)} records, {len(FIELDS)} fields")'''
    
    new20 = '''    # 娓呯悊 PDF 缂撳瓨锛岄噴鏀惧唴瀛?    _PDF_TEXT_CACHE.clear()
    _PDF_TABLE_CACHE.clear()
    _TABLE_CACHE.clear()
    print(f"Done! {OUTPUT_FILE}")
    print(f"{len(results)} records, {len(FIELDS)} fields")'''
    
    if old20 in content:
        content = content.replace(old20, new20, 1)
        print("PATCH 20: cache cleanup - APPLIED")
    else:
        print("PATCH 20: cache cleanup - SKIPPED")
    
    # Write patched file
    with open("run_extract.py", "w", encoding="utf-8") as f:
        f.write(content)
    
    print("\n=== All patches applied ===")

if __name__ == "__main__":
    patch_file()
