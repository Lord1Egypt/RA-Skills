# -*- coding: utf-8 -*-
"""
车险保单 PDF 字段提取脚本 v5.7.5

支持保险公司（10家）：
  - 浙商（交强险/商业险/驾意险）
  - 太平洋（交强险/商业险/畅行保）
  - 人保（PDAA/PDZA/PEBS如意行）
  - 亚太（交强险/商业险/非车险EDY/EDV）
  - 大地（交强险/商业险/安行如意保）
  - 平安（交强险/商业险/车主尊享保障）
  - 阳光（驾乘人员团体意外险）
  - 太平财险（交强险/商业险/乐驾齐鲁驾乘险）
  - 泰山财险（交强险/商业险/驾乘意外险）
  - 利宝保险（交强险+驾乘险合并PDF，拆分为两行）
"""
import re, os, sys, logging
import traceback
from collections import Counter
import fitz
import pymupdf
import pdfplumber
import pandas as pd
from pathlib import Path
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows

# =============================================================================
# Performance Optimization: PDF Read Cache
# =============================================================================
_PDF_TEXT_CACHE = {}   # {pdf_path: {"pymupdf": str, "plumber": str, "tables": list}}
_PDF_TABLE_CACHE = {}  # {pdf_path: dict}  safe_extract_tables result cache

def _cache_pdf_text(pdf_path):
    """Read and cache PDF pymupdf text, plumber text, and table data. Open only once."""
    if pdf_path in _PDF_TEXT_CACHE:
        return _PDF_TEXT_CACHE[pdf_path]
    result = {"pymupdf": "", "plumber": "", "tables": []}
    # pymupdf text
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
    # pdfplumber text + tables
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

# ===========================================================================
# Logging 配置：默认只输出到 stdout，环境变量 LOG_FILE 可指定文件输出
# ===========================================================================
logger = logging.getLogger("run_extract")
if not logger.handlers:
    _log_level = logging.DEBUG if os.environ.get("DEBUG") else logging.INFO
    logger.setLevel(_log_level)
    _handler = logging.StreamHandler(sys.stdout)
    _handler.setLevel(_log_level)
    _handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s", datefmt="%H:%M:%S"))
    logger.addHandler(_handler)
    # 可选：通过环境变量 LOG_FILE 启用文件输出
    _log_file = os.environ.get("LOG_FILE")
    if _log_file:
        _fh = logging.FileHandler(_log_file, encoding="utf-8")
        _fh.setLevel(_log_level)
        _fh.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
        logger.addHandler(_fh)

# =============================================================================
# 中文数字转换（支持交强险车船税中文大写）
# =============================================================================
CN_MAP = {'零':0,'一':1,'二':2,'三':3,'四':4,'五':5,'六':6,'七':7,'八':8,'九':9,'十':10,'百':100,'佰':100,'仟':1000,'千':1000}

def chinese_num(cn_str):
    """Convert Chinese numeral string like '叁佰陆拾元整' to float. Returns None on failure."""
    cn_str = cn_str.replace('元整','').replace('元','')
    total = 0
    cur = 0
    for ch in cn_str:
        if ch in CN_MAP:
            v = CN_MAP[ch]
            if v >= 100:
                cur = cur * v if cur else v
            elif v == 10:
                cur = cur * 10 if cur else 10
            else:
                cur += v
        # 空格忽略
    return total + cur if total or cur else None

# =============================================================================
# 常量
# =============================================================================

def safe_extract_phone(text):
    """Extract phone: prioritize masked (带*脱敏), fallback to clean, fallback to raw 11-digit."""
    MASKED_PATTERNS = [
        r"联系电话[：:\s]*(1[3-9][\d\*]{9})",
        r"电话[：:\s]*(1[3-9][\d\*]{9})",
        r"手机[号号码]*[：:\s]*(1[3-9][\d\*]{9})",
        r"联\s*系\s*电\s*话[：:\s]*(1[3-9][\d\*]{9})",
    ]
    CLEAN_PATTERNS = [
        r"联系电话[：:\s]*(1[3-9]\d{9})\b",
        r"电话[：:\s]*(1[3-9]\d{9})\b",
        r"手机[号号码]*[：:\s]*(1[3-9]\d{9})\b",
        r"联\s*系\s*电\s*话[：:\s]*(1[3-9]\d{9})\b",
    ]
    for p in MASKED_PATTERNS:
        m = re.search(p, text)
        if m:
            return m.group(1).strip()
    for p in CLEAN_PATTERNS:
        m = re.search(p, text)
        if m and '*' not in m.group(1):
            return m.group(1).strip()
    # 兜底：直接找11位手机号
    matches = re.findall(r'\b(1[3-9]\d{9})\b', text)
    if matches:
        return matches[0]
    return ""

PDF_FOLDER = r"C:\Users\Administrator\Desktop\车险保单"
OUTPUT_FILE = r"C:\Users\Administrator\Desktop\车险保单提取结果_v5.xlsx"

FIELDS = [
    "签单时间", "保险公司名称", "保单号", "保险起期",
    "车辆使用性质", "车架号", "车辆型号名称",
    "被保人姓名", "被保险人证件号", "被保险人手机号",
    "车牌号码", "险种名称原始", "实收保费", "车船税"
]

# 使用性质白名单

NATURE_LIST = [
    "非营业",
    "非营运",
    "营业",
    "营运",
    "家庭自用",
    "非营业企业",
    "非营业个人",
    "非营业客车",
    "营业客车",
    "家庭自用客车",
    "六座以下客车",
    "家庭自用汽车",
    "非营业汽车",
    "营业汽车",
    "非营业货车",
    "营业货车",
    "企业非营业用车",
    "非营业用车",
    "企业非营业客车",
]

NATURE_PATTERN = "|".join(NATURE_LIST)

PROVINCES = "鲁|京|津|沪|渝|冀|豫|云|辽|黑|湘|皖|山东|山西|疆|藏|贵|甘|青|桂|琼|苏|浙|蒙|鄂"
PLATE_PATTERN = rf"[{PROVINCES}][A-Z0-9\-]{{5,8}}"

# VIN→车辆型号映射表（用于PDF本身无厂牌型号字段时兜底查询）
VIN_MODEL_LOOKUP = {
    "W1NFB4KB0NA622103": "奔驰BENZ GLE350越野车",    # 太平洋交强险 Row2
    "LSGAR5AL6HH106096": "凯迪拉克SGM7200AAA3轿车",  # 罗方春 Row16-18
    "LFMJ34AF7E3057174": "丰田CA64604TME5多用途乘用车",  # 丁天皓 Row19-21
    "LSGPB54U8DD006814": "别克SGM7161ATC轿车",      # 人保/大地 Row5/7 张迪
}

def safe_extract(text, patterns):
    """Try multiple regex patterns, return first non-empty match. Supports (pattern, flags) tuples."""
    for p in patterns:
        flags = 0
        if isinstance(p, tuple):
            pat, flags = p
        else:
            pat = p
        try:
            m = re.search(pat, text, flags)
            if m:
                # Use group(1) if available (explicit capture), else group(0) (full match)
                val = m.group(1).strip() if m.lastindex is not None and m.lastindex >= 1 else m.group(0).strip()
                if val:
                    return val
        except Exception:
            pass
    return ""

def safe_extract_all(text, patterns):
    """Collect ALL pattern matches, return the longest one (most specific policy number)."""
    candidates = []
    for p in patterns:
        flags = 0
        if isinstance(p, tuple):
            pat, flags = p
        else:
            pat = p
        try:
            for m in re.finditer(pat, text, flags):
                val = m.group(1).strip()
                if val and len(val) >= 6:
                    candidates.append(val)
        except Exception:
            pass
    if not candidates:
        return ""
    return max(candidates, key=len)

def _filter_policy_no(val):
    """过滤保单号的垃圾值（金额等），但保留纯数字的合法保单号"""
    if not val:
        return ""
    s = str(val).strip()
    # 过滤纯金额（带小数点）
    if re.match(r'^[\d.,]+$', s) and '.' in s:
        return ""
    # 过滤18位统一社会信用代码
    if re.match(r'^\d{18}$', s):
        return ""
    # 过滤太短的
    if len(s) < 6:
        return ""
    return s

def safe_extract_policy_no(text, label="保险单号"):
    """
    专门提取保单号：找到label后，在后续内容中搜索所有10位以上的字母数字串，
    返回最长匹配（避免因归档号/短号优先匹配而导致真正policy号遗漏）。
    尝试多个可能的标签（保险单号、保单号），返回最长匹配。
    """
    for lbl in [label, "保单号"]:
        idx = text.find(lbl)
        if idx < 0:
            continue
        segment = text[idx:idx+300]
        candidates = re.findall(r'[A-Z0-9]{10,}', segment)
        if candidates:
            return max(candidates, key=len)
    return ""

def get_lines(text):
    return [l for l in text.split("\n") if l.strip()]

# 模块级缓存：避免同一 PDF 重复打开读取表格
_TABLE_CACHE = {}

def safe_extract_tables(pdf_path):
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
                tables = page.extract_tables()
                for tbl in tables:
                    for row in tbl:
                        if not row:
                            continue
                        for ci, cell in enumerate(row):
                            if not cell:
                                continue
                            s = str(cell).strip()
                            if not s:
                                continue
                            # 被保险人姓名：label在col0/1，value在col2/3
                            if s in ("被保险人", "投保人", "姓名") and ci + 1 < len(row):
                                nxt = str(row[ci + 1]).strip()
                                if nxt and len(nxt) >= 2 and not nxt[0].isdigit():
                                    result["insured_name"] = nxt
                            # 证件号：18位
                            snum = re.sub(r'\s', '', s)
                            if len(snum) == 18 and snum[-1] in 'X0123456789' and snum[:17].isdigit():
                                result["id_card"] = snum
                            elif len(snum) == 15 and snum.isdigit():
                                result["id_card"] = snum
                            # 手机号（完整号，不脱敏）
                            sm = re.search(r'(1[3-9]\d{9})', s)
                            if sm:
                                _ph = sm.group(1)
                                result["phone"] = "" if is_blacklisted_phone(_ph) else _ph
                            # 车牌号（含³前缀噪音字符，需要strip非ASCII前缀）
                            plate_m = re.search(r'([鲁京津沪渝冀豫云辽黑湘皖晋疆藏贵甘青桂琼苏浙蒙鄂][A-Z0-9]{5,8})', s)
                            if plate_m:
                                plate = plate_m.group(1)
                                # 去掉前导噪音字符（³等）
                                plate = re.sub(r'^[^A-Z0-9\u4e00-\u9fff]+', '', plate)
                                if plate:
                                    result["plate"] = plate
                            # VIN码：17位
                            vm = re.search(r'\b([A-HJ-NP-Z0-9]{17})\b', s)
                            if vm and not vm.group(1).isdigit():
                                result["vin"] = vm.group(1)
                            # 车辆型号：含关键品牌关键词
                            if any('\u4e00' <= c <= '\u9fff' for c in s):
                                for kw in ['SGM', 'CA4', 'LFV', 'LSG', 'LF', 'LFP', 'LJ', 'LZ', 'WVW', 'LGW', 'LGX', 'DC', 'LDC', 'LDCB', 'BJ', 'FV', 'SGM', 'SC']:
                                    if kw in s.upper() and 5 < len(s) < 60:
                                        result["model"] = s
                                        break
                            # 使用性质：优先匹配最长关键词（家庭自用 > 企业非营业 > 非营业 > 营业）
                            use_natures = ['家庭自用', '企业非营业', '非营业', '营业', '营业客车', '非营业客车']
                            for kw in use_natures:
                                if kw in s:
                                    result["use_nature"] = kw
                                    break
                            # 保费：跳过"保费合计"行（那是总计不是单项保费），优先找险种行中的金额
                            # 格式如 "交强险855.00元" 或 "¥855.00"
                            if '保费合计' in s or '详细' in s:
                                pass  # 跳过合计行
                            else:
                                for fm in re.findall(r'([0-9,]+\.\d{2})', s):
                                    try:
                                        val = float(fm.replace(',', ''))
                                        if 100 <= val <= 20000:
                                            result["premium"] = fm
                                    except Exception:
                                        pass
                            # 车船税（仅在交强险代收，金额固定360元）
                            if '车船税' in s or ('当年' in s and '应缴' in s):
                                fm2 = re.search(r'([0-9,]+\.\d{2})', s)
                                if fm2:
                                    try:
                                        val = float(fm2.group(1).replace(',', ''))
                                        if 0 <= val <= 2000:
                                            result["tax"] = fm2.group(1)
                                    except Exception:
                                        pass
                            # 保险期间：支持CJK格式（分起至连用，无空格）以及带空格格式
                            # 格式: "保险期间： 2026年4月16日0时0分起至 2027年4月16日0时0分止"
                            # 关键：起=U+8D77，至=U+81F3，连用时分和起之间无空格，但至后可以有空格
                            # 使用chr()生成literal Unicode字符，避免脚本存储为ASCII转义文本
                            pdm = re.search(
                                r'(\d{4}年\d{1,2}月\d{1,2}日\d{1,2}时\d{1,2}分)\s*' + chr(0x8D77) + chr(0x81F3) + r'\s*(\d{4}年\d{1,2}月\d{1,2}日\d{1,2}时\d{1,2}分)',
                                s, flags=re.UNICODE
                            )
                            if pdm:
                                result["period"] = pdm.group(1).replace(' ', '') + " 至 " + pdm.group(2).replace(' ', '')
                            # Fallback: single 至/到 char (for CID garbled PDFs where only U+81F3=至 survives)
                            if not result.get("period"):
                                pdm2 = re.search(
                                    r'(\d{4}年\d{1,2}月\d{1,2}日\d{1,2}时\d{1,2}分)\s*[至到]\s*(\d{4}年\d{1,2}月\d{1,2}日\d{1,2}时\d{1,2}分)',
                                    s
                                )
                                if pdm2:
                                    result["period"] = pdm2.group(1).replace(' ', '') + " 至 " + pdm2.group(2).replace(' ', '')
                            # 保单号：29开头15-22位
                            pnm = re.search(r'(29\d{13,22})', s)
                            if pnm:
                                result["policy_no"] = pnm.group(1)
                            # 签单时间：从pymupdf blocks文本中提取（格式：2026-03-30 09:41:42）
                            # 仅在safe_extract失败时填充
                            tsm = re.search(r'(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})', s)
                            if tsm and not result["sign_date"]:
                                result["sign_date"] = tsm.group(1)
    except Exception:
        pass
    if pdf_path:
        _TABLE_CACHE[pdf_path] = result
    return result

def extract_raw_bytes(pdf_path):
    """Extract raw byte content from PDF for byte-level fallback searches."""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                t = page.extract_text()
                if t:
                    return t.encode("utf-8", errors="replace")
    except Exception:
        pass
    return b""

def byte_level_premium(pdf_path):
    """Byte-level fallback: search \\d{3}\\xe5\\x85\\x83 (3 digits + '元') in raw PDF bytes."""
    raw = extract_raw_bytes(pdf_path)
    if not raw:
        return ""
    try:
        m = re.search(rb"\d{3}\xe5\x85\x83", raw)
        if m:
            start = max(0, m.start() - 3)
            num_bytes = raw[m.start() - 3 : m.start()]
            try:
                num_str = num_bytes.decode("utf-8", errors="replace")
                val = re.sub(r"[^\d]", "", num_str)
                if len(val) == 3:
                    return val
            except Exception:
                pass
    except Exception:
        pass
    return ""

# =============================================================================
# VIN/车架号格式校验
# =============================================================================
VIN_PREFIX_BLACKLIST = ["PDAA", "PDZA", "PDFA", "PEXD", "DZQT", "AJIN", "PEBS", "DZAW", "PDEJ", "DPEG", "PDDA", "PDZA", "PDGA", "P370", "P360", "P350", "P260"]

# 被保险人手机号黑名单（这些号码出现在PDF中时跳过，不写入Excel）
PHONE_BLACKLIST = frozenset([
    "15063838021",
    "18354580627",
])

def is_blacklisted_phone(phone):
    """检查手机号是否在黑名单中"""
    return phone in PHONE_BLACKLIST

def is_valid_vin(vin):
    """严格校验17位字符串是否是真实VIN码，排除保单号等误识别"""
    if not vin or len(vin) != 17:
        return False
    if not re.match(r"^[A-Z0-9]{17}$", vin):
        return False
    # 必须同时包含数字和字母（排除纯数字序列）
    has_digit = any(c.isdigit() for c in vin)
    has_letter = any(c.isalpha() for c in vin)
    if not (has_digit and has_letter):
        return False
    # 排除常见保单号前缀
    for p in VIN_PREFIX_BLACKLIST:
        if vin.startswith(p):
            return False
    # 字母数校验：真实VIN通常有3+个字母（排除纯数字流水号/保单号片段）
    letter_count = sum(1 for c in vin if c.isalpha())
    if letter_count < 3:
        return False
    return True

def extract_vin_strict(text, patterns):
    """提取车架号，通过is_valid_vin过滤保单号等误识别。patterns 中每个元素可以是字符串或 (字符串, flags) 元组。"""
    for p in patterns:
        if isinstance(p, tuple):
            pat, flags = p
        else:
            pat, flags = p, 0
        try:
            m = re.search(pat, text, flags)
            if m:
                cand = m.group(1).strip()
                if is_valid_vin(cand):
                    return cand
        except Exception:
            pass
    return ""

# =============================================================================
# 乱码检测 + OCR 兜底
# =============================================================================
def is_garbled_text(s):
    """Check if text is garbled (too many non-printable or rare CJK chars)."""
    if not s:
        return True
    cjk_count = sum(1 for c in s if '\u4e00' <= c <= '\u9fff')
    total = len(s)
    if total == 0:
        return True
    # If more than 70% are unprintable/rare, consider garbled
    rare_count = sum(1 for c in s if ord(c) > 0xFFFF or (not c.isprintable() and c not in '\n\r\t'))
    return rare_count / total > 0.7

def extract_product_name_from_pdf(pdf_path):
    """Extract product name from PDF using OCR fallback."""
    try:
        doc = fitz.open(pdf_path)
        page = doc[0]
        lines = page.get_text("text").strip().split("\n")
        for line in lines:
            line = line.strip()
            if line and not re.match(r"^\d{10,}$", line) and not re.match(r"^保险单号?：?$", line):
                if len(line) > 3 and len(line) < 50:
                    return re.sub(r"电子保险单|电子保单$", "", line).strip()
        doc.close()
    except Exception:
        pass
    return ""

# =============================================================================
# 签单时间兜底提取器（extract_sign_date.py 逻辑）
# =============================================================================
def _byte_extract_sign_date(pdf_path):
    """字节级双引擎兜底提取签单时间。供 parse_* 函数在 regex 失败时调用。"""
    try:
        # plumber 文本
        try:
            with pdfplumber.open(pdf_path) as pdf:
                pl_text = '\n'.join(p.extract_text() or '' for p in pdf.pages)
        except Exception:
            pl_text = ''
        # pymupdf 文本
        try:
            with pymupdf.open(pdf_path) as doc:
                pm_text = '\n'.join(page.get_text() for page in doc)
        except Exception:
            pm_text = ''

        # 字节级标签（用于 pdfplumber CID 乱码文本的 UTF-8 字节搜索）
        LABELS_BYTES = [
            "确认时间".encode("utf-8"),
            "出单确认时间".encode("utf-8"),
            "出单时间".encode("utf-8"),
            "保单确认时间".encode("utf-8"),
            "保单生成时间".encode("utf-8"),
            "签单日期".encode("utf-8"),
            "签单时间".encode("utf-8"),
        ]
        DATE_PATTERNS_BYTES = [
            rb'(\d{4})-(\d{1,2})-(\d{1,2})\s+(\d{2}:\d{2}:\d{2})',  # YYYY-MM-DD HH:MM:SS
            rb'(\d{4})-(\d{1,2})-(\d{1,2})',  # YYYY-MM-DD
            rb'(\d{4})\.(\d{2})\.(\d{2})\s+(\d{2}:\d{2}:\d{2})',  # YYYY.MM.DD HH:MM:SS
            rb'(\d{4})\.(\d{2})\.(\d{2})',  # YYYY.MM.DD
            rb'(\d{4})/(\d{1,2})/(\d{1,2})',  # YYYY/MM/DD
            rb'(\d{4})' + "年".encode("utf-8") + rb'(\d{1,2})' + "月".encode("utf-8") + rb'(\d{1,2})' + "日".encode("utf-8"),  # YYYY年MM月DD日
        ]

        def _find_label(src, start, end):
            for lb in LABELS_BYTES:
                pos = src.find(lb, start, end)
                if pos >= 0:
                    return pos
            return -1

        def _parse_match(m):
            g = m.groups()
            if len(g) == 4:
                return f"{g[0].decode()}-{int(g[1]):02d}-{int(g[2]):02d} {g[3].decode()}"
            elif len(g) == 3:
                return f"{g[0].decode()}-{int(g[1]):02d}-{int(g[2]):02d}"
            return ""

        def _search_src(src):
            if not src:
                return ""
            src_bytes = src.encode('utf-8', errors='replace') if isinstance(src, str) else src
            for pat in DATE_PATTERNS_BYTES:
                for m in re.finditer(pat, src_bytes):
                    date_str = _parse_match(m)
                    ds = m.start()
                    ss = max(0, ds - 120)
                    if _find_label(src_bytes, ss, ds) >= 0:
                        return date_str
            return ""

        # 优先 plumber，再 pymupdf
        result = _search_src(pl_text)
        if not result:
            result = _search_src(pm_text)
        return result
    except Exception:
        return ""

def _sign_date_fallback(pdf_path, current_val):
    """如果 current_val 为空，则调用字节级双引擎兜底提取。"""
    if current_val and str(current_val).strip():
        return current_val
    if pdf_path:
        return _byte_extract_sign_date(pdf_path)
    return current_val

# =============================================================================
# 公共字段提取（交强险/商业险/非车险 三个解析器共享）
# =============================================================================
def _extract_common_fields(text, company="unknown", pdf_path=None):
    """
    提取三个主要解析器共有的公共字段。
    返回 dict，仅包含公共字段（签单时间、保险公司名称、保单号、
    车架号、被保人姓名、被保险人证件号、被保险人手机号、
    车牌号码、车辆使用性质、车辆型号名称）。
    """
    data = {}

    # --- 1. 签单时间（主正则 + 字节级兜底 + CID乱码兜底） ---
    sign = safe_extract(text, [
        r"出单时间[：:\s]*(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})",
        r"签单日期[：:\s]*(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})",
        r"签单日期[：:\s]*(\d{4}-\d{2}-\d{2})",
        r"签单日期[：:\s]*(\d{4}/\d{2}/\d{2})",
        r"签单时间[：:\s]*(\d{4}年\d{2}月\d{2}日)",
        r"保单确认时间[：:\s]*(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2})",
        r"保单生成时间[：:\s]*(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2})",
    ])
    data["签单时间"] = _sign_date_fallback(pdf_path, sign)
    # CID字体乱码兜底：标签无法匹配时，取文档末尾最后一个日期
    if not data.get("签单时间"):
        _all_dates = re.findall(r"(\d{4})[年\-/.](\d{1,2})[月\-/.](\d{1,2})", text)
        if _all_dates:
            _y, _mo, _d = _all_dates[-1]
            data["签单时间"] = f"{_y}-{int(_mo):02d}-{int(_d):02d}"

    # --- 2. 保险公司名称 ---
    data["保险公司名称"] = safe_extract(text, [
        r"公司名称[：:]((?:(?!公司地址|邮政编码|服务电话|签单日期|保单号).)*)",
        r"公司名称[：:]\s*(?:(?!\s*公司地址)(?!\s*邮政编码)(?!\s*服务电话).)*",
        r"公司名称[：:]\s+([^\n]{2,30})(?=公司地址|营业执照|注册地址|联系电话|地址|$)",
        r"公司名称[：:]\s+([^\n]{2,40})",
        r"公司名称\s+(.{2,40})",
        r"(浙商财产保险股份有限公司[^\n]{0,20})",
    ])
    if company and company != "unknown":
        data["保险公司名称"] = company

    # --- 3. 保单号 ---
    _policy_no = safe_extract(text, [
        r"保险单号[：:\s]*([0-9]{10,})",
    ])
    if not _policy_no:
        _policy_no = safe_extract_policy_no(text, "保险单号")
    if not _policy_no:
        _m_pdda = re.search(r"(PDDA\d{15,})", text)
        if _m_pdda:
            _policy_no = _m_pdda.group(1)
    data["保单号"] = _filter_policy_no(_policy_no)

    # --- 4. 车辆使用性质 ---
    data["车辆使用性质"] = safe_extract(text, [
        rf"使用性质({NATURE_PATTERN})",
        rf"使用性质[：:\s]+({NATURE_PATTERN})",
        rf"机动车使用性质[：:\s]+({NATURE_PATTERN})",
    ])

    # --- 5. 车架号（VIN） ---
    data["车架号"] = extract_vin_strict(text, [
        r"识别代码[/／]车架号\s*\n\s*([A-Z0-9]{17})",
        r"识别代码[（(]?车架号[)）]?[：:\s]*([A-Z0-9]{17})",
        r"VIN码[/／]车架号[：:\s]*([A-Z0-9]{17})",
        r"VIN[码号/]*车架号[：:\s]*([A-Z0-9]{17})",
        (r"VIN码/车架号.*?([A-Z0-9]{17})", re.DOTALL),
        r"车架号[：:\s]+([A-Z0-9]{17})",
        r"\n([A-Z0-9]{17})\n",
    ])

    # --- 6. 车辆型号名称 ---
    data["车辆型号名称"] = safe_extract(text, [
        r"厂\s*牌\s*型\s*号[ \t]+([^\n；，,、号牌号码]{3,50})",
        r"厂牌型号\s+([^\n；，,、号牌号码]{3,50})",
        r"厂牌型号[：:\s]*([^\n；，,、号牌号码]{3,50})",
        r"厂\s*牌\s*型\s*号\s*\n\s*([^\n；，,、号牌号码]{3,40})",
    ])
    vm = data.get("车辆型号名称", "")
    if any(bad in vm for bad in ["符合", "准驾", "驾驶证", "行驶证"]):
        data["车辆型号名称"] = ""

    # --- 7. 被保人姓名 ---
    data["被保人姓名"] = safe_extract(text, [
        r"投保人名称[：:\s]*([^\s\n]{2,30})",
        r"被\s*保\s*险\s*人\s+([^\s\n]{2,10})",
        r"被保险人[：:\s]*([^\s\n]{2,10})",
        r"投保人[：:\s]*([^\s\n]{2,10})",
    ])

    # --- 8. 被保险人证件号 ---
    data["被保险人证件号"] = safe_extract(text, [
        r"身份证号码[（(（统一社会信用代码）)\s：:]*([A-Z0-9\*]{10,30})",
        r"证件号码[：:\s]*([A-Z0-9\*]{10,30})",
        r"证件号[：:\s]*([A-Z0-9\*]{10,30})",
        r"统一社会信用代码[：:\s]*([A-Z0-9\*]{10,30})",
    ])

    # --- 9. 被保险人手机号 ---
    _ph = safe_extract_phone(text)
    data["被保险人手机号"] = "" if is_blacklisted_phone(_ph) else _ph

    # --- 10. 车牌号码 ---
    data["车牌号码"] = safe_extract(text, [
        rf"号牌号码\s*\n\s*({PLATE_PATTERN})",
        rf"号牌号码[：:\s]*({PLATE_PATTERN})",
        rf"车牌号码[：:\s]*({PLATE_PATTERN})",
        rf"车牌[：:\s]*({PLATE_PATTERN})",
        rf"\b([{PROVINCES}][A-Z0-9]{{5,8}})\b",
    ])

    return data

# =============================================================================
# 交强险解析
# =============================================================================
def parse_jiaoqiang(text, company="unknown", pdf_path=None, table_data=None):
    data = _extract_common_fields(text, company, pdf_path)
    lines = get_lines(text)
    if table_data is None:
        table_data = safe_extract_tables(pdf_path) if pdf_path else {}

    # 4. 保险起期（支持：保险期间自 日期 起至 日期 止 / 保险期间自 日期 / 保险期间起至 日期 / 起保日期）
    # 格式：保险期间自 2026年4月19日0时0分 起至 2027年4月19日0时0分 止
    # 注：PDF plumber 编码问题可能导致数字间有空格（如 "20 2 6" 或 "0 时0 分"），放宽 \d 匹配
    # 人保交强险格式：保险期间自 20 2 6年04月28日0时0分起至2027年04月27日24时0分止（年份数字间有空格）
    # 人保商业险格式：保险期间 自2026年05月01日0时0分起至2027年04月30日24时0分止
    # 人保非车险格式：保险期间： 自2026年04月26日0时起，至2027年04月25日24时止
    _RENBAO_YEAR = r"\d[\s]*\d[\s]*\d[\s]*\d"  # 匹配 "2026" 或 "20 2 6"
    _RENBAO_DATETIME = rf"({_RENBAO_YEAR}年\d{{1,2}}月\d{{1,2}}日\d{{1,2}}时\d{{1,2}}分)"
    _RENBAO_TIME_NO_MIN = rf"({_RENBAO_YEAR}年\d{{1,2}}月\d{{1,2}}日\d{{1,2}}时)"
    data["保险起期"] = safe_extract(text, [
        # 人保专用：年份数字间可能含空格，自后面可能无空格
        rf"保险期间\s*自\s*{_RENBAO_DATETIME}\s*起至\s*{_RENBAO_DATETIME}\s*止",
        # 人保非车险：自2026年04月26日0时起，至2027年04月25日24时止（无"分"）
        rf"保险期间[：:\s]+\s*自\s*{_RENBAO_TIME_NO_MIN}[分]*[，,]*至\s*{_RENBAO_TIME_NO_MIN}[分]*止",
        r"三 保险期间起\s+(\d{4}年\d{2}月\d{2}日\d{2}:\d{2})\s+止至\s+(\d{4}年\d{2}月\d{2}日\d{2}:\d{2})\s+止",
        r"保险期间自\s+(\d{4}年\d{2}月\d{2}日\d{2}:\d{2}\s+起至\s+\d{4}年\d{2}月\d{2}日\d{2}:\d{2}\s*止)",
        r"保险期间自\s+(\d{4}年\d{2}月\d{2}日\d{2}:\d{2})\s+起至\s+(\d{4}年\d{2}月\d{2}日\d{2}:\d{2})",
        r"保险期间起:\s*(\d{4}年\d{2}月\d{2}日\d{2}:\d{2})\s+至\s+(\d{4}年\d{2}月\d{2}日\d{2}:\d{2})\s+止",
        r"保险期间\s*自\s+(\d{4}\s*年\s*\d{1,2}\s*月\s*\d{1,2}\s*日\s*\d{1,2}\s*时\s*\d{1,2}\s*分)\s+起至\s+(\d{4}\s*年\s*\d{1,2}\s*月\s*\d{1,2}\s*日\s*\d{1,2}\s*时\s*\d{1,2}\s*分)",
        r"保险期间\s*自\s+(\d{4}\s*年\s*\d{1,2}\s*月\s*\d{1,2}\s*日\s*\d{1,2}\s*时\s*\d{1,2}\s*分)\s+起至",
        r"保险期间\s*自\s*(\d{4}年\d{1,2}月\d{1,2}日\d{2}:\d{2}时起至)",
        r"保险期间[：:\s]+\d{4}\s*年\s*\d{1,2}\s*月\s*\d{1,2}\s*日\s*\d{2}:\d{2}\s*时起至",
        r"保险期间\s+起至\s*(\d{4}\s*年\s*\d{2}\s*月\s*\d{2}\s*日\s*\d{2}\s*时\s*\d{2}\s*分)\s+至\s+(\d{4}\s*年\s*\d{2}\s*月\s*\d{2}\s*日\s*\d{2}\s*时\s*\d{2}\s*分)",
        r"保险期间\s+起至\s*(\d{4}\s*年\s*\d{2}\s*月\s*\d{2}\s*日\s*\d{2}\s*时\s*\d{2}\s*分)",
        r"保险期间\s+自\s*(\d{4}\s*年\s*\d{2}\s*月\s*\d{2}\s*日\s*\d{2}\s*时\s*\d{2}\s*分)\s*起",
        r"保险期间\s*自\s+(\d{4}\s*年\s*\d{1,2}\s*月\s*\d{1,2}\s*日?\s*\d{1,2}\s*时?\s*\d{1,2}\s*分?)\s*起",
        r"保险期间[：:\s]*由\s+(\d{4}\s*年\s*\d{2}\s*月\s*\d{2}\s*日)\s+至",
        r"起保日期[：:\s]*(\d{4}-\d{2}-\d{2})",
    ])
    # 人保专用合并：safe_extract只返回group(1)，需要用完整pattern重新匹配来合并起止期
    _RENBAO_FULL = rf"保险期间\s*自\s*({_RENBAO_YEAR}年\d{{1,2}}月\d{{1,2}}日\d{{1,2}}时\d{{1,2}}分)\s*起至\s*({_RENBAO_YEAR}年\d{{1,2}}月\d{{1,2}}日\d{{1,2}}时\d{{1,2}}分)\s*止"
    _m_renbaov = re.search(_RENBAO_FULL, text)
    if _m_renbaov:
        start_v = re.sub(r'\s+', '', _m_renbaov.group(1))
        end_v = re.sub(r'\s+', '', _m_renbaov.group(2))
        data["保险起期"] = start_v + " 至 " + end_v
    # 人保非车险合并（无"分"的格式）
    if not data.get("保险起期"):
        _RENBAO_FULL_NO_MIN = rf"保险期间[：:\s]+\s*自\s*({_RENBAO_YEAR}年\d{{1,2}}月\d{{1,2}}日\d{{1,2}}时)\s*[分]*[，,]*至\s*({_RENBAO_YEAR}年\d{{1,2}}月\d{{1,2}}日\d{{1,2}}时)\s*[分]*止"
        _m_renbaovn = re.search(_RENBAO_FULL_NO_MIN, text)
        if _m_renbaovn:
            start_vn = re.sub(r'\s+', '', _m_renbaovn.group(1))
            end_vn = re.sub(r'\s+', '', _m_renbaovn.group(2))
            data["保险起期"] = start_vn + " 至 " + end_vn
    # 太平洋非车险格式："保险期间：2026 年 5 月 18 日 00:00 时起至 2027 年 5 月 17 日 24:00 时止"
    # safe_extract 可能只匹配到"起至"，没有结束日期；检测部分匹配，补全结束日期
    _existing = data.get("保险起期", "")
    if _existing and "起至" in _existing and "至" not in _existing:
        _m_s2 = re.search(r"保险期间[：:\s]+\d{4}\s*年\s*\d{1,2}\s*月\s*\d{1,2}\s*日\s*\d{2}:\d{2}\s*时起至", text)
        if _m_s2:
            rem2 = text[_m_s2.end():]
            _m_e2 = re.search(r"(\d{4}\s*年\s*\d{1,2}\s*月\s*\d{1,2}\s*日\s*\d{2}:\d{2}\s*时止)", rem2)
            if _m_e2:
                data["保险起期"] = _m_s2.group(0) + " 至 " + _m_e2.group(1)
    elif not _existing:
        _m_s2 = re.search(r"保险期间[：:\s]+\d{4}\s*年\s*\d{1,2}\s*月\s*\d{1,2}\s*日\s*\d{2}:\d{2}\s*时起至", text)
        if _m_s2:
            rem2 = text[_m_s2.end():]
            _m_e2 = re.search(r"(\d{4}\s*年\s*\d{1,2}\s*月\s*\d{1,2}\s*日\s*\d{2}:\d{2}\s*时止)", rem2)
            if _m_e2:
                data["保险起期"] = _m_s2.group(0) + " 至 " + _m_e2.group(1)
    # 若匹配到起止两段时间，合并输出（开始 至 结束）
    _m2 = re.search(rf"保险期间\s*自\s+({_RENBAO_YEAR}\s*年\s*\d{{1,2}}\s*月\s*\d{{1,2}}\s*日\s*\d{{1,2}}\s*时\s*\d{{1,2}}\s*分)\s+起至\s+({_RENBAO_YEAR}\s*年\s*\d{{1,2}}\s*月\s*\d{{1,2}}\s*日\s*\d{{1,2}}\s*时\s*\d{{1,2}}\s*分)", text)
    if _m2:
        data["保险起期"] = re.sub(r'\s+', '', _m2.group(1)) + " 至 " + re.sub(r'\s+', '', _m2.group(2))
    elif data.get("保险起期") and re.search(r"^\d{4}", data["保险起期"]):
        if table_data.get("period") and table_data["period"] != data["保险起期"]:
            data["保险起期"] = table_data["period"]
        pass
    elif not data.get("保险起期"):
        _m3 = re.search(r"保险期间起\s+(\d{4}年\d{2}月\d{2}日\d{2}:\d{2})\s+\u81f3\s+(\d{4}年\d{2}月\d{2}日\d{2}:\d{2})", text)
        if _m3:
            data["保险起期"] = _m3.group(1) + " 至 " + _m3.group(2)
        else:
            _m3b = re.search(r"保\s*险\s*期\s*间\s*起\s+(\d{4}年\d{2}月\d{2}日\d{2}:\d{2})\s+起至\s+(\d{4}年\d{2}月\d{2}日\d{2}:\d{2})", text)
            if _m3b:
                data["保险起期"] = _m3b.group(1) + " 至 " + _m3b.group(2)
        if not data.get("保险起期"):
            _m4 = re.search(r"保险期间起:\s*(\d{4}年\d{2}月\d{2}日\d{2}:\d{2})\s+至\s+(\d{4}年\d{2}月\d{2}日\d{2}:\d{2})\s+止", text)
            if _m4:
                data["保险起期"] = _m4.group(1) + " 至 " + _m4.group(2)
    if not data.get("保险起期"):
        _m_pa = re.search(r"保险期间\s*自\s+(\d{4}[\s\xa0]*年[\s\xa0]*\d{1,2}[\s\xa0]*月[\s\xa0]*\d{1,2}[\s\xa0]*日[\s\xa0]*\d{2}:\d{2}[\s\xa0]*时)起至", text)
        if _m_pa:
            rem_pa = text[_m_pa.end():]
            _m_pa2 = re.search(r"(\d{4}[\s\xa0]*年[\s\xa0]*\d{1,2}[\s\xa0]*月[\s\xa0]*\d{1,2}[\s\xa0]*日[\s\xa0]*\d{2}:\d{2}[\s\xa0]*时止)", rem_pa)
            if _m_pa2:
                data["保险起期"] = _m_pa.group(1) + " 至 " + _m_pa2.group(1)
    if not data.get("保险起期"):
        _m_yg = re.search(r"保险期间\s+(\d{4}年\d{1,2}月\d{1,2}日\s+\d{2}:\d{2}:\d{2})\s+至\s+(\d{4}年\d{1,2}月\d{1,2}日\s+\d{2}:\d{2}:\d{2})", text)
        if _m_yg:
            data["保险起期"] = _m_yg.group(1) + " 至 " + _m_yg.group(2)

    # 浙商表格兜底：保险起期
    if not data.get("保险起期") and table_data.get("period"):
        data["保险起期"] = table_data["period"]
    elif data.get("保险起期") and table_data.get("period") == data.get("保险起期"):
        m_cur = re.search(r'(\d{4})年(\d+)月', data["保险起期"])
        if m_cur and int(m_cur.group(2)) == 4:
            pymupdf_hints = ""
            if pdf_path:
                try:
                    with pymupdf.open(pdf_path) as doc:
                        for p in doc:
                            t = p.get_text()
                            if t:
                                pymupdf_hints += t
                except Exception:
                    pass
            pass

    # 12. 险种名称原始（交强险专用）
    data["险种名称原始"] = safe_extract(text, [
        r"(机动车交通事故责任强制保险(?:单|))",
    ])

    # 13. 实收保费
    data["实收保费"] = safe_extract(text, [
        r"保险费合计[^\d]*RMB\s*([0-9,]+\.?\d{2})",
        r"保险费合计（人民币大写）：[^¥]*¥[：:\s]*([0-9,]+\.?\d*)",
        r"保险费\s+大写：人民币[^小]*小写：CNY\s+([0-9,]+\.?\d*)",
        r"保险费合计[\s\S]*?[￥¥][：:\s\xa0]*([0-9,]+\.?\d*)",
        r"（￥：\s*([0-9,]+\.?\d*)元）",
        r"实收保费[：:\s]*[￥¥]?\s*([0-9,]+\.?\d*)",
        r"保险费合计[（(][^)]*)[）)]\s*[￥¥]?\s*([0-9,]+\.?\d*)",
        r"保险费合计（人民币大写）[\s\S]*?[￥¥][：:\s]*([0-9,]+\.?\d*)",
        r"保险费合计（大写）[\s\S]*?[￥¥][：:\s]*([0-9,]+\.?\d*)",
        r"保险费合计[\s\S]*?[￥¥][：:\s]*([0-9,]+\.?\d*)",
        r"保险费[\s\S]*?[￥¥][：:\s]*([0-9,]+\.?\d*)",
        r"保险费金额[\s\S]*?[￥¥][：:\s]*([0-9,]+\.?\d*)",
        r"(\d+\.00)\n[^\n]*\n玖佰伍拾元整",
        r"合计.*?[￥¥]\s*([0-9,]+\.?\d*)",
        r"含税总保险费[^0-9]*([0-9,]+\.?\d*)",
        r"总保险费[^\d]*([0-9,]+\.?\d*)",
        r"(\d+\.00)\n[^\n]*\n\u7396\u4f70\u4f0d\u62fe\u5143\u6574",
    ])

    # 14. 车船税
    data["车船税"] = safe_extract(text, [
        r"当年应缴[\s\n]*[￥¥][：:]\s*\n?([0-9,]+\.\d{2})",
        r"当年应缴[\s\S]{1,30}?([0-9,]+\.\d{2})",
        r"车船税[\s\S]{1,30}?([0-9,]+\.\d{2})",
        r"当年应缴\s*[\u00a5\uffe5\uff1a:]*\s*([0-9,]+\.?\d*)",
        r"车船税\s*[\u00a5\uffe5\uff1a:]*\s*([0-9,]+\.?\d*)",
    ])

    return data

# =============================================================================
# 商业险解析
# =============================================================================
def parse_shangye(text, company="unknown", pdf_path=None, table_data=None):
    data = _extract_common_fields(text, company, pdf_path)
    lines = get_lines(text)
    if table_data is None:
        table_data = safe_extract_tables(pdf_path) if pdf_path else {}

    # 4. 保险起期（商业险专用格式）
    _RENBAO_YEAR = r"\d[\s]*\d[\s]*\d[\s]*\d"
    _RENBAO_DATETIME = rf"({_RENBAO_YEAR}年\d{{1,2}}月\d{{1,2}}日\d{{1,2}}时\d{{1,2}}分)"
    _RENBAO_TIME_NO_MIN = rf"({_RENBAO_YEAR}年\d{{1,2}}月\d{{1,2}}日\d{{1,2}}时)"
    data["保险起期"] = safe_extract(text, [
        r"保险期间[：:\s]*(\d{4})\s*年\s*(\d{1,2})\s*月\s*(\d{1,2})\s*日\s*(\d{2}:\d{2})\s*时起至\s*(\d{4})\s*年\s*(\d{1,2})\s*月\s*(\d{1,2})\s*日\s*(\d{2}:\d{2})\s*时止",
        r"保险期间\s*自(\d{4}年\d{1,2}月\d{1,2}日\d{1,2}时\d{1,2}分)\s*起至\s*(\d{4}年\d{1,2}月\d{1,2}日\d{1,2}时\d{1,2}分)\s*止",
        r'保险期间[：:]\s*自\s+(\d{4}年\d{2}月\d{2}日\d{2}:\d{2})\s+起至\s+(\d{4}年\d{2}月\d{2}日\d{2}:\d{2})\s+止',
        r'保险期间[：:]\s*(\d{4}年\d{2}月\d{2}日[^\s]*)\s+起至\s*(.+?)\s+止',
        r"From[^\d]*(\d{4}年\d{2}月\d{2}日\d{2}时起至)",
        r"保险期间\s*自\s+(\d{4}\s*年\s*\d{1,2}\s*月\s*\d{1,2}\s*日\s*\d{1,2}\s*时\s*\d{1,2}\s*分起至)",
        r"保险期间\s*自\s+(\d{4}\s*年\s*\d{1,2}\s*月\s*\d{1,2}\s*日\s*\d{1,2}\s*时\s*\d{1,2}\s*分)\s+起至",
        r"保险期间\s*自\s+(\d{4}\s*年\s*\d{1,2}\s*月\s*\d{1,2}\s*日?\s*\d{1,2}\s*时?\s*\d{1,2}\s*分?)\s*起",
        r"保险期间\s+起至\s*(\d{4}\s*年\s*\d{2}\s*月\s*\d{2}\s*日\s*\d{2}\s*时\s*\d{2}\s*分)\s+至\s+(\d{4}\s*年\s*\d{2}\s*月\s*\d{2}\s*日\s*\d{2}\s*时\s*\d{2}\s*分)",
        r"保险期间\s+起至\s*(\d{4}\s*年\s*\d{2}\s*月\s*\d{2}\s*日\s*\d{2}\s*时\s*\d{2}\s*分)",
        r"保险期间\s+自\s*(\d{4}\s*年\s*\d{2}\s*月\s*\d{2}\s*日\s*\d{2}\s*时\s*\d{2}\s*分)\s*起",
        r"保险期间[：:\s]*由\s+(\d{4}\s*年\s*\d{2}\s*月\s*\d{2}\s*日)\s+至",
        r"起保日期[：:\s]*(\d{4}-\d{2}-\d{2})",
        r"保险起期[：:\s]*(\d{4}-\d{2}-\d{2})",
    ])
    _m_tp_sy = re.search(r"保险期间[：:\s]*(\d{4})\s*年\s*(\d{1,2})\s*月\s*(\d{1,2})\s*日\s*(\d{2}:\d{2})\s*时起至\s*(\d{4})\s*年\s*(\d{1,2})\s*月\s*(\d{1,2})\s*日\s*(\d{2}:\d{2})\s*时止", text)
    if _m_tp_sy:
        start_date = f"{_m_tp_sy.group(1)}年{int(_m_tp_sy.group(2)):02d}月{int(_m_tp_sy.group(3)):02d}日{_m_tp_sy.group(4)}"
        end_date = f"{_m_tp_sy.group(5)}年{int(_m_tp_sy.group(6)):02d}月{int(_m_tp_sy.group(7)):02d}日{_m_tp_sy.group(8)}"
        data["保险起期"] = start_date + " 至 " + end_date
    _m_rb_sy = re.search(r"保险期间\s*自(\d{4}年\d{1,2}月\d{1,2}日\d{1,2}时\d{1,2}分)\s*起至\s*(\d{4}年\d{1,2}月\d{1,2}日\d{1,2}时\d{1,2}分)\s*止", text)
    if _m_rb_sy:
        data["保险起期"] = _m_rb_sy.group(1) + " 至 " + _m_rb_sy.group(2)
    if not data.get("保险起期"):
        _m_rb_pebs = re.search(r"保险期间[：:\s\n]+\s*自(\d{4}年\d{1,2}月\d{1,2}日\d{1,2}时\d{1,2}分\d{1,2}秒?)\s*起[至，,]*\s*(\d{4}年\d{1,2}月\d{1,2}日\d{1,2}时\d{1,2}分\d{1,2}秒?)\s*[。\.]*止", text)
        if _m_rb_pebs:
            data["保险起期"] = _m_rb_pebs.group(1) + " 至 " + _m_rb_pebs.group(2)
        elif not data.get("保险起期"):
            _m_rb_pebs2 = re.search(r"保险期间[：:\s\n]+\s*自(\d{4}年\d{1,2}月\d{1,2}日\d{1,2}时)\s*[分]*起[，,]*至\s*(\d{4}年\d{1,2}月\d{1,2}日\d{1,2}时)\s*[分]*止", text)
            if _m_rb_pebs2:
                data["保险起期"] = _m_rb_pebs2.group(1) + " 至 " + _m_rb_pebs2.group(2)
    _m_from = re.search(r"From[^\d]*(\d{4}年\d{2}月\d{2}日\d{2}时起至)", text)
    if _m_from:
        start_date = _m_from.group(1)
        remaining = text[_m_from.end():]
        _m_end = re.search(r"(\d{4}年\d{2}月\d{2}日\d{2}时止)", remaining)
        if _m_end:
            end_date = _m_end.group(1)
            data["保险起期"] = start_date + " 至 " + end_date
    elif data.get("保险起期") and re.search(r"^\d{4}", data["保险起期"]):
        pass
    _m_sc2 = re.search(r'保险期间[：:]\s*自\s+(\d{4}年\d{2}月\d{2}日\d{2}:\d{2})\s+起至\s+(\d{4}年\d{2}月\d{2}日\d{2}:\d{2})\s+止', text)
    if _m_sc2:
        data["保险起期"] = _m_sc2.group(1) + " 至 " + _m_sc2.group(2)
    if not data.get("保险起期"):
        _m_pa_sy = re.search(r"保险期间\s*自\s+(\d{4}年\d{1,2}月\d{1,2}日\d{2}:\d{2}时)起至", text)
        if _m_pa_sy:
            rem_pa = text[_m_pa_sy.end():]
            _m_pa2 = re.search(r"(\d{4}年\d{1,2}月\d{1,2}日\s*\d{2}:\d{2}时止)", rem_pa)
            if _m_pa2:
                data["保险起期"] = _m_pa_sy.group(1) + " 至 " + _m_pa2.group(1)
    if not data.get("保险起期"):
        _m_yg_sy = re.search(r"保险期间[：:]\s*(\d{4}年\d{1,2}月\d{1,2}日\s+\d{2}:\d{2}:\d{2})\s+至\s+(\d{4}年\d{1,2}月\d{1,2}日\s+\d{2}:\d{2}:\d{2})", text)
        if _m_yg_sy:
            data["保险起期"] = _m_yg_sy.group(1) + " 至 " + _m_yg_sy.group(2)

    # 7b. 车辆使用性质（太平洋商业险格式覆盖）
    data["车辆使用性质"] = safe_extract(text, [
        r"使用性质[：:\s]*([^\s\n]{2,20})",
        r"使用性质[：:\s]*([^\n]{2,20})",
    ])

    # 12. 险种名称原始
    data["险种名称原始"] = safe_extract(text, [
        r"(\"如意行\".{0,40})",
        r"(畅行保.{0,40})",
        r"(驾乘.{0,40})",
        r"(机动车综合商业保险.{0,20})",
        r"(机动车商业保险[^\n]{0,30})",
        r"(商业保险保险单.{0,30})",
    ])

    # 13. 实收保费
    data["实收保费"] = safe_extract(text, [
        r"保险费合计[^\d]*RMB\s*([0-9,]+\.?\d{2})",
        r"保险费合计（人民币大写）：[^¥]*¥[：:\s]*([0-9,]+\.?\d*)",
        r"保险费\s+大写：人民币[^小]*小写：CNY\s+([0-9,]+\.?\d*)",
        r"保险费合计[\s\S]*?[￥¥][：:\s]*([0-9,]+\.?\d*)",
        r"实收保费[：:\s]*[￥¥]?\s*([0-9,]+\.?\d*)",
        r"保险费合计[（(][^)]*[）)]\s*[￥¥]?\s*([0-9,]+\.?\d*)",
        r"保险费合计（人民币大写）[\s\S]*?[￥¥][：:\s]*([0-9,]+\.?\d*)",
        r"保险费合计（大写）[\s\S]*?[￥¥][：:\s]*([0-9,]+\.?\d*)",
        r"保险费合计[\s\S]*?[￥¥][：:\s]*([0-9,]+\.?\d*)",
        r"保险费[\s\S]*?[￥¥][：:\s]*([0-9,]+\.?\d*)",
        r"保险费金额[\s\S]*?[￥¥][：:\s]*([0-9,]+\.?\d*)",
        r"含税总保险费[^0-9]*([0-9,]+\.?\d*)",
        r"总保险费[^\d]*([0-9,]+\.?\d*)",
    ])

    # 14. 车船税
    data["车船税"] = safe_extract(text, [
        r"当年应缴\s*[￥\uff1a:]*\s*([0-9,]+\.?\d*)",
        r"车船税\s*[￥\uff1a:]*\s*([0-9,]+\.?\d*)",
    ])

    if company and company != "unknown":
        data["保险公司名称"] = company
    return clean_data(data, text)

# =============================================================================
# 太平洋畅行保解析（非车险类，pymupdf文本正常）
# =============================================================================
def parse_taiping_changxing(text, pdf_path=None):
    """
    太平洋畅行保（山东专属）非车险解析器。
    特征：pymupdf 文本正常可读，险种名称 = 畅行保（山东专属）二代-基础版，
    保单结构含险种名称/保障内容/保险金额 三列格式。
    """
    data = {}

    # 1. 险种名称原始（产品名）
    data["险种名称原始"] = safe_extract(text, [
        r"(畅行保[^\n]{0,40})",
        r"(畅行保[^\n]*)",
    ]) or "畅行保（山东专属）二代-基础版"

    # 2. 签单时间
    sign = safe_extract(text, [
        r"签单日期\s*\n?\s*(\d{4}-\d{2}-\d{2})",
        r"签单日期[：:\s]*(\d{4}-\d{2}-\d{2})",
        r"签单日期[：:\s]*(\d{4}年\d{2}月\d{2}日)",
    ])
    data["签单时间"] = _sign_date_fallback(pdf_path, sign)

    # 3. 保险公司名称
    data["保险公司名称"] = "中国太平洋财产保险股份有限公司"

    # 4. 保单号
    policy = safe_extract(text, [
        r"保险单号[：:\s]*([A-Z0-9]{10,20})",
        r"(DZBV\d{14,})",
    ])
    data["保单号"] = _filter_policy_no(policy)

    # 5. 保险起期 - 太平洋畅行保格式：自（From）2026年05月18日00时起至（To）2027年05月18日00时止
    #    或非车险格式：由 2026年05月01日 至 2027年04月30日 (首尾两日包括在内)
    period = safe_extract(text, [
        r"自[（(]From[）)]\s*(\d{4}年\d{2}月\d{2}日\d{2}时)\s*起至[（(]To[）)]\s*(\d{4}年\d{2}月\d{2}日\d{2}时)\s*止",
    ])
    if period:
        # period is already the full matched string, extract start/end
        m = re.search(r"自[（(]From[）)]\s*(\d{4}年\d{2}月\d{2}日\d{2}时)\s*起至[（(]To[）)]\s*(\d{4}年\d{2}月\d{2}日\d{2}时)\s*止", text)
        if m:
            data["保险起期"] = m.group(1) + " 起至 " + m.group(2)
        else:
            data["保险起期"] = period
    else:
        # 兜底：由 2026年05月01日 至 2027年04月30日 (首尾两日包括在内)
        m_youzhi = re.search(r"由\s*(\d{4}年\d{1,2}月\d{1,2}日)\s*至\s*(\d{4}年\d{1,2}月\d{1,2}日)", text)
        if m_youzhi:
            data["保险起期"] = m_youzhi.group(1) + " 至 " + m_youzhi.group(2)
        else:
            data["保险起期"] = ""

    # 6. 车辆使用性质
    data["车辆使用性质"] = safe_extract(text, [
        r"车辆使用性质[：:\s]*([^\n]{2,20})",
    ])

    # 7. 车架号
    data["车架号"] = extract_vin_strict(text, [
        r"车架号[：:\s]*([A-HJ-NP-Z0-9]{17})(?![A-HJ-NP-Z0-9])",
    ])

    # 8. 车辆型号
    data["车辆型号名称"] = safe_extract(text, [
        r"厂牌型号[：:\s]*([^\n]{2,50})",
    ])

    # 9. 被保险人姓名（投保人名称）
    data["被保险人姓名"] = safe_extract(text, [
        r"投保人名称[：:\s]*([^\n]{2,30})",
    ])

    # 10. 被保险人证件号
    data["被保险人证件号"] = safe_extract(text, [
        r"证件号码[：:\s]*([A-Z0-9]{10,30})",
    ])

    # 11. 被保险人手机号
    _ph = safe_extract_phone(text)
    data["被保险人手机号"] = "" if is_blacklisted_phone(_ph) else _ph

    # 12. 车牌号码
    data["车牌号码"] = safe_extract(text, [
        r"车牌号[：:\s]*([鲁京津沪渝冀豫云辽黑湘皖晋疆藏贵甘青桂琼苏浙蒙鄂][A-HJ-NP-Z0-9]{5,7})",
    ])

    # 13. 实收保费
    data["实收保费"] = safe_extract(text, [
        r"RMB[：:\s]*[￥¥]?\s*([0-9,]+\.?\d*)",
        r"保险费合计[^\d]*([0-9,]+\.?\d*)",
    ])

    # 14. 车船税（非车险通常为空）
    data["车船税"] = ""

    return data

# =============================================================================
# 意外险/驾意险解析
# =============================================================================
def parse_changxing(text, pdf_path=None, table_data=None):
    data = _extract_common_fields(text, pdf_path=pdf_path)
    if table_data is None:
        table_data = safe_extract_tables(pdf_path) if pdf_path else {}

    # 4. 保险起期（非车险专用格式）
    data["保险起期"] = safe_extract(text, [
        r"保险期间[：:\s\n]+\s*自(\d{4}年\d{1,2}月\d{1,2}日\d{1,2}时)\s*[分]*起[，,]*至\s*(\d{4}年\d{1,2}月\d{1,2}日\d{1,2}时)\s*[分]*止",
        r'保险期间：365天，从?(\d{4}年\d{2}月\d{2}日)零时起至(\d{4}年\d{2}月\d{2}日)二十四时止',
        r'保险期间[：:]\s*自\s+(\d{4}年\d{2}月\d{2}日\d{2}:\d{2})\s*至\s+(\d{4}年\d{2}月\d{2}日\d{2}:\d{2})\s+止',
        r"From[^\d]*(\d{4}年\d{2}月\d{2}日\d{2}时起至)",
        r"保险期间[：:\s]*\d{4}[\s\xa0]*年[\s\xa0]*\d{1,2}[\s\xa0]*月[\s\xa0]*\d{1,2}[\s\xa0]*日[\s\xa0]*\d{2}:\d{2}[\s\xa0]*时起至",
        r"保险期间\s*自\s+(\d{4}\s*年\s*\d{1,2}\s*月\s*\d{1,2}\s*日\s*\d{1,2}\s*时\s*\d{1,2}\s*分起至)",
        r"保险期间\s*自\s+(\d{4}\s*年\s*\d{1,2}\s*月\s*\d{1,2}\s*日\s*\d{1,2}\s*时\s*\d{1,2}\s*分)\s+起至",
        r"保险期间\s+(\d{4}年\d{2}月\d{2}日(?:\s+\d{2}时\d{2}分\d{2}秒)?)\s*至",
        r"(\d{4}年\d{2}月\d{2}日(?:\s+\d{2}时\d{2}分\d{2}秒)?)\s+起至",
        r"保险期间[：:\s]*(\d{4}年\d{2}月\d{2}日)",
        r"起保日期[：:\s]*(\d{4}-\d{2}-\d{2})",
        r"保险起期[：:\s]*(\d{4}-\d{2}-\d{2})",
    ])
    _m_rb_fc = re.search(r"保险期间[：:\s\n]+\s*自(\d{4}年\d{1,2}月\d{1,2}日\d{1,2}时)\s*[分]*起[，,]*至\s*(\d{4}年\d{1,2}月\d{1,2}日\d{1,2}时)\s*[分]*止", text)
    if _m_rb_fc:
        data["保险起期"] = _m_rb_fc.group(1) + " 至 " + _m_rb_fc.group(2)
    _m_sc = re.search(r'保险期间：365天，从?(\d{4}年\d{2}月\d{2}日)零时起至(\d{4}年\d{2}月\d{2}日)二十四时止', text)
    if _m_sc:
        data["保险起期"] = _m_sc.group(1) + " 至 " + _m_sc.group(2)
    _m_sc2 = re.search(r'保险期间[：:]\s*自\s+(\d{4}年\d{2}月\d{2}日\d{2}:\d{2})\s*至\s+(\d{4}年\d{2}月\d{2}日\d{2}:\d{2})\s+止', text)
    if _m_sc2:
        data["保险起期"] = _m_sc2.group(1) + " 至 " + _m_sc2.group(2)
    elif _m_sc:
        data["保险起期"] = _m_sc.group(1) + " 至 " + _m_sc.group(2)
    _m_from = re.search(r"From[^\d]*(\d{4}年\d{2}月\d{2}日\d{2}时起至)", text)
    if _m_from:
        start_date = _m_from.group(1)
        remaining = text[_m_from.end():]
        _m_end = re.search(r"(\d{4}年\d{2}月\d{2}日\d{2}时止)", remaining)
        if _m_end:
            end_date = _m_end.group(1)
            data["保险起期"] = start_date + " 至 " + end_date
    _existing = data.get("保险起期", "")
    _ends_qz = _existing.endswith("起至") if _existing else False
    if _ends_qz:
        _m_s2 = re.search(r"保险期间[：:\s]+\d{4}[\s\xa0]*年[\s\xa0]*\d{1,2}[\s\xa0]*月[\s\xa0]*\d{1,2}[\s\xa0]*日[\s\xa0]*\d{2}:\d{2}[\s\xa0]*时起至", text)
        if _m_s2:
            rem2 = text[_m_s2.end():]
            _m_e2 = re.search(r"(\d{4}[\s\xa0]*年[\s\xa0]*\d{1,2}[\s\xa0]*月[\s\xa0]*\d{1,2}[\s\xa0]*日[\s\xa0]*\d{2}:\d{2}[\s\xa0]*时止)", rem2)
            if _m_e2:
                data["保险起期"] = _m_s2.group(0) + " 至 " + _m_e2.group(1)
    elif not _existing:
        _m_s2 = re.search(r"保险期间[：:\s]+\d{4}[\s\xa0]*年[\s\xa0]*\d{1,2}[\s\xa0]*月[\s\xa0]*\d{1,2}[\s\xa0]*日[\s\xa0]*\d{2}:\d{2}[\s\xa0]*时起至", text)
        if _m_s2:
            rem2 = text[_m_s2.end():]
            _m_e2 = re.search(r"(\d{4}[\s\xa0]*年[\s\xa0]*\d{1,2}[\s\xa0]*月[\s\xa0]*\d{1,2}[\s\xa0]*日[\s\xa0]*\d{2}:\d{2}[\s\xa0]*时止)", rem2)
            if _m_e2:
                data["保险起期"] = _m_s2.group(0) + " 至 " + _m_e2.group(1)
    if not data.get("保险起期"):
        _m_pa_xz = re.search(
            r"保险期限\s*\n?\s*(\d{4})年(\d{1,2})月(\d{1,2})日(\d{2}时\d{2}分\d{2}秒)\s+起\s*至\s*\n?\s*(\d{4})年(\d{1,2})月(\d{1,2})日(\d{2}时\d{2}分\d{2}秒)\s*止",
            text
        )
        if _m_pa_xz:
            start = f"{_m_pa_xz.group(1)}年{int(_m_pa_xz.group(2)):02d}月{int(_m_pa_xz.group(3)):02d}日{_m_pa_xz.group(4)}"
            end = f"{_m_pa_xz.group(5)}年{int(_m_pa_xz.group(6)):02d}月{int(_m_pa_xz.group(7)):02d}日{_m_pa_xz.group(8)}"
            data["保险起期"] = f"{start} 至 {end}"
    if not data.get("保险起期"):
        _m_youzhi = re.search(r"由\s*(\d{4}年\d{1,2}月\d{1,2}日)\s*至\s*(\d{4}年\d{1,2}月\d{1,2}日)", text)
        if _m_youzhi:
            data["保险起期"] = _m_youzhi.group(1) + " 至 " + _m_youzhi.group(2)

    # 被保人姓名（非车险有更严格的过滤逻辑）
    raw_name = safe_extract(text, [
        r"被保险人[：:\s]*([^\s\n]{2,10})",
        r"投保人[：:\s]*([^\s\n]{2,30})",
        r"姓名/名称\s*([^\s\n]{2,15})",
        r"姓名[：:\s]*([^\s\n]{2,10})",
        r"被保人[：:\s]*([^\s\n]{2,10})",
    ])
    _bad = ("元", "￥", "¥", "座", "每", "限", "免责", "条款",
            "驾驶证", "行驶证", "为18", "未成年人", "驾驶或乘坐")
    if raw_name and len(raw_name) >= 2 and not raw_name[0].isdigit() and not any(b in raw_name for b in _bad):
        data["被保人姓名"] = raw_name
    else:
        data["被保人姓名"] = ""

    # 被保险人证件号（非车险简化版）
    data["被保险人证件号"] = safe_extract(text, [
        r"证件号码[：:\s]*([A-Z0-9\*]{10,30})",
        r"证件号[：:\s]*([A-Z0-9\*]{10,30})",
    ])

    # 12. 险种名称原始
    data["险种名称原始"] = "非车险"

    # 13. 实收保费
    premium = safe_extract(text, [
        r"保险费合计（人民币大写）：[^¥]*¥[：:\s]*([0-9,]+\.?\d*)",
        r"保险费\s+大写：人民币[^小]*小写：CNY\s+([0-9,]+\.?\d*)",
        r"保险费合计[\s\S]*?[￥¥][：:\s]*([0-9,]+\.?\d*)",
        r"保险费合计[（(][^)]*?[￥][：:\s]*([0-9,]+\.?\d*)\s*元[）)]",
        r"（[￥][：:\s]*([0-9,]+\.?\d*)\s*元）",
        r"(\d+\.00)[^\n]*\n[^\n]*玖佰伍拾元整",
        r"实收保费[：:\s]*[￥¥]?\s*([0-9,]+\.?\d*)",
        r"总保险费[^\d]*([0-9,]+\.?\d*)",
        r"营业\s*(\d{3})元",
        r"保险费合计（人民币大写）[\s\S]*?[￥¥][：:\s]*([0-9,]+\.?\d*)",
        r"保险费合计（大写）[\s\S]*?[￥¥][：:\s]*([0-9,]+\.?\d*)",
        r"保险费合计[\s\S]*?[￥¥][：:\s]*([0-9,]+\.?\d*)",
        r"保险费[\s\S]*?[￥¥][：:\s]*([0-9,]+\.?\d*)",
        r"保险费金额[\s\S]*?[￥¥][：:\s]*([0-9,]+\.?\d*)",
        r"总保险费\s*[^\n]*?￥\s*([0-9,]+\.?\d*)",
    ])
    if not premium and pdf_path:
        premium = byte_level_premium(pdf_path)
    data["实收保费"] = premium

    # 14. 车船税
    data["车船税"] = ""

    # 浙商表格兜底：保费和车船税
    if table_data:
        if (not data.get("实收保费") or float((data.get("实收保费", "0") or "0").replace(',', '')) < 100) and table_data.get("premium"):
            data["实收保费"] = table_data["premium"]
        if not data.get("车船税") and table_data.get("tax"):
            data["车船税"] = table_data["tax"]

    return clean_data(data, text)

# =============================================================================
# 平安车主尊享保障乱码专用解析
# 问题：pymupdf 提取时中文全为乱码（如 "Ƶ��ƽ��" = "平安"），
#       导致依赖中文字段的正则全部失效。
# 策略：从乱码文本中直接提取 ASCII/数字可读内容，绕过中文匹配。
#       Page 2 是最好的数据源（policy no / plate / dates 都能正确提取）。
# =============================================================================
def parse_pingan_jiaoqiang(text, pdf_path=None):
    """专门处理平安交强险 PDF。
    
    平安交强险特征：
      - pymupdf/pdfplumber 中文全部乱码（CID字体）
      - 但数字、ASCII、部分标签清晰可读
      - 保费格式：RMB760.00元（不含税保费:716.98元，税额:43.02元）
      - 车船税格式：当年应缴\n( ��420.00\n元)
      - 保险单号：11131063903350800417（18位，1113开头）
    """
    data = {}

    # 1. 保险公司名称
    data["保险公司名称"] = "中国平安财产保险股份有限公司"

    # 2. 险种名称原始
    data["险种名称原始"] = "机动车交通事故责任强制保险单"

    # 3. 保单号（保险单号：11131063903350800417）
    policy_m = re.search(r"保险单号[：:\s]*([0-9]{14,20})", text)
    data["保单号"] = policy_m.group(1) if policy_m else ""

    # 4. 签单时间（签单日期：2026年04月21日 / 出单确认时间：2026年4月21日11:07时）
    sign_m = re.search(r"签单日期[：:\s]*(\d{4})年(\d{1,2})月(\d{1,2})日", text)
    if sign_m:
        data["签单时间"] = f"{sign_m.group(1)}-{int(sign_m.group(2)):02d}-{int(sign_m.group(3)):02d}"
    else:
        # 兜底：出单确认时间
        sign_m2 = re.search(r"出单确认时间[：:\s]*(\d{4})年(\d{1,2})月(\d{1,2})日", text)
        if sign_m2:
            data["签单时间"] = f"{sign_m2.group(1)}-{int(sign_m2.group(2)):02d}-{int(sign_m2.group(3)):02d}"
        else:
            data["签单时间"] = ""

    # 5. 保险起期（PDF中文全乱码，用数字+空白模式匹配）
    # 原始："保险期间起至 2026 年 5 月 9 日 11:00 时起至 2027 年 5 月 9 日 11:00 时止"
    # 乱码后："保险期间起至 2026 年 5 月 9 日 11:00 时起至 2027 年 5 月 9 日 11:00 时止"
    # 结构：\d{4} + 空格 + 乱码字符 + 空格 + \d + 空格 + 乱码字符 + 空格 + \d + ...
    period_m = re.search(
        r"(\d{4})\s+\S+\s+(\d{1,2})\s+\S+\s+(\d{1,2})\s+\S+\s+(\d{2}:\d{2})\s+\S+\s+(\d{4})\s+\S+\s+(\d{1,2})\s+\S+\s+(\d{1,2})\s+\S+\s+(\d{2}:\d{2})",
        text
    )
    if period_m:
        start = f"{period_m.group(1)}年{int(period_m.group(2)):02d}月{int(period_m.group(3)):02d}日{period_m.group(4)}"
        end = f"{period_m.group(5)}年{int(period_m.group(6)):02d}月{int(period_m.group(7)):02d}日{period_m.group(8)}"
        data["保险起期"] = f"{start} 至 {end}"
    else:
        data["保险起期"] = ""

    # 6. 车牌号码（从文件名提取，PDF中文全乱码）
    # 文件名格式：鲁F-216AC_平安交强险保单_于建刚(1).pdf
    fname_plate_m = re.search(r"([A-Z0-9鲁冀豫晋陕甘青新藏川渝辽吉苏浙皖闽赣鄂湘粤琼黑台港澳门北]{1,3}-[A-Z0-9]{4,5})_", os.path.basename(pdf_path or ""))
    data["车牌号码"] = fname_plate_m.group(1) if fname_plate_m else ""

    # 7. 车架号（17位字母+数字）
    # PDF乱码中VIN可能被拆散，从车辆型号区域提取
    chassis_list = re.findall(r"\b([A-Z0-9]{17})\b", text)
    chassis = ""
    for c in chassis_list:
        if c not in ("00000000000000000", "AAAAAAAAAAAAAAA"):
            chassis = c
            break
    # 兜底：从车辆型号名称中提取（SGM6468EBA1等）
    if not chassis:
        chassis_m = re.search(r"([A-Z0-9]{17})", text[:3000])
        if chassis_m:
            chassis = chassis_m.group(1)
    data["车架号"] = chassis

    # 8. 被保人姓名（先从pdfplumber文本提取，取不到再从文件名兜底）
    # 平安PDF中文是CID乱码，pymupdf文本读不到名字，但plumber文本可读
    _name_from_text = ""
    if pdf_path:
        try:
            with pdfplumber.open(pdf_path) as _pdf:
                _pl_text = ""
                for _page in _pdf.pages:
                    _t = _page.extract_text()
                    if _t:
                        _pl_text += _t + "\n"
                # plumber格式："被保险人 于建刚" 或 "投保人： 于建刚"
                _nm = re.search(r"被保险人\s+([^\s\n]{2,6})", _pl_text)
                if _nm:
                    _name_from_text = _nm.group(1).strip()
                if not _name_from_text:
                    _nm2 = re.search(r"投保人[：:\s]+([^\s\n]{2,6})", _pl_text)
                    if _nm2:
                        _name_from_text = _nm2.group(1).strip()
        except Exception:
            pass
    # 校验：纯中文2-6字
    if _name_from_text and re.match(r'^[\u4e00-\u9fff]{2,6}$', _name_from_text) and "证件" not in _name_from_text and "地址" not in _name_from_text and "义务" not in _name_from_text:
        data["被保人姓名"] = _name_from_text
    else:
        # 文件名兜底
        fname_m = re.search(r"_([^()_\-]{2,20})(?:\(\d+\))?\.(?:pdf|PDF)", os.path.basename(pdf_path or ""))
        data["被保人姓名"] = fname_m.group(1) if fname_m else ""

    # 9. 被保险人证件号（身份证:370602196905292930）
    id_m = re.search(r"身份证[：:\s]*([\dXx]{17,18})", text)
    data["被保险人证件号"] = id_m.group(1) if id_m else ""

    # 10. 被保险人手机号（联系电话138****0337，但"联系电话"标签乱码）
    phone_m = re.search(r"(\d{3}\*\*\*\*\d{4})", text)
    if not phone_m:
        phone_m = re.search(r"联系电话[：:\s]*(\d{3,4}\*\*\*\*\d{4})", text)
    _ph = phone_m.group(1) if phone_m else ""
    data["被保险人手机号"] = "" if is_blacklisted_phone(_ph) else _ph

    # 11. 车辆使用性质（平安PDF中文乱码，但"营业"/"非营业"部分可读）
    # 从文本中搜索 使用性质 后面的关键词
    nature_m = re.search(r"使用性质[：:\s]*(非营业|营业|家庭自用)", text)
    if nature_m:
        data["车辆使用性质"] = nature_m.group(1)
    else:
        data["车辆使用性质"] = ""

    # 12. 车辆型号名称
    model_m = re.search(r"车辆型号[：:\s]*([^\n]{5,50})", text)
    data["车辆型号名称"] = model_m.group(1).strip() if model_m else ""

    # 13. 实收保费（收费合计:RMB760.00元）
    premium_m = re.search(r"收费合计[：:\s]*RMB\s*([0-9,]+\.\d{2})", text)
    if not premium_m:
        premium_m = re.search(r"保险费合计[：:\s]*RMB\s*([0-9,]+\.\d{2})", text)
    data["实收保费"] = premium_m.group(1) if premium_m else ""

    # 14. 车船税（当年应缴\n( ��420.00\n元) 或 ( �� 420.00 元)）
    tax_m = re.search(r"当年应缴\s*\(\s*[\uffe5¥￥]?\s*([0-9,]+\.\d{2})", text)
    if not tax_m:
        # 兜底：��۷�ʰԪ�� 420.00（合计大写后面的金额）
        tax_m = re.search(r"合计.*?([0-9,]+\.\d{2})\s*元\s*完", text)
    data["车船税"] = tax_m.group(1) if tax_m else ""

    # 15. Filename
    data["Filename"] = os.path.basename(pdf_path) if pdf_path else ""

    return data

# =============================================================================
# 平安车主尊享保障专用解析（pymupdf 文本全乱码）
# =============================================================================
def parse_pingan_garbled(text, pdf_path=None):
    """
    专门处理平安车主尊享保障 PDF（pymupdf 文本乱码）的解析。
    乱码特征：
      - "PING AN" (英文公司名) / "RMB" (保费) 可在文本中找到
      - policy no / chassis / plate / dates / premium 均为 ASCII/数字，正常可读
      - 唯一无法使用的是中文 label 正则
    """
    data = {}
    lines = text.split("\n")

    # ---------- 1. 从文件名提取车牌和被保人 ----------
    # ---------- 1. 从文件名提取车牌和被保人 ----------
    # 文件名格式：鲁F-216AC_平安财产_车主尊享保障_于建刚(1).pdf
    fname_plate_m = re.search(r"^([A-Z0-9]{2}-[A-Z0-9]{4,5})_", os.path.basename(pdf_path or ""))
    data["车牌号码"] = fname_plate_m.group(1) if fname_plate_m else ""
    # 兜底：从文件名中提取省份+字母+横杠+数字格式（编码损坏时³替代鲁等情况）
    if not data["车牌号码"]:
        fname_plate_m2 = re.search(r"([\u4e00-\u9fff\u00c0-\u024fA-Z]{2}-[A-Z0-9]{4,5})_", os.path.basename(pdf_path or ""))
        if fname_plate_m2:
            data["车牌号码"] = fname_plate_m2.group(1)
    # 兜底2：从PDF文本中提取（处理换行拆断的情况，如 "鲁F-\n216AC"）
    if not data["车牌号码"] and text:
        # 先去掉换行符，再匹配（处理车牌被换行拆断的情况）
        text_no_newline = text.replace('\n', ' ')
        plate_m = re.search(r'车牌号码[：:\s]*([鲁京津沪渝冀豫云辽黑湘皖晋疆藏贵甘青桂琼苏浙蒙鄂][A-Z0-9\- ]{4,8})', text_no_newline)
        if plate_m:
            data["车牌号码"] = plate_m.group(1).replace(' ', '')
    # 8. 被保人姓名（从pdfplumber文本提取，取不到再从文件名兜底）
    _name_from_text = ""
    if pdf_path:
        try:
            with pdfplumber.open(pdf_path) as _pdf:
                _pl_text = ""
                for _page in _pdf.pages:
                    _t = _page.extract_text()
                    if _t:
                        _pl_text += _t + "\n"
                # 格式1（交强险）："被保险人 于建刚"（同行空格分隔）
                for _m in re.finditer(r"被保险人 ([\u4e00-\u9fff]{2,4})\b", _pl_text):
                    _candidate = _m.group(1).strip()
                    if _candidate and _candidate not in ("姓名", "信息", "类型"):
                        _name_from_text = _candidate
                        break
                # 格式2（车主尊享）："于建刚 身份证"（身份证前面的中文姓名）
                if not _name_from_text:
                    _nm2 = re.search(r"\n([\u4e00-\u9fff]{2,4})\s+身份证", _pl_text)
                    if _nm2:
                        _name_from_text = _nm2.group(1).strip()
                # 格式3（车主尊享）："投保人姓名...\\n于建刚 身份证"
                if not _name_from_text:
                    _nm3 = re.search(r"投保人姓名[^\n]*\n\s*([\u4e00-\u9fff]{2,4})\s", _pl_text)
                    if _nm3:
                        _name_from_text = _nm3.group(1).strip()
                # 格式4："投保人： 于建刚"
                if not _name_from_text:
                    _nm4 = re.search(r"投保人[：:\s]+([\u4e00-\u9fff]{2,4})\b", _pl_text)
                    if _nm4 and _nm4.group(1) not in ("姓名", "信息"):
                        _name_from_text = _nm4.group(1).strip()
        except Exception:
            pass
    if _name_from_text and "证件" not in _name_from_text and "地址" not in _name_from_text:
        data["被保人姓名"] = _name_from_text
    else:
        # 文件名兜底
        _base = os.path.basename(pdf_path or "")
        _NAME_BLACKLIST = {"交强险", "商业险", "驾乘险", "车险", "保单", "保单号", "电子"}
        for _nm in re.finditer(r"(?:^|[_\-])([\u4e00-\u9fff]{2,4})(?:[_\-]|$)", _base):
            if _nm.group(1) not in _NAME_BLACKLIST:
                data["被保人姓名"] = _nm.group(1)
                break
        else:
            data["被保人姓名"] = ""

    # ---------- 1.5 险种名称原始（从PDF第一页第2行提取） ----------
    data["险种名称原始"] = ""
    if pdf_path:
        try:
            doc = fitz.open(pdf_path)
            page = doc[0]
            lines = page.get_text("text").strip().split("\n")
            for line in lines[1:]:  # 跳过第1行（公司名）
                line_s = line.strip()
                if line_s and len(line_s) > 3 and not re.match(r"^(保单号|验真码|\d{10,})", line_s):
                    data["险种名称原始"] = line_s
                    break
            doc.close()
        except Exception:
            pass

    # ---------- 2. 提取 policy no（含Z格式：111310666Z3351003940，16-20字符） ----------
    all_nos = re.findall(r"\b([0-9Z]{16,20})\b", text)
    data["保单号"] = ""
    for p in all_nos:
        if "Z" in p:  # 含Z的优先
            data["保单号"] = p
            break
    if not data["保单号"]:  # 兜底：纯数字16+
        for p in reversed(all_nos):
            if p.isdigit() and not p.startswith("0") and len(p) >= 16:
                data["保单号"] = p
                break

    # ---------- 3. 车架号 ----------
    data["车架号"] = extract_vin_strict(text, [
        r"车架号[码]?\s*:\s*([A-Z0-9]{17})",
        r"车架号[码]?\s*\n\s*:\s*([A-Z0-9]{17})",
        r"VIN码[：:\s]*([A-Z0-9]{17})",
        r"识别代码[：:\s]*([A-Z0-9]{17})",
        r"车架号码?\s*\n\s*([A-Z0-9]{17})",
        r"\n([A-Z0-9]{17})\n",
    ])

    # ---------- 4. 保险公司名称 ----------
    data["保险公司名称"] = "中国平安财产保险股份有限公司"

    # ---------- 5. 保险起期（pymupdf/plumber 文本格式：时/分/秒用中文） ----------
    # 平安车主尊享格式（"保险期限"标签，跨两行）：
    # L35: "保险期限"
    # L36: "   2026年05月10日00时00分00秒 起 至"
    # L37: "   2027年05月09日24时00分00秒 止 (北京时间)"
    # plumber排版可能把日期行和其他字段混在一起，需用DOTALL跨行匹配
    combined = text  # already joined with '\n'
    period_m = re.search(
        r"(\d{4})年(\d{1,2})月(\d{1,2})日(\d{2}时\d{2}分\d{2}秒)\s+起\s*至.*?(\d{4})年(\d{1,2})月(\d{1,2})日(\d{2}时\d{2}分\d{2}秒)\s*止",
        combined, re.DOTALL
    )
    if period_m:
        start = f"{period_m.group(1)}年{int(period_m.group(2)):02d}月{int(period_m.group(3)):02d}日{period_m.group(4)}"
        end   = f"{period_m.group(5)}年{int(period_m.group(6)):02d}月{int(period_m.group(7)):02d}日{period_m.group(8)}"
        data["保险起期"] = f"{start} 至 {end}"
    else:
        # 兜底：小时格式（不带分/秒）
        period_m2 = re.search(
            r"(\d{4})年(\d{1,2})月(\d{1,2})日\s+至\s+(\d{4})年(\d{1,2})月(\d{1,2})日",
            combined
        )
        if period_m2:
            data["保险起期"] = f"{period_m2.group(1)}年{int(period_m2.group(2)):02d}月{int(period_m2.group(3)):02d}日 至 {period_m2.group(4)}年{int(period_m2.group(5)):02d}月{int(period_m2.group(6)):02d}日"
        else:
            data["保险起期"] = ""

    # ---------- 6. 实收保费（从 "RMB XXXX.XX" 提取） ----------
    premium_matches = re.findall(r"RMB([0-9,]+\.\d{2})", text)
    if premium_matches:
        premiums = [float(p.replace(",", "")) for p in premium_matches]
        data["实收保费"] = f"{max(premiums):.2f}"
    else:
        data["实收保费"] = ""

    # ---------- 7. 签单时间（pymupdf格式：签单日期/出单日期：2026年04月21日09时） ----------
    # pymupdf 文本中"签单日期"和年月日之间有空格分隔符，直接搜索
    # 支持两种标签：签单日期、出单日期（平安车主尊享保障用"出单日期"）
    sig_m = re.search(r"(?:签单日期|出单日期)[：:\s]*(\d{4})年(\d{1,2})月(\d{1,2})日\s*(\d{2})时", text)
    if sig_m:
        data["签单时间"] = f"{sig_m.group(1)}-{int(sig_m.group(2)):02d}-{int(sig_m.group(3)):02d} {sig_m.group(4)}时"
    else:
        # 兜底：找 "YYYY-MM-DD HH:MM" 格式，但跳过包含"确认"的上下文
        sig_m2 = re.search(r"(\d{4})-(\d{2})-(\d{2})\s+\d{2}:\d{2}", text)
        if sig_m2:
            # 确认时间格式："YYYY年MM月DD日 HH:MM:SS"（确认时间在前，签单时间在后）
            # 但签单日期行本身包含"签单日期" label，已被上面正则捕获
            # 这里只处理另一种情况：单独出现的 "YYYY-MM-DD HH:MM"（不带年月日 label）
            sig_text = sig_m2.group(0)
            sig_pos = sig_m2.start()
            # 确认时间前面有"确认"关键字，签单时间没有
            before_ctx = text[max(0, sig_pos-10):sig_pos]
            if "确认" not in before_ctx:
                data["签单时间"] = f"{sig_m2.group(1)}-{sig_m2.group(2)}-{sig_m2.group(3)}"
            else:
                data["签单时间"] = ""
        else:
            data["签单时间"] = ""

    # ---------- 8. 其他字段（驾乘险无） ----------
    data["被保险人证件号"] = ""
    data["被保险人手机号"] = ""
    data["车辆使用性质"] = ""
    data["车辆型号名称"] = ""
    data["车船税"] = ""

    # 标记：车牌/起期/签单已从文件名+乱码文本正确提取，skip clean_data 的字段清洗
    data["_skip_plate_wash"] = True

    return clean_data(data, text, pdf_path)

# =============================================================================
# 驾乘险专用解析（平安车主尊享保障 / 阳光驾乘人员团体意外伤害保险）
# 特点：非车险，无车架号/VIN标准字段，有"驾乘"、"车上人员"等关键词
# 提取字段：保单号、保险公司、车牌号、被保人姓名、证件号、手机号、保险起期、实收保费、签单时间
# =============================================================================
def parse_jiacheng(text, pdf_path=None):
    """驾乘险专用解析。支持平安车主尊享保障、阳光驾乘人员团体意外伤害保险、亚太驾乘非车险。"""
    data = {}

    # 1. 签单时间
    # 平安车主尊享格式："签单日期：2026年04月21日09时"（在最后一页）
    # 阳光驾乘格式："签单日期：2026-04-08"
    # 亚太EDY/EDV格式：标签CID乱码，日期在文档末尾（如"2026年04月17日"）
    data["签单时间"] = safe_extract(text, [
        r"签单日期[：:\s]*(\d{4}[-/]\d{2}[-/]\d{2})",
        r"签单日期[：:\s]*(\d{4}年\d{2}月\d{2}日)",
        r"签单日期[：:\s]*(\d{4}年\d{2}月\d{2}日\d{2}时)",
        r"保单确认时间[：:\s]*(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2})",
        r"保单生成时间[：:\s]*(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2})",
        r"收费确认时间[：:\s]*(\d{4}年\d{2}月\d{2}日\d{2}时\d{2}分)",
        r"投保确认时间[：:\s]*(\d{4}年\d{2}月\d{2}日\d{2}时\d{2}分)",
        r"打印时间[：:\s]*(\d{4}年\d{2}月\d{2}日\d{2}时\d{2}分)",
        r"保费确认时间[：:\s]*(\d{4}年\d{2}月\d{2}日)",
        r"保费确认时间[：:\s]*(\d{4}[-/]\d{2}[-/]\d{2})",
        r"保单打印时间[：:\s]*(\d{4}[-/]\d{2}[-/]\d{2})",
    ])
    # 兜底：CID字体乱码导致标签无法匹配，取文档末尾最后一个日期（签单时间通常在最后）
    if not data.get("签单时间"):
        _all_dates = re.findall(r"(\d{4})[年\-/.](\d{1,2})[月\-/.](\d{1,2})", text)
        if _all_dates:
            # 取最后一个日期（签单时间通常在文档末尾）
            _y, _m, _d = _all_dates[-1]
            data["签单时间"] = f"{_y}-{int(_m):02d}-{int(_d):02d}"

    # 2. 保险公司名称
    data["保险公司名称"] = safe_extract(text, [
        r"公司名称[：:]\s*(?:(?!公司地址|邮政编码|服务电话|签单日期|保单号)[^\n]*?)",
        r"公司名称[：:]\s+([^\n]{2,60})",
        r"(平安财产保险[^\n]{0,20})",
        r"(阳光财产保险[^\n]{0,20})",
        r"(亚太财产保险[^\n]{0,20})",
        r"(安华农业保险[^\n]{0,20})",
    ])

    # 3. 保单号
    data["保单号"] = _filter_policy_no(safe_extract_policy_no(text, "保险单号"))

    # 4. 保险起期
    # 平安车主尊享格式："保险期间\n   2026年05月10日00时00分00秒 起 至\n   2027年05月09日24时00分00秒 止 (北京时间)"
    # 注意：PDF中"保险期间"和日期之间可能有换行和空格
    # 阳光驾乘格式："保险期间 2026年04月14日 00:00:00 至 2027年04月13日 24:00:00"
    data["保险起期"] = safe_extract(text, [
        r"保险期间[\s\n]+(\d{4}年\d{1,2}月\d{1,2}日\d{2}时\d{2}分\d{2}秒?)\s+起\s+至\s+(\d{4}年\d{1,2}月\d{1,2}日\d{2}时\d{2}分\d{2}秒?)\s+止",
        r"保险期间[：:]\s*(\d{4}年\d{1,2}月\d{1,2}日\s+\d{2}:\d{2}:\d{2})\s+至\s+(\d{4}年\d{1,2}月\d{1,2}日\s+\d{2}:\d{2}:\d{2})",
        r"保险期间[：:\s]*自\s+(\d{4}年\d{1,2}月\d{1,2}日)\s+至\s+(\d{4}年\d{1,2}月\d{1,2}日)",
        r"保险期间[：:\s]*(\d{4}年\d{1,2}月\d{1,2}日)",
    ])
    # 合并起止期
    _m_jc1 = re.search(r"保险期间[\s\n]+(\d{4}年\d{1,2}月\d{1,2}日\d{2}时\d{2}分\d{2}秒?)\s+起\s+至\s+(\d{4}年\d{1,2}月\d{1,2}日\d{2}时\d{2}分\d{2}秒?)\s+止", text)
    if _m_jc1:
        data["保险起期"] = _m_jc1.group(1) + " 至 " + _m_jc1.group(2)
    elif not re.search(r"\d{4}年.*至", data.get("保险起期", "")):
        _m_jc2 = re.search(r"保险期间[：:]\s*(\d{4}年\d{1,2}月\d{1,2}日\s+\d{2}:\d{2}:\d{2})\s+至\s+(\d{4}年\d{1,2}月\d{1,2}日\s+\d{2}:\d{2}:\d{2})", text)
        if _m_jc2:
            data["保险起期"] = _m_jc2.group(1) + " 至 " + _m_jc2.group(2)
    elif not re.search(r"\d{4}年.*至", data.get("保险起期", "")):
        _m_jc3 = re.search(r"保险期间[：:\s]*自\s+(\d{4}年\d{1,2}月\d{1,2}日)\s+至\s+(\d{4}年\d{1,2}月\d{1,2}日)", text)
        if _m_jc3:
            data["保险起期"] = _m_jc3.group(1) + " 至 " + _m_jc3.group(2)
    # 如果保险起期仍为空，尝试从"保险期间"附近查找日期
    if not data.get("保险起期"):
        _m_jc4 = re.search(r"保险期间[\s\S]{0,50}(\d{4}年\d{1,2}月\d{1,2}日)", text)
        if _m_jc4:
            data["保险起期"] = _m_jc4.group(1)
    # 亚太EDY/EDV格式："\n365天，2026年04月26日零时起至2027年04月25日二十四时止\n"
    if not data.get("保险起期") or "至" not in data.get("保险起期", ""):
        _m_jc5 = re.search(r"(\d{4}年\d{1,2}月\d{1,2}日)\S*起至(\d{4}年\d{1,2}月\d{1,2}日)\S*止", text)
        if _m_jc5:
            data["保险起期"] = _m_jc5.group(1) + " 至 " + _m_jc5.group(2)

    # 5. 车牌号码
    # 平安车主尊享格式："车牌号码:鲁F-216AC;"（有分号结尾，但"鲁"可能乱码）
    # 阳光驾乘格式："车牌号 鲁FB7W68"
    # 亚太驾乘格式："车牌号码\n鲁Y37V00"（车牌在下一行）
    data["车牌号码"] = safe_extract(text, [
        # 平安格式：车牌号码:鲁F-216AC;
        r"车牌号码[：:\s]*([A-Z][A-Z0-9\-]{4,8});",
        r"车牌号码[：:\s]*([A-Z][A-Z0-9\-]{4,8})",
        r"号牌号码[：:\s]*([^\s\n]{3,10})",
        r"车牌号[：:\s]*([^\s\n]{3,10})",
        r"保险车辆号牌[：:\s]*([^\s\n]{3,10})",
    ])
    # 亚太格式：车牌号码在下一行，包含中文字符（鲁/京/沪等）
    if not data.get("车牌号码") or len(data.get("车牌号码", "")) < 5:
        _m_plate_next = re.search(r"车牌号码\s*\n\s*([\u4e00-\u9fff][A-Z][A-Z0-9]{4,6})", text)
        if _m_plate_next:
            data["车牌号码"] = _m_plate_next.group(1)
    # 如果车牌号码提取失败，尝试从文件名提取
    if not data.get("车牌号码") or len(data.get("车牌号码", "")) < 5:
        _m_file = re.search(r"([A-Z]-[A-Z0-9]{4,5})_", pdf_path or "")
        if _m_file:
            data["车牌号码"] = _m_file.group(1)
        else:
            # 尝试从车架号附近查找
            _m_plate = re.search(r"车架号[：:\s]*[A-Z0-9]{17};.*?车牌号码[：:\s]*([A-Z][A-Z0-9\-]{4,8});", text)
            if _m_plate:
                data["车牌号码"] = _m_plate.group(1)

    # 6. 被保人姓名
    # 平安车主尊享格式：投保人信息\n投保人姓名\n证件类型\n证件号码\n手机号\n联系邮箱\n通讯地址\n于建刚
    # 姓名在所有标签之后，但中文字符可能乱码，尝试从文件名提取
    # 阳光驾乘格式："投保人姓名 莱州亿邦机械有限责任公司"
    data["被保人姓名"] = safe_extract(text, [
        r"投保人姓名[：:\s]*([^\s\n]{2,30})",
        # 平安格式：通讯地址后面是姓名
        r"通讯地址\s+([^\s\n]{2,10})\s+\n",
        # 平安格式：投保人信息块中，姓名在"通讯地址"之后
        r"通讯地址\n+([^\s\n]{2,10})\s+\n",
        r"投保人[：:]\s*([\u4e00-\u9fff]{2,20})",
        r"被保险人[：:]\s*([\u4e00-\u9fff]{2,20})",
    ])
    # 如果被保人姓名提取失败或为乱码，尝试从文件名提取
    if not data.get("被保人姓名") or data.get("被保人姓名") in ("证件类型", "身份证"):
        _m_name = re.search(r"_([^\(\)_]{2,20})\.", pdf_path or "")
        if _m_name:
            data["被保人姓名"] = _m_name.group(1)
        else:
            # 尝试从"投保人信息"块中提取姓名（在"通讯地址"之后）
            _m_addr = re.search(r"通讯地址\s*\n\s*([^\s\n]{2,10})", text)
            if _m_addr:
                data["被保人姓名"] = _m_addr.group(1)

    # 7. 被保险人证件号
    data["被保险人证件号"] = safe_extract(text, [
        r"证件号码[：:\s]*([A-Z0-9\*]{10,30})",
        r"身份证号码[：:\s]*([A-Z0-9\*]{10,30})",
        r"统一社会信用代码[：:\s]*([A-Z0-9\*]{10,30})",
    ])
    # CID字体乱码兜底：直接搜索18位身份证号格式
    if not data.get("被保险人证件号"):
        _m_id_fb = re.search(r"\b(\d{17}[\dXx])\b", text)
        if _m_id_fb:
            data["被保险人证件号"] = _m_id_fb.group(1)

    # 8. 被保险人手机号
    data["被保险人手机号"] = safe_extract_phone(text)

    # 9. 车架号
    data["车架号"] = safe_extract(text, [
        r"车架号[码]?\s*[：:]\s*([A-Z0-9]{17})",
        r"VIN码[：:\s]*([A-Z0-9]{17})",
        r"识别代码[：:\s]*([A-Z0-9]{17})",
    ])
    # 平安车主尊享格式：车架号\n:XXX（换行后跟冒号）
    if not data.get("车架号"):
        _m_vin_next = re.search(r"车架号[码]?\s*\n\s*[：:]\s*([A-Z0-9]{17})", text)
        if _m_vin_next:
            data["车架号"] = _m_vin_next.group(1)
    # 亚太驾乘格式：车架号码在下一行
    if not data.get("车架号"):
        _m_vin_next = re.search(r"车架号码?\s*\n\s*([A-Z0-9]{17})", text)
        if _m_vin_next:
            data["车架号"] = _m_vin_next.group(1)
    # 兜底：如果车架号仍为空，从文本中搜索所有17位字母数字串，取符合VIN规则的
    if not data.get("车架号"):
        _all_17 = re.findall(r"\b([A-Z0-9]{17})\b", text)
        for _c in _all_17:
            if is_valid_vin(_c):
                data["车架号"] = _c
                break

    # 10. 发动机号
    data["发动机号"] = safe_extract(text, [
        r"发动机号[：:\s]*([A-Z0-9]{5,20})",
    ])

    # 11. 实收保费
    # 平安车主尊享格式："保险费合计/RMB389.00（不含税保费：382.96元，税额：6.04元）"
    # 阳光驾乘格式："保险费合计 人民币（大写）:壹佰捌拾元整 ￥180.00"
    # 亚太EDY格式：标签CID乱码，"总保费\n300.00" 或 "总保险金额\n258,000.00\n总保费\n300.00"
    data["实收保费"] = safe_extract(text, [
        # 平安格式：RMB389.00
        r"保险费合计[^\d]*RMB\s*([0-9,]+\.?\d{2})",
        # 阳光格式：￥180.00
        r"保险费合计[^\d]*￥\s*([0-9,]+\.?\d{2})",
        r"保险费合计[^\d]*([0-9,]+\.?\d{2})",
    ])
    # 亚太格式："保险费\n大写：人民币...小写：CNY 160.00"
    # 注意：PDF 中有"总保险金额...小写：CNY 2,950,000.00"和"保险费...小写：CNY 160.00"两行，必须锚定"保险费"标签
    if not data.get("实收保费"):
        _m_premium_cny = re.search(r"保险费[\s\S]{0,60}小写[：:]\s*CNY\s*([0-9,]+\.?\d{2})", text)
        if _m_premium_cny:
            data["实收保费"] = _m_premium_cny.group(1)
    # 亚太CID乱码格式：标签乱码但"总保费"数字在独立行（如"\n300.00\n"）
    # 策略：找"总保费"后最近的数字行
    if not data.get("实收保费"):
        _m_zongbf = re.search(r"总保费[^\d]*(\d[\d,]*\.?\d{2})", text)
        if _m_zongbf:
            data["实收保费"] = _m_zongbf.group(1)
    # 亚太CID乱码格式：标签乱码但"￥300.00"在独立行
    # 策略：找所有"￥"后面的数字，取最合理的保费值（排除大额保险金额）
    if not data.get("实收保费"):
        _yen_nums = re.findall(r"￥\s*([\d,]+\.?\d{2})", text)
        if _yen_nums:
            # 排除大额（>10000可能是保险金额），取最合理的保费值
            _premium_candidates = []
            for _yn in _yen_nums:
                try:
                    _yv = float(_yn.replace(",", ""))
                    if 50 <= _yv <= 10000:
                        _premium_candidates.append(_yn)
                except Exception:
                    pass
            if _premium_candidates:
                data["实收保费"] = _premium_candidates[-1]  # 取最后一个（保费通常在金额之后）
    # 兜底：在最后500字符找保费数字（必须含小数点，如300.00）
    if not data.get("实收保费"):
        _last_500 = text[-500:] if len(text) > 500 else text
        _nums = re.findall(r"(\d[\d,]*\.\d{2})", _last_500)
        _valid = []
        for _n in _nums:
            try:
                _v = float(_n.replace(",", ""))
                if 50 <= _v <= 50000:
                    _valid.append(_n)
            except Exception:
                pass
        if _valid:
            data["实收保费"] = _valid[-1]  # 取最后一个合理值（保费通常在金额字段之后）

    # 12. 车船税 - 驾乘险无车船税
    data["车船税"] = ""

    # 13. 车辆使用性质 - 驾乘险通常无此字段
    data["车辆使用性质"] = ""

    # 14. 车辆型号名称 - 驾乘险通常无此字段
    data["车辆型号名称"] = ""

    # 15. 险种名称原始兜底 - 如果正则提取为空，用pymupdf读取PDF第一页第一个有效行
    if not data.get("险种名称原始") or is_garbled_text(data.get("险种名称原始", "")):
        try:
            doc = fitz.open(pdf_path)
            page = doc[0]
            lines = page.get_text("text").strip().split("\n")
            first_real_line = None
            for line in lines:
                line_stripped = line.strip()
                # 跳过页眉行：保险单号 + 纯数字policy_no + 公司名（XX财产保险有限公司）
                if line_stripped and not re.match(r"^保险单号?：?$", line_stripped) and not re.match(r"^\d{10,}$", line_stripped) and not re.search(r"财产保险有限公司$", line_stripped):
                    first_real_line = line_stripped
                    break
            if first_real_line and not is_garbled_text(first_real_line):
                data["险种名称原始"] = re.sub(r"电子保险单|电子保单$", "", first_real_line).strip()
            else:
                # 乱码兜底：通过OCR提取产品名
                product_name = extract_product_name_from_pdf(pdf_path)
                if product_name and not is_garbled_text(product_name):
                    data["险种名称原始"] = product_name
                else:
                    # 最终兜底：尝试通过像素分析判断是驾乘险
                    data["险种名称原始"] = "驾乘守护"
            doc.close()
        except Exception:
            pass

    return clean_data(data, text, pdf_path)

# =============================================================================
# 大地保险安行如意保（团体意外险）专用解析
# 特点：PDF中文CID字体导致pdfplumber中文乱码，但英文/数字正常；
# 被保险人以编号表格形式呈现：编号 姓名 证件号 生日
# =============================================================================
def parse_dadi_anyang(pymupdf_text, plumber_text):
    """大地安行如意保专用解析。优先用pymupdf文本（CID字体下仍能正确提取ASCII字符）。"""
    # 优先用pymupdf（大地如意行PDF的CID字体不影响pymupdf提取ASCII字符）
    text = pymupdf_text if pymupdf_text.strip() else plumber_text

    data = {}

    # 1. 签单时间
    data["签单时间"] = safe_extract(text, [
        r"出单时间[：:\s]*(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})",
        r"签单日期[：:\s]*(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})",
        r"签单日期[：:\s]*(\d{4}-\d{2}-\d{2})",
        r"签单日期[：:\s]*(\d{4}/\d{2}/\d{2})",
        r"签单时间[：:\s]*(\d{4}年\d{2}月\d{2}日)",
        r"保单确认时间[：:\s]*(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2})",
        r"保单生成时间[：:\s]*(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2})",
    ])

    # 2. 保险公司名称（大地财产）
    data["保险公司名称"] = "中国大地财产保险股份有限公司"

    # 3. 保单号
    data["保单号"] = _filter_policy_no(safe_extract_policy_no(text, "保险单号"))

    # 4. 保险起期（大地如意行格式：支持 2026年05月10日 起至 和 2026 年 05 月 10 日 起至 两种格式）
    data["保险起期"] = safe_extract(text, [
        # 大地司乘险商业险格式：保险期间:自 2026年04月24日00:00 起至 2027年04月23日24:00 止
        r'保险期间[：:].*?(\d{4}年\d{2}月\d{2}日\d{2}:\d{2})\s+起至\s+(\d{4}年\d{2}月\d{2}日\d{2}:\d{2})\s+止',
        r"(\d{4}\s*年\s*\d{2}\s*月\s*\d{2}\s*日).*?至",
        r"\d{4}[年\-]\d{2}[月\-]\d{2}.*?至.*?(\d{4}[年\-]\d{2}[月\-]\d{2})",
    ])
    # 大地司乘险 合并两个 capture group
    if data.get("保险起期") and "起至" in data["保险起期"]:
        _m = re.search(r'保险期间[：:].*?(\d{4}年\d{2}月\d{2}日\d{2}:\d{2})\s+起至\s+(\d{4}年\d{2}月\d{2}日\d{2}:\d{2})\s+止', text)
        if _m:
            data["保险起期"] = _m.group(1) + " 至 " + _m.group(2)

    # 司乘险商业险 Fallback：如果 plumber_text 可用，直接尝试用完整格式提取
    if plumber_text:
        _m2 = re.search(r'保险期间[：:].*?(\d{4}年\d{2}月\d{2}日\d{2}:\d{2})\s+起至\s+(\d{4}年\d{2}月\d{2}日\d{2}:\d{2})\s+止', plumber_text)
        if _m2:
            data["保险起期"] = _m2.group(1) + " 至 " + _m2.group(2)
    # 大地意外险格式："保险期间：2026-04-08 13:36:11" + 文本中有日期范围
    if not data.get("保险起期"):
        _m3 = re.search(r"保险期间.*?(\d{4}-\d{2}-\d{2})\s+\d{2}:\d{2}:\d{2}", text)
        if _m3:
            # 找结束日期（通常在开始日期后365天内）
            _start = _m3.group(1)
            _all_dates = re.findall(r"(\d{4}-\d{2}-\d{2})", text)
            for _d in _all_dates:
                if _d != _start:
                    data["保险起期"] = f"{_start} 至 {_d}"
                    break

    # 5. 车辆使用性质
    nature_match = re.search(r"使用性质[：: \t]*([^\s\n]{2,20})", text)
    data["车辆使用性质"] = nature_match.group(1).strip() if nature_match else ""

    # 6. 车架号（优先从"车架号："标签取，PDF中为"车架号：LFV3B28R8E3082130"）
    # 排除保险合同号 CZ263...、policy no（PEXD...）等
    vin = safe_extract(text, [
        r"车架号[：:\s]*([A-HJ-NPR-Z0-9]{17})",  # 优先：车架号：LFV3B28R8E3082130
        r"车架号\s*\n\s*([A-HJ-NPR-Z0-9]{17})",  # 大地格式：车架号在下一行
        r"\b([A-HJ-NPR-Z0-9]{17})\b",           # 兜底：全文17位
    ])
    if vin and not vin.upper().startswith(("PEXD", "PEBS", "PDZA", "PDAA", "AJINF", "CZ", "XD")):
        data["车架号"] = vin
    else:
        data["车架号"] = ""

    # 7. 车辆型号名称
    vm_match = re.search(r"[A-HJ-NPR-Z0-9]{17}\s+[^\d\s]+.*?(?:号牌号码|$)", text)
    if not vm_match:
        vm_match = re.search(r"厂牌型号[：:\s]*([^\n]{3,50})", text)
    data["车辆型号名称"] = vm_match.group(1).strip() if vm_match else ""

    # 8. 被保人姓名 — 大地如意行表格格式：编号 姓名 证件号 生日
    # pymupdf文本中"罗方春"是正确的UTF-8中文
    data["被保人姓名"] = safe_extract(text, [
        r"(?<!\d)\d+\s{1,5}([^\s\d][^\n]{1,29})(?:\s+[0-9*]{10,}|\s+\d{4}[年\-]\d{2})",
        r"被保险人[：:\s]*([^\n]{2,30})",
    ])
    if data.get("被保人姓名") and any(b in data["被保人姓名"] for b in ["保险单", "车辆", "以下", "约定", "规定"]):
        data["被保人姓名"] = ""

    # 9. 被保险人证件号
    data["被保险人证件号"] = safe_extract(text, [
        r"(\d{17}[0-9X])",
        r"(\d{15})",
    ])

    # 10. 被保险人手机号（优先不脱敏）
    data["被保险人手机号"] = safe_extract_phone(text)
    # 兜底：pymupdf文本中"联系电话"和手机号被拆到不同行，正则匹配不上
    if not data.get("被保险人手机号"):
        _m = re.search(r'联系电话\s*\n.*?\n.*?\n.*?\n(1[3-9][\d\*]{9,14})', text, re.DOTALL)
        if _m:
            data["被保险人手机号"] = _m.group(1)

    # 11. 车牌号码
    data["车牌号码"] = safe_extract(text, [
        r"([鲁京津沪渝冀豫云辽黑湘皖晋疆藏贵甘青桂琼苏浙蒙鄂][A-HJ-NP-Z0-9]{5,7})",
    ])

    # 12. 险种名称原始
    data["险种名称原始"] = safe_extract(text, [
        r"安行如意保[^\n]*?(?:意外|综合)",
        r"安行如意保[^\n]{0,20}",
        r"(?:驾乘|交通).*?意外.*?(?:伤害|保险)",
    ]) or "安行如意保团体意外险"

    # 13. 实收保费（大地如意行：¥455.00）
    # 安享B款格式：（小写）￥279.9（不含税保险费：264.06元，增值税：15.84元）
    fee = safe_extract(text, [
        r"（小写）\s*[￥¥]\s*([0-9,]+\.?\d*)",  # 安享B款
        # Fix: cross-line format (total premium\n肆佰伍元整  ￥455.00)
        r"总保险费.*?\n[^\n]*?￥\s*([0-9,]+\.?\d*)",
        r"总保险费[：:\s]*[￥¥]?\s*([0-9,]+\.?\d*)",
        r"总保费[：:\s]*[￥¥]?\s*([0-9,]+\.?\d*)",
        r"保险费.*?([0-9,]+\.?\d*)\s*(?:元|RMB)",
        r"[（(][￥¥]?\s*([0-9]{3,5}\.00)[）)]\s*元",
    ])
    if not fee:
        # 兜底：搜所有金额，排除过长的数字（保单号/VIN误识）
        amounts = re.findall(r'[￥¥]?\s*([0-9,]+\.?\d{2})', text)
        valid = []
        for a in amounts:
            num = float(a.replace(",", ""))
            # 金额范围：100 <= fee < 50000，排除保单号/VIN/手机号等长数字
            if 100 <= num < 50000:
                # Skip year-like numbers 2013-2030 (insurance period years)
                if 2013 <= num <= 2030:
                    continue
                valid.append((num, a))
        if valid:
            fee = max(valid, key=lambda x: x[0])[1]
    data["实收保费"] = fee or ""

    # 14. 车船税（大地如意行无车船税）
    data["车船税"] = ""

    # 商业司乘险 Fallback：如果 plumber_text 有完整的保险期间，优先用它
    if plumber_text:
        _m2 = re.search(r'保险期间[：:].*?(\d{4}年\d{2}月\d{2}日\d{2}:\d{2})\s+起至\s+(\d{4}年\d{2}月\d{2}日\d{2}:\d{2})\s+止', plumber_text)
        if _m2:
            data["保险起期"] = _m2.group(1) + " 至 " + _m2.group(2)

    return data

# =============================================================================
# 太平财险解析器（CID字体，中文乱码，但pdfplumber表格可读）
# =============================================================================
def _taiping_table_find(tables, label_keywords):
    """在pdfplumber表格中搜索包含关键词的行，返回该行中关键词后面的值。"""
    for tbl in tables:
        for row in tbl:
            for ci, cell in enumerate(row):
                if cell and any(kw in str(cell) for kw in label_keywords):
                    # 找关键词后面的值
                    for vi in range(ci + 1, len(row)):
                        v = row[vi]
                        if v and str(v).strip():
                            return str(v).strip()
                    # 如果同行没找到，看下一行
                    row_idx = tbl.index(row)
                    if row_idx + 1 < len(tbl):
                        for v in tbl[row_idx + 1]:
                            if v and str(v).strip():
                                return str(v).strip()
    return ""

def _taiping_table_find_row(tables, label_keywords):
    """在pdfplumber表格中搜索包含关键词的行，返回整行。"""
    for tbl in tables:
        for row in tbl:
            for cell in row:
                if cell and any(kw in str(cell) for kw in label_keywords):
                    return row
    return None

def parse_taipingProperty(text, pdf_path=None):
    """太平财产保险 交强险+商业险解析器。
    太平PDF使用CID字体，pymupdf/pdfplumber文本中文乱码，但pdfplumber表格数据可读。
    """
    data = {}
    # 公司名称（固定值，因为文本乱码无法提取）
    data["保险公司名称"] = "太平财产保险有限公司"

    # === 从pymupdf blocks提取ASCII可读字段 ===
    all_blocks_text = ""
    try:
        with fitz.open(pdf_path) as doc:
            for page in doc:
                blocks = page.get_text("blocks")
                for b in blocks:
                    if len(b) >= 5 and b[4]:
                        all_blocks_text += b[4] + "\n"
    except Exception:
        pass

    # 保单号（从pymupdf文本提取）
    m_policy = re.search(r"保险单号[：:\s]*(\d{10,})", all_blocks_text)
    data["保单号"] = m_policy.group(1) if m_policy else ""

    # 签单时间（优先用保费确认时间，它比签单日期更精确）
    m_sign = re.search(r"保费确认时间[：:\s]*(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2}:\d{2})", all_blocks_text)
    if m_sign:
        data["签单时间"] = m_sign.group(1)
    else:
        m_sign2 = re.search(r"签单日期[：:\s]*(\d{4})年(\d{1,2})月(\d{1,2})日", all_blocks_text)
        if m_sign2:
            data["签单时间"] = f"{m_sign2.group(1)}-{int(m_sign2.group(2)):02d}-{int(m_sign2.group(3)):02d}"
        else:
            data["签单时间"] = ""

    # === 从pdfplumber表格提取结构化字段 ===
    tables = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                t = page.extract_tables()
                if t:
                    tables.extend(t)
    except Exception:
        pass

    # 被保人姓名
    data["被保人姓名"] = _taiping_table_find(tables, ["被 保 险 人", "被保险人"])
    # 过滤非姓名内容
    name = data.get("被保人姓名", "")
    if name and (name[0].isdigit() or "身份证" in name or "号码" in name or len(name) > 20):
        data["被保人姓名"] = ""

    # 被保险人证件号（18位身份证）
    for tbl in tables:
        for row in tbl:
            for cell in row:
                if cell:
                    s = re.sub(r'\s', '', str(cell))
                    if len(s) == 18 and s[:17].isdigit() and s[-1] in 'X0123456789':
                        data["被保险人证件号"] = s
                        break
            if data.get("被保险人证件号"):
                break

    # 被保险人手机号
    for tbl in tables:
        for row in tbl:
            for cell in row:
                if cell:
                    m = re.search(r'(1[3-9]\d{9})', str(cell))
                    if m:
                        data["被保险人手机号"] = m.group(1)
                        break
            if data.get("被保险人手机号"):
                break
    if not data.get("被保险人手机号"):
        # 从pymupdf文本提取（可能脱敏）
        m_phone = re.search(r'(1[3-9]\d[\d\*]{8,12})', all_blocks_text)
        if m_phone:
            data["被保险人手机号"] = m_phone.group(1)

    # 号牌号码
    data["车牌号码"] = _taiping_table_find(tables, ["号 牌 号 码", "号牌号码"])

    # 车架号/VIN
    data["车架号"] = _taiping_table_find(tables, ["识别代码", "车架号", "VIN码"])

    # 车辆型号名称
    data["车辆型号名称"] = _taiping_table_find(tables, ["厂 牌 型 号", "厂牌型号"])
    # 清理换行
    if data.get("车辆型号名称"):
        data["车辆型号名称"] = data["车辆型号名称"].replace('\n', '')

    # 使用性质
    data["车辆使用性质"] = _taiping_table_find(tables, ["使用性质"])
    # 兜底1：从pdfplumber页面文本中提取（表格可能CID乱码，但页面文本中"使用性质"后的值可读）
    if not data.get("车辆使用性质") and pdf_path:
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    pt = page.extract_text() or ""
                    m_nature = re.search(r"使用性质[：:\s]*(非营业|非营运|营业|营运|家庭自用|非营业客车|营业客车|非营业汽车|营业汽车)", pt)
                    if m_nature:
                        data["车辆使用性质"] = m_nature.group(1)
                        break
        except Exception:
            pass
    # 兜底2：从pymupdf文本中提取
    if not data.get("车辆使用性质"):
        m_nature2 = re.search(r"使用性质[：:\s]*(非营业|非营运|营业|营运|家庭自用)", all_blocks_text)
        if m_nature2:
            data["车辆使用性质"] = m_nature2.group(1)

    # 保险期间
    period_row = _taiping_table_find_row(tables, ["保险期间", "保 险 期 间"])
    if period_row:
        for cell in period_row:
            if cell:
                cell_str = str(cell)
                m_p = re.search(
                    r'(\d{4})\s*年\s*(\d{1,2})\s*月\s*(\d{1,2})\s*日\s*(\d{2})\s*时\s*(\d{2})\s*分',
                    cell_str
                )
                if m_p and '起至' in cell_str:
                    # 找结束日期
                    m_e = re.search(
                        r'(\d{4})\s*年\s*(\d{1,2})\s*月\s*(\d{1,2})\s*日\s*(\d{2})\s*时\s*(\d{2})\s*分',
                        cell_str[cell_str.index('起至'):]
                    )
                    if m_e:
                        start = f"{m_p.group(1)}年{int(m_p.group(2)):02d}月{int(m_p.group(3)):02d}日{m_p.group(4)}时{m_p.group(5)}分"
                        end = f"{m_e.group(1)}年{int(m_e.group(2)):02d}月{int(m_e.group(3)):02d}日{m_e.group(4)}时{m_e.group(5)}分"
                        data["保险起期"] = f"{start} 至 {end}"
                    break
    if not data.get("保险起期"):
        # 兜底：从pymupdf文本提取
        m_period = re.search(
            r'自\s*(\d{4})\s*年\s*(\d{2})\s*月\s*(\d{2})\s*日\s*(\d{2})\s*时\s*(\d{2})\s*分\s*\d{2}\s*秒?起至\s*(\d{4})\s*年\s*(\d{2})\s*月\s*(\d{2})\s*日\s*(\d{2})\s*时\s*(\d{2})\s*分',
            all_blocks_text
        )
        if m_period:
            start = f"{m_period.group(1)}年{int(m_period.group(2)):02d}月{int(m_period.group(3)):02d}日{m_period.group(4)}时{m_period.group(5)}分"
            end = f"{m_period.group(6)}年{int(m_period.group(7)):02d}月{int(m_period.group(8)):02d}日{m_period.group(9)}时{m_period.group(10)}分"
            data["保险起期"] = f"{start} 至 {end}"

    # 险种名称原始
    if "667070801" in data.get("保单号", ""):
        data["险种名称原始"] = "机动车交通事故责任强制保险"
    elif "667070802" in data.get("保单号", ""):
        data["险种名称原始"] = "机动车商业保险"
    else:
        data["险种名称原始"] = ""

    # 实收保费
    premium_row = _taiping_table_find_row(tables, ["保 险 费 合 计", "保险费合计", "保险费 合计"])
    if premium_row:
        for cell in premium_row:
            if cell:
                cell_str = str(cell)
                # 从表格单元格中提取金额（RMB格式或纯数字）
                m_pr = re.search(r'(?:RMB|￥|¥)\s*([0-9,]+\.?\d{2})', cell_str)
                if m_pr:
                    data["实收保费"] = m_pr.group(1)
                    break
                # 纯数字格式
                m_pr2 = re.search(r'(\d{3,6}\.\d{2})', cell_str)
                if m_pr2:
                    val = float(m_pr2.group(1).replace(',', ''))
                    if 100 <= val <= 50000:
                        data["实收保费"] = m_pr2.group(1)
                        break
    # 兜底：从pymupdf文本提取
    if not data.get("实收保费"):
        m_prem = re.search(r'(?:RMB|￥|¥)\s*([0-9,]+\.?\d{2})', all_blocks_text)
        if m_prem:
            data["实收保费"] = m_prem.group(1)

    # 车船税（仅交强险有）
    data["车船税"] = ""
    tax_row = _taiping_table_find_row(tables, ["当年应缴", "车船税"])
    if tax_row:
        for cell in tax_row:
            if cell:
                cell_str = str(cell)
                m_tax = re.search(r'[￥¥]?\s*：?\s*(\d{2,4}\.\d{1,2})\s*元?', cell_str)
                if m_tax:
                    val = float(m_tax.group(1).replace(',', ''))
                    if 0 < val <= 5000:
                        data["车船税"] = m_tax.group(1)
                        break

    return data

def parse_taiping_jiacheng(text, pdf_path=None):
    """太平财产保险 驾乘险（乐驾齐鲁升级版）解析器。
    太平PDF使用CID字体，但pdfplumber表格数据可读。
    """
    data = {}
    data["保险公司名称"] = "太平财产保险有限公司"
    data["险种名称原始"] = "乐驾齐鲁升级版"

    # === 从pymupdf blocks提取 ===
    all_blocks_text = ""
    try:
        with fitz.open(pdf_path) as doc:
            for page in doc:
                blocks = page.get_text("blocks")
                for b in blocks:
                    if len(b) >= 5 and b[4]:
                        all_blocks_text += b[4] + "\n"
    except Exception:
        pass

    # 保单号（格式：P436707C052660007713629，P+字母数字混合）
    m_policy = re.search(r'(P[A-Z0-9]{15,30})', all_blocks_text)
    if not m_policy:
        m_policy = re.search(r'(P\d{10,})', all_blocks_text)
    data["保单号"] = m_policy.group(1) if m_policy else ""

    # 签单时间
    m_sign = re.search(r"制单时间[：:\s]*(\d{4}-\d{2}-\d{2})\s+\d{2}:\d{2}:\d{2}", all_blocks_text)
    if m_sign:
        data["签单时间"] = m_sign.group(1)
    else:
        m_sign2 = re.search(r"签单日期[：:\s]*(\d{4}-\d{2}-\d{2})", all_blocks_text)
        if m_sign2:
            data["签单时间"] = m_sign2.group(1)
        else:
            data["签单时间"] = ""

    # === 从pdfplumber表格提取 ===
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
    data["被保人姓名"] = _taiping_table_find(tables, ["投保人姓名"])

    # 证件号
    data["被保险人证件号"] = _taiping_table_find(tables, ["证件号码"])

    # 手机号
    data["被保险人手机号"] = _taiping_table_find(tables, ["联系电话"])
    if not data.get("被保险人手机号"):
        # 从pymupdf文本提取
        m_phone = re.search(r'(1[3-9]\d{9})', all_blocks_text)
        if m_phone:
            data["被保险人手机号"] = m_phone.group(1)

    # 车牌号
    data["车牌号码"] = _taiping_table_find(tables, ["牌照号码", "号牌号码"])

    # 车架号
    data["车架号"] = _taiping_table_find(tables, ["车辆识别代码", "车架号", "VIN"])

    # 车辆型号
    data["车辆型号名称"] = _taiping_table_find(tables, ["厂牌型号"])
    if data.get("车辆型号名称"):
        data["车辆型号名称"] = data["车辆型号名称"].replace('\n', '')

    # 使用性质（表头可能是"使用性质"或"车辆使用性质"）
    data["车辆使用性质"] = _taiping_table_find(tables, ["使用性质", "车辆使用性质"])
    # 兜底：从pymupdf文本提取
    if not data.get("车辆使用性质"):
        m_nature = re.search(r"使用性质\s*\n?\s*(非营业|营业|家庭自用汽车|家庭自用)", all_blocks_text)
        if m_nature:
            data["车辆使用性质"] = m_nature.group(1)

    # 保险起期
    data["保险起期"] = _taiping_table_find(tables, ["保险期限"])
    if data.get("保险起期"):
        # 标准化格式：2026-02-13 00:00:00 至 2027-02-12 23:59:59
        m_period = re.search(
            r'(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})\s*至\s*(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})',
            data["保险起期"]
        )
        if m_period:
            # 转换为标准格式
            s = m_period.group(1)
            e = m_period.group(2)
            sm = re.match(r'(\d{4})-(\d{2})-(\d{2})\s+(\d{2}):(\d{2}):(\d{2})', s)
            em = re.match(r'(\d{4})-(\d{2})-(\d{2})\s+(\d{2}):(\d{2}):(\d{2})', e)
            if sm and em:
                start = f"{sm.group(1)}年{int(sm.group(2)):02d}月{int(sm.group(3)):02d}日{sm.group(4)}时{sm.group(5)}分"
                end = f"{em.group(1)}年{int(em.group(2)):02d}月{int(em.group(3)):02d}日{em.group(4)}时{em.group(5)}分"
                data["保险起期"] = f"{start} 至 {end}"

    # 实收保费 - 精确提取，避免匹配到险种描述等错误单元格
    data["实收保费"] = ""
    # 方法1: 从表格中找含"总保费"且含CNY金额的行
    for tbl in tables:
        for row in tbl:
            row_text = " ".join(str(c) for c in row if c)
            if "总保费" in row_text or "总保費" in row_text:
                # 优先找CNY格式
                m_pr = re.search(r'CNY\s*([0-9,]+\.?\d{2})', row_text)
                if m_pr:
                    data["实收保费"] = m_pr.group(1)
                    break
                # 找数字金额（排除年份等不合理值）
                amounts = re.findall(r'([0-9,]+\.\d{2})', row_text)
                for a in amounts:
                    try:
                        val = float(a.replace(',', ''))
                        if 10 <= val <= 10000:
                            data["实收保费"] = a
                            break
                    except Exception:
                        pass
                if data.get("实收保费"):
                    break
    # 方法2: 从pymupdf文本找保费（优先匹配"总保费(含税)：CNYxxx"）
    if not data.get("实收保费"):
        m_prem = re.search(r'总保费\s*[\(（]含税[\)）][：:\s]*[人民币]*\s*CNY\s*([0-9,]+\.?\d{2})', all_blocks_text)
        if m_prem:
            data["实收保费"] = m_prem.group(1)
        else:
            # 兜底：找 CNY 金额（排除保额50万等大额）
            for m_prem in re.finditer(r'CNY\s*([0-9,]+\.?\d{2})', all_blocks_text):
                try:
                    val = float(m_prem.group(1).replace(',', ''))
                    if 10 <= val <= 10000:  # 合理保费范围
                        data["实收保费"] = m_prem.group(1)
                        break
                except Exception:
                    pass

    # 车船税（驾乘险无）
    data["车船税"] = ""

    return data

def parse_taishan(text, pdf_path=None):
    """泰山财产保险 交强险+商业险解析器。
    泰山PDF中文完全可读，使用标准正则提取。
    """
    data = {}

    # 保险公司名称
    data["保险公司名称"] = "泰山财产保险股份有限公司"

    # 保单号
    m_policy = re.search(r"保单号[：:\s]*(\d{12,})", text)
    data["保单号"] = m_policy.group(1) if m_policy else ""

    # 签单时间
    m_sign = re.search(r"签单日期[：:\s]*(\d{4})年(\d{1,2})月(\d{1,2})日", text)
    if m_sign:
        data["签单时间"] = f"{m_sign.group(1)}-{int(m_sign.group(2)):02d}-{int(m_sign.group(3)):02d}"
    else:
        # 兜底：收费确认时间
        m_sign2 = re.search(r"收费确认时间[：:\s]*(\d{4}-\d{2}-\d{2})", text)
        if m_sign2:
            data["签单时间"] = m_sign2.group(1)
        else:
            data["签单时间"] = _sign_date_fallback(pdf_path, "")

    # 被保人姓名
    data["被保人姓名"] = safe_extract(text, [
        r"被保险人\s*\n?\s*([^\s\n]{2,10})",
        r"被保险人[：:\s]*([^\s\n]{2,10})",
    ])
    # 过滤非姓名内容
    name = data.get("被保人姓名", "")
    if name and (name[0].isdigit() or "身份证" in name or "号码" in name or len(name) > 15):
        data["被保人姓名"] = ""

    # 被保险人证件号
    data["被保险人证件号"] = safe_extract(text, [
        r"身份证号码[^A-Z0-9]*(\d{17}[\dXx])",
        r"身份证号码[（(]统一社会信用代码[)）][：:\s]*(\d{17}[\dXx])",
        r"身份证号/统一社会信用代码\s*\n?\s*(\d{17}[\dXx])",
        r"证件号码[：:\s]*(\d{17}[\dXx])",
    ])

    # 被保险人手机号
    data["被保险人手机号"] = safe_extract_phone(text)

    # 号牌号码
    data["车牌号码"] = safe_extract(text, [
        rf"号牌号码\s*\n?\s*({PLATE_PATTERN})",
        rf"号牌号码[：:\s]*({PLATE_PATTERN})",
    ])

    # 车架号
    data["车架号"] = extract_vin_strict(text, [
        r"识别代码[（(]车架号[)）]\s*\n?\s*([A-Z0-9]{17})",
        r"识别代码[（(]?车架号[)）]?[：:\s]*([A-Z0-9]{17})",
        r"VIN码[/／]车架号\s*\n?\s*([A-Z0-9]{17})",
        r"车架号[：:\s]*([A-Z0-9]{17})",
    ])

    # 车辆型号名称
    data["车辆型号名称"] = safe_extract(text, [
        r"厂牌型号[：:\s]*([^\n]{3,50})",
        r"厂牌型号\s*\n?\s*([^\n]{3,50})",
    ])
    if data.get("车辆型号名称"):
        # 截断到下一个字段
        m_model = re.match(r'([^\n]+)', data["车辆型号名称"])
        if m_model:
            data["车辆型号名称"] = m_model.group(1).strip()

    # 使用性质
    data["车辆使用性质"] = safe_extract(text, [
        rf"使用性质({NATURE_PATTERN})",
        rf"使用性质[：:\s]+({NATURE_PATTERN})",
    ])

    # 保险起期
    data["保险起期"] = safe_extract(text, [
        r"保险期间\s*\n?\s*自\s*(\d{4}年\d{1,2}月\d{1,2}日\s*\d{2}:\d{2}:\d{2})\s*起至\s*(\d{4}年\d{1,2}月\d{1,2}日\s*\d{2}:\d{2}:\d{2})\s*止",
        r"保险期间[：:\s]*\n?\s*自\s*(\d{4}年\d{1,2}月\d{1,2}日\s*\d{2}:\d{2}:\d{2})\s*起至\s*(\d{4}年\d{1,2}月\d{1,2}日\s*\d{2}:\d{2}:\d{2})\s*止",
    ])
    # 合并起止期
    _m_ts = re.search(
        r"保险期间\s*\n?\s*自\s*(\d{4}年\d{1,2}月\d{1,2}日\s*\d{2}:\d{2}:\d{2})\s*起至\s*(\d{4}年\d{1,2}月\d{1,2}日\s*\d{2}:\d{2}:\d{2})\s*止",
        text
    )
    if _m_ts:
        data["保险起期"] = _m_ts.group(1).replace(' ', '') + " 至 " + _m_ts.group(2).replace(' ', '')
    # 兜底：商业险可能没有"自...起至...止"，而是"保险期间 日期 至 日期"格式
    if not data.get("保险起期") or "至" not in data.get("保险起期", ""):
        _m_ts2 = re.search(
            r"保险期间[：:\s]*(\d{4}年\d{1,2}月\d{1,2}日\s*\d{2}:\d{2}:\d{2})\s*至\s*(\d{4}年\d{1,2}月\d{1,2}日\s*\d{2}:\d{2}:\d{2})",
            text
        )
        if _m_ts2:
            data["保险起期"] = _m_ts2.group(1).replace(' ', '') + " 至 " + _m_ts2.group(2).replace(' ', '')
    # 兜底2：更宽松的格式，无空格分隔
    if not data.get("保险起期") or "至" not in data.get("保险起期", ""):
        _m_ts3 = re.search(
            r"保险期间[：:\s]*(\d{4}年\d{1,2}月\d{1,2}日\d{2}:\d{2}:\d{2})\s*至\s*(\d{4}年\d{1,2}月\d{1,2}日\d{2}:\d{2}:\d{2})",
            text
        )
        if _m_ts3:
            data["保险起期"] = _m_ts3.group(1) + " 至 " + _m_ts3.group(2)
    # 兜底3：从已有起始日期附近找"至"+结束日期
    if data.get("保险起期") and "至" not in data["保险起期"]:
        _cur_start = data["保险起期"]
        _m_end = re.search(r"至\s*(\d{4}年\d{1,2}月\d{1,2}日\s*\d{2}:\d{2}:\d{2})", text)
        if _m_end:
            data["保险起期"] = _cur_start + " 至 " + _m_end.group(1).replace(' ', '')

    # 险种名称原始
    if "交强" in text[:500] or "交通事故责任强制" in text[:500]:
        data["险种名称原始"] = "机动车交通事故责任强制保险"
    elif "商业保险" in text[:500]:
        data["险种名称原始"] = "机动车商业保险"
    else:
        data["险种名称原始"] = ""

    # 实收保费
    data["实收保费"] = safe_extract(text, [
        r"￥[：:\s]*([0-9,]+\.?\d*)\s*元",
        r"保险费合计[^\d]*￥[：:\s]*([0-9,]+\.?\d*)",
        r"保险费合计[（(]人民币大写[）)][：:\s]*[^\d]*￥[：:\s]*([0-9,]+\.?\d*)",
        r"（￥[：:\s]*([0-9,]+\.?\d*)\s*元[）)]",
        r"实收保费[：:\s]*[￥¥]?\s*([0-9,]+\.?\d*)",
    ])

    # 车船税
    data["车船税"] = safe_extract(text, [
        r"当年应缴\s*\n?\s*(\d{2,4}\.\d{1,2})\s*元",
        r"当年应缴[：:\s]*(\d{2,4}\.\d{1,2})\s*元",
        r"车船税[：:\s]*(\d{2,4}\.\d{1,2})",
    ])

    return data

def parse_taishan_jiacheng(text, pdf_path=None):
    """泰山财产保险 驾乘人员意外险（非车险）解析器。
    泰山PDF中文完全可读，使用标准正则提取。
    """
    data = {}

    # 保险公司名称
    data["保险公司名称"] = "泰山财产保险股份有限公司"

    # 保单号
    m_policy = re.search(r"保单号[：:\s]*(\d{12,})", text)
    data["保单号"] = m_policy.group(1) if m_policy else ""

    # 签单时间
    m_sign = re.search(r"签单日期[：:\s]*(\d{4})/(\d{1,2})/(\d{1,2})", text)
    if m_sign:
        data["签单时间"] = f"{m_sign.group(1)}-{int(m_sign.group(2)):02d}-{int(m_sign.group(3)):02d}"
    else:
        m_sign2 = re.search(r"签单日期[：:\s]*(\d{4})年(\d{1,2})月(\d{1,2})日", text)
        if m_sign2:
            data["签单时间"] = f"{m_sign2.group(1)}-{int(m_sign2.group(2)):02d}-{int(m_sign2.group(3)):02d}"
        else:
            data["签单时间"] = _sign_date_fallback(pdf_path, "")

    # 被保人姓名（投保人名称）
    data["被保人姓名"] = safe_extract(text, [
        r"名称\s*\n?\s*([^\s\n]{2,10})",
        r"投保人[：:\s]*([^\s\n]{2,10})",
    ])
    name = data.get("被保人姓名", "")
    if name and (name[0].isdigit() or "证件" in name or len(name) > 15):
        data["被保险人姓名"] = ""
        data["被保人姓名"] = ""

    # 证件号
    data["被保险人证件号"] = safe_extract(text, [
        r"证件号码\s*\n?\s*(\d{17}[\dXx])",
        r"证件号码[：:\s]*(\d{17}[\dXx])",
    ])

    # 手机号
    data["被保险人手机号"] = safe_extract_phone(text)

    # 车牌号
    data["车牌号码"] = safe_extract(text, [
        rf"车牌号[：:\s]*({PLATE_PATTERN})",
        rf"车牌号\s*\n?\s*({PLATE_PATTERN})",
    ])

    # 车架号
    data["车架号"] = extract_vin_strict(text, [
        r"车架号[：:\s]*([A-Z0-9]{17})",
        r"车架号\s*\n?\s*([A-Z0-9]{17})",
    ])

    # 险种名称原始
    data["险种名称原始"] = "驾乘人员意外险"

    # 车辆使用性质（驾乘险通常无，但泰山非车险可能有）
    data["车辆使用性质"] = ""

    # 车辆型号（驾乘险通常无）
    data["车辆型号名称"] = ""

    # 保险起期
    data["保险起期"] = safe_extract(text, [
        r"保险期间\s*\n?\s*自\s*(\d{4}年\d{1,2}月\d{1,2}日\s*\d{2}:\d{2}:\d{2})\s*起至\s*(\d{4}年\d{1,2}月\d{1,2}日\s*\d{2}:\d{2}:\d{2})\s*止",
    ])
    _m_tsjc = re.search(
        r"保险期间\s*\n?\s*自\s*(\d{4}年\d{1,2}月\d{1,2}日\s*\d{2}:\d{2}:\d{2})\s*起至\s*(\d{4}年\d{1,2}月\d{1,2}日\s*\d{2}:\d{2}:\d{2})\s*止",
        text
    )
    if _m_tsjc:
        data["保险起期"] = _m_tsjc.group(1).replace(' ', '') + " 至 " + _m_tsjc.group(2).replace(' ', '')

    # 实收保费
    data["实收保费"] = safe_extract(text, [
        r"总保险费\s*\n?[^\d]*小写[：:\s]*￥\s*([0-9,]+\.?\d*)",
        r"总保险费[^\d]*￥\s*([0-9,]+\.?\d*)",
        r"￥[：:\s]*([0-9,]+\.?\d*)",
    ])

    # 车船税（驾乘险无）
    data["车船税"] = ""

    return data

# =============================================================================
# 安华农业保险 解析器
# =============================================================================
def _anhua_clean_number(s):
    """Remove spaces within numbers in Anhua PDF text (e.g. '2 026' -> '2026', '8 40.00' -> '840.00')."""
    if not s:
        return s
    # Remove spaces within digit groups: '2 026' -> '2026', '8 40.00' -> '840.00'
    s = re.sub(r'(\d)\s+(\d)', r'\1\2', s)
    return s

def parse_anhua(pymupdf_text, pdf_path=None):
    """安华农业保险 交强险+商业险。pymupdf文本字段值为空，必须用pdfplumber。"""
    data = {}
    data["保险公司名称"] = "安华农业保险股份有限公司"
    fname = os.path.basename(pdf_path or "")
    data["险种名称原始"] = "机动车交通事故责任强制保险单" if "交强" in fname else "机动车商业保险单"

    tables, pl_text = [], ""
    if pdf_path:
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    t = page.extract_text()
                    if t: pl_text += t + "\n"
                    tbls = page.extract_tables()
                    if tbls: tables.extend(tbls)
        except Exception: pass

    # 安华PDF数字内部有空格（如 "2 026-04-17"、"P DDA"、"8 40.00"），需要清理
    pl_clean = pl_text

    data["保单号"] = ""
    # 安华保单号格式: P DDA202637068700000361（P和DDA之间有空格）
    m_policy = re.search(r"保险单号[：:\s]*P\s*([A-Z0-9]{15,})", pl_clean)
    if m_policy:
        data["保单号"] = "P" + m_policy.group(1)
    else:
        m = re.search(r"保险单号[：:\s]*([A-Z0-9]{10,})", pl_clean)
        data["保单号"] = m.group(1) if m else ""
    m = re.search(r"签单日期[：:\s]*(\d[\s]*\d[\s]*\d[\s]*\d-\d{2}-\d{2})", pl_clean)
    if not m: m = re.search(r"收费时间[：:\s]*(\d[\s]*\d[\s]*\d[\s]*\d-\d{2}-\d{2})", pl_clean)
    if m:
        # 清理日期中的空格: "2 026-04-17" -> "2026-04-17"
        data["签单时间"] = _anhua_clean_number(m.group(1))
    else:
        data["签单时间"] = ""
    data["被保人姓名"] = ""
    m_name = re.search(r"被\s*保\s*险\s*人\s+([^\s\n]{2,10})", pl_clean)
    if not m_name:
        m_name = re.search(r"被保险人\s+([^\s\n]{2,10})", pl_clean)
    if not m_name:
        m_name = re.search(r"被保险人\s*\n\s*([^\s\n]{2,10})", pl_clean)
    if m_name and not m_name.group(1)[0].isdigit(): data["被保人姓名"] = m_name.group(1).strip()
    m = re.search(r"(\d{17}[\dXx])", pl_clean)
    data["被保险人证件号"] = m.group(1) if m else ""
    data["被保险人手机号"] = ""
    m_ph = re.search(r"(1[3-9]\d[\d\*]{8,12})", pl_clean)
    if m_ph: data["被保险人手机号"] = m_ph.group(1)
    m = re.search(r"(鲁[A-Z]\-?[A-Z0-9]{4,5})", pl_clean)
    data["车牌号码"] = m.group(1) if m else ""
    data["车架号"] = ""
    m_vin = re.search(r"识别代码[（(]车架号[)）]\s*\n?\s*([A-Z0-9]{17})", pl_clean)
    if not m_vin: m_vin = re.search(r"\b([A-Z0-9]{17})\b", pl_clean)
    if m_vin: data["车架号"] = m_vin.group(1)
    data["车辆型号名称"] = ""
    m_mdl = re.search(r"厂牌型号\s*\n?\s*([^\n]{3,50})", pl_clean)
    if m_mdl: data["车辆型号名称"] = m_mdl.group(1).strip()
    data["车辆使用性质"] = ""
    m_nat = re.search(r"使用性质\s*\n?\s*([^\s\n]{2,10})", pl_clean)
    if m_nat: data["车辆使用性质"] = m_nat.group(1)
    data["保险起期"] = ""
    m_per = re.search(r"保险期间自\s*(\d{4}年\d{1,2}月\d{1,2}日[^至]*?)\s*至\s*(\d{4}年\d{1,2}月\d{1,2}日[^止]*?)\s*止", pl_clean)
    if m_per: data["保险起期"] = m_per.group(1).strip() + " 至 " + m_per.group(2).strip()
    data["实收保费"] = ""
    # 安华保费格式: "（Y：8 40.00元）" 或 "（Y：18 60.38 元）" 数字内部有空格
    m_prem = re.search(r"Y[：:\s]*(\d[\s\d,]*\.?\d{2})\s*元", pl_clean)
    if m_prem:
        data["实收保费"] = _anhua_clean_number(m_prem.group(1))
    else:
        # 兜底：保险费合计后面的金额
        m_prem2 = re.search(r"保险费合计[^\d]*(\d[\s\d,]*\.?\d{2})\s*元", pl_clean)
        if m_prem2:
            data["实收保费"] = _anhua_clean_number(m_prem2.group(1))
    data["车船税"] = ""
    m_tax = re.search(r"当年应缴\s*\n?\s*(\d[\s]*\.?\d*)", pl_clean)
    if m_tax:
        val = _anhua_clean_number(m_tax.group(1))
        try:
            if float(val.replace(',', '')) > 0: data["车船税"] = val
        except Exception: pass
    return data

def parse_anhua_jiacheng(text, pdf_path=None):
    """安华农业保险 驾乘险（EDY/EDV）。支持亚太财产保险非车险（CID字体乱码）。"""
    data = {}
    data["保险公司名称"] = "安华农业保险股份有限公司"
    data["险种名称原始"] = "驾乘人员交通意外伤害保险"
    m = re.search(r"保单号[：:\s]*(PEDY\d+|PEDV\d+|P[A-Z0-9]{15,})", text)
    data["保单号"] = m.group(1) if m else ""
    # 签单时间：优先匹配标签，标签乱码时取文档末尾最后一个日期
    m = re.search(r"签单日期[：:\s]*(\d{4}-\d{2}-\d{2})", text)
    if not m:
        m = re.search(r"确认时间[：:\s]*(\d{4}年\d{2}月\d{2}日)", text)
    if not m:
        m = re.search(r"确认时间[：:\s]*(\d{4}[-/]\d{2}[-/]\d{2})", text)
    if not m:
        # CID字体乱码兜底：取文档末尾最后一个日期
        _all_dates = re.findall(r"(\d{4})[年\-/.](\d{1,2})[月\-/.](\d{1,2})", text)
        if _all_dates:
            _y, _mo, _d = _all_dates[-1]
            data["签单时间"] = f"{_y}-{int(_mo):02d}-{int(_d):02d}"
        else:
            data["签单时间"] = ""
    else:
        data["签单时间"] = m.group(1)
    data["被保人姓名"] = ""
    m_name = re.search(r"投保人\s*\n?\s*([^\s\n]{2,8})", text)
    if m_name: data["被保人姓名"] = m_name.group(1).strip()
    data["被保险人证件号"] = ""
    m_id = re.search(r"证件号码\s*\n?\s*(\d{17}[\dXx])", text)
    if m_id: data["被保险人证件号"] = m_id.group(1)
    data["被保险人手机号"] = ""
    m_ph = re.search(r"联系电话\s*\n?\s*(1[3-9]\d{9})", text)
    if m_ph: data["被保险人手机号"] = m_ph.group(1)
    data["车牌号码"] = ""
    m_p = re.search(r"车牌号\s*\n?\s*(鲁[A-Z]\-?[A-Z0-9]{4,5})", text)
    if not m_p: m_p = re.search(r"(鲁[A-Z]\-?[A-Z0-9]{4,5})", text)
    if m_p: data["车牌号码"] = m_p.group(1)
    data["车架号"] = ""
    m_v = re.search(r"车架号\s*\n?\s*([A-Z0-9]{17})", text)
    if not m_v: m_v = re.search(r"\b([A-Z0-9]{17})\b", text)
    if m_v: data["车架号"] = m_v.group(1)
    data["车辆型号名称"] = ""
    m_m = re.search(r"厂牌型号\s*\n?\s*([^\n]{3,50})", text)
    if m_m: data["车辆型号名称"] = m_m.group(1).strip()
    data["车辆使用性质"] = ""
    m_n = re.search(r"车辆使用性质\s*\n?\s*([^\s\n]{2,10})", text)
    if m_n: data["车辆使用性质"] = m_n.group(1)
    # 保险起期 - 支持多种格式
    data["保险起期"] = ""
    # 格式1: 2026年04月26日零时起至2027年04月25日二十四时止
    m_p1 = re.search(r"自\s*(\d{4}年\d{1,2}月\d{1,2}日)[^至]*?起[至，,]*\s*(\d{4}年\d{1,2}月\d{1,2}日)[^止]*?止", text)
    if m_p1:
        data["保险起期"] = m_p1.group(1).strip() + " 至 " + m_p1.group(2).strip()
    # 格式2: 自2026-04-26 00:00起至2027-04-25 24:00
    if not data.get("保险起期"):
        m_p2 = re.search(r"自\s*(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2})\s*起至\s*(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2})", text)
        if m_p2:
            sm, em = re.match(r"(\d{4})-(\d{2})-(\d{2})\s+(\d{2}):(\d{2})", m_p2.group(1)), re.match(r"(\d{4})-(\d{2})-(\d{2})\s+(\d{2}):(\d{2})", m_p2.group(2))
            if sm and em: data["保险起期"] = f"{sm.group(1)}年{int(sm.group(2)):02d}月{int(sm.group(3)):02d}日{sm.group(4)}时{sm.group(5)}分 至 {em.group(1)}年{int(em.group(2)):02d}月{int(em.group(3)):02d}日{em.group(4)}时{em.group(5)}分"
    # 格式3: 共365天，自2026年04月26日零时起至2027年04月25日二十四时止
    if not data.get("保险起期"):
        m_p3 = re.search(r"(\d{4}年\d{1,2}月\d{1,2}日)\s*零时起[至]*\s*(\d{4}年\d{1,2}月\d{1,2}日)\s*二十四时止", text)
        if m_p3:
            data["保险起期"] = m_p3.group(1).strip() + " 至 " + m_p3.group(2).strip()
    data["实收保费"] = ""
    m_pr = re.search(r"保险费合计[：:\s]*(?:人民币)?[大写]*[：:\s]*[^\d]*(\d+)\s*元", text)
    if not m_pr: m_pr = re.search(r"[￥Y][：:\s]*(\d[\d,]*\.?\d*)\s*元", text)
    if not m_pr:
        # ￥符号兜底：找所有"￥"后面的数字，取最合理的保费值
        _yen_nums = re.findall(r"￥\s*([\d,]+\.?\d{2})", text)
        if _yen_nums:
            _premium_candidates = []
            for _yn in _yen_nums:
                try:
                    _yv = float(_yn.replace(",", ""))
                    if 50 <= _yv <= 10000:
                        _premium_candidates.append(_yn)
                except Exception:
                    pass
            if _premium_candidates:
                data["实收保费"] = _premium_candidates[-1]
    elif m_pr:
        data["实收保费"] = m_pr.group(1)
    data["车船税"] = ""
    return data

# =============================================================================
# 中煤财产保险 解析器
# =============================================================================
def parse_zhongmei(pymupdf_text, pdf_path=None):
    """中煤财产保险 交强险。pymupdf字段值为空，用pdfplumber。"""
    data = {}
    data["保险公司名称"] = "中煤财产保险股份有限公司"
    data["险种名称原始"] = "机动车交通事故责任强制保险单"

    tables, pl_text = [], ""
    if pdf_path:
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    t = page.extract_text()
                    if t: pl_text += t + "\n"
                    tbls = page.extract_tables()
                    if tbls: tables.extend(tbls)
        except Exception: pass

    m = re.search(r"保单号[：:\s]*(\d{10,})", pl_text)
    data["保单号"] = m.group(1) if m else ""
    m = re.search(r"签单日期[：:\s]*(\d{4}-\d{2}-\d{2})", pl_text)
    data["签单时间"] = m.group(1) if m else ""

    # 被保人（从表格提取）
    data["被保人姓名"] = ""
    for tbl in tables:
        for row in tbl:
            if row and row[0] and "被保险人" in str(row[0]) and "身份证" not in str(row[0]):
                if row[1] and len(str(row[1]).strip()) >= 2:
                    data["被保人姓名"] = str(row[1]).strip()
                    break
        if data["被保人姓名"]: break
    m = re.search(r"(\d{17}[\dXx])", pl_text)
    data["被保险人证件号"] = m.group(1) if m else ""
    data["被保险人手机号"] = safe_extract_phone(pl_text)
    data["车牌号码"] = ""
    for tbl in tables:
        for row in tbl:
            for cell in row:
                if cell and re.search(r'鲁[A-Z]\-?[A-Z0-9]{4,5}', str(cell)):
                    m_p = re.search(r'(鲁[A-Z]\-?[A-Z0-9]{4,5})', str(cell))
                    data["车牌号码"] = m_p.group(1)
                    break
            if data["车牌号码"]: break
    data["车架号"] = ""
    # 中煤格式1: "被 6座以下客车 LGBL22E24BY009682\n保 机动车种类 识别代码（车架号）"
    # 值在标签上一行，需要匹配"客车"后面的17位字母数字
    m_v = re.search(r"客车\s+([A-Z0-9]{17})", pl_text)
    if not m_v: m_v = re.search(r"识别代码[（(]车架号[)）]\s*\n?\s*([A-Z0-9]{17})", pl_text)
    if not m_v: m_v = re.search(r"车架号\s*\n?\s*([A-Z0-9]{17})", pl_text)
    if not m_v: m_v = re.search(r"识别代码[（(]车架号[)）]\s*([A-Z0-9]{17})", pl_text)
    if m_v: data["车架号"] = m_v.group(1)
    # 兜底: 从全文本搜索有效VIN（17位，含字母+数字）
    if not data.get("车架号"):
        for c in re.findall(r"[A-Z0-9]{17}", pl_text):
            if re.search(r"[A-Z]", c) and re.search(r"[0-9]", c):
                data["车架号"] = c
                break
    data["车辆型号名称"] = ""
    m_m = re.search(r"厂牌型号\s*\n?\s*([^\n]{3,50})", pl_text)
    if m_m: data["车辆型号名称"] = m_m.group(1).strip().replace('\n', '')
    data["车辆使用性质"] = ""
    m_n = re.search(r"使用性质\s*\n?\s*([^\s\n]{2,10})", pl_text)
    if m_n: data["车辆使用性质"] = m_n.group(1)
    data["保险起期"] = ""
    m_per = re.search(r"保险期间自\s*(\d{4}年\d{1,2}月\d{1,2}日[^至]*?)\s*至\s*(\d{4}年\d{1,2}月\d{1,2}日[^止]*?)\s*止", pl_text)
    if m_per: data["保险起期"] = m_per.group(1).strip() + " 至 " + m_per.group(2).strip()
    data["实收保费"] = ""
    m_pr = re.search(r"[￥¥][：:\s]*(\d[\d,]*\.?\d{2})\s*元", pl_text)
    if m_pr: data["实收保费"] = m_pr.group(1)
    # 车船税
    data["车船税"] = ""
    m_tax = re.search(r"当年应缴\s*[￥¥]?\s*[：:]*\s*(\d+\.?\d*)\s*元", pl_text)
    if m_tax and float(m_tax.group(1).replace(',', '')) > 0:
        data["车船税"] = m_tax.group(1)
    else:
        for tbl in tables:
            for row in tbl:
                row_str = " ".join(str(c) for c in row if c)
                if "当年应缴" in row_str:
                    m_t = re.search(r"[￥¥][：:\s]*(\d+\.?\d*)\s*元?", row_str)
                    if m_t and float(m_t.group(1).replace(',', '')) > 0:
                        data["车船税"] = m_t.group(1)
                        break
            if data["车船税"]: break
    # 兜底: 如果车架号仍为空，从pymupdf_text搜索
    if not data.get("车架号") and pymupdf_text:
        for c in re.findall(r"[A-Z0-9]{17}", pymupdf_text):
            if re.search(r"[A-Z]", c) and re.search(r"[0-9]", c):
                data["车架号"] = c
                break
    return data

def parse_zhongmei_jiacheng(text, pdf_path=None):
    """中煤财产保险 意外险/驾乘险。使用pdfplumber文本（pymupdf标签和值分行导致正则失效）。"""
    data = {}
    data["保险公司名称"] = "中煤财产保险股份有限公司"
    data["险种名称原始"] = "机动车辆驾乘人员意外伤害保险"
    
    # 使用pdfplumber文本（pymupdf文本中标签和值分行，正则无法匹配）
    pl_text = text  # 默认用传入的text
    if pdf_path:
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    t = page.extract_text()
                    if t: pl_text += t + "\n"
        except Exception: pass
    
    m = re.search(r"保单号[：:\s]*([A-Z0-9]{10,})", pl_text)
    data["保单号"] = m.group(1) if m else ""
    m = re.search(r"签单日期[：:\s]*(\d{4}-\d{2}-\d{2})", pl_text)
    data["签单时间"] = m.group(1) if m else ""
    data["被保人姓名"] = ""
    m_name = re.search(r"投保险人[：:\s]+([\u4e00-\u9fff]{2,10})", pl_text)
    if not m_name: m_name = re.search(r"投保人[：:\s]+([\u4e00-\u9fff]{2,10})", pl_text)
    if not m_name: m_name = re.search(r"被保险人[：:\s]+([\u4e00-\u9fff]{2,10})", pl_text)
    if m_name and m_name.group(1) not in ("地址", "电话", "证件", "号码", "类型"):
        data["被保人姓名"] = m_name.group(1).strip()
    m = re.search(r"(\d{17}[\dXx])", pl_text)
    data["被保险人证件号"] = m.group(1) if m else ""
    data["被保险人手机号"] = ""
    m_ph = re.search(r"电话号码[：:\s]*(\d{11})", pl_text)
    if not m_ph: m_ph = re.search(r"联系电话[：:\s]*(\d{11})", pl_text)
    if not m_ph: m_ph = re.search(r"(1[3-9]\d{9})", pl_text)
    if m_ph: data["被保险人手机号"] = m_ph.group(1)
    data["车牌号码"] = ""
    m_p = re.search(r"车牌号[：:\s]*(鲁[A-Z]\-?[A-Z0-9]{4,5})", pl_text)
    if not m_p: m_p = re.search(r"(鲁[A-Z]\-?[A-Z0-9]{4,5})", pl_text)
    if m_p: data["车牌号码"] = m_p.group(1)
    data["车架号"] = ""
    m_v = re.search(r"车架号[：:\s]*([A-Z0-9]{17})", pl_text)
    if m_v: data["车架号"] = m_v.group(1)
    data["车辆型号名称"] = ""
    m_m = re.search(r"厂牌型号[：:\s]*([^\n]{3,50})", pl_text)
    if m_m: data["车辆型号名称"] = m_m.group(1).strip()
    data["车辆使用性质"] = ""
    m_n = re.search(r"车辆性质[：:\s]*([^\s\n]{2,10})", pl_text)
    if not m_n: m_n = re.search(r"使用性质[：:\s]*([^\s\n]{2,10})", pl_text)
    if m_n: data["车辆使用性质"] = m_n.group(1)
    data["保险起期"] = ""
    # 中煤意外险格式: "自2026-04-08 23:00:00起,至2027-04-08 23:00:00止" (逗号后无空格)
    m_p = re.search(r"自\s*(\d{4}-\d{2}-\d{2})\s+(\d{2}):(\d{2}):(\d{2})起[,，]*至\s*(\d{4}-\d{2}-\d{2})\s+(\d{2}):(\d{2}):(\d{2})止", pl_text)
    if m_p:
        # group(1)=start_date, (2)=start_h, (3)=start_m, (4)=start_s
        # group(5)=end_date, (6)=end_h, (7)=end_m, (8)=end_s
        start_d = m_p.group(1)
        end_d = m_p.group(5)
        data["保险起期"] = f"{start_d[0:4]}年{int(start_d[5:7]):02d}月{int(start_d[8:10]):02d}日{m_p.group(2)}时{m_p.group(3)}分 至 {end_d[0:4]}年{int(end_d[5:7]):02d}月{int(end_d[8:10]):02d}日{m_p.group(6)}时{m_p.group(7)}分"
    else:
        m_p = re.search(r"自\s*(\d{4}-\d{2}-\d{2})\s+(\d{2}):(\d{2})起至\s*(\d{4}-\d{2}-\d{2})\s+(\d{2}):(\d{2})止", pl_text)
        if m_p:
            start_d = m_p.group(1)
            end_d = m_p.group(4)
            data["保险起期"] = f"{start_d[0:4]}年{int(start_d[5:7]):02d}月{int(start_d[8:10]):02d}日{m_p.group(2)}时{m_p.group(3)}分 至 {end_d[0:4]}年{int(end_d[5:7]):02d}月{int(end_d[8:10]):02d}日{m_p.group(5)}时{m_p.group(6)}分"
    data["实收保费"] = ""
    m_pr = re.search(r"保险费合计[：:\s]*[^\d]*(\d+)\s*元", pl_text)
    if not m_pr: m_pr = re.search(r"[￥Y][：:\s]*(\d[\d,]*\.?\d*)\s*元", pl_text)
    if m_pr: data["实收保费"] = m_pr.group(1)
    data["车船税"] = ""
    return data
def clean_data(data, text, pdf_path=None):
    """数据清洗主函数：调用各子清洗函数。"""
    data["保险公司名称"] = _clean_company_name(data.get("保险公司名称", ""), text)
    data["车牌号码"] = _clean_plate(data.get("车牌号码", ""), text)
    data["车辆使用性质"] = _clean_nature(data.get("车辆使用性质", ""), text, pdf_path)
    data["车架号"] = _validate_vin(data.get("车架号", ""), text)
    data["车辆型号名称"] = _clean_model(data.get("车辆型号名称", ""), data.get("车架号", ""))
    return data

def _clean_company_name(c, text):
    """保险公司名称标准化：截断垃圾内容、全文搜索兜底、去掉支公司后缀。"""
    bad_company_prefixes = (
        "公司地址", "邮政编码", "服务电话", "签单日期", "保单号",
        "公司名称", "公司", "投保人名称", "被保险人名称",
        "投保人", "被保险人", "联系电话", "行驶证地址", "尊敬的客户",
        "根据",
    )
    needs_fix = c.startswith(bad_company_prefixes) or not c or len(c) < 4
    has_junk = bool(re.search(r"[0-9]{5,}", c))
    if needs_fix or has_junk:
        newline_pos = c.find("\n")
        space_digit_pos = None
        for m in re.finditer(r"\s\d", c):
            space_digit_pos = m.start()
            break
        field_stop_words = ["公司地址", "营业执照", "邮政编码", "服务热线", "投诉热线",
                           "全国统一", "全国服务", "网址", "电子邮件", "注册地址"]
        field_pos = len(c)
        for w in field_stop_words:
            idx = c.find(w)
            if 0 <= idx < field_pos:
                field_pos = idx
        stop_pos = len(c)
        if newline_pos > 0:
            stop_pos = newline_pos
        else:
            if space_digit_pos is not None:
                stop_pos = space_digit_pos
            else:
                digit_match = re.search(r"\s*([0-9]{5,})", c)
                if digit_match and digit_match.start() > 2:
                    stop_pos = digit_match.end()
                elif field_pos < stop_pos:
                    stop_pos = field_pos
        c = c[:stop_pos] if stop_pos > 0 else c
        if c.startswith(bad_company_prefixes) or not c or len(c) < 4:
            c = ""
    # 公司名含多余内容时截断到公司名结尾
    if c and ("有限公司" in c or "股份有限公" in c):
        m_co = re.search(r'([\u4e00-\u9fff]{2,20}(?:股份有限公司|股份有限公|有限公司))', c)
        if m_co:
            c = m_co.group(1)
            if c.endswith("股份有限公"):
                c += "司"
    # 全文搜索兜底
    if not c or c.startswith(bad_company_prefixes) or len(c) < 4:
        for keyword, full_name in [
            ("浙商财产保险", "浙商财产保险股份有限公司"),
            ("太平洋财产保险", "中国太平洋财产保险股份有限公司"),
            ("中国人民财产保险", "中国人民财产保险股份有限公司"),
            ("亚太财产保险", "亚太财产保险有限公司"),
            ("大地财产保险", "中国大地财产保险股份有限公司"),
            ("华海", "华海财产保险股份有限公司"),
            ("平安财产保险", "中国平安财产保险股份有限公司"),
            ("阳光财产保险", "阳光财产保险股份有限公司"),
        ]:
            if keyword in text:
                c = full_name
                break
    # 去掉支公司/分公司后缀
    if c:
        suffixes = ["中心支公司", "支公司", "分公司"]
        for suffix in suffixes:
            if c.endswith(suffix):
                c = c[:-len(suffix)].rstrip()
                break
        if "公司" in c and not any(suffix in c for suffix in ["中心支公司", "支公司", "分公司"]):
            last_co_idx = c.rfind("公司")
            if last_co_idx > 5:
                c = c[:last_co_idx + 2].rstrip()
    return c

def _clean_plate(plate, text):
    """车牌清洗：过滤明显不是车牌的值，兜底从全文提取。"""
    bad_plates = {"发动机号", "核定载质量", "使用性质", "车架号",
                  "号牌号码", "保险期间", "VIN码"}
    if plate in bad_plates:
        m = re.search(rf"([{PROVINCES}][A-Z0-9]{{5,8}})", text)
        return m.group(1) if m else ""
    return plate

def _clean_nature(nature, text, pdf_path=None):
    """使用性质清洗：验证白名单，兜底从pymupdf/表格提取。"""
    valid_natures = set(NATURE_LIST)
    if nature not in valid_natures:
        m = re.search(rf"使用性质[：:\s]+({NATURE_PATTERN})", text)
        if m:
            nature = m.group(1)
        else:
            m2 = re.search(r"(非营运|非营业|营业|家庭自用)", text)
            nature = m2.group(1) if m2 else ""
    # 平安/乱码PDF兜底
    if not nature and pdf_path:
        try:
            with pymupdf.open(pdf_path) as doc:
                for page in doc:
                    t = page.get_text()
                    if t:
                        m = re.search(r"使用性质[：:\s]*(非营业|非营运|营业|家庭自用)", t)
                        if m:
                            nature = m.group(1)
                            break
        except Exception:
            pass
    # PDAA/PDZA 表格兜底
    if not nature and pdf_path:
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    tables = page.extract_tables()
                    for table in tables:
                        for row in table:
                            for cell in row:
                                if cell and ("企业非营业客车" in str(cell) or "企业非营业货车" in str(cell)):
                                    nature = str(cell).strip()
                                    break
        except Exception:
            pass
    return nature

def _validate_vin(vin, text):
    """VIN 二次校验 + 全文兜底搜索。"""
    if vin and not is_valid_vin(vin):
        candidates = re.findall(r"\b([A-HJ-NP-Z0-9]{17})\b", text)
        if candidates:
            vin = candidates[0]
        else:
            vin = ""
    return vin

def _clean_model(model, vin):
    """车辆型号清理：VIN查表兜底 + 去尾部垃圾字段。"""
    # VIN→车辆型号兜底
    if not model.strip() and vin and len(vin) == 17:
        for v, m in VIN_MODEL_LOOKUP.items():
            if vin.upper() == v.upper():
                model = m
                break
    # 去掉尾部垃圾
    if model:
        model = re.sub(r'\s*核\s*定\s*载\s*客.*$', '', model)
        model = re.sub(r'\s*核\s*定\s*载\s*质\s*量.*$', '', model)
        model = re.sub(r'\s*绝对免赔额.*$', '', model)
        model = model.strip()
    return model

def _parse_liberty_jq(text, pdf_path=None):
    """解析利宝交强险部分（第1页内容）"""
    data = {}
    
    # 1. 保险公司名称
    data["保险公司名称"] = "利宝保险有限公司"
    
    # 2. 险种名称原始
    data["险种名称原始"] = "机动车交通事故责任强制保险单"
    
    # 3. 保单号
    # 格式：保险单号：8805083706260003460000
    m = re.search(r"保险单号[：:\s]*(\d{16,})", text)
    data["保单号"] = m.group(1) if m else ""
    
    # 4. 签单时间
    # 格式：缴费确认时间：2026-04-17 15:02:27 / 保单生成时间：2026-04-17 15:02:27
    m = re.search(r"缴费确认时间[：:\s]*(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})", text)
    if not m:
        m = re.search(r"保单生成时间[：:\s]*(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})", text)
    if not m:
        m = re.search(r"录单日期[：:\s]*(\d{4}年\d{2}月\d{2}日)", text)
        if m:
            data["签单时间"] = re.sub(r'年|月|日', lambda x: '-', m.group(1)).rstrip('-')
    else:
        data["签单时间"] = m.group(1) if m else ""
    
    # 5. 保险起期
    # 格式：保险期限：2026年04月18日0时0分起至2027年04月18日0时0分止
    # 注意PDF中可能有乱码字符（如 "2026年04S月18日0时0分起至2027年04月A18日0时0分止"）
    m = re.search(
        r"保险期限[：:\s]*(\d{4})年(\d{1,2})[A-Za-z]*月(\d{1,2})日(\d{1,2})时(\d{1,2})分"
        r"起至"
        r"(\d{4})年(\d{1,2})[A-Za-z]*月(\d{1,2})日(\d{1,2})时(\d{1,2})分",
        text
    )
    if m:
        start = f"{m.group(1)}年{int(m.group(2)):02d}月{int(m.group(3)):02d}日{m.group(4)}时{m.group(5)}分"
        end = f"{m.group(6)}年{int(m.group(7)):02d}月{int(m.group(8)):02d}日{m.group(9)}时{m.group(10)}分"
        data["保险起期"] = start + " 至 " + end
    else:
        # 兜底格式
        m = re.search(r"保险期限[：:\s]*(\d{4}年\d{1,2}月\d{1,2}日[^至]*?)起至(\d{4}年\d{1,2}月\d{1,2}日[^止]*?)止", text)
        if m:
            data["保险起期"] = m.group(1).strip() + " 至 " + m.group(2).strip()
    
    # 6. 被保人姓名
    # 格式：被保险人 王有建
    m = re.search(r"被保险人\s+([^\n]{2,10})", text)
    if m:
        data["被保人姓名"] = m.group(1).strip()
    else:
        data["被保人姓名"] = safe_extract(text, [
            r"被保险人[：:\s]*([^\s\n]{2,10})",
        ])
    
    # 7. 被保险人证件号
    # 格式：被保险人身份证号码(统一社会信用代码) 371082197809304916
    m = re.search(r"身份证号码[（(].*?[）)]?\s*([0-9Xx]{15,18})", text)
    if m:
        data["被保险人证件号"] = m.group(1)
    else:
        data["被保险人证件号"] = safe_extract(text, [
            r"身份证号码[（(]?.*?[）)]?[：:\s]*([0-9Xx]{15,18})",
            r"证件号码[：:\s]*([0-9Xx]{15,18})",
        ])
    
    # 8. 被保险人手机号
    data["被保险人手机号"] = safe_extract(text, [
        r"联系电话\s*(1[3-9][\d*]{8,12})",
    ])
    if not data["被保险人手机号"]:
        data["被保险人手机号"] = safe_extract_phone(text)
    
    # 9. 车牌号码
    # 格式：号牌号码 鲁F7E975
    data["车牌号码"] = safe_extract(text, [
        r"号牌号码\s*(鲁[A-Z0-9\-]{5,7})",
        r"车牌[：:\s]*([A-Z][A-Z0-9\-]{4,8})",
    ])
    if not data["车牌号码"]:
        m = re.search(r"(鲁[A-Z][A-Z0-9]{4,6})", text)
        if m:
            data["车牌号码"] = m.group(1)
    
    # 10. 车架号
    # 格式：识别代码(车架号) L6T7622S0AN013957 或 识别代码（车架号）
    data["车架号"] = extract_vin_strict(text, [
        r"识别代码[（(（]车架号[）)）]?\s*([A-Z0-9]{17})",
        r"车架号[：:\s]*([A-Z0-9]{17})",
        r"识别代码[（(（]车架号[）)）]?\s*\n?\s*([A-Z0-9]{17})",
        r"\b([A-Z0-9]{17})\b",
    ])
    
    # 11. 车辆型号名称
    # 格式：厂牌型号 吉利美日MR7150B4轿车
    data["车辆型号名称"] = safe_extract(text, [
        r"厂牌型号\s*([^\n]{3,40})",
        r"厂牌型号[：:\s]*([^\n]{3,40})",
    ])
    vm = data.get("车辆型号名称", "")
    if any(bad in vm for bad in ["符合", "准驾", "驾驶证", "行驶证"]):
        data["车辆型号名称"] = ""
    
    # 12. 车辆使用性质
    # 格式：使用性质 家庭自用汽车
    data["车辆使用性质"] = safe_extract(text, [
        rf"使用性质\s+({NATURE_PATTERN})",
        rf"使用性质[：:\s]+({NATURE_PATTERN})",
    ])
    
    # 13. 实收保费
    # 格式：保险费合计(人民币大写):陆佰陆拾伍元 （￥：665.00 元）
    data["实收保费"] = safe_extract(text, [
        r"（￥[：:\s]*([0-9,]+\.?\d*)\s*元[）)]",
        r"（¥[：:\s]*([0-9,]+\.?\d*)\s*元[）)]",
        r"￥[：:\s]*([0-9,]+\.?\d*)\s*元",
        r"保险费合计[^元]*?([0-9,]+\.?\d*)",
    ])
    
    # 14. 车船税（交强险有）
    # 格式：代收车船税 / 当年应缴 ￥：360.00 元 / 合计（人民币大写）： 叁佰陆拾元 （￥：360.00 元）
    data["车船税"] = safe_extract(text, [
        r"当年应缴\s*[￥¥][：:\s]*([0-9,]+\.?\d*)\s*元",
        r"车船税.*?￥[：:\s]*([0-9,]+\.?\d*)",
        r"合计[（(]人民币大写[）)][：:][^（]*(￥[：:\s]*([0-9,]+\.?\d*)\s*元)",
    ])
    # 如果上面的匹配没有捕获到group正确，用更精确的模式
    if not data.get("车船税"):
        m = re.search(r"当年应缴\s*[￥¥][：:\s]*([0-9,]+\.?\d*)", text)
        if m:
            data["车船税"] = m.group(1)
        else:
            # 从"代收车船税"区域查找
            m = re.search(r"代收车船税[\s\S]{0,200}?([0-9,]+\.\d{2})", text)
            if m:
                data["车船税"] = m.group(1)
    
    return data

def _parse_liberty_jc(text, pdf_path=None):
    """解析利宝驾乘险部分（第3页内容）"""
    data = {}
    
    # 1. 保险公司名称
    data["保险公司名称"] = "利宝保险有限公司"
    
    # 2. 险种名称原始
    data["险种名称原始"] = "驾乘人员意外伤害保险"
    
    # 3. 保单号
    # 驾乘险保单号以882724开头（不同于交强险的880508）
    # 格式：保险单号 8827243706260002889000
    m = re.search(r"保险单号\s+(\d{16,})", text)
    if m and m.group(1).startswith("882724"):
        data["保单号"] = m.group(1)
    else:
        # 兜底：搜索882724开头的保单号
        m = re.search(r"(882724\d{10,})", text)
        if m:
            data["保单号"] = m.group(1)
        elif m:
            data["保单号"] = m.group(1)
        else:
            # 用 safe_extract_policy_no 获取所有保单号，取第二个（驾乘险）
            data["保单号"] = ""
    
    # 4. 签单时间
    # 格式：缴费时间 2026-04-17 / 出单时间 2026-04-17
    m = re.search(r"缴费时间\s*(\d{4}-\d{2}-\d{2})", text)
    if not m:
        m = re.search(r"出单时间\s*(\d{4}-\d{2}-\d{2})", text)
    if m:
        data["签单时间"] = m.group(1)
    else:
        data["签单时间"] = ""
    
    # 5. 保险起期
    # 格式：保单生效日 2026-04-18 0:00:00 / 保单到期日 2027-04-17 24:00:00
    start_m = re.search(r"保单生效日[：:\s]*(\d{4})-(\d{2})-(\d{2})\s*(\d{1,2}):(\d{2}):(\d{2})", text)
    end_m = re.search(r"保单到期日[：:\s]*(\d{4})-(\d{2})-(\d{2})\s*(\d{1,2}):(\d{2}):(\d{2})", text)
    if start_m and end_m:
        start = f"{start_m.group(1)}年{int(start_m.group(2)):02d}月{int(start_m.group(3)):02d}日{start_m.group(4)}时{start_m.group(5)}分"
        end = f"{end_m.group(1)}年{int(end_m.group(2)):02d}月{int(end_m.group(3)):02d}日{end_m.group(4)}时{end_m.group(5)}分"
        data["保险起期"] = start + " 至 " + end
    else:
        data["保险起期"] = ""
    
    # 6. 被保人姓名
    # 格式：投保人名称 王有建
    data["被保人姓名"] = safe_extract(text, [
        r"投保人名称[：:\s]*([^\s\n]{2,10})",
        r"被保险人[：:\s]*([^\s\n]{2,10})",
    ])
    
    # 7. 被保险人证件号 - 驾乘险无
    data["被保险人证件号"] = ""
    
    # 8. 被保险人手机号 - 驾乘险无
    data["被保险人手机号"] = ""
    
    # 9. 车牌号码
    # 格式：车牌号码 鲁F7E975
    data["车牌号码"] = safe_extract(text, [
        r"车牌号码[：:\s]*([A-Z][A-Z0-9\-]{4,8})",
        r"车牌号[：:\s]*([A-Z][A-Z0-9\-]{4,8})",
    ])
    if not data["车牌号码"]:
        m = re.search(r"(鲁[A-Z][A-Z0-9]{4,6})", text)
        if m:
            data["车牌号码"] = m.group(1)
    
    # 10. 车架号
    # 格式：车架号 L6T7622S0AN013957
    data["车架号"] = extract_vin_strict(text, [
        r"车架号[：:\s]*([A-Z0-9]{17})",
        r"车架号\s+([A-Z0-9]{17})",
        r"车架号码?\s*([A-Z0-9]{17})",
    ])
    # 兜底：如果上面的没匹配到，从全文搜索VIN（驾乘险的车架号字段可能在不同位置）
    if not data.get("车架号"):
        _all_vin = re.findall(r"\b([A-Z0-9]{17})\b", text)
        for _v in _all_vin:
            if is_valid_vin(_v):
                data["车架号"] = _v
                break
    
    # 11. 车辆型号名称
    # 格式：厂牌型号 吉利美日MR7150B4轿车
    data["车辆型号名称"] = safe_extract(text, [
        r"厂牌型号[：:\s]*([^\n]{3,40})",
    ])
    
    # 12. 车辆使用性质
    # 格式：使用性质 非营业
    data["车辆使用性质"] = safe_extract(text, [
        rf"使用性质[：:\s]+({NATURE_PATTERN})",
        rf"使用性质\s+({NATURE_PATTERN})",
    ])
    
    # 13. 实收保费
    # 格式：总保险费 50.00
    data["实收保费"] = safe_extract(text, [
        r"总保险费[：:\s]*([0-9,]+\.?\d*)",
        r"保险费[：:\s]*([0-9,]+\.?\d*)",
    ])
    
    # 14. 车船税（驾乘险无）
    data["车船税"] = ""
    
    return data

# =============================================================================
# 利宝保险主解析函数（返回2条记录：交强险+驾乘险）
# =============================================================================
def parse_liberty(pymupdf_text, plumber_text, pdf_path=None):
    """
    利宝保险专用解析器。
    
    利宝特殊结构：
    - 每个PDF包含2个险种：交强险(第1页) + 驾乘人员意外伤害保险(第3页) + 条款
    - 交强险和驾乘险各有独立保险单号
    - 交强险有车船税，驾乘险没有
    - 需要拆分为2条记录返回
    
    返回: [交强险记录dict, 驾乘险记录dict]
    """
    # 优先使用 plumber_text（利宝的pdfplumber提取正常可读）
    text = plumber_text if plumber_text and len(plumber_text) > len(pymupdf_text) else pymupdf_text
    # 两个文本拼接，确保全覆盖
    full_text = text
    if plumber_text and pymupdf_text and plumber_text != pymupdf_text:
        full_text = plumber_text + "\n" + pymupdf_text
    
    results = []
    
    # 提取交强险部分
    jq_data = _parse_liberty_jq(full_text, pdf_path)
    results.append(clean_data(jq_data, full_text, pdf_path))
    
    # 提取驾乘险部分
    jc_data = _parse_liberty_jc(full_text, pdf_path)
    results.append(clean_data(jc_data, full_text, pdf_path))
    
    return results

def parse_zhongyin(text, company="中银保险有限公司", pdf_path=None):
    """中银保险PDF专用解析器（pdfplumber优先，pymupdf兜底散列字段）"""
    data = {}
    data["保险公司名称"] = company
    # 用pymupdf_text兜底：中银商业险pdfplumber丢数据，pymupdf有完整值
    fallback = text  # run_extract.py的text已经是最佳文本

    # === 保单号 ===
    data["保单号"] = ""
    for pat in [
        r"保险单号[：:]\s*([A-Z0-9]{10,})",
        r"保单号码[：:]\s*([A-Z0-9]{10,})",
    ]:
        m = re.search(pat, text)
        if m:
            data["保单号"] = m.group(1)
            break
    if not data["保单号"]:
        m = re.search(r'(?:^|\n)\s*(305\d{12,})\s*(?:\n|$)', text)
        if m:
            data["保单号"] = m.group(1)

    # === 签单时间 ===
    data["签单时间"] = safe_extract(text, [
        r"签单日期[：:\s]*(\d{4}-\d{2}-\d{2})",
        r"收费确认时间[：:\s]*(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})",
        r"有效保单生成时间[：:\s]*(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})",
    ])

    # === 保险起期 ===
    data["保险起期"] = safe_extract(text, [
        r"保险期间自\s+(\d{4}年\d{1,2}月\d{1,2}日\d{1,2}时\d{1,2}分)\s*起",
        r"保险期间自\s+(\d{4}年\d{1,2}月\d{1,2}日[0-9\s时分]+)\s*起",
    ])

    # === 被保人姓名 ===
    data["被保人姓名"] = safe_extract(text, [
        r"被保险人\s+([^\s\n]{2,10})",
        r"被保险人[：:\s]*([^\s\n]{2,10})",
    ])
    if data["被保人姓名"] and any(bad in data["被保人姓名"] for bad in
            ["证件号码", "身份证号码", "联系电话", "地址", "签单日期", "保险单号"]):
        data["被保人姓名"] = ""
    # 散列格式兜底：找"被保险人"后第一个独立中文名
    if not data["被保人姓名"]:
        lines = fallback.split('\n')
        in_section = False
        for i, line in enumerate(lines):
            s = line.strip()
            if '被保险人' in s and len(s) < 20:
                in_section = True
                continue
            if in_section and s and len(s) >= 2 and len(s) <= 10:
                if any(bad in s for bad in ["证件", "身份", "联系", "地址", "号牌", "住所",
                        "保", "厂牌", "型号", "使用", "性质", "发动机", "核定", "初次",
                        "登记", "金额", "责任", "免赔", "期间", "争议", "公司", "邮编",
                        "签单", "核保", "制单", "经办", "条款", "总则"]):
                    continue
                if s[0].isdigit():
                    continue
                if any(c in s for c in "，。、：；（）()￥¥"):
                    continue
                if re.match(r'^[\u4e00-\u9fff]{2,4}$', s):
                    data["被保人姓名"] = s
                    break

    # === 证件号码 ===
    data["被保险人证件号"] = safe_extract(text, [
        r"身份证号码[^\n]*?([0-9]{17}[0-9X])",
        r"证件号码[：:\s]*([A-Z0-9\*]{10,30})",
        r"被保险人身份证号码[^\n]*?([0-9]{17}[0-9X])",
        r"([0-9]{6}[12][0-9]{2}[01][0-9]{2}[0-3][0-9][0-9X]{2}\*{0,4})",
    ])

    # === 手机号 ===
    data["被保险人手机号"] = safe_extract(text, [
        r"联系电话[：:\s]*(1[3-9][\d\*]{9,14})",
        r"电话[：:\s]*(1[3-9][\d\*]{9,14})",
    ])

    # === 车牌号 ===
    data["车牌号码"] = safe_extract(text, [
        rf"号牌号码[：:\s]*({PLATE_PATTERN})",
        rf"\b([{PROVINCES}][A-Z0-9]{{5,8}})\b",
    ])

    # === 车架号（中银PDF的VIN可能有空格） ===
    vin_raw = safe_extract(text, [
        r"VIN[/／]车架号[：:\s]*([A-HJ-NPR-Z0-9\s]{17,30})",
        r"车架号[：:\s]*([A-HJ-NPR-Z0-9\s]{17,30})",
        r"VIN[码号/]*[：:\s]*([A-HJ-NPR-Z0-9\s]{17,30})",
    ])
    if vin_raw:
        vin_clean = re.sub(r'\s+', '', vin_raw).upper()
        if len(vin_clean) == 17 and is_valid_vin(vin_clean):
            data["车架号"] = vin_clean
        else:
            data["车架号"] = ""
    else:
        data["车架号"] = ""

    # === 厂牌型号 ===
    data["车辆型号名称"] = safe_extract(text, [
        r"厂牌型号[\s]+([^\n]{3,40})",
        r"厂牌型号[：:\s]*([^\n]{3,40})",
    ])

    # === 使用性质 ===
    data["车辆使用性质"] = safe_extract(text, [
        rf"使用性质[\s]+({NATURE_PATTERN})",
        rf"使用性质[：:\s]+({NATURE_PATTERN})",
    ])

    # === 险种名称 ===
    header = text[:1500]
    if "机动车交通事故责任强制保险" in header:
        data["险种名称原始"] = "机动车交通事故责任强制保险"
    elif "机动车商业保险" in header:
        data["险种名称原始"] = "机动车商业保险"
    else:
        data["险种名称原始"] = ""

    # === 保费 ===
    data["实收保费"] = ""
    # 策略0：先清理cid乱码，再提取￥...元片段（中银PDF特有）
    for src in [text, fallback]:
        if not src:
            continue
        cleaned = re.sub(r'\(cid:\d+\)', '', src)
        segments = re.findall(r'[￥¥]（?\s*(.*?)\s*元', cleaned)
        for seg in segments:
            digits = re.sub(r'[^\d.]', '', seg)
            try:
                if float(digits) >= 100:
                    data["实收保费"] = digits
                    break
            except ValueError:
                pass
        if data["实收保费"]:
            break
    # 策略0.5：中文大写金额转数字（中银PDF特有：柒佰陆拾元整->760.00）
    if not data["实收保费"]:
        _cn_digit = {'零':0,'壹':1,'贰':2,'叁':3,'肆':4,'伍':5,'陆':6,'柒':7,'捌':8,'玖':9,
                     '一':1,'二':2,'三':3,'四':4,'五':5,'六':6,'七':7,'八':8,'九':9}
        def _cn_to_num(s):
            total = cur = 0
            for c in s:
                if c in _cn_digit: cur = _cn_digit[c]
                elif c == '拾': total += (cur or 1) * 10; cur = 0
                elif c == '佰': total += cur * 100; cur = 0
                elif c == '仟': total += cur * 1000; cur = 0
                elif c == '万': total = (total + cur) * 10000; cur = 0
                elif c == '元': total += cur; cur = 0
                elif c == '角': total += cur * 0.1; cur = 0
                elif c == '分': total += cur * 0.01; cur = 0
            return round(total, 2)
        for src in [text, fallback]:
            if not src:
                continue
            for line in src.split('\n'):
                m = re.search(r'([零壹贰叁肆伍陆柒捌玖一二三四五六七八九佰拾仟万]+元[整角分]*)', line)
                if m:
                    val = _cn_to_num(m.group(1))
                    if 100 <= val <= 10000:
                        data["实收保费"] = f"{val:.2f}"
                        break
            if data["实收保费"]:
                break
    # 策略1：从文本匹配
    for pat in [
        r"[￥¥][（(]?\s*(\d[\d,]*\.\d{2})\s*[）]?\s*元",
        r"保险费合计[（(][^)]*[）)]\s*[￥¥]?\s*([0-9,]+\.?\d*)",
        r"保险费合计[\s\S]*?[￥¥][：:\s]*([0-9,]+\.?\d*)",
    ]:
        m = re.search(pat, text)
        if m:
            val = m.group(1).replace(',', '')
            try:
                if float(val) >= 100:
                    data["实收保费"] = val
                    break
            except ValueError:
                pass
    # 策略2：pymupdf兜底（中银商业险pdfplumber丢金额）
    if not data["实收保费"] and fallback != text:
        for pat in [
            r"[￥¥][（(]?\s*(\d[\d,]*\.\d{2})\s*[）]?\s*元",
            r"保险费合计[\s\S]*?[￥¥][：:\s]*([0-9,]+\.?\d*)",
        ]:
            m = re.search(pat, fallback)
            if m:
                val = m.group(1).replace(',', '')
                try:
                    if float(val) >= 100:
                        data["实收保费"] = val
                        break
                except ValueError:
                    pass
    # 策略3：散列格式，找"保险费合计"附近独立金额（跳过"当年应缴"行的金额，避免匹配车船税）
    if not data["实收保费"]:
        for src in [text, fallback]:
            if not src:
                continue
            lines = src.split('\n')
            for i, line in enumerate(lines):
                if '保险费合计' in line:
                    for j in range(i, min(len(lines), i + 8)):
                        if '当年应缴' in lines[j] or '车船税' in lines[j]:
                            continue
                        m = re.search(r'[￥¥]?\s*([0-9,]+\.\d{2})', lines[j])
                        if m:
                            val = m.group(1).replace(',', '')
                            try:
                                if float(val) >= 100:
                                    data["实收保费"] = val
                                    break
                            except ValueError:
                                pass
                    if data["实收保费"]:
                        break
    # 策略4：pymupdf散列格式，在"保险费合计"后搜合理范围内的独立金额（排除责任限额/日期）
    if not data["实收保费"] and fallback != text:
        lines = fallback.split('\n')
        start_idx = 0
        for i, line in enumerate(lines):
            if '保险费合计' in line:
                start_idx = i
                break
        for j in range(start_idx, min(len(lines), start_idx + 200)):
            m = re.search(r'\b(\d{3,}\.\d{2})\b', lines[j])
            if m:
                val = m.group(1)
                try:
                    fval = float(val)
                    if 100 <= fval <= 10000 and not re.match(r'^20\d{2}\.\d{2}$', val):
                        data["实收保费"] = val
                        break
                except ValueError:
                    pass

    # === 车船税（仅交强险有） ===
    data["车船税"] = safe_extract(text, [
        r"当年应缴\s*[￥¥]?\s*([0-9,]+\.\d{2})\s*元",
        r"车船税[\s\S]*?[￥¥]?\s*([0-9,]+\.\d{2})",
    ])

    return data

# =============================================================================
# 险种路由
# =============================================================================
def route_company(text):
    """根据PDF内的公司名称字段识别公司，返回：taiping/taipingProperty/taishan/renbao/yatai/dadi/zheshang/pingan/yangguang/liberty"""
    # 先查公司名称字段（精确匹配各公司关键词）
    # 非贪婪+边界 lookahead，防止吞掉后续地址等字段
    m = re.search(r"公司名称[：:]\s*(.{5,30}?)(?=公司地址|营业执照|注册地址|联系电话|地址|$)", text)
    if m:
        name = m.group(1)
        if "太平洋" in name: return "taiping"
        if "中国人民" in name: return "renbao"
        if "亚太财产" in name: return "yatai"
        if "大地财产" in name: return "dadi"
        if "浙商财产" in name: return "zheshang"
        if "平安财产" in name: return "pingan"
        if "阳光财产" in name: return "yangguang"
        if "太平财产" in name: return "taipingProperty"
        if "泰山" in name: return "taishan"
        if "利宝" in name: return "liberty"
        if "中银" in name: return "zhongyin"
    # 利宝保险：用关键词检测
    if "利宝保险" in text:
        return "liberty"
    # 太平财险：文本乱码时用TAIPING英文名或保单号前缀检测
    if "TAIPING" in text or "太平财产" in text:
        # 根据保单号前缀区分交强/商业/驾乘
        return "taipingProperty"
    # 泰山财险：用关键词检测
    if "泰山" in text and ("财产保险" in text or "泰山保险" in text):
        return "taishan"
    if "中银保险" in text:
        return "zhongyin"
    return "unknown"

def route_type(text):
    header = text[:400]
    has_jiao_hdr = "机动车交通事故责任强制保险" in header
    # "机动车辆商业保险保险单"（多"辆"字）是浙商商业险的格式
    has_shang_hdr = ("机动车商业保险保险单" in header) or ("机动车辆商业保险保险单" in header)

    if has_jiao_hdr:
        return "交强险"
    elif has_shang_hdr:
        return "商业险"

    # use early_text (first 2000 chars) to avoid false positives from clause references in body
    early_text = text[:2000]
    has_jiao_full = "机动车交通事故责任强制保险" in early_text
    has_shang_full = ("机动车商业保险保险单" in text) or ("机动车辆商业保险保险单" in text) or ("机动车商业保险示范条款" in early_text) or ("机动车综合商业" in early_text)

    if has_jiao_full and has_shang_full:
        return "需人工判断"
    elif has_jiao_full:
        return "交强险"
    elif has_shang_full:
        return "商业险"
    else:
        # 驾乘险检测
        jiacheng_keywords = ["驾乘", "车上人员", "车主尊享", "驾乘人员团体意外", "驾乘人员团体意外"]
        if any(kw in text for kw in jiacheng_keywords):
            return "驾乘险"
        return "非车险"

# =============================================================================
# 主解析函数
# =============================================================================
def parse_pdf(pdf_path):
    logger.debug("parse_pdf START: %s", os.path.basename(pdf_path))
    data = {}
    data["文件名"] = os.path.basename(pdf_path)
    # ===== Step 1+2: 使用缓存读取 PDF 文本（避免重复打开） =====
    cached = _cache_pdf_text(pdf_path)
    pymupdf_text = cached["pymupdf"]
    plumber_text = cached["plumber"]

    # ===== Step 3a: 利宝保险PDF → 交强险+驾乘险合并PDF，拆分为两行 =====
    if "利宝保险" in (pymupdf_text + plumber_text):
        results = parse_liberty(pymupdf_text, plumber_text, pdf_path)
        return results  # Returns list of 2 dicts

    # ===== Step 3: 浙商PDF → 直接走pdfplumber+关键词映射，不依赖pymupdf公司名 =====
    if "浙商财产保险" in plumber_text:
        rt = route_type(plumber_text)
        table_data = safe_extract_tables(pdf_path) if pdf_path else {}
        # 从pymupdf_text提取签单时间（浙商PDF的pymupdf blocks含正确日期如"2026-03-30 09:42:12"）
        sign_date_from_pymupdf = ""
        if pymupdf_text:
            tsm = re.search(r'(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})', pymupdf_text)
            if tsm:
                sign_date_from_pymupdf = tsm.group(1)
        if rt in ("交强险", "需人工判断"):
            data = parse_jiaoqiang(plumber_text, "浙商财产保险股份有限公司烟台市牟平支公司", pdf_path)
            if sign_date_from_pymupdf and not data.get("签单时间"):
                data["签单时间"] = sign_date_from_pymupdf
        elif rt == "商业险":
            data = parse_shangye(plumber_text, "浙商财产保险股份有限公司烟台市牟平支公司", pdf_path)
            if sign_date_from_pymupdf and not data.get("签单时间"):
                data["签单时间"] = sign_date_from_pymupdf
        else:
            data = parse_changxing(plumber_text, pdf_path)
            if sign_date_from_pymupdf and not data.get("签单时间"):
                data["签单时间"] = sign_date_from_pymupdf
        # 表格兜底：被保险人/证件号/手机/车牌/VIN/使用性质/保费/车船税/保险起期
        if table_data:
            if not data.get("被保人姓名") or data.get("被保人姓名") in ("", "需核实"):
                if table_data.get("insured_name"):
                    data["被保人姓名"] = table_data["insured_name"]
            if not data.get("被保险人证件号"):
                if table_data.get("id_card"):
                    data["被保险人证件号"] = table_data["id_card"]
            if not data.get("被保险人手机号"):
                if table_data.get("phone"):
                    data["被保险人手机号"] = table_data["phone"]
            if not data.get("车牌号码"):
                if table_data.get("plate"):
                    data["车牌号码"] = table_data["plate"]
            if not data.get("车架号"):
                if table_data.get("vin"):
                    data["车架号"] = table_data["vin"]
            if not data.get("车辆使用性质"):
                if table_data.get("use_nature"):
                    data["车辆使用性质"] = table_data["use_nature"]
            if not data.get("实收保费") or float((data.get("实收保费", "0") or "0").replace(',', '')) < 100:
                if table_data.get("premium"):
                    data["实收保费"] = table_data["premium"]
            if not data.get("车船税"):
                if table_data.get("tax"):
                    data["车船税"] = table_data["tax"]
            # 保险起期：优先用table_data（含CID中文格式），覆盖garbled结果
            # 关键：如果table_data是garbled值（month=4对于应该=5的情况），跳过table_data
            _tbl_period = table_data.get("period", "")
            _tbl_month_m = re.search(r'(\d{4})年(\d{1,2})月', _tbl_period) if _tbl_period else None
            _tbl_month = int(_tbl_month_m.group(2)) if _tbl_month_m else 0
            _cur_month_m = re.search(r'(\d{4})年(\d{1,2})月', data.get("保险起期", "")) if data.get("保险起期") else None
            _cur_month = int(_cur_month_m.group(2)) if _cur_month_m else 0
            # 如果tbl period存在且月份为4但当前值（parse_jiaoqiang已修正）为5，则跳过tbl覆盖
            if _tbl_period and _tbl_month == 4 and _cur_month == 5:
                pass  # 保持parse_jiaoqiang的修正值
            elif _tbl_period and chr(0x4FDD) not in _tbl_period:
                data["保险起期"] = _tbl_period
        return clean_data(data, plumber_text, pdf_path)

    # ===== Step 4 - PEBS商业险优先检测 =====
    if "PEBS" in (pymupdf_text + plumber_text):
        # Strip UTF-16 LE BOM from plumber_text (corrupts Chinese chars)
        if plumber_text.startswith('\xff\xfe') or plumber_text.startswith('\ufeff'):
            try:
                bom_stripped = plumber_text.encode('utf-16', errors='replace').decode('utf-16-le', errors='replace').encode('utf-8', errors='replace').decode('utf-8', errors='replace')
                if bom_stripped and len(bom_stripped) > 10:
                    plumber_text = bom_stripped
            except Exception:
                pass
        _co = ""
        for kw, full_name in [
            ("太平洋", "中国太平洋财产保险股份有限公司"),
            ("中国人民", "中国人民财产保险股份有限公司"),
            ("亚太财产", "亚太财产保险有限公司"),
        ]:
            if kw in plumber_text:
                _co = full_name
                break
        # 使用 pymupdf_text（正确提取中文），不用 plumber_text（有编码问题）
        return clean_data(parse_shangye(pymupdf_text, _co or "中国太平洋财产保险股份有限公司", pdf_path), pymupdf_text, pdf_path)

    # ===== Step 4b: 华海 PDF 前置检测（优先于 route_company，防止误识） =====
    if "华海" in pymupdf_text or "华海" in plumber_text:
        rt = route_type(pymupdf_text if pymupdf_text else plumber_text)
        huanghai_company = "华海财产保险股份有限公司"
        # 华海PDF: pymupdf 经常只读第一页就停止，第二页的保费数据读不到。
        # pymupdf_text 可能含有 ¥ 但金额数字被截断（如 "¥           元）"）。
        # 判断依据：pymupdf 里金额数字（4 3 9）是否存在。
        _has_amount = bool(re.search(r"¥\s+[0-9]", pymupdf_text)) if pymupdf_text else False
        text = plumber_text if (not _has_amount and plumber_text) else (pymupdf_text if pymupdf_text else plumber_text)
        if rt in ("交强险", "需人工判断"):
            data = parse_jiaoqiang(text, huanghai_company, pdf_path)
            # 华海交强险：¥符号后数字在CID字体里，用garbled提取。
            # 交强险 = 交强险保费（garbled，skip小于100的干扰项）+ 车船税（garbled + 中文数字兜底）。
            # 不再以 parse_jiaoqiang 返回值作为判断依据，直接尝试garbled。
            total = 0.0
            count = 0
            # 1. 交强险保费garbled
            idx = text.find('保险费合计')
            if idx >= 0:
                segment = text[idx:idx+300]
                for n_digits in [4, 3, 2]:
                    garbled = re.search(
                        r'¥[：:\s]*([0-9](?:\s*[0-9]){' + str(n_digits-1) + r'}\s*[.．]\s*[0-9]\s*[0-9])\s*元[）]?',
                        segment
                    )
                    if garbled:
                        digits = re.sub(r'[^\d]', '', garbled.group(1))
                        if len(digits) >= 5:
                            val = float(digits[:-2] + "." + digits[-2:])
                            if val >= 100:
                                total += val
                                count += 1
                                break
            # 2. 当年应缴（车船税）garbled — 仅记录garbled_tax，不加入total
            idx2 = text.find('当年应缴')
            garbled_tax = None
            if idx2 >= 0:
                seg2 = text[idx2:idx2+300]
                for n_digits in [4, 3, 2]:
                    garbled2 = re.search(
                        r'¥[：:\s]*([0-9](?:\s*[0-9]){' + str(n_digits-1) + r'}\s*[.．]\s*[0-9]\s*[0-9])\s*元[）]?',
                        seg2
                    )
                    if garbled2:
                        digits2 = re.sub(r'[^\d]', '', garbled2.group(1))
                        if len(digits2) >= 5:
                            val2 = float(digits2[:-2] + "." + digits2[-2:])
                            garbled_tax = val2  # 不限范围，记录后break
                            break
            # 3. garbled_tax 强制覆盖车船税（parse_jiaoqiang的值可能是错的）
            if garbled_tax is not None:
                data["车船税"] = f"{garbled_tax:.2f}"
            if count >= 1 and total > 0:
                data["实收保费"] = f"{total:.2f}"
            return clean_data(data, text, pdf_path)
        elif rt == "商业险":
            data = parse_shangye(text, huanghai_company, pdf_path)
            # 华海商业险：¥符号后的数字在CID字体里，文字层读不到。
            # 在"保险费合计"附近找 garbled 区（¥ X X X . X X）并清理提取。
            # 支持2/3/4位整数部分（因为不知道是几百还是几千）
            if not data.get("实收保费") or float((data.get("实收保费", "0") or "0").replace(',', '')) < 100:
                idx = text.find('保险费合计')
                if idx >= 0:
                    segment = text[idx:idx+300]
                    for n_digits in [4, 3, 2]:  # 尝试4/3/2位整数
                        garbled = re.search(
                            r'¥\s*([0-9](?:\s*[0-9]){' + str(n_digits-1) + r'}\s*[.．]\s*[0-9]\s*[0-9])',
                            segment
                        )
                        if garbled:
                            digits = re.sub(r'[^\d]', '', garbled.group(1))
                            if len(digits) >= 5:
                                val = float(digits[:-2] + "." + digits[-2:])
                                if 300 <= val <= 3000:
                                    data["实收保费"] = f"{val:.2f}"
                                    break
                # 兜底：300~3000范围最大数字
                if not data.get("实收保费") or float((data.get("实收保费", "0") or "0").replace(',', '')) < 100:
                    all_nums = re.findall(r"\d+\.\d{2}", text)
                    valid = [float(n) for n in all_nums if 300 <= float(n) <= 3000]
                    if valid:
                        data["实收保费"] = f"{max(valid):.2f}"
            return clean_data(data, text)
        else:
            data = parse_changxing(text, pdf_path)
            # 华海司乘险兜底：被保人姓名从pdfplumber"投保人"字段补全
            _clause_kw = ("驾驶", "合同", "指定", "保险", "期间", "责任", "事故", "赔偿", "义务", "条款", "道路")
            _cur_name = str(data.get("被保人姓名", ""))
            _need_name_fix = (not _cur_name or _cur_name in ("nan", "None") or any(kw in _cur_name for kw in _clause_kw))
            if _need_name_fix and pdf_path and "司乘" in os.path.basename(pdf_path or ""):
                try:
                    import pdfplumber as _pb
                    with _pb.open(pdf_path) as _pdf:
                        for _page in _pdf.pages:
                            _pt = _page.extract_text() or ""
                            _nm = re.search(r"投保人[：:]\s*([\u4e00-\u9fff]{2,4})\b", _pt)
                            if _nm and _nm.group(1) not in ("姓名", "信息"):
                                data["被保人姓名"] = _nm.group(1)
                                break
                except Exception:
                    pass
            return clean_data(data, text, pdf_path)

    # ===== Step 4c: 中银保险 PDF =====
    if "中银保险" in (pymupdf_text + plumber_text):
        rt = route_type(pymupdf_text if pymupdf_text else plumber_text)
        text = plumber_text if plumber_text else pymupdf_text
        company = "中银保险有限公司"
        data = parse_zhongyin(text, company, pdf_path)
        return clean_data(data, text, pdf_path)

    # ===== Step 4: 通用路径：先用pymupdf，失败则fallback到pdfplumber =====
    # 如果pymupdf返回空文本，直接用pdfplumber（pymupdf对这些PDF完全失效）
    if not pymupdf_text and plumber_text:
        text = plumber_text
        company_check2 = ''
        for kw, full_name in [
            ("太平洋", "中国太平洋财产保险股份有限公司"),
            ("中国人民", "中国人民财产保险股份有限公司"),
            ("亚太财产", "亚太财产保险有限公司"),
            ("大地财产", "中国大地财产保险股份有限公司"),
            ("华海", "华海财产保险股份有限公司"),
            ("平安财产", "中国平安财产保险股份有限公司"),
            ("阳光财产", "阳光财产保险股份有限公司"),
        ]:
            if kw in plumber_text:
                company_check2 = full_name
                break
        rt = route_type(text)
        if rt in ("交强险", "需人工判断"):
            return parse_jiaoqiang(text, company_check2, pdf_path)
        elif rt == "商业险":
            return parse_shangye(text, company_check2, pdf_path)
        elif rt == "驾乘险":
            if re.search(r"\b\d{16,}\b", text) and "RMB" in text:
                return clean_data(parse_pingan_garbled(text, pdf_path), text, pdf_path)
            return clean_data(parse_jiacheng(text, pdf_path), text, pdf_path)
        else:
            return clean_data(parse_changxing(text, pdf_path), text, pdf_path)

    def looks_valid(company_val):
        logger.debug("looks_valid called")
        if not company_val or len(company_val) < 4:
            return False
        bad = ("公司地址", "邮政编码", "服务电话", "签单日期", "保单号", "公司名称", "公司")
        return not company_val.startswith(bad)

    text = pymupdf_text  # 默认用pymupdf
    pymupdf_company = safe_extract(pymupdf_text, [
        r"公司名称[：:]\s+([^\n]{2,30})(?=公司地址|营业执照|注册地址|联系电话|地址|$)",
        r"公司名称[：:]\s+([^\n]{2,40})",
    ])
    if not looks_valid(pymupdf_company) and plumber_text:
        # pymupdf公司名无效，但pdfplumber有内容 → 用pdfplumber并搜索公司关键词
        text = plumber_text
        company_check2 = ''
        for kw, full_name in [
            ("太平洋", "中国太平洋财产保险股份有限公司"),
            ("中国人民", "中国人民财产保险股份有限公司"),
            ("亚太财产", "亚太财产保险有限公司"),
            ("大地财产", "中国大地财产保险股份有限公司"),
            ("华海", "华海财产保险股份有限公司"),
            ("平安财产", "中国平安财产保险股份有限公司"),
            ("阳光财产", "阳光财产保险股份有限公司"),
        ]:
            if kw in plumber_text:
                company_check2 = full_name
                break
        # 大地安行如意保最优先检测（防止被商业险/非车险路由截断）
        if ("大地财产" in text and ("安行如意保" in text or "团体意外险" in text)) or \
           (re.search(r"63706700\d{10,}", text) and "驾乘" in text and "中煤财产" not in text) or \
           (re.search(r"237067006B\d{10,}", text) and "中煤财产" not in text):
            return clean_data(parse_dadi_anyang(pymupdf_text, plumber_text), text, pdf_path)
        # 太平财险检测（CID字体，用TAIPING英文名或保单号前缀检测）
        if "TAIPING" in text or "太平财产" in text:
            policy_m = re.search(r'((?:P\d+|66707080\d+)\d*)', text)
            if policy_m and policy_m.group(1).startswith('P'):
                return clean_data(parse_taiping_jiacheng(text, pdf_path), text, pdf_path)
            else:
                return clean_data(parse_taipingProperty(text, pdf_path), text, pdf_path)
        # 泰山财险检测
        if "泰山" in text and ("财产保险" in text or "泰山保险" in text):
            if "驾乘人员意外险" in text or "非车险" in os.path.basename(pdf_path):
                return clean_data(parse_taishan_jiacheng(text, pdf_path), text, pdf_path)
            else:
                return clean_data(parse_taishan(text, pdf_path), text, pdf_path)
        # 安华农业保险检测
        if "安华农业" in text or "AHIC" in text or "95540" in text:
            fname = os.path.basename(pdf_path)
            if "EDY" in fname or "EDV" in fname or "驾乘" in text:
                return clean_data(parse_anhua_jiacheng(text, pdf_path), text, pdf_path)
            else:
                return clean_data(parse_anhua(pymupdf_text, pdf_path), text, pdf_path)
        # 中煤财产保险检测
        if "中煤财产" in text or "4006536888" in text:
            fname = os.path.basename(pdf_path)
            if "意外险" in fname or "驾乘" in text or "意外伤害" in text:
                return clean_data(parse_zhongmei_jiacheng(text, pdf_path), text, pdf_path)
            else:
                return clean_data(parse_zhongmei(pymupdf_text, pdf_path), text, pdf_path)
        # 太平洋畅行保优先检测（防止被非车险通用路由截断）
        if "太平洋" in text and "畅行保" in text:
            return clean_data(parse_taiping_changxing(text, pdf_path), text, pdf_path)
        # 平安交强险优先检测（CID字体中文全乱码，需要独立解析）
        if "平安财产" in text or "PAIC" in text or "pingan" in text.lower():
            if route_type(text) in ("交强险", "需人工判断"):
                return clean_data(parse_pingan_jiaoqiang(text, pdf_path), text, pdf_path)
        rt = route_type(text)
        if rt in ("交强险", "需人工判断"):
            data = parse_jiaoqiang(text, company_check2, pdf_path)
        elif rt == "商业险":
            data = parse_shangye(text, company_check2, pdf_path)
        elif rt == "驾乘险":
            # 乱码检测：policy no 格式（16+字符，含Z或纯数字）+ "RMB" → 走 parse_pingan_garbled
            if re.search(r"\b[0-9Z]{16,}\b", text) and "RMB" in text:
                data = parse_pingan_garbled(text, pdf_path)
            else:
                data = parse_jiacheng(text, pdf_path)
        else:
            data = parse_changxing(text, pdf_path)
        # VIN 兜底：plumber 分支中 parse_jiacheng 可能匹配不到全角冒号格式
        if not data.get("车架号") and pymupdf_text:
            vin_fb = extract_vin_strict(pymupdf_text, [
                r"车架号[码]?\s*[：:]\s*([A-Z0-9]{17})",
                r"车架号[码]?\s*\n\s*[：:]\s*([A-Z0-9]{17})",
                r"\b([A-Z0-9]{17})\b",
            ])
            if vin_fb:
                data["车架号"] = vin_fb
        return clean_data(data, text, pdf_path)

    if not text:
        return {}

    # 路由判断（正常pymupdf路径）
    company = route_company(text)
    rt = route_type(text)
    logger.debug("ROUTE: company=%s rt=%s text_len=%d TAIPING=%s 大地=%s PAIC=%s",
                 company, rt, len(text), 'TAIPING' in text, '大地' in text, 'PAIC' in text)
    # 太平财险最优先检测（CID字体中文乱码，用TAIPING英文名或保单号前缀检测）
    if "TAIPING" in text or company == "taipingProperty":
        # 根据保单号前缀区分：P开头=驾乘险，667070801=交强险，667070802=商业险
        policy_m = re.search(r'((?:P\d+|66707080\d+)\d*)', text)
        if policy_m and policy_m.group(1).startswith('P'):
            data = parse_taiping_jiacheng(text, pdf_path)
        else:
            data = parse_taipingProperty(text, pdf_path)
    # 泰山财险检测
    elif company == "taishan" or ("泰山" in text and ("财产保险" in text or "泰山保险" in text)):
        # 根据保单号或标题区分：驾乘险/非车险 vs 交强/商业
        if "驾乘人员意外险" in text or "非车险" in os.path.basename(pdf_path):
            data = parse_taishan_jiacheng(text, pdf_path)
        else:
            data = parse_taishan(text, pdf_path)
    # 大地安行如意保最优先检测（防止被商业险/非车险路由截断）
    # CID字体导致"大地""安行如意保"乱码，用保单号前缀兜底检测
    elif ("大地财产" in text and ("安行如意保" in text or "团体意外险" in text)) or \
         (re.search(r"63706700\d{10,}", text) and rt == "驾乘险") or \
         (re.search(r"237067006B\d{10,}", text) and "中煤财产" not in text):
        data = parse_dadi_anyang(pymupdf_text, plumber_text)
    # 太平洋畅行保优先检测
    elif "太平洋" in text and "畅行保" in text:
        data = parse_taiping_changxing(text, pdf_path)
    # 安华农业保险检测（pymupdf路径，CID字体导致标签/值分离）
    elif "安华农业" in text or "AHIC" in text or "95540" in text:
        fname = os.path.basename(pdf_path)
        if "EDY" in fname or "EDV" in fname or "驾乘" in text:
            data = parse_anhua_jiacheng(text, pdf_path)
        else:
            data = parse_anhua(pymupdf_text, pdf_path)
    # 平安交强险优先检测（CID字体中文全乱码，用PAIC/RMB检测）
    elif ("PAIC" in text or "RMB" in text) and rt in ("交强险", "需人工判断"):
        data = parse_pingan_jiaoqiang(text, pdf_path)
    elif rt == "商业险":
        data = parse_shangye(text, company, pdf_path)
    elif rt in ("交强险", "需人工判断"):
        logger.debug("JQ called: company=%s text_len=%d", company, len(text))
        data = parse_jiaoqiang(text, company, pdf_path)
        logger.debug("JQ result: policy=%s sign=%s", data.get('保单号',''), data.get('签单时间',''))
    elif rt == "驾乘险":
        # 乱码检测：policy no 格式（16+数字）+ "RMB" → 走 parse_pingan_garbled
        if re.search(r"\b\d{16,}\b", text) and "RMB" in text:
            data = parse_pingan_garbled(text, pdf_path)
        else:
            data = parse_jiacheng(text, pdf_path)
    elif rt == "非车险":
        # 平安车主尊享保障乱码检测：公司含"Ƶ��ƽ��"乱码 + 含Z policy no + RMB
        if ("Ƶ��ƽ��" in text or "pingan" in text.lower()) and re.search(r"\b[0-9Z]{16,20}\b", text) and "RMB" in text:
            data = parse_pingan_garbled(text, pdf_path)
        else:
            data = parse_changxing(text, pdf_path)
    else:
        data = parse_changxing(text, pdf_path)
    # VIN 兜底：如果车架号为空，从 pymupdf_text 提取（pdfplumber CID 字体可能丢失 VIN）
    if not data.get("车架号") and pymupdf_text:
        vin_fallback = extract_vin_strict(pymupdf_text, [
            r"车架号[码]?\s*:\s*([A-Z0-9]{17})",
            r"车架号[码]?\s*\n\s*:\s*([A-Z0-9]{17})",
            r"VIN码[：:\s]*([A-Z0-9]{17})",
            r"识别代码[：:\s]*([A-Z0-9]{17})",
            r"车架号码?\s*\n\s*([A-Z0-9]{17})",
            r"\n([A-Z0-9]{17})\n",
        ])
        if vin_fallback:
            data["车架号"] = vin_fallback
    # DEBUG: 全量兜底 - 如果车架号仍为空，用 is_valid_vin 从 pymupdf_text 搜索
    if not data.get("车架号") and pymupdf_text:
        _all_17 = re.findall(r"\b([A-Z0-9]{17})\b", pymupdf_text)
        for _c in _all_17:
            if is_valid_vin(_c):
                data["车架号"] = _c
                break
    return clean_data(data, text, pdf_path)

# =============================================================================
# 同车合并：同一公司+车牌+车架号，车辆型号互相补全
# =============================================================================
def fill_nature_from_same_car(df):
    """同保险公司+车牌+车架号的记录，车辆使用性质互相补全。"""
    key_cols = ["保险公司名称", "车牌号码", "车架号"]
    valid = df.dropna(subset=key_cols, how="any")
    valid = valid[valid["车辆使用性质"].str.strip() != ""]
    if valid.empty:
        return df
    lookup = {}
    for _, row in valid.iterrows():
        key = (str(row["保险公司名称"]), str(row["车牌号码"]), str(row["车架号"]))
        if key not in lookup:
            lookup[key] = row["车辆使用性质"]
    for idx, row in df.iterrows():
        key = (str(row["保险公司名称"]), str(row["车牌号码"]), str(row["车架号"]))
        nature = str(row["车辆使用性质"]).strip()
        if nature == "" and key in lookup:
            df.at[idx, "车辆使用性质"] = lookup[key]
            print(f"  [同车补全] {row['车牌号码']} -> 车辆使用性质：{lookup[key]}")
    return df

def fill_vehicle_model_from_same_car(df):
    """同保险公司+车牌+车架号的记录，车辆型号互相补全。"""
    key_cols = ["保险公司名称", "车牌号码", "车架号"]
    # 过滤掉空白关键字段的记录（无法参与匹配）
    valid = df.dropna(subset=key_cols, how="any")
    valid = valid[valid["车辆型号名称"].str.strip() != ""]
    if valid.empty:
        return df

    # 构建 lookup: (公司, 车牌, 车架) -> 车辆型号
    lookup = {}
    for _, row in valid.iterrows():
        key = (str(row["保险公司名称"]), str(row["车牌号码"]), str(row["车架号"]))
        if key not in lookup:
            lookup[key] = row["车辆型号名称"]

    # 遍历原df，空白项从lookup补全
    for idx, row in df.iterrows():
        key = (str(row["保险公司名称"]), str(row["车牌号码"]), str(row["车架号"]))
        model = str(row["车辆型号名称"]).strip()
        if model == "" and key in lookup:
            df.at[idx, "车辆型号名称"] = lookup[key]
            print(f"  [同车补全] {row['车牌号码']} -> 车辆型号：{lookup[key]}")

    return df

# =============================================================================
# 被保人姓名黑名单：包含这些关键词的一律视为免责条款文字，不是真实姓名
# =============================================================================
INSURED_NAME_BLACKLIST = frozenset([
    "特定被保险人", "被保险人证件号", "被保险人手机", "未成年人",
    "县级", "公立", "保险人", "不予", "不承", "不含",
    "被保险人人数", "特定", "姓名", "为18周岁", "为保险单载明",
])

def is_valid_insured_name(v):
    """判断被保人姓名是否有效（不是免责条款/乱码）。"""
    if not v or not str(v).strip():
        return False
    s = str(v).strip()
    if len(s) < 2:
        return False
    # 数字开头直接排除（如1800元）
    if s[0].isdigit():
        return False
    # 排除明显无效内容
    bad = ("nan", "None", "null", " ", "　", "/?", "#N/A",
            "特定", "被保险人", "被保人", "姓名", "未成年人",
            "投保人", "免责", "应当", "公立", "县级", "保险人",
            "被保险人证件号", "不予", "不承", "不含", "规定")
    for b in bad:
        if b in s:
            return False
    return True

# 车牌→被保人姓名映射表（已知的确定映射，用于修正错误提取）
PLATE_INSURED_LOOKUP = {}

def fill_insured_name_from_same_car(df):
    """先用已知车牌→姓名表修正，再用同车互补兜底。"""

    def type_priority(ins_name_raw):
        s = str(ins_name_raw).strip().lower()
        if "交强险" in s or "强制" in s:
            return 0
        if "商业险" in s:
            return 1
        return 2

    def _col(name):
        """安全获取列位置，优先用名称，回退用 iloc 索引。"""
        if name in df.columns:
            return name
        # 回退到位置索引（兼容 openpyxl 列名编码问题）
        col_map = {"文件名": 0, "被保人姓名": 8, "车牌号码": 11, "车架号": 6, "险种名称原始": 12}
        idx = col_map.get(name)
        if idx is not None and idx < len(df.columns):
            return df.columns[idx]
        return name

    def get_plate(row):
        """从文件名（列位置0）提取车牌，兼容被openpyxl存为Filename的列名。"""
        fn = str(row.iloc[0])  # 第0列是文件名
        m = re.search(r'([鲁京津沪渝冀豫云辽黑湘皖晋疆藏贵甘青桂琼苏浙蒙鄂][A-HJ-NP-Z0-9]{5,7})', fn)
        if m:
            return m.group(1)
        # 回退到车牌列
        plate_col = _col("车牌号码")
        raw = row.get(plate_col)
        if raw is not None and not isinstance(raw, float):
            plate = str(raw).strip()
            if len(plate) >= 5:
                return plate
        return ""

    filled = 0

    # Step 1: 用车牌 lookup 直接修正（最高优先级）
    name_col = _col("被保人姓名")
    for idx, row in df.iterrows():
        plate = get_plate(row)
        name_val = row.get(name_col)
        current = str(name_val).strip() if name_val is not None and not isinstance(name_val, float) else ""
        fixable = (not is_valid_insured_name(current)) and (plate in PLATE_INSURED_LOOKUP)
        if fixable:
            new_name = PLATE_INSURED_LOOKUP[plate]
            df.at[idx, name_col] = new_name
            print(f"  [被保人姓名修正] idx={idx} {plate} -> {new_name}")
            filled += 1

    # Step 2: 同车互补（车牌+车架相同的记录，有效姓名互相填充）
    vin_col = _col("车架号")
    name_col = _col("被保人姓名")
    type_col = _col("险种名称原始")
    groups = {}
    for idx, row in df.iterrows():
        plate = get_plate(row)
        vin_raw = row.get(vin_col)
        vin = str(vin_raw).strip() if vin_raw and not isinstance(vin_raw, float) else ""
        if not plate or not vin:
            continue
        key = (plate, vin)
        name_raw = row.get(name_col)
        ins = str(name_raw).strip() if name_raw and not isinstance(name_raw, float) else ""
        ins_type_raw = row.get(type_col) if type_col in df.columns else ""
        priority = type_priority(str(ins_type_raw) if ins_type_raw else "")
        if key not in groups:
            groups[key] = []
        groups[key].append((priority, ins, idx))

    for key, candidates in groups.items():
        valid_names = [(p, n) for p, n, _ in candidates if is_valid_insured_name(n)]
        if not valid_names:
            continue
        valid_names.sort(key=lambda x: x[0])
        best_name = valid_names[0][1]
        for _, _, idx in candidates:
            current_raw = df.at[idx, name_col]
            current = str(current_raw).strip() if current_raw and not isinstance(current_raw, float) else ""
            if not is_valid_insured_name(current):
                df.at[idx, name_col] = best_name
                print(f"  [被保人姓名补全] {key[0]} -> {best_name}")
                filled += 1

    if filled:
        print(f"  [被保人姓名] 共修正 {filled} 条")
    return df

# =============================================================================
# 同车证件号/手机号补全：车架号+车牌+保险公司相同 → 组内有值则填空白
# =============================================================================
def fill_id_phone_from_same_car(df):
    """对每个分组，手机号和证件号有值则填充空白。"""
    filled = 0
    key_cols = ["保险公司名称", "车牌号码", "车架号"]
    for idx, row in df.iterrows():
        key = (str(row["保险公司名称"]), str(row["车牌号码"]), str(row["车架号"]))
        mask = (df["保险公司名称"].astype(str) == key[0]) & \
               (df["车牌号码"].astype(str) == key[1]) & \
               (df["车架号"].astype(str) == key[2])
        group = df[mask]
        for field in ["被保险人证件号", "被保险人手机号"]:
            # 收集组内非空值
            vals = [(gidx, str(df.at[gidx, field]).strip())
                    for gidx in group.index
                    if str(df.at[gidx, field]).strip()
                    and str(df.at[gidx, field]).strip() not in ("nan", "None")]
            if not vals:
                continue
            # 优先取非"*"(非脱敏)的真实值
            best = next(((gidx, v) for gidx, v in vals if "*" not in v), vals[0])
            for gidx in group.index:
                cur = str(df.at[gidx, field]).strip()
                if not cur or cur in ("nan", "None", "") or (cur != best[1] and "*" in cur):
                    df.at[gidx, field] = best[1]
                    filled += 1
    if filled:
        print(f"  [证件/电话补全] 填充 {filled} 条")
    return df
# =============================================================================
def fix_by_majority_vote(df):
    """对每个分组，被保人姓名/车辆型号/手机/证件号 以组内出现次数最多的值为准。"""
    fix_count = 0
    for idx, row in df.iterrows():
        key = (str(row["保险公司名称"]), str(row["车牌号码"]), str(row["车架号"]))
        mask = (df["保险公司名称"].astype(str) == key[0]) & \
               (df["车牌号码"].astype(str) == key[1]) & \
               (df["车架号"].astype(str) == key[2])
        group = df[mask]
        for field in ["被保人姓名", "车辆型号名称", "被保险人手机号", "被保险人证件号", "车辆使用性质"]:
            vals = [str(v).strip() for v in group[field]
                    if v and str(v).strip() and str(v).strip() not in ("nan", "None", "")]
            if len(vals) < 2:
                continue
            majority = Counter(vals).most_common(1)[0][0]
            for _, gidx in group.iterrows():
                cur = str(df.at[gidx.name, field]).strip()
                if cur not in ("nan", "None", "") and cur != majority:
                    df.at[gidx.name, field] = majority
                    fix_count += 1
    if fix_count:
        print(f"  [多数纠正] 修复 {fix_count} 条数据")
    return df

if __name__ == "__main__":
    pdfs = sorted(Path(PDF_FOLDER).glob("*.pdf"))
    results = []
    for pdf_path in pdfs:
        print(f"Processing {pdf_path.name}...")
        try:
            data = parse_pdf(str(pdf_path))
        except Exception as e:
            print(f"Error: {e}")
            traceback.print_exc()
            data = {}
        # 利宝保险返回2条记录（交强险+驾乘险）
        if isinstance(data, list):
            for d in data:
                row = {f: d.get(f, "") for f in FIELDS}
                row["Filename"] = pdf_path.name
                results.append(row)
        else:
            row = {f: data.get(f, "") for f in FIELDS}
            row["Filename"] = pdf_path.name
            results.append(row)

    df = pd.DataFrame(results)
    # 同车车辆型号补全
    print("=== 同车型号补全 ===")
    df = fill_vehicle_model_from_same_car(df)
    # 同车车辆使用性质补全
    df = fill_nature_from_same_car(df)
    # 同车被保人姓名补全
    print("=== 同车被保人姓名补全 ===")
    df = fill_insured_name_from_same_car(df)
    # 同车证件号/电话补全
    print("=== 同车证件/电话补全 ===")
    df = fill_id_phone_from_same_car(df)
    # 组内多数纠正（被保人姓名/车辆型号/手机/证件号）
    print("=== 组内多数纠正 ===")
    df = fix_by_majority_vote(df)
    cols = ["Filename"] + FIELDS
    # 如果同时有"险种名称"和"险种名称原始"，去掉"险种名称"，保留"险种名称原始"
    cols_filtered = [c for c in cols if c in df.columns]
    if "险种名称" in cols_filtered and "险种名称原始" in cols_filtered:
        cols_filtered.remove("险种名称")
    df = df[cols_filtered]
    # 保单号强制为字符串，防止Excel科学计数法显示
    if '保单号' in df.columns:
        df['保单号'] = df['保单号'].apply(lambda x: '' if pd.isna(x) or str(x) in ('nan', 'None', '') else str(x))
    # 按保险公司名称↑ + 车牌号码↑ 排序
    df = df.sort_values(by=["保险公司名称", "车牌号码"], ascending=True)
    # 清理非法字符，防止 openpyxl IllegalCharacterError
    _ILLEGAL_RE = __import__('re').compile(r'[\x00-\x08\x0b\x0c\x0e-\x1f]')
    for col in df.columns:
        if df[col].dtype.kind == 'O':
            df[col] = df[col].apply(lambda v: _ILLEGAL_RE.sub('', v) if isinstance(v, str) else v)
    wb = Workbook()
    ws = wb.active
    for r in dataframe_to_rows(df, index=False, header=True):
        ws.append(r)
    wb.save(OUTPUT_FILE)
    print(f"Done! {OUTPUT_FILE}")
    print(f"{len(results)} records, {len(FIELDS)} fields")
