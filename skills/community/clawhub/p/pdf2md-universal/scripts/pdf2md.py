#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pdf2md-universal 核心转换脚本
把 PDF 转成结构化 Markdown，分三层策略，输出 token 预估对比。

策略:
  L1 文本型: pdftotext 抽取（快、免费、零 token）
  L2 增强型: pdfplumber 检测标题层级，还原结构（文本型 PDF 推荐）
  L3 扫描型: pypdfium2 渲染成图 → OCR 兜底（百炼 qwen3-vl-plus 或 tesseract）

用法:
  pdf2md.py <input.pdf> [--output out.md] [--mode full|summary] [--ocr auto|force|none]
  pdf2md.py <input.pdf> --token-estimate    # 只估算不转换

输出:
  - 转换后的 Markdown 文件
  - stderr 打印 token 对比报告
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile

# ---------- 常量 ----------
CJK_RE = re.compile(r'[\u4e00-\u9fff\u3400-\u4dbf]')
TEXT_PAGE_THRESHOLD = 300   # 每页有效字符 < 此值 → 判定扫描型
OCR_SYSTEM_BAILIAN = "bailian"
OCR_SYSTEM_TESSERACT = "tesseract"

# 常见视觉模型每页图像 token 估算（供对比）
VISION_TOKENS_PER_PAGE = 650


# ---------- 工具函数 ----------

def find_pdftotext():
    return shutil.which("pdftotext")


def find_tesseract():
    return shutil.which("tesseract")


def find_bailian_adapter():
    """定位百炼 CLI adapter。

    优先级：
    1. 环境变量 BAILIAN_ADAPTER 指定的路径
    2. 命令行 --bailian-adapter 参数（在 main 中处理）
    3. 默认路径（若存在）
    """
    env_path = os.environ.get("BAILIAN_ADAPTER")
    if env_path and os.path.exists(env_path):
        return env_path
    candidates = [
        os.path.expanduser("~/bailian_cli_adapter.py"),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "bailian_cli_adapter.py"),
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    return None


def count_tokens(text: str) -> int:
    """混合中英文 token 估算：中文 1 字 ≈ 1 token，英文 4 字符 ≈ 1 token。"""
    cjk = len(CJK_RE.findall(text))
    ascii_chars = len(re.sub(r'\s', '', text)) - cjk
    return cjk + ascii_chars // 4


def run_pdftotext(pdf: str, out_txt: str) -> bool:
    exe = find_pdftotext()
    if not exe:
        return False
    r = subprocess.run([exe, "-layout", pdf, out_txt], capture_output=True)
    return r.returncode == 0 and os.path.exists(out_txt)


def detect_scan_type(pdf: str, txt_path: str) -> tuple:
    """判断 PDF 是文本型还是扫描型。返回 (is_scanned, page_count, total_chars, chars_per_page)"""
    total = ""
    if txt_path and os.path.exists(txt_path):
        total = open(txt_path, encoding="utf-8", errors="ignore").read()
    total_chars = len(total.strip())
    # 页数
    pages = 1
    r = subprocess.run([find_pdftotext(), "-v"], capture_output=True)
    info = subprocess.run(
        [find_pdftotext() or "pdftotext", pdf, "-"],
        capture_output=True)
    # 用 pdfinfo 更可靠
    pdfinfo = shutil.which("pdfinfo")
    if pdfinfo:
        r2 = subprocess.run([pdfinfo, pdf], capture_output=True, text=True)
        m = re.search(r"Pages:\s+(\d+)", r2.stdout)
        if m:
            pages = int(m.group(1))
    chars_per_page = total_chars / max(pages, 1)
    is_scanned = chars_per_page < TEXT_PAGE_THRESHOLD
    return is_scanned, pages, total_chars, chars_per_page


def ocr_with_bailian(pdf: str, out_md: str, pages_limit: int = 50) -> str:
    """扫描型 PDF：pypdfium2 渲染成图 → 百炼 qwen3-vl-plus OCR。"""
    try:
        import pypdfium2 as pdfium
        from PIL import Image
    except ImportError:
        return None
    adapter = find_bailian_adapter()
    if not adapter:
        return None
    sys.path.insert(0, os.path.dirname(adapter))
    try:
        from bailian_cli_adapter import vision_describe
    except ImportError:
        try:
            mod_name = os.path.splitext(os.path.basename(adapter))[0]
            mod = __import__(mod_name)
            vision_describe = mod.vision_describe
        except Exception:
            return None

    doc = pdfium.PdfDocument(pdf)
    n = min(len(doc), pages_limit)
    md_parts = [f"<!-- OCR via qwen3-vl-plus, {n} pages, truncated at {pages_limit} -->", ""]
    prompt = (
        "你是文档 OCR 引擎。把这一页的内容完整转成 Markdown 文本："
        "保留标题层级、表格（转成 Markdown 表格）、列表。"
        "只输出转换后的 Markdown，不要解释。若页面无有效内容输出空白。"
    )
    with tempfile.TemporaryDirectory() as td:
        for i in range(n):
            page = doc[i]
            bitmap = page.render(scale=2.0)
            img = bitmap.to_pil()
            p = os.path.join(td, f"p{i:03d}.png")
            img.save(p, format="PNG")
            try:
                res = vision_describe(p, prompt=prompt, timeout=300)
                text = res if isinstance(res, str) else str(res)
                text = re.sub(r"^```(?:markdown)?\s*", "", text.strip())
                text = re.sub(r"\s*```$", "", text)
                md_parts.append(f"## 第 {i+1} 页\n\n{text}\n")
            except Exception as e:
                md_parts.append(f"## 第 {i+1} 页\n\n<!-- OCR 失败: {e} -->\n")
    result = "\n".join(md_parts)
    open(out_md, "w", encoding="utf-8").write(result)
    return result


def structure_with_pdfplumber(pdf: str, txt_path: str, out_md: str) -> None:
    """文本型增强：pdftotext 文本为底 + pdfplumber 提取标题层级。"""
    text = open(txt_path, encoding="utf-8", errors="ignore").read()
    # 标题检测：用 pdfplumber 每页取字号最大且短的文本行
    headings = {}  # page -> list of (size, text)
    try:
        import pdfplumber
        with pdfplumber.open(pdf) as pdf:
            for pno, page in enumerate(pdf.pages, 1):
                words = page.extract_words(extra_attrs=["size"])
                if not words:
                    continue
                max_size = max(w.get("size", 0) for w in words)
                if max_size <= 0:
                    continue
                # 收集 >= 90% 最大字号的短行
                cand = sorted(
                    (w for w in words if w.get("size", 0) >= max_size * 0.9),
                    key=lambda w: (round(w["top"]), w["x0"]))
                lines = {}
                for w in cand:
                    key = round(w["top"] / 3)
                    lines.setdefault(key, []).append(w)
                merged = []
                for k in sorted(lines):
                    ws = sorted(lines[k], key=lambda w: w["x0"])
                    line_text = "".join(w.get("text", "") for w in ws).strip()
                    # 标题判定过滤：长度 3-60、不以句末标点结尾、不含引号包裹的引用语、
                    # 不全是大写缩写噪音、必须有真实词首字母
                    if (line_text and 3 <= len(line_text) <= 60
                            and not re.search(r'[.。!?！？:：;,，、…]$', line_text)
                            and not re.search(r'["“”\'‘’]$', line_text)
                            and not re.search(r'^["“”\'‘’]', line_text)
                            and not line_text.isdigit()):
                        merged.append((max_size, line_text))
                if merged:
                    headings[pno] = merged
    except ImportError:
        pass

    # 组装 Markdown：逐页插入标题标记
    pages_text = re.split(r"\f", text)
    md = []
    for i, page_text in enumerate(pages_text, 1):
        lines = [l.rstrip() for l in page_text.splitlines() if l.strip()]
        if not lines:
            continue
        h_marks = {}
        for size, htext in headings.get(i, []):
            # 粗略按字号分级
            level = 1 if size >= 18 else (2 if size >= 14 else 3)
            h_marks[htext] = "#" * level
        for ln in lines:
            ln_s = ln.strip()
            if not ln_s:
                continue
            if ln_s in h_marks:
                md.append(f"\n{h_marks[ln_s]} {ln_s}\n")
            else:
                md.append(ln)
        md.append("")  # 页间空行
    open(out_md, "w", encoding="utf-8").write("\n".join(md))


def write_plain(text: str, out_md: str) -> None:
    open(out_md, "w", encoding="utf-8").write(text)


def token_report(pdf: str, out_md: str, md_text: str, is_scanned: bool, pages: int, mode: str) -> str:
    """生成 token 对比报告（给用户看的核心价值）。"""
    md_tokens = count_tokens(md_text)
    direct_pdf_tokens = pages * VISION_TOKENS_PER_PAGE + md_tokens  # 视觉+文本
    savings = direct_pdf_tokens / max(md_tokens, 1)
    lines = [
        "══════════ PDF→Markdown 转换报告 ══════════",
        f"文件: {os.path.basename(pdf)}",
        f"页数: {pages} | 类型: {'扫描型(OCR)' if is_scanned else '文本型'} | 模式: {mode}",
        f"输出: {out_md}",
        "",
        f"直接读 PDF (多模态): ~{direct_pdf_tokens:,} token",
        f"转 Markdown 后读取: ~{md_tokens:,} token",
        f"节省: {savings:.1f}x   (token), 成本通常省 10-30x",
        "══════════════════════════════════════════",
    ]
    return "\n".join(lines)


# ---------- 主流程 ----------

def main():
    ap = argparse.ArgumentParser(description="PDF → Markdown 通用转换器")
    ap.add_argument("input", help="输入 PDF 路径")
    ap.add_argument("--output", "-o", help="输出 md 路径（默认同目录同名 .md）")
    ap.add_argument("--mode", choices=["full", "summary"], default="full",
                    help="full=全量转换(默认), summary=只保留前几页/高密度内容")
    ap.add_argument("--ocr", choices=["auto", "force", "none"], default="auto",
                    help="auto=扫描型才OCR(默认), force=强制OCR, none=禁用OCR")
    ap.add_argument("--token-estimate", action="store_true",
                    help="只做 token 估算，不写文件")
    ap.add_argument("--bailian-adapter", default=None,
                    help="百炼 CLI adapter 路径（覆盖默认查找逻辑）")
    args = ap.parse_args()

    # 允许命令行覆盖 adapter 路径
    if args.bailian_adapter:
        os.environ["BAILIAN_ADAPTER"] = args.bailian_adapter

    pdf = args.input
    if not os.path.exists(pdf):
        print(f"错误: 找不到文件 {pdf}", file=sys.stderr)
        sys.exit(1)

    out_md = args.output or os.path.splitext(pdf)[0] + ".md"
    # 1. L1: pdftotext
    txt_path = None
    if find_pdftotext():
        txt_path = tempfile.mktemp(suffix=".txt")
        if not run_pdftotext(pdf, txt_path):
            txt_path = None

    is_scanned, pages, total_chars, cpp = detect_scan_type(pdf, txt_path)

    # 纯估算模式
    if args.token_estimate:
        md_text = ""
        if txt_path and os.path.exists(txt_path):
            md_text = open(txt_path, encoding="utf-8", errors="ignore").read()
        print(token_report(pdf, "(估算)", md_text, is_scanned, pages, args.mode))
        sys.exit(0)

    # 2. 分层策略
    ocr_requested = (args.ocr == "force") or (is_scanned and args.ocr == "auto")

    if args.ocr == "none":
        ocr_requested = False

    if is_scanned and not ocr_requested and args.ocr == "auto":
        # 扫描型但 OCR 被禁用/不可用 → 降级为纯文本占位
        print("⚠️ 检测到扫描型 PDF，且 OCR 不可用。建议 --ocr force。", file=sys.stderr)
        if txt_path:
            write_plain(open(txt_path, encoding="utf-8", errors="ignore").read(), out_md)
        else:
            write_plain(f"<!-- 扫描型 PDF，无法提取文本: {os.path.basename(pdf)} -->", out_md)
        md_text = open(out_md, encoding="utf-8").read()
    elif ocr_requested:
        md_text = ocr_with_bailian(pdf, out_md)
        if md_text is None:
            # OCR 不可用 → 回退 tesseract
            tess = find_tesseract()
            if tess and txt_path:
                r = subprocess.run([tess, pdf, "stdout", "-l", "chi_sim+eng"],
                                   capture_output=True)
                md_text = r.stdout.decode("utf-8", errors="ignore")
                write_plain(md_text, out_md)
            else:
                print("⚠️ OCR 引擎不可用（需要百炼 adapter 或 tesseract）", file=sys.stderr)
                write_plain(f"<!-- 扫描型 PDF，OCR 不可用: {os.path.basename(pdf)} -->", out_md)
                md_text = open(out_md, encoding="utf-8").read()
    else:
        # 文本型：增强结构
        if txt_path:
            structure_with_pdfplumber(pdf, txt_path, out_md)
            md_text = open(out_md, encoding="utf-8").read()
        else:
            print("⚠️ pdftotext 不可用，尝试 pdfplumber 直接提取", file=sys.stderr)
            try:
                import pdfplumber
                parts = []
                with pdfplumber.open(pdf) as p:
                    for page in p.pages:
                        parts.append(page.extract_text() or "")
                write_plain("\n\n".join(parts), out_md)
                md_text = open(out_md, encoding="utf-8").read()
            except Exception as e:
                print(f"错误: {e}", file=sys.stderr)
                sys.exit(1)

    # 清理临时文件
    if txt_path and os.path.exists(txt_path):
        os.remove(txt_path)

    print(token_report(pdf, out_md, md_text, is_scanned, pages, args.mode), file=sys.stderr)
    print(f"✅ 已输出: {out_md}", file=sys.stderr)


if __name__ == "__main__":
    main()
