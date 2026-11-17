#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Office 文档（docx / xlsx / pptx）→ md 转换器（stdlib-only，零第三方依赖）

本脚本是 ct- 系列**共享件**（单一真源位于 ct-base/scripts/office_to_md.py），
供各 ct- 技能经 `publish_inject.py` 注入或在本地 `sys.path` 导入复用。

用途（对应 ct-base/BASE.md §6.7 用户上传文件处理规范）：
用户以 .docx / .xlsx / .pptx 附件提供模板、方案、材料时，本地先把附件转成 md
（段落 + 表格结构保留），再拼入处理链路（如 original_question / 本地分析上下文）。

设计约束（§6.7 分层方案）：
- docx / xlsx / pptx 同为 OOXML zip 格式（zipfile + xml.etree.ElementTree 即可解析），
  **一个解析族覆盖三种**，不为每种格式维护一套轮子；
- .pdf 无法 stdlib 可靠解析（二进制格式）→ 指引调用环境 pdf 技能 / 提示安装；
- .doc / .xls / .ppt 老格式（OLE 二进制）→ 指引「另存为新格式」或安装 word-reader / antiword。

体积门（2026-09-23 新增）：
- 单文件上限 ``MAX_FILE_BYTES``（5 MB）。超限**直接拒绝并给出可执行的压缩建议**，
  不进入解析（既避免无谓的本地解析开销，也避免超大正文挤爆下游提示词预算）。
- 注意：**对 OOXML 再 zip 收益很小且不稳定**（实测 0.9%~24.5%，媒体型文档常 <1%，
  无法把超限文件压进限内）；减流量的正确杠杆见
  `docs/2026-09-23-upload-limits-and-compression.md`。

用法：
    python office_to_md.py <file.docx|file.xlsx|file.pptx>         # 输出 md 到 stdout
    python office_to_md.py <file> --check                          # 仅校验体积与可解析性
"""

import os
import sys
import zipfile
import re
import xml.etree.ElementTree as ET

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
P = "{http://schemas.openxmlformats.org/presentationml/2006/main}"
S = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"

# ── 体积门 ────────────────────────────────────────────────────────────────────
MAX_FILE_BYTES = 5 * 1024 * 1024        # 5 MB
MAX_MB = MAX_FILE_BYTES // (1024 * 1024)

SUPPORTED_EXTS = (".docx", ".xlsx", ".pptx")
LEGACY_EXTS = (".doc", ".xls", ".ppt")

# 单表渲染上限（防止超大表格把下游提示词预算吃光；超出即截断并显式标注）
XLSX_MAX_ROWS = 300
XLSX_MAX_COLS = 30


class UploadRejected(ValueError):
    """上传被拒（体积超限 / 格式不支持 / 文件不可读）。

    继承 ValueError 以兼容既有 ``except ValueError`` 调用方；
    ``str(e)`` 即为**可直接展示给用户**的可读原因与修正建议。
    """


def check_upload(path: str) -> int:
    """上传前置校验：存在性 + 体积门 + 扩展名支持度。返回文件字节数。

    超限/不支持即刻抛 ``UploadRejected``（消息面向用户，含具体修正动作）。
    该函数是本地 Office 上传的**唯一门禁**，任何调用 ``office_to_md`` 的路径都会经过它。
    """
    if not isinstance(path, str) or not path.strip():
        raise UploadRejected("未提供文件路径。请重新上传文件后重试。")
    if not os.path.exists(path):
        raise UploadRejected(f"文件不存在或不可读：{path}")
    if not os.path.isfile(path):
        raise UploadRejected(f"该路径不是文件：{path}")

    size = os.path.getsize(path)
    if size > MAX_FILE_BYTES:
        raise UploadRejected(
            f"文件体积 {size / 1048576:.1f} MB，超过单文件上限 {MAX_MB} MB，已拒绝接收。\n"
            "请按以下任一方式修正后重新上传：\n"
            "  1) 删除文档中的大图片 / 嵌入对象 / 高分辨率截图（这通常是超限主因）；\n"
            "  2) 在 Office 中「另存为」精简版本，或拆分为多个较小文件分别上传；\n"
            "  3) 仅保留本次咨询所需的章节 / 工作表，删除无关页；\n"
            "  4) 若只需其中部分数据，直接把关键表格或段落**粘贴为文本**，无需上传文件。"
        )

    low = path.lower()
    if low.endswith(".zip"):
        raise UploadRejected(
            "检测到 .zip 压缩包。请解压后上传其中的原始文档。\n"
            "提示：对 Office 文件（.docx/.xlsx/.pptx）再压缩**收益很小且不稳定**"
            "——它们本身就是 zip+deflate 结构；实测再 ZIP 一层只能瘦身约 1%~25%"
            "（图片/媒体为主的文档常低于 1%），基本无法把超限文件压到限内。"
            "要减小体积，请删除大图片/嵌入对象，或拆分为多个文件。"
        )
    if low.endswith(LEGACY_EXTS):
        raise UploadRejected(
            f"{os.path.splitext(path)[1]} 是 Office 老格式（OLE 二进制），无法零依赖解析。\n"
            "请用 Office/WPS 打开后「另存为」新格式：.doc → .docx、.xls → .xlsx、.ppt → .pptx，"
            "然后重新上传。"
        )
    if low.endswith(".pdf"):
        raise UploadRejected(
            ".pdf 无法零依赖解析。请调用环境中的 pdf 技能处理"
            "（扫描件需先 OCR），或把关键段落粘贴为文本。"
        )
    if not low.endswith(SUPPORTED_EXTS):
        raise UploadRejected(
            f"不支持的格式：{os.path.splitext(path)[1] or '(无扩展名)'}。"
            f"当前支持 {' / '.join(SUPPORTED_EXTS)}。"
        )
    return size


# ===== docx =====

def _w_para_text(p) -> str:
    """docx 段落文本：w:t 拼接，w:tab→制表符，w:br→换行。"""
    parts = []
    for node in p.iter():
        tag = node.tag
        if tag == W + "t":
            parts.append(node.text or "")
        elif tag == W + "tab":
            parts.append("\t")
        elif tag == W + "br":
            parts.append("\n")
    return "".join(parts).strip()


def _w_cell_text(tc) -> str:
    """docx 单元格文本：多段落用空格连接。"""
    texts = []
    for p in tc.findall(W + "p"):
        t = _w_para_text(p)
        if t:
            texts.append(t)
    return " ".join(texts)


def _rows_to_md(rows) -> str:
    """二维单元格列表 → md 表格（首行作表头 + 分隔行，列数按首行补齐）。"""
    if not rows:
        return ""
    ncol = max(len(r) for r in rows)
    lines = []
    header = (rows[0] + [""] * ncol)[:ncol]
    lines.append("| " + " | ".join(header) + " |")
    lines.append("| " + " | ".join(["---"] * ncol) + " |")
    for r in rows[1:]:
        row = (r + [""] * ncol)[:ncol]
        lines.append("| " + " | ".join(row) + " |")
    return "\n".join(lines)


def docx_to_md(path: str) -> str:
    """docx → md：段落与表格按文档顺序交错输出。"""
    with zipfile.ZipFile(path) as z:
        try:
            xml_data = z.read("word/document.xml")
        except KeyError:
            raise ValueError(f"{path} 不是有效的 docx（缺少 word/document.xml）")
    root = ET.fromstring(xml_data)
    body = root.find(W + "body")
    if body is None:
        return ""
    out = []
    for child in body:
        if child.tag == W + "p":
            t = _w_para_text(child)
            if t:
                out.append(t)
        elif child.tag == W + "tbl":
            rows = []
            for tr in child.findall(W + "tr"):
                rows.append([_w_cell_text(tc) for tc in tr.findall(W + "tc")])
            t = _rows_to_md(rows)
            if t:
                out.append(t)
    return "\n\n".join(out)


# ===== xlsx =====

def _col_index(ref: str) -> int:
    """单元格引用（如 "C5"）→ 0 基列号（C → 2）。无字母 → 0。"""
    m = re.match(r"([A-Za-z]+)", ref or "")
    if not m:
        return 0
    n = 0
    for ch in m.group(1).upper():
        n = n * 26 + (ord(ch) - 64)
    return n - 1


def _xlsx_shared_strings(z) -> list:
    """读取 xl/sharedStrings.xml → 字符串表。

    仅聚合 `si` 直属的 `t` 与富文本 `r/t`，**跳过 `rPh`（拼音/注音提示）**，
    否则中文表格里会混入重复的注音文本。
    """
    try:
        xml_data = z.read("xl/sharedStrings.xml")
    except KeyError:
        return []
    try:
        root = ET.fromstring(xml_data)
    except ET.ParseError:
        return []
    out = []
    for si in root.findall(S + "si"):
        parts = [t.text or "" for t in si.findall(S + "t")]
        for r in si.findall(S + "r"):
            parts.extend(t.text or "" for t in r.findall(S + "t"))
        out.append("".join(parts).strip())
    return out


def _xlsx_sheets(z) -> list:
    """→ [(sheet 名, 部件路径)]，按 workbook 声明顺序；取不到则按文件名数字序兜底。"""
    rels = {}
    try:
        rr = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
        for rel in rr:
            rels[rel.get("Id")] = rel.get("Target") or ""
    except (KeyError, ET.ParseError):
        pass

    sheets = []
    try:
        wb = ET.fromstring(z.read("xl/workbook.xml"))
        holder = wb.find(S + "sheets")
        if holder is not None:
            for sh in holder.findall(S + "sheet"):
                target = rels.get(sh.get(R + "id"), "")
                if target:
                    target = target.lstrip("/")
                    if not target.startswith("xl/"):
                        target = "xl/" + target
                if target:
                    sheets.append((sh.get("name") or "", target))
    except (KeyError, ET.ParseError):
        pass
    if sheets:
        return sheets

    names = sorted(
        [n for n in z.namelist() if re.match(r"xl/worksheets/sheet\d+\.xml$", n)],
        key=lambda n: int(re.search(r"(\d+)", n).group(1)),
    )
    return [(f"Sheet{i + 1}", n) for i, n in enumerate(names)]


def _xlsx_cell_value(c, shared) -> str:
    """单元格值 → 字符串。

    t 语义：s=共享字符串索引 | inlineStr=内联字符串 | str=公式缓存串 |
    b=布尔 | e=错误 | 缺省/ n=数值（**不做日期序列换算**，原样保留以免猜错格式）。
    """
    t = c.get("t")
    if t == "inlineStr":
        holder = c.find(S + "is")
        if holder is None:
            return ""
        return "".join(x.text or "" for x in holder.iter(S + "t")).strip()
    v = c.find(S + "v")
    if v is None or v.text is None:
        return ""
    raw = v.text
    if t == "s":
        try:
            return shared[int(raw)]
        except (ValueError, IndexError):
            return ""
    if t == "b":
        return "TRUE" if raw.strip() == "1" else "FALSE"
    return raw.strip()


def xlsx_to_md(path: str) -> str:
    """xlsx → md：每个工作表一节（## Sheet N: 名称），内容为 md 表格。

    - 按单元格 ref 的列字母还原列位，故稀疏/跳跃列不会串列；
    - 跳过全空行；首个表头行若为空则跳过该行再用下一行作表头；
    - 超过 XLSX_MAX_ROWS / XLSX_MAX_COLS 的部分截断，并在表后显式标注。
    """
    with zipfile.ZipFile(path) as z:
        shared = _xlsx_shared_strings(z)
        sheets = _xlsx_sheets(z)
        if not sheets:
            raise ValueError(f"{path} 不是有效的 xlsx（缺少 xl/worksheets/sheetN.xml）")

        parts = []
        for idx, (name, spath) in enumerate(sheets, 1):
            try:
                root = ET.fromstring(z.read(spath))
            except (KeyError, ET.ParseError):
                continue

            all_rows = list(root.iter(S + "row"))
            rows = []
            for r in all_rows[:XLSX_MAX_ROWS]:
                cells = {}
                maxc = -1
                for c in r.findall(S + "c"):
                    ci = _col_index(c.get("r") or "")
                    if ci < 0 or ci >= XLSX_MAX_COLS:
                        continue
                    val = _xlsx_cell_value(c, shared)
                    if val:
                        cells[ci] = val
                        maxc = max(maxc, ci)
                if maxc < 0:
                    continue                       # 全空行不入表
                rows.append([cells.get(i, "") for i in range(maxc + 1)])

            if not rows:
                parts.append(f"## Sheet {idx}: {name or '(未命名)'}\n\n（空工作表）")
                continue

            # 首行全空则不用它当表头（数据区下移一行）
            if not any(cell.strip() for cell in rows[0]) and len(rows) > 1:
                rows = rows[1:]

            ncol = max(len(r) for r in rows)
            notes = []
            if len(all_rows) > XLSX_MAX_ROWS:
                notes.append(f"共 {len(all_rows)} 行，已截断显示前 {XLSX_MAX_ROWS} 行")
            if ncol >= XLSX_MAX_COLS:
                notes.append(f"有效列数 ≥ {XLSX_MAX_COLS}，已截断显示前 {XLSX_MAX_COLS} 列")
            note = ("\n\n> （" + "；".join(notes) + "）") if notes else ""

            parts.append(f"## Sheet {idx}: {name or '(未命名)'}\n\n{_rows_to_md(rows)}{note}")
        return "\n\n".join(parts)


# ===== pptx =====

def _iter_els(el, skip_tag=None):
    """递归遍历元素，可跳过指定标签的整棵子树（iter() 无法跳过）。"""
    if skip_tag is not None and el.tag == skip_tag:
        return
    yield el
    for child in el:
        yield from _iter_els(child, skip_tag)


def _pptx_shape_text(sp) -> str:
    """pptx 形状内文本：a:p → 段落，a:t 拼接。"""
    lines = []
    for p in sp.findall(".//" + A + "p"):
        t = "".join(n.text or "" for n in p.iter(A + "t")).strip()
        if t:
            lines.append(t)
    return "\n".join(lines)


def _pptx_graphic_tables(gf) -> list:
    """pptx graphicFrame 内的表格 → md 表格列表。"""
    tables = []
    for tbl in gf.iter(A + "tbl"):
        rows = []
        for tr in tbl.iter(A + "tr"):
            cells = []
            for tc in tr.iter(A + "tc"):
                c = " ".join(
                    "".join(t.text or "" for t in p.iter(A + "t")).strip()
                    for p in tc.iter(A + "p")
                    if "".join(t.text or "" for t in p.iter(A + "t")).strip()
                )
                cells.append(c)
            rows.append(cells)
        t = _rows_to_md(rows)
        if t:
            tables.append(t)
    return tables


def _pptx_slide_text(root) -> str:
    """单张 slide → md：spTree 内按顺序交替文本形状与表格。"""
    sp_tree = root.find(".//" + P + "spTree")
    if sp_tree is None:
        return ""
    out = []
    for child in sp_tree:
        if child.tag == P + "sp":
            t = _pptx_shape_text(child)
            if t:
                out.append(t)
        elif child.tag == P + "graphicFrame":
            for t in _pptx_graphic_tables(child):
                if t:
                    out.append(t)
    return "\n\n".join(out)


def pptx_to_md(path: str) -> str:
    """pptx → md：每张 slide 一节（### Slide N），保留表格。"""
    with zipfile.ZipFile(path) as z:
        slides = sorted(
            [n for n in z.namelist() if re.match(r"ppt/slides/slide\d+\.xml$", n)],
            key=lambda n: int(re.search(r"(\d+)", n).group(1)),
        )
        if not slides:
            raise ValueError(f"{path} 不是有效的 pptx（缺少 ppt/slides/slideN.xml）")
        parts = []
        for i, s in enumerate(slides, 1):
            root = ET.fromstring(z.read(s))
            text = _pptx_slide_text(root)
            if text:
                parts.append(f"### Slide {i}\n\n{text}")
    return "\n\n".join(parts)


# ===== 统一入口 =====

def office_to_md(path: str) -> str:
    """按扩展名分发：.docx / .xlsx / .pptx。先过体积门，其余抛 UploadRejected。

    依据 BASE.md §6.7 分层方案：
    - .docx / .xlsx / .pptx → 本解析族（stdlib-only 零依赖）；
    - .doc / .xls / .ppt 老格式（OLE）→ 抛错，指引「另存为新格式」；
    - .pdf → 抛错，指引调用环境中的 pdf 技能（扫描件需 OCR）；
    - 任意格式 > MAX_FILE_BYTES（5 MB）→ 直接拒绝，并给出压缩建议。
    """
    check_upload(path)
    low = path.lower()
    if low.endswith(".docx"):
        return docx_to_md(path)
    if low.endswith(".xlsx"):
        return xlsx_to_md(path)
    if low.endswith(".pptx"):
        return pptx_to_md(path)
    # check_upload 已覆盖其余情形；此处为防御性兜底
    raise UploadRejected(f"不支持的格式: {path}（支持 {' / '.join(SUPPORTED_EXTS)}）")


def main() -> int:
    if len(sys.argv) < 2:
        print(
            f"usage: python office_to_md.py <file.docx|file.xlsx|file.pptx> [--check]\n"
            f"       单文件上限 {MAX_MB} MB",
            file=sys.stderr,
        )
        return 2
    path = sys.argv[1]
    try:
        size = check_upload(path)
        md = office_to_md(path)
    except UploadRejected as e:
        print(f"拒绝接收：{e}", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"错误: {e}", file=sys.stderr)
        return 1
    if "--check" in sys.argv:
        print(f"OK: {size / 1024:.1f} KB / 上限 {MAX_MB} MB, {len(md)} 字符, {md.count(chr(10))} 行")
        return 0
    print(md)
    return 0


if __name__ == "__main__":
    sys.exit(main())
