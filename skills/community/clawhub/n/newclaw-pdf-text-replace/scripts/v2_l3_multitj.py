#!/usr/bin/env python3
"""
v2_l3_multitj.py — L3 多 Tj 替换模块（Multi-Tj Replacement）

将 PyPI 包 pdf_text_replace.advanced 中的实现适配为
openclaw 主入口（pdf_text_replace.py）期望的文件级接口：

    replace_multi_tj(input_path, old_text, new_text, output_path, page_num) -> bool

策略：
  解析 PDF 内容流中所有 Tj/TJ 操作，按 Y 坐标分组，
  查找跨越多个 Tj 调用的文本并执行替换。
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Optional

from pypdf import PdfReader, PdfWriter


# ─────────────────────────────────────────────────────────────────────────────
# CMap 解析
# ─────────────────────────────────────────────────────────────────────────────

def _parse_cmap(cmap_data: str) -> dict:
    """解析 PDF ToUnicode CMap -> {byte_code: unicode_char}，支持两种格式合并"""
    mapping = {}
    # Format 1: beginbfrange <XX><XX><YYYY>
    for m in re.finditer(r"<([0-9a-fA-F]+)><\1><([0-9a-fA-F]+)>", cmap_data):
        code = int(m.group(1), 16)
        uchar = chr(int(m.group(2), 16))
        mapping[code] = uchar
    # Format 2: beginbfchar <XX> <YYYY>（合并，不覆盖已有映射）
    for m in re.finditer(r"<([0-9a-fA-F]{2,4})>\s+<([0-9a-fA-F]{4})>", cmap_data):
        src_hex = m.group(1)
        dst_hex = m.group(2)
        if dst_hex == "0000":
            continue
        code = int(src_hex, 16)
        if code not in mapping:
            uchar = chr(int(dst_hex, 16))
            mapping[code] = uchar
    return mapping


# ─────────────────────────────────────────────────────────────────────────────
# 数据结构
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class TextOperation:
    """从内容流中提取的单个 Tj 或 TJ 文本绘制操作"""
    tm_x: float
    tm_y: float
    font: str
    size: float
    text_encoded: str      # 原始 latin-1 字符串（包含括号）
    text_decoded: str      # 经 CMap 解码后的可读文本
    offset: int            # '(' 在流中的字节偏移
    length: int            # '(...)' 的字节长度（含括号）
    op_type: str = "Tj"    # 'Tj' 或 'TJ'


# ─────────────────────────────────────────────────────────────────────────────
# 内容流解析
# ─────────────────────────────────────────────────────────────────────────────

_TM_RE = re.compile(
    rb"([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s+Tm"
)
_FONT_RE = re.compile(rb"(/\w+)\s+([\d.]+)\s+Tf")


def _find_balanced_string(data: bytes, start: int) -> tuple:
    """从 start 位置（必须是 '('）开始，找到匹配的 ')'。
    返回 (start_inclusive, end_exclusive)，处理转义和嵌套括号。
    """
    assert data[start:start+1] == b"(", "期望 '(' 在 start 处"
    depth = 0
    i = start
    while i < len(data):
        b = data[i:i+1]
        if b == b"\\":
            i += 2
            continue
        if b == b"(":
            depth += 1
        elif b == b")":
            depth -= 1
            if depth == 0:
                return start, i + 1
        i += 1
    raise ValueError(f"未匹配的 '(' 在偏移 {start}")


def _decode_string(raw: bytes, cmap: dict) -> str:
    """通过字体 CMap 解码原始 PDF 字符串字节。
    先尝试 2 字节编码，再尝试 1 字节编码。
    """
    result = []
    i = 0
    while i < len(raw):
        if i + 1 < len(raw):
            two = (raw[i] << 8) | raw[i + 1]
            if two in cmap:
                result.append(cmap[two])
                i += 2
                continue
        one = raw[i]
        result.append(cmap.get(one, "\ufffd"))
        i += 1
    return "".join(result)


def parse_text_operations(content_stream: bytes, font_cmaps: Optional[dict] = None) -> list:
    """解析 PDF 内容流，返回 TextOperation 对象列表。

    font_cmaps: {'/TT2': {code_int: char, ...}, ...}
    """
    if font_cmaps is None:
        font_cmaps = {}

    ops: list = []
    data = content_stream
    cur_font = ""
    cur_size = 0.0
    cur_tm_x = 0.0
    cur_tm_y = 0.0

    i = 0
    n = len(data)

    while i < n:
        m = _TM_RE.match(data, i)
        if m:
            cur_tm_x = float(m.group(5))
            cur_tm_y = float(m.group(6))
            i = m.end()
            continue

        m = _FONT_RE.match(data, i)
        if m:
            cur_font = m.group(1).decode("latin-1")
            cur_size = float(m.group(2))
            i = m.end()
            continue

        if data[i:i+1] == b"(":
            try:
                str_start, str_end = _find_balanced_string(data, i)
            except ValueError:
                i += 1
                continue

            rest = data[str_end:].lstrip(b" \t\r\n")
            if rest[:2] == b"Tj":
                raw_content = data[str_start + 1: str_end - 1]
                cmap = font_cmaps.get(cur_font, {})
                decoded = (
                    _decode_string(raw_content, cmap)
                    if cmap
                    else raw_content.decode("latin-1", errors="replace")
                )
                ops.append(TextOperation(
                    tm_x=cur_tm_x,
                    tm_y=cur_tm_y,
                    font=cur_font,
                    size=cur_size,
                    text_encoded=data[str_start:str_end].decode("latin-1"),
                    text_decoded=decoded,
                    offset=str_start,
                    length=str_end - str_start,
                    op_type="Tj",
                ))
                i = str_end
                continue

        if data[i:i+1] == b"[":
            j = data.find(b"]", i)
            if j != -1:
                arr_rest = data[j + 1:].lstrip(b" \t\r\n")
                if arr_rest[:2] == b"TJ":
                    arr_data = data[i + 1: j]
                    strings = []
                    k = 0
                    while k < len(arr_data):
                        if arr_data[k:k+1] == b"(":
                            try:
                                s_start, s_end = _find_balanced_string(arr_data, k)
                                strings.append(arr_data[s_start + 1: s_end - 1])
                                k = s_end
                            except ValueError:
                                k += 1
                        else:
                            k += 1

                    raw_content = b"".join(strings)
                    cmap = font_cmaps.get(cur_font, {})
                    decoded = (
                        _decode_string(raw_content, cmap)
                        if cmap
                        else raw_content.decode("latin-1", errors="replace")
                    )
                    ops.append(TextOperation(
                        tm_x=cur_tm_x,
                        tm_y=cur_tm_y,
                        font=cur_font,
                        size=cur_size,
                        text_encoded=data[i: j + 1].decode("latin-1"),
                        text_decoded=decoded,
                        offset=i,
                        length=j + 1 - i,
                        op_type="TJ",
                    ))
                    i = j + 1
                    continue

        i += 1

    return ops


def _group_ops_by_line(ops: list, y_tolerance: float = 2.0) -> list:
    """按 Y 坐标将 TextOperation 分组（同一行的操作在同一组）。"""
    if not ops:
        return []

    sorted_ops = sorted(ops, key=lambda o: (-o.tm_y, o.tm_x))
    groups: list = []
    current_group: list = [sorted_ops[0]]
    current_y = sorted_ops[0].tm_y

    for op in sorted_ops[1:]:
        if abs(op.tm_y - current_y) <= y_tolerance:
            current_group.append(op)
        else:
            groups.append(sorted(current_group, key=lambda o: o.tm_x))
            current_group = [op]
            current_y = op.tm_y

    groups.append(sorted(current_group, key=lambda o: o.tm_x))
    return groups


def replace_across_tj(
    content_stream: bytes,
    old_text: str,
    new_text: str,
    font_cmaps: Optional[dict] = None,
) -> bytes:
    """
    替换可能跨越多个 Tj 操作的文本（流级别）。

    移植自 PyPI 包 advanced.py::replace_across_tj()。
    """
    if font_cmaps is None:
        font_cmaps = {}

    ops = parse_text_operations(content_stream, font_cmaps)
    if not ops:
        return content_stream

    lines = _group_ops_by_line(ops)
    stream = bytearray(content_stream)
    cumulative_delta = 0

    for line in lines:
        line_text = ""
        char_sources: list = []
        for op_idx, op in enumerate(line):
            for char_idx, ch in enumerate(op.text_decoded):
                line_text += ch
                char_sources.append((op_idx, char_idx))

        pos = line_text.find(old_text)
        if pos == -1:
            continue

        first_char_src = char_sources[pos]
        last_char_src = char_sources[pos + len(old_text) - 1]
        first_op_idx = first_char_src[0]
        last_op_idx = last_char_src[0]
        touched_ops = line[first_op_idx: last_op_idx + 1]

        if len(touched_ops) == 1:
            op = touched_ops[0]
            cmap = font_cmaps.get(op.font, {})
            reverse_cmap = {v: k for k, v in cmap.items()}

            if all(c in reverse_cmap for c in new_text):
                encoded_new = bytes(reverse_cmap[c] for c in new_text)
                new_paren = b"(" + encoded_new + b")"
            else:
                try:
                    new_paren = b"(" + new_text.encode("latin-1") + b")"
                except UnicodeEncodeError:
                    print(f"[L3] 无法编码 '{new_text}'，跳过")
                    continue

            adjusted_offset = op.offset + cumulative_delta
            stream[adjusted_offset: adjusted_offset + op.length] = new_paren
            cumulative_delta += len(new_paren) - op.length
            print(f"[L3] 单 op 替换 Y={op.tm_y:.1f}: '{op.text_decoded}' -> '{new_text}'")

        else:
            first_op = touched_ops[0]
            last_op = touched_ops[-1]
            cmap = font_cmaps.get(first_op.font, {})
            reverse_cmap = {v: k for k, v in cmap.items()}

            if all(c in reverse_cmap for c in new_text):
                encoded_new = bytes(reverse_cmap[c] for c in new_text)
                new_paren = b"(" + encoded_new + b") Tj"
            else:
                try:
                    new_paren = b"(" + new_text.encode("latin-1") + b") Tj"
                except UnicodeEncodeError:
                    print(f"[L3] 无法跨 op 编码 '{new_text}'，跳过")
                    continue

            adjusted_first = first_op.offset + cumulative_delta
            adjusted_last_end = last_op.offset + last_op.length + cumulative_delta

            suffix_view = stream[adjusted_last_end: adjusted_last_end + 10]
            if b"Tj" not in suffix_view and b"TJ" not in suffix_view:
                print("[L3] 无法定位 last op 后的 Tj，跳过")
                continue

            ws_tj_end = adjusted_last_end
            while ws_tj_end < len(stream) and stream[ws_tj_end:ws_tj_end+1] in (b" ", b"\t", b"\r", b"\n"):
                ws_tj_end += 1
            if stream[ws_tj_end: ws_tj_end + 2] in (b"Tj", b"TJ"):
                ws_tj_end += 2

            stream[adjusted_first: ws_tj_end] = new_paren
            cumulative_delta += len(new_paren) - (ws_tj_end - adjusted_first)
            print(f"[L3] 多 op 替换（{len(touched_ops)} 个 op）Y={first_op.tm_y:.1f}: '{old_text}' -> '{new_text}'")

    return bytes(stream)


# ─────────────────────────────────────────────────────────────────────────────
# 主入口期望的文件级接口
# ─────────────────────────────────────────────────────────────────────────────

def replace_multi_tj(
    input_path: str,
    old_text: str,
    new_text: str,
    output_path: str,
    page_num: int = 0,
) -> bool:
    """
    文件级 L3 多 Tj 替换接口，与 pdf_text_replace.py 的调用签名一致。

    1. 打开 PDF，收集字体 CMap 映射
    2. 对目标页所有内容流执行跨 Tj 替换
    3. 将结果写入 output_path

    返回 True 表示至少有一个替换成功，False 表示未找到目标文本。
    """
    reader = PdfReader(input_path)
    page = reader.pages[page_num]

    # 收集所有字体的 CMap
    font_cmaps: dict = {}
    fonts = page.get("/Resources", {}).get("/Font", {})
    for fname, fref in fonts.items():
        font = fref.get_object()
        if "/ToUnicode" not in font:
            continue
        try:
            cmap_str = font["/ToUnicode"].get_object().get_data().decode("latin-1")
            font_cmaps[fname] = _parse_cmap(cmap_str)
        except Exception as e:
            print(f"[L3] 解析字体 {fname} CMap 失败: {e}")

    writer = PdfWriter()
    writer.append_pages_from_reader(reader)
    out_page = writer.pages[page_num]

    contents = out_page["/Contents"]
    if not isinstance(contents, list):
        contents = [contents]

    replaced = False
    for content_ref in contents:
        content_obj = content_ref.get_object()
        raw = content_obj.get_data()

        # 预检：decoded text 中是否存在 old_text
        # （通过 CMap 解码后判断，避免无谓处理）
        modified = replace_across_tj(raw, old_text, new_text, font_cmaps)
        if modified != raw:
            content_obj.set_data(modified)
            replaced = True

    if replaced:
        with open(output_path, "wb") as f:
            writer.write(f)
    else:
        print(f"[L3] '{old_text}' 未在任何内容流中找到")

    return replaced
