#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""docx_text.py — 零依赖 .docx → 文本抽取（v5.3.0 新增）

论文作者的真实输入是 Word 文档。本模块用标准库（zipfile + xml.etree）
从 .docx 抽取正文文本：按 w:p 段落切分、拼接 w:t 文本节点、保留换行结构。
不引入任何第三方依赖（100% 本地契约不变）。

安全护栏（解压炸弹/恶意包防护）：
  - 压缩包总解压上限 MAX_UNCOMPRESSED（默认 30MB），超限拒绝
  - 成员数量上限 MAX_MEMBERS（默认 500），超限拒绝
  - 只读 word/ 主文档部件（document.xml 及 header/footer 可选），不落盘任何中间文件
  - XML 由 ElementTree 解析（不处理 DTD/外部实体）

用法（库）:
    from docx_text import docx_to_text
    text = docx_to_text("thesis.docx")

用法（CLI，便于诊断）:
    python3 docx_text.py thesis.docx [--output out.txt]
"""
import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

MAX_UNCOMPRESSED = 30 * 1024 * 1024   # 解压后总字节上限
MAX_MEMBERS = 500                      # zip 成员数上限
_W_NS = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


class DocxError(ValueError):
    """docx 解析失败（格式/超限）。类型归入 ValueError 族，pp_api 契约一致。"""


def _guard_zip(zf: zipfile.ZipFile):
    infos = zf.infolist()
    if len(infos) > MAX_MEMBERS:
        raise DocxError(f"docx 成员数超上限（{len(infos)} > {MAX_MEMBERS}），拒绝解析")
    total = sum(i.file_size for i in infos)
    if total > MAX_UNCOMPRESSED:
        raise DocxError(f"docx 解压后总量超上限（{total:,} > {MAX_UNCOMPRESSED:,} 字节），拒绝解析")


def _para_text(p_el) -> str:
    parts = []
    for node in p_el.iter():
        tag = node.tag
        if tag == f"{_W_NS}t":
            parts.append(node.text or "")
        elif tag == f"{_W_NS}tab":
            parts.append("\t")
        elif tag in (f"{_W_NS}br", f"{_W_NS}cr"):
            parts.append("\n")
    return "".join(parts)


def docx_to_text(path) -> str:
    """抽取 .docx 正文文本（按段落保留换行）。非 docx/损坏文件抛 DocxError。"""
    p = Path(path)
    if not p.exists():
        raise DocxError(f"文件不存在: {p}")
    try:
        zf = zipfile.ZipFile(p)
    except zipfile.BadZipFile as e:
        raise DocxError(f"不是有效的 docx（ZIP）文件: {p}") from e
    with zf:
        _guard_zip(zf)
        target = "word/document.xml"
        if target not in zf.namelist():
            raise DocxError(f"docx 缺少主文档部件（{target}）")
        try:
            root = ET.fromstring(zf.read(target))
        except ET.ParseError as e:
            raise DocxError(f"docx 主文档 XML 解析失败: {e}") from e
    paras = [_para_text(pe) for pe in root.iter(f"{_W_NS}p")]
    text = "\n\n".join(x.strip() for x in paras if x and x.strip())
    if not text.strip():
        raise DocxError("docx 未抽取到正文文本（可能是空文档或纯图片文档）")
    return text


def is_docx(path) -> bool:
    return str(path).lower().endswith(".docx")


_BINARY_MAGICS = (
    (b"%PDF-", "PDF 不受支持：零依赖解析无法保证中文文本抽取的正确性，"
               "请先将 PDF 转存为 .docx 或 .txt 再检测（Word「另存为」或任意转换工具均可）。"),
    (b"\x89PNG", "PNG 图片不受支持：请先转存为文本格式（.txt/.docx）。"),
    (b"\xff\xd8\xff", "JPEG 图片不受支持：请先转存为文本格式（.txt/.docx）。"),
    (b"PK\x03\x04", "ZIP 容器不是 .docx（如 .zip/.pptx/.xlsx）：本工具仅支持 .docx 文本抽取，"
                  "请先另存为 .docx 或 .txt。"),
)


def read_text_any(path):
    """统一文本读取入口：.docx 走抽取，其余按 UTF-8（GBK 容错）读；
    二进制格式（PDF/图片等）按魔数识别并给出明确转存建议（v5.4.0），拒绝静默乱码。

    供各入口脚本共用——调用方不再各自处理 docx 分支。
    """
    p = Path(path)
    if is_docx(p):
        return docx_to_text(p)
    raw = p.read_bytes()
    for magic, msg in _BINARY_MAGICS:
        if raw[:len(magic)] == magic:
            raise DocxError(msg)
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        return raw.decode("gbk", errors="replace")


def main():
    import argparse
    ap = argparse.ArgumentParser(description=".docx → 文本抽取（零依赖，诊断用）")
    ap.add_argument("file")
    ap.add_argument("--output", default=None, help="输出 txt（默认打印到 stdout）")
    args = ap.parse_args()
    try:
        text = docx_to_text(args.file)
    except DocxError as e:
        from pp_errors import print_friendly
        print_friendly(e)
        return 2
    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
        print(f"已写出: {args.output}（{len(text)} 字）")
    else:
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
