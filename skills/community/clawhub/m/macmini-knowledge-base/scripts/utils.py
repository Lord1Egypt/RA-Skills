#!/usr/bin/env python3
"""
知识库共享工具函数 v2.1
2026-08-12 修复：
- 修复 OCR 路径不工作（--skip-text → --force-ocr）
- 新增 CMap 残缺度自检（is_cmap_broken, 阈值 0.03）
- 新增 PDFExtractError 异常类（含文件路径）
- OCR 超时 60s → 600s（支持大文档）
"""
import os
import sys
import json
import shutil
import subprocess
import re as re_module
import uuid
import tempfile
import pymupdf
import docx
import openpyxl
import pptx

try:
    from kreuzberg import extract_file_sync as kreuzberg_extract
    KREUZBERG_AVAILABLE = True
except Exception:
    KREUZBERG_AVAILABLE = False

_DEFAULT_KNOWLEDGE_DIR = os.path.expanduser("~/.openclaw/workspace/knowledge")
_STATE_FILE    = os.path.join(_DEFAULT_KNOWLEDGE_DIR, ".analysis/analysis_state.json")
_CACHE_FILE    = os.path.join(_DEFAULT_KNOWLEDGE_DIR, ".analysis/.catalog_cache.json")
_PROGRESS_FILE = os.path.join(_DEFAULT_KNOWLEDGE_DIR, ".analysis/.catalog_progress.json")
_SUMMARY_INDEX_FILE = os.path.join(_DEFAULT_KNOWLEDGE_DIR, ".analysis/summary_index.json")

# ==== 状态键 schema ====
# v1: 用 basename 做键 → 不同目录下的同名文件互相顶替，一份被永久静默跳过
# v2: 用相对 knowledge/ 的路径做键 → 唯一标识每个文件
STATE_SCHEMA_VERSION = 2


def rel_key(abs_path, knowledge_dir=None):
    """状态键：文件相对 knowledge/ 的路径。

    v1 用 basename 做键，同名文件（不同目录下）会互相顶替，导致其中一份
    永远不会被分析且无任何告警（实测 104 组 / 106 份）。v2 改用相对路径。
    """
    root = knowledge_dir or _DEFAULT_KNOWLEDGE_DIR
    return os.path.relpath(abs_path, root)

# ==== 异常类 ====
class PDFExtractError(Exception):
    """PDF 提取失败异常（含文件路径）"""
    def __init__(self, filepath, reason):
        self.filepath = filepath
        self.reason = reason
        super().__init__(f"PDF 提取失败: {filepath} - {reason}")


# v2.1: 通用文件提取失败异常
class ExtractError(Exception):
    """通用文件提取失败异常（含文件路径）"""
    def __init__(self, filepath, reason):
        self.filepath = filepath
        self.reason = reason
        super().__init__(f"文件提取失败: {filepath} - {reason}")

# ==== CMap 残缺度检测（C 方案核心）====
CMAP_BAD_RATIO_THRESHOLD = 0.03   # 异常字符比例阈值（用户指定）
CMAP_CID_COUNT_THRESHOLD = 10      # (cid:xxxx) 出现次数阈值
CMAP_SAMPLE_CHARS_MIN = 50         # 文本长度低于此值不做自检（可能是图像PDF）

# v2.2: 文本提取上限（用户要求"完整阅读"，原 [:8000] 太小）
# 50 万字 ≈ 1MB，覆盖 99.9% 正常文档；超大 Excel/Word 也不会无限制膨胀
MAX_EXTRACT_LEN = 500_000

def is_cmap_broken(text, threshold=CMAP_BAD_RATIO_THRESHOLD):
    """检测文本是否含异常字符（CMap残缺/PUA污染/未映射CID字面值）

    Returns:
        bool: True 表示需要走 OCR
    """
    if not text or len(text.strip()) < CMAP_SAMPLE_CHARS_MIN:
        return False

    total = len(text)
    # PUA 私用区 U+E000-F8FF
    pua_count = sum(1 for c in text if 0xE000 <= ord(c) <= 0xF8FF)
    # CJK 扩展 B/C/D
    cjk_ext = sum(1 for c in text if 0x20000 <= ord(c) <= 0x2EBEF)
    # CJK 兼容区 U+F900-FAFF
    cjk_compat = sum(1 for c in text if 0xF900 <= ord(c) <= 0xFAFF)
    # (cid:xxxx) 字面值（pdfplumber 提取失败标志）
    cid_count = text.count('(cid:')

    bad_count = pua_count + cjk_ext + cjk_compat + cid_count
    bad_ratio = bad_count / total

    return bad_ratio > threshold or cid_count > CMAP_CID_COUNT_THRESHOLD



def clean_noise(text):
    """清理 PDF 摘要的噪音（v2.2.2 - span-based disclaimer 删除）

    关键修复：处理 PDF 文本是单行连续流（无换行）的场景
    - 阶段 1: 尝试在句子边界插换行（让 line-based 能工作）
    - 阶段 2: span-based 兜底 - 找 disclaimer 关键词，扩展到段落边界，删除
    """
    if not text:
        return text
    
    import re as _re
    text = _re.sub(r'\r\n?', '\n', text)
    
    # 阶段 1: 在常见段落边界插换行
    if text.count('\n') < 3:
        # 句末 + 大写/中文 → 换行
        text = _re.sub(r'([.!?。！？])\s+(?=[A-Z\u4e00-\u9fff])', r'\1\n', text)
        # 关键词 "Copyright / Disclaimer / Notice / Legal" 前
        text = _re.sub(r'\s+(?=Copyright|Disclaimer|Notice|Legal|This foregoing|This restriction)', r'\n', text, flags=_re.IGNORECASE)
        text = _re.sub(r'(All rights reserved\.?)\s*', r'\1\n', text, flags=_re.IGNORECASE)
        text = _re.sub(r'(Copyright \([Cc]\) \d{4})\s*', r'\1\n', text)
    
    # 阶段 1.5: 行级过滤（处理已有换行的 PDF）
    keywords = [
        'in whole or in part, to train or finetune',
        'to train or finetune a machine learning',
        'to provide or reproduce this information',
        'as a prompt or input to any',
        'This information is confidential',
        'This material is confidential',
        'Information contained herein',
        'The information contained herein',
        'Subject to the terms and conditions',
        'All rights reserved',
        'May not be reproduced',
        'Not for distribution',
        'past performance is not indicative',
        'MUFG shall have no liability',
        'Neither MUFG nor any',
    ]
    
    lines = text.split('\n')
    cleaned_lines = []
    for line in lines:
        if any(kw.lower() in line.lower() for kw in keywords):
            continue
        if _re.match(r'^[=\-\s*~·]{20,}$', line.strip()):
            continue
        if _re.match(r'^\s*(\d+|图\s*\d+|图表\s*\d+)\s*$', line.strip()):
            continue
        cleaned_lines.append(line)
    text = '\n'.join(cleaned_lines)
    
    # 阶段 2: span-based 兜底（处理仍在连续流中的 disclaimer 关键词）
    span_keywords = [
        'in whole or in part',
        'to train or finetune',
        'as a prompt or input to any',
        'to provide or reproduce this information',
        'may not be reproduced',
        'this foregoing restriction',
        'without the express written consent',
        'past performance is not indicative',
        'all rights reserved',
        'subject to the terms and conditions',
    ]
    
    for kw in span_keywords:
        max_iter = 5
        while max_iter > 0:
            max_iter -= 1
            pos = text.lower().find(kw.lower())
            if pos < 0:
                break
            # 向前找最近句末（最多 800 字符）
            window_start = max(0, pos - 800)
            chunk_before = text[window_start:pos]
            # 找最近的 ". " / "! " / "? " 或 "。" / "！" / "？"
            sentence_end = None
            for m2 in _re.finditer(r'[.!?。！？]\s', chunk_before):
                sentence_end = m2.end()
            if sentence_end is not None:
                start = window_start + sentence_end
            else:
                start = max(0, pos - 200)  # 兜底
            # 向后找最近句末（最多 800 字符）
            window_end = min(len(text), pos + len(kw) + 800)
            chunk_after = text[pos + len(kw):window_end]
            sentence_end_after = _re.search(r'[.!?。！？]\s', chunk_after)
            if sentence_end_after:
                end = pos + len(kw) + sentence_end_after.end()
            else:
                end = window_end
            # 删 [start, end)
            text = text[:start] + text[end:].lstrip()
    
    # 阶段 2.5: 专门处理常见 disclaimer 公式
    # 模式: "...liability (in negligence or otherwise, and in whole or in part) for any..."
    # 删整个公式 + 后面到句末的内容
    patterns = [
        # "...liability (in negligence or otherwise, and in whole or in part) for any ..."
        r'[^.]{0,80}liability\s*\(\s*in\s+negligence\s+or\s+otherwise[^)]*?in\s+whole\s+or\s+in\s+part\)\s*for\s+any[^.]{0,500}[.!?]',
        # "...shall have no liability..."
        r'[^.]{0,80}shall\s+have\s+no\s+liability[^.]{0,500}[.!?]',
        # "...may not be duplicated, reproduced, re-disseminated, redistributed..."
        r'may\s+not\s+be\s+duplicated[^.]{0,500}[.!?]',
        # "...without the express written consent of..."
        r'\bwithout\s+the\s+express\s+written\s+consent\s+of[^.]{0,200}[.!?]',
        # "...errors or omissions in the..."
        r'\berrors\s+or\s+omissions\s+in\s+the\b[^.]{0,200}[.!?]',
        # "...viruses..."
        r'\bviruses\.\s*The\s+sender[^.]{0,300}[.!?]',
    ]
    for pat in patterns:
        text = _re.sub(pat, '', text, flags=_re.IGNORECASE | _re.DOTALL)
    
    # 最终清理
    text = _re.sub(r'\n{4,}', '\n\n\n', text)
    text = '\n'.join(l.rstrip() for l in text.split('\n'))
    return text.strip()

def load_json(path=None):
    if path is None:
        path = _STATE_FILE
    if os.path.exists(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return None

def save_json(path, data):
    """把 data 序列化写入 path（JSON / UTF-8 / indent=2）。

    ⚠️ 覆盖语义：目标文件若已存在会被**整体替换** —— 以 'w' 模式打开，
    写入前即截断原内容；不做合并、不保留旧版本、不做备份。
    本函数用于持久化分析状态（analysis_state.json）、目录缓存与进度文件，
    写入的始终是**完整快照**，因此"替换"是预期行为而非意外。

    参数：
        path: 目标文件路径；传 None 时落到默认的 _STATE_FILE
        data: 可 JSON 序列化的对象

    副作用：
        - 自动创建父目录（exist_ok=True）
        - 目标文件权限继承当前 umask；若该文件含敏感内容，
          调用方需自行 chmod 600 或以受限 umask 调用
    """
    if path is None:
        path = _STATE_FILE
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_state():
    data = load_json(_STATE_FILE)
    return data if data else {}

def save_state(state):
    save_json(_STATE_FILE, state)

def load_summary_index():
    """摘要索引：summary 文件名 → 源文件相对路径。

    持久化，不随单次运行覆盖。用于把 archives/ 里的历史摘要回溯到确切源文件
    （否则同名文档的摘要无法消歧）。
    只存文件名不存全路径 → 摘要被 06:00 cron 移到 archives/ 后索引依然有效。
    """
    data = load_json(_SUMMARY_INDEX_FILE)
    return data if data else {}


def save_summary_index(index):
    save_json(_SUMMARY_INDEX_FILE, index)


def load_cache():
    data = load_json(_CACHE_FILE)
    return data if data else {}

def save_cache(cache):
    save_json(_CACHE_FILE, cache)

def load_progress():
    data = load_json(_PROGRESS_FILE)
    return data if data else {}

def save_progress(progress):
    save_json(_PROGRESS_FILE, progress)

def is_gibberish(text, strict=False):
    if not text or len(text.strip()) < 20:
        return True
    alpha_count   = sum(1 for c in text if c.isalpha())
    upper_count   = sum(1 for c in text if c.isupper())
    space_count   = sum(1 for c in text if c.isspace())
    chinese_count = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
    chinese_ratio = chinese_count / len(text) if len(text) > 0 else 0
    if alpha_count > 10:
        upper_ratio = upper_count / alpha_count
        space_ratio = space_count / len(text)
        if upper_ratio > 0.45 and space_ratio < 0.05:
            return True
    if chinese_ratio > 0.3:
        return False
    cleaned = re_module.sub(r'[\s\n]', '', text)
    if len(cleaned) == 0:
        return True
    normal_count = len(re_module.findall(r'[A-Za-z0-9 .,;:\'"!?()-]', cleaned))
    ratio = normal_count / len(cleaned) if len(cleaned) > 0 else 0
    return ratio < (0.5 if strict else 0.3)

def extract_via_kreuzberg(filepath):
    if not KREUZBERG_AVAILABLE:
        return None
    try:
        result = kreuzberg_extract(filepath)
        if result and result.content and result.content.strip():
            return result.content
    except Exception as e:
        import sys
        print(f"  ⚠️  kreuzberg 异常: {filepath}: {type(e).__name__}: {e}", file=sys.stderr)
    return None


def _quick_page_check(filepath):
    """快速预检前3页是否需要走OCR（文字量极少=编码PDF）"""
    try:
        doc = pymupdf.open(filepath)
        total_chars = 0
        for i in range(min(3, len(doc))):
            t = doc[i].get_text()
            total_chars += len(t.strip())
        doc.close()
        if total_chars < 200:
            return True
    except Exception as e:
        import sys
        print(f"  ⚠️  _quick_page_check 异常: {filepath}: {type(e).__name__}: {e}", file=sys.stderr)
    return False

def extract_doc_via_antiword(filepath):
    try:
        result = subprocess.run(['antiword', filepath], capture_output=True, timeout=10)
        if result.returncode == 0:
            text = result.stdout.decode('utf-8', errors='replace')
            if len(text) > 100:
                return clean_noise(text)
    except Exception as e:
        import sys
        print(f"  ⚠️  kreuzberg 异常: {filepath}: {type(e).__name__}: {e}", file=sys.stderr)
    return None

def _kill_proc_tree(pid):
    try:
        # v1.4.3: 替换 os.system 为 subprocess.run（避免 shell 注入 + 抑制输出）
        subprocess.run(["pkill", "-P", str(pid)],
                       capture_output=True, timeout=5)
    except subprocess.TimeoutExpired:
        pass  # pkill 超时属预期，继续走下面的 kill
    except OSError as e:
        print(f"[进程树清理失败] pkill {pid}: {e}", file=sys.stderr)
    try:
        os.kill(pid, 9)
    except ProcessLookupError:
        pass  # 进程已退出，属预期情况
    except OSError as e:
        print(f"[进程清理失败] kill {pid}: {e}", file=sys.stderr)

def convert_old_office(filepath, ext):
    # v1.4.3 fix2: 拆分为内部函数（finally 清理 tmp_dir 前先把结果 cp 到稳定位置）
    tmp_dir = tempfile.mkdtemp(prefix="office_convert_")
    try:
        convert_map = {".doc": "docx", ".xls": "xlsx", ".ppt": "pptx"}
        new_ext = convert_map.get(ext)
        if not new_ext:
            return (False, "")
        expected_name = os.path.basename(filepath).replace(ext, '.' + new_ext)
        tmp_out = os.path.join(tmp_dir, expected_name)
        if os.path.exists(tmp_out):
            try:
                os.remove(tmp_out)
            except OSError as e:
                # 残留的旧转换产物删不掉：记录，避免静默堆积
                print(f"[临时文件清理失败] {tmp_out}: {e}", file=sys.stderr)
        proc = subprocess.Popen(
            ['soffice', '--headless', '--convert-to', new_ext, '--outdir', tmp_dir, filepath],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        try:
            outs, errs = proc.communicate(timeout=60)
            if proc.returncode == 0 and os.path.exists(tmp_out):
                # v1.4.3 fix2: 把结果 cp 到 tmp_dir 外的稳定路径（否则 finally 会删掉）
                # 用 tempfile.mkstemp（更安全，无 race condition）
                stable_fd, stable_out = tempfile.mkstemp(suffix='.' + new_ext)
                os.close(stable_fd)
                shutil.copy2(tmp_out, stable_out)
                return (True, stable_out)
        except subprocess.TimeoutExpired:
            try:
                proc.kill()
            except ProcessLookupError:
                pass  # 进程已退出，属预期情况
            except OSError as e:
                print(f"[进程清理失败] kill: {e}", file=sys.stderr)
            _kill_proc_tree(proc.pid)
        return (False, "")
    finally:
        # v1.4.3: finally 清理私有目录
        shutil.rmtree(tmp_dir, ignore_errors=True)

def extract_doc_text(filepath):
    """提取 .doc 文本（v2.1: 加 OCR fallback）

    流程：
    1. antiword 提取（直接读 .doc 流）
    2. CMap 自检（is_cmap_broken）
    3. 自检失败 → soffice 转 PDF + OCRmyPDF 强制 OCR
    4. 失败 → 抛 ExtractError（含文件路径）
    """
    text = extract_doc_via_antiword(filepath)
    if text and not is_cmap_broken(text):
        return clean_noise(text)

    # 兜底：antiword 提取为空或乱码 → 走 OCR
    success, converted = convert_old_office(filepath, '.doc')
    if success:
        try:
            doc = docx.Document(converted)
            text = "\n".join(p.text for p in doc.paragraphs if p.text.strip())
            if text.strip() and not is_cmap_broken(text):
                return clean_noise(text)[:MAX_EXTRACT_LEN]
        finally:
            try:
                os.remove(converted)
            except OSError as e:
                # 临时文件清理失败：记录以便排查残留（不再静默吞掉）
                print(f"[临时文件清理失败] {converted}: {e}", file=sys.stderr)

    # 最终兜底：OCR
    ocr_text = ocr_office_via_ocr(filepath, '.doc')
    if ocr_text:
        return ocr_text
    raise ExtractError(filepath, ".doc 提取失败：antiword/soffice/OCR 都返回空或乱码")

def extract_pdf_text(filepath):
    """提取 PDF 文本（CMap 残缺度自检 v2.1）

    流程：
    1. _quick_page_check：前 3 页文字量少 → 直接 OCR
    2. kreuzberg 默认提取 + CMap 自检
    3. pymupdf 默认提取 + CMap 自检
    4. 自检失败或提取为空 → OCR（--force-ocr 已修复）
    5. OCR 失败 → 抛 PDFExtractError（含文件路径）
    """
    # 前 3 页文字量少 = 可能是扫描件/图像 PDF
    if _quick_page_check(filepath):
        result = extract_pdf_via_ocr(filepath)
        if result and not result.startswith("【"):
            return clean_noise(result)
        raise PDFExtractError(filepath, "OCR 后仍无文本（可能是扫描件或损坏文件）")

    # kreuzberg 提取 + CMap 自检
    # v2.2.5 修复：主路径漏调 clean_noise → 投行研报 disclaimer 噪音没被清理
    text = extract_via_kreuzberg(filepath)
    if text and not is_cmap_broken(text):
        return clean_noise(text)

    # pymupdf 提取 + CMap 自检
    # v2.2 修复：不再吞掉异常，记录错误原因（用于重试和诊断）
    pymupdf_err = None
    try:
        doc = pymupdf.open(filepath)
        text = ""
        for page_num in range(len(doc)):
            t = doc[page_num].get_text()
            if t.strip():
                text += t + "\n"
        doc.close()
        if text.strip() and not is_cmap_broken(text):
            return clean_noise(text)
    except Exception as e:
        pymupdf_err = f"pymupdf 异常: {type(e).__name__}: {e}"
        import sys; print(f"  ⚠️  {filepath}: {pymupdf_err}", file=sys.stderr)

    # 走到这里：默认提取失败或检测到乱码 → 走 OCR
    result = extract_pdf_via_ocr(filepath)
    if result and not result.startswith("【"):
        return clean_noise(result)
    raise PDFExtractError(filepath, "OCR 失败：所有提取路径都返回空或乱码")

def extract_docx_text(filepath):
    text = extract_via_kreuzberg(filepath)
    if text:
        return clean_noise(text)
    try:
        doc = docx.Document(filepath)
        text = "\n".join(p.text for p in doc.paragraphs if p.text.strip())
        return text[:MAX_EXTRACT_LEN] if text.strip() else "【Word文档无文字内容】"
    except Exception as e:
        return "【DOCX提取失败】" + str(e)

def extract_xlsx_text(filepath):
    text = extract_via_kreuzberg(filepath)
    if text:
        return clean_noise(text)
    try:
        wb = openpyxl.load_workbook(filepath, data_only=True)
        sheets_text = []
        for sheet in wb.worksheets:
            for row in sheet.iter_rows(values_only=True):
                row_text = " ".join(str(c) for c in row if c is not None)
                if row_text.strip():
                    sheets_text.append(row_text)
        return "\n".join(sheets_text)[:MAX_EXTRACT_LEN] if sheets_text else "【Excel无内容】"
    except Exception as e:
        return "【XLSX提取失败】" + str(e)

def extract_pptx_text(filepath):
    text = extract_via_kreuzberg(filepath)
    if text:
        return clean_noise(text)
    try:
        prs = pptx.Presentation(filepath)
        text_parts = []
        for i, slide in enumerate(prs.slides[:20]):
            slide_text = []
            for shape in slide.shapes:
                if hasattr(shape, "text") and shape.text.strip():
                    slide_text.append(shape.text)
            if slide_text:
                text_parts.append(f"[Page {i+1}]\n" + "\n".join(slide_text))
        return "\n".join(text_parts)[:MAX_EXTRACT_LEN] if text_parts else "【PPT无文字内容】"
    except Exception as e:
        return "【PPTX提取失败】" + str(e)

def extract_pdf_via_ocr(filepath):
    """用 OCRmyPDF 强制 OCR 提取 PDF 文本（v2.1 已修复 --force-ocr）

    Returns:
        str: 提取的文本。如果失败，返回 "【XXX失败】..." 标记
    """
    # v1.4.3: 用 tempfile.mkdtemp() 创建 per-run 私有目录
    tmp_dir = tempfile.mkdtemp(prefix="ocrmypdf_")
    tmp_pdf = os.path.join(tmp_dir, uuid.uuid4().hex + ".pdf")
    tmp_out = os.path.join(tmp_dir, uuid.uuid4().hex + "_ocr.pdf")
    try:
        shutil.copy2(filepath, tmp_pdf)
        # v2.1 修复：用 --force-ocr 替代 --skip-text，确保 OCRmyPDF 强制 OCR 所有页面
        result = subprocess.run(
            ["ocrmypdf", "-l", "chi_sim+eng", "--force-ocr",
             "--pages", "1-999", tmp_pdf, tmp_out],
            capture_output=True, timeout=600   # v2.1: 超时从 60s 提升到 600s
        )
        if result.returncode == 0 and os.path.exists(tmp_out):
            doc = pymupdf.open(tmp_out)
        else:
            doc = pymupdf.open(filepath)
        text = ""
        for page_num in range(len(doc)):
            t = doc[page_num].get_text()
            if t.strip():
                text += t + "\n"
        doc.close()
        if text.strip():
            # 过滤封面页乱码片段
            lines = text.split('\n')
            cleaned_lines = []
            for line in lines:
                if is_gibberish(line) and len(line.strip()) < 100:
                    continue
                cleaned_lines.append(line)
            text = '\n'.join(cleaned_lines).strip()
            if text:
                return clean_noise(text)
    except Exception as e:
        import sys; print(f"  ⚠️  OCR 异常: {filepath}: {type(e).__name__}: {e}", file=sys.stderr)
    finally:
        # v1.4.3: finally 清理整个私有目录
        shutil.rmtree(tmp_dir, ignore_errors=True)
    return "【PDF文字提取失败】"

def ocr_office_via_ocr(filepath, source_ext):
    """通用 Office 文件 OCR 路径（v2.1 新增）

    流程：
    1. soffice headless 转 PDF
    2. OCRmyPDF --force-ocr
    3. pymupdf 读文本

    Returns:
        str: 提取的文本。失败返回 None。
    """
    # v1.4.3: 用 tempfile.mkdtemp() 创建 per-run 私有目录
    tmp_dir = tempfile.mkdtemp(prefix="office_ocr_")
    try:
        # 1. soffice 转 PDF
        proc = subprocess.Popen(
            ['soffice', '--headless', '--convert-to', 'pdf', '--outdir', tmp_dir, filepath],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        try:
            proc.communicate(timeout=120)
        except subprocess.TimeoutExpired:
            try:
                proc.kill()
            except ProcessLookupError:
                pass  # 进程已退出，属预期情况
            except OSError as e:
                print(f"[进程清理失败] kill: {e}", file=sys.stderr)
            _kill_proc_tree(proc.pid)
        
        # 找生成的 PDF
        base = os.path.splitext(os.path.basename(filepath))[0]
        converted_pdf = os.path.join(tmp_dir, base + ".pdf")
        if not os.path.exists(converted_pdf):
            return None
        
        # 2. OCRmyPDF --force-ocr
        ocr_pdf = os.path.join(tmp_dir, uuid.uuid4().hex + "_ocr.pdf")
        result = subprocess.run(
            ["ocrmypdf", "-l", "chi_sim+eng", "--force-ocr",
             "--pages", "1-999", converted_pdf, ocr_pdf],
            capture_output=True, timeout=600
        )
        # 3. 读文本
        if result.returncode == 0 and os.path.exists(ocr_pdf):
            doc = pymupdf.open(ocr_pdf)
        else:
            # OCRmyPDF 失败：记录 returncode 与 stderr 尾部，再降级读原 PDF 文字层
            stderr_tail = ""
            if result.stderr:
                stderr_tail = result.stderr.decode("utf-8", "replace").strip()[-500:]
            print(f"[OCRmyPDF 失败] {filepath}: returncode={result.returncode} "
                  f"stderr={stderr_tail}", file=sys.stderr)
            doc = pymupdf.open(converted_pdf)
        text = ""
        for page_num in range(len(doc)):
            t = doc[page_num].get_text()
            if t.strip():
                text += t + "\n"
        doc.close()
        return text.strip() if text.strip() else None
    except Exception as e:
        # 不再静默吞掉：记录原始异常与源文件路径，便于排障
        print(f"[OCR 失败] {filepath}: {type(e).__name__}: {e}", file=sys.stderr)
        return None
    finally:
        # v1.4.3: finally 清理整个私有目录
        shutil.rmtree(tmp_dir, ignore_errors=True)


def extract_xls_text(filepath):
    """Extract text from legacy .xls Excel files using xlrd"""
    try:
        import xlrd
        wb = xlrd.open_workbook(filepath)
        text_parts = []
        for sheet in wb.sheets():
            text_parts.append(f"[{sheet.name}]")
            for row in sheet.get_rows():
                row_data = []
                for cell in row:
                    if cell.ctype == xlrd.XL_CELL_TEXT:
                        row_data.append(cell.value)
                    elif cell.ctype == xlrd.XL_CELL_NUMBER:
                        row_data.append(str(cell.value))
                    elif cell.ctype == xlrd.XL_CELL_DATE:
                        try:
                            dt = xlrd.xldate_as_datetime(cell.value, wb.datemode)
                            row_data.append(dt.strftime('%Y-%m-%d'))
                        except Exception as e:
                            # 单元格日期解析失败：降级为原始值，但记录原因
                            print(f"[Excel 日期解析失败] {filepath}: {e}", file=sys.stderr)
                            row_data.append(str(cell.value))
                    elif cell.ctype == xlrd.XL_CELL_EMPTY:
                        pass
                if any(row_data):
                    text_parts.append(' | '.join(row_data))
        return '\n'.join(text_parts)
    except Exception as e:
        return None
