#!/usr/bin/env python3
"""
v2_l2_varlen.py — L2 变长替换模块（Variable-Length Replacement）

将 PyPI 包 pdf_text_replace.features 中的实现适配为
openclaw 主入口（pdf_text_replace.py）期望的文件级接口：

    replace_variable_length(input_path, old_text, new_text, output_path, page_num) -> bool

策略：
  Strategy A - Tz Horizontal Scaling（字符数差异 ≤ 30%）
  Strategy B - Position Reflow（字符数差异 > 30%）
"""

from __future__ import annotations

import io
import re
from pathlib import Path
from typing import Optional

from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject, NumberObject, ArrayObject, DictionaryObject, DecodedStreamObject
from fontTools.ttLib import TTFont
from fontTools import subset as ft_subset


# ─────────────────────────────────────────────────────────────────────────────
# 辅助函数（与 features.py 保持一致）
# ─────────────────────────────────────────────────────────────────────────────

_FONT_FALLBACKS = {
    "serif": [
        "/System/Library/Fonts/Supplemental/Georgia Bold.ttf",
        "/System/Library/Fonts/Supplemental/Times New Roman Bold.ttf",
        "/System/Library/Fonts/Supplemental/Georgia.ttf",
        "/System/Library/Fonts/Supplemental/Times New Roman.ttf",
    ],
    "sans": [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/System/Library/Fonts/Supplemental/Verdana Bold.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
    ],
}


def _find_system_font(prefer_serif: bool = True) -> str:
    key = "serif" if prefer_serif else "sans"
    for path in _FONT_FALLBACKS[key]:
        if Path(path).exists():
            return path
    for p in Path("/usr/share/fonts").rglob("*.ttf"):
        if "bold" in p.name.lower():
            return str(p)
    raise FileNotFoundError("未找到合适的系统字体")


def _parse_cmap(cmap_data: str) -> dict:
    """解析 PDF ToUnicode CMap -> {byte_code: unicode_char}"""
    mapping = {}
    # Format 1: beginbfrange <XX><XX><YYYY>
    for m in re.finditer(r"<([0-9a-fA-F]+)><\1><([0-9a-fA-F]+)>", cmap_data):
        code = int(m.group(1), 16)
        uchar = chr(int(m.group(2), 16))
        mapping[code] = uchar
    # Format 2: beginbfchar <XX> <YYYY>（两种格式合并）
    for m in re.finditer(r"<([0-9a-fA-F]{2,4})>\s+<([0-9a-fA-F]{4})>", cmap_data):
        src_hex = m.group(1)
        dst_hex = m.group(2)
        if dst_hex == "0000":
            continue
        code = int(src_hex, 16)
        if code not in mapping:  # 不覆盖已有映射
            uchar = chr(int(dst_hex, 16))
            mapping[code] = uchar
    return mapping


def _create_font_subset(system_font_path: str, chars: str) -> bytes:
    font = TTFont(system_font_path)
    subsetter = ft_subset.Subsetter()
    subsetter.populate(text=chars)
    subsetter.subset(font)
    buf = io.BytesIO()
    font.save(buf)
    return buf.getvalue()


def _build_pdf_font(writer: PdfWriter, subset_data: bytes, chars: str):
    fstream = DecodedStreamObject()
    fstream.set_data(subset_data)
    fstream[NameObject("/Length1")] = NumberObject(len(subset_data))

    fdesc = DictionaryObject()
    for k, v in [
        ("/Type", "/FontDescriptor"), ("/FontName", "/ZZZZZZ+ReplacementFont"),
        ("/Flags", 32), ("/ItalicAngle", 0), ("/Ascent", 917),
        ("/Descent", -230), ("/CapHeight", 692), ("/StemV", 139),
    ]:
        fdesc[NameObject(k)] = (
            NumberObject(v) if isinstance(v, int) else NameObject(v)
        )
    fdesc[NameObject("/FontBBox")] = ArrayObject(
        [NumberObject(x) for x in [-222, -218, 1389, 939]]
    )
    fdesc[NameObject("/FontFile2")] = writer._add_object(fstream)

    ranges = "\n".join(
        f"<{ord(c):02X}><{ord(c):02X}><{ord(c):04X}>" for c in chars
    )
    cmap_bytes = (
        "/CIDInit /ProcSet findresource begin\n"
        "12 dict begin begincmap\n"
        "/CIDSystemInfo << /Registry (Adobe) /Ordering (UCS) /Supplement 0 >> def\n"
        "/CMapName /Adobe-Identity-UCS def /CMapType 2 def\n"
        "1 begincodespacerange <00><FF> endcodespacerange\n"
        f"{len(chars)} beginbfrange\n{ranges}\n"
        "endbfrange\nendcmap\n"
        "CMapName currentdict /CMap defineresource pop end end\n"
    ).encode("latin-1")
    tu_stream = DecodedStreamObject()
    tu_stream.set_data(cmap_bytes)

    codes = sorted(ord(c) for c in chars)
    fdict = DictionaryObject()
    for k, v in [
        ("/Type", "/Font"), ("/Subtype", "/TrueType"),
        ("/BaseFont", "/ZZZZZZ+ReplacementFont"),
        ("/Encoding", "/WinAnsiEncoding"),
    ]:
        fdict[NameObject(k)] = NameObject(v)
    fdict[NameObject("/FirstChar")] = NumberObject(codes[0])
    fdict[NameObject("/LastChar")] = NumberObject(codes[-1])

    tt = TTFont(io.BytesIO(subset_data))
    hmtx = tt["hmtx"]
    upem = tt["head"].unitsPerEm
    best_cmap = tt.getBestCmap()
    widths = []
    for code in range(codes[0], codes[-1] + 1):
        gname = best_cmap.get(code)
        w = hmtx[gname][0] * 1000 // upem if gname else 0
        widths.append(NumberObject(w))
    fdict[NameObject("/Widths")] = ArrayObject(widths)
    fdict[NameObject("/FontDescriptor")] = writer._add_object(fdesc)
    fdict[NameObject("/ToUnicode")] = writer._add_object(tu_stream)
    return writer._add_object(fdict)


def _char_advance_pts(char_width: int, upem: int, font_size: int) -> float:
    return (char_width / upem) * font_size


def _extract_tm_before(stream_str: str, up_to_idx: int) -> Optional[re.Match]:
    block = stream_str[max(0, up_to_idx - 600): up_to_idx]
    matches = list(re.finditer(
        r"([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s+Tm",
        block
    ))
    return matches[-1] if matches else None


# ─────────────────────────────────────────────────────────────────────────────
# 核心替换函数（page 对象级别，来自 features.py）
# ─────────────────────────────────────────────────────────────────────────────

def _replace_variable_length_page(
    page, writer: PdfWriter, old_text: str, new_text: str, font_info: dict
) -> bool:
    """
    在单个 page 对象上执行变长替换。
    直接移植自 PyPI 包的 features.py::replace_variable_length()。
    """
    char_to_code: dict = font_info["char_to_code"]
    font_name: str = font_info["font_name"]
    char_width: int = font_info.get("char_width", 1000)
    upem: int = font_info.get("upem", 1000)
    font_size: int = font_info.get("font_size", 12)

    old_len = len(old_text)
    new_len = len(new_text)
    delta_ratio = abs(new_len - old_len) / max(old_len, 1)
    use_tz_scaling = delta_ratio <= 0.30

    try:
        encoded_old = "".join(chr(char_to_code[c]) for c in old_text)
    except KeyError as e:
        print(f"[L2] 字符 {e} 不在字体 CMap 中")
        return False

    contents = page["/Contents"]
    if not isinstance(contents, list):
        contents = [contents]

    found = False
    for content_ref in contents:
        content_obj = content_ref.get_object()
        raw = content_obj.get_data()
        decoded = raw.decode("latin-1")

        needle = f"({encoded_old})"
        if needle not in decoded:
            continue

        found = True
        idx = decoded.find(needle)
        missing_chars = [c for c in new_text if c not in char_to_code]

        if missing_chars:
            sys_font = _find_system_font(prefer_serif=True)
            subset_data = _create_font_subset(sys_font, "".join(missing_chars))
            font_ref = _build_pdf_font(writer, subset_data, "".join(missing_chars))
            existing = set(str(k) for k in page["/Resources"]["/Font"].keys())
            new_font_name = None
            for i in range(9, 30):
                cand = f"/TT{i}"
                if cand not in existing:
                    new_font_name = cand
                    break
            page["/Resources"]["/Font"][NameObject(new_font_name)] = font_ref

            tm_match = _extract_tm_before(decoded, idx)
            if not tm_match:
                print("[L2] 未找到 Tm，中止")
                return False

            tx, ty = tm_match.group(5), tm_match.group(6)
            prefix = ""
            for ch in new_text:
                if ch in char_to_code:
                    prefix += ch
                else:
                    break
            suffix = new_text[len(prefix):]
            encoded_prefix = "".join(chr(char_to_code[c]) for c in prefix) if prefix else ""
            char_advance = _char_advance_pts(char_width, upem, font_size)
            x_overlay = float(tx) + len(prefix) * char_advance

            if prefix:
                overlay = (
                    f"({encoded_prefix}) Tj "
                    f"ET BT {font_name} {font_size} Tf "
                    f"{font_size} 0 0 {font_size} {x_overlay:.4f} {ty} Tm "
                    f"({suffix}) Tj"
                )
            else:
                overlay = (
                    f"ET BT {new_font_name} {font_size} Tf "
                    f"{font_size} 0 0 {font_size} {tx} {ty} Tm "
                    f"({new_text}) Tj"
                )

            decoded = decoded.replace(f"{needle} Tj", overlay)
            content_obj.set_data(decoded.encode("latin-1"))
            print(f"[L2] overlay-font '{old_text}' -> '{new_text}'")
            return True

        encoded_new = "".join(chr(char_to_code[c]) for c in new_text)

        if use_tz_scaling:
            scale = old_len / new_len * 100.0
            replacement = f"{scale:.4f} Tz ({encoded_new}) Tj 100 Tz"
            decoded = decoded.replace(f"{needle} Tj", replacement)
            print(f"[L2] Tz={scale:.1f}% '{old_text}' -> '{new_text}'")
        else:
            decoded = decoded.replace(needle, f"({encoded_new})")
            tm_match = _extract_tm_before(decoded, decoded.find(f"({encoded_new})"))
            if not tm_match:
                print("[L2] reflow 模式未找到 Tm，保持现状")
                content_obj.set_data(decoded.encode("latin-1"))
                return True

            ref_y = float(tm_match.group(6))
            char_advance = _char_advance_pts(char_width, upem, font_size)
            width_delta = (new_len - old_len) * char_advance

            def _shift_tm(m: re.Match) -> str:
                a2, b2, c2, d2, tx2, ty2 = (
                    m.group(1), m.group(2), m.group(3),
                    m.group(4), m.group(5), m.group(6),
                )
                if abs(float(ty2) - ref_y) < 1.0:
                    new_tx = float(tx2) + width_delta
                    return f"{a2} {b2} {c2} {d2} {new_tx:.4f} {ty2} Tm"
                return m.group(0)

            replaced_idx = decoded.find(f"({encoded_new})")
            before = decoded[:replaced_idx]
            after = decoded[replaced_idx:]

            first_tm_in_after = re.search(
                r"([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s+Tm",
                after,
            )
            if first_tm_in_after:
                split_at = first_tm_in_after.end()
                after_rest = after[split_at:]
                after_rest = re.sub(
                    r"([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s+Tm",
                    _shift_tm,
                    after_rest,
                )
                decoded = before + after[:split_at] + after_rest

            print(f"[L2] reflow delta={width_delta:+.2f}pt '{old_text}' -> '{new_text}'")

        content_obj.set_data(decoded.encode("latin-1"))
        return True

    if not found:
        print(f"[L2] '{old_text}' 未在内容流中找到")
    return found


# ─────────────────────────────────────────────────────────────────────────────
# 主入口期望的文件级接口
# ─────────────────────────────────────────────────────────────────────────────

def replace_variable_length(
    input_path: str,
    old_text: str,
    new_text: str,
    output_path: str,
    page_num: int = 0,
) -> bool:
    """
    文件级 L2 变长替换接口，与 pdf_text_replace.py 的调用签名一致。

    1. 打开 PDF，找到包含 old_text 的字体及其 CMap
    2. 调用页面级替换函数
    3. 将结果写入 output_path

    返回 True 表示替换成功，False 表示失败。
    """
    reader = PdfReader(input_path)
    page = reader.pages[page_num]

    fonts = page.get("/Resources", {}).get("/Font", {})
    font_info = None

    for fname, fref in fonts.items():
        font = fref.get_object()
        if "/ToUnicode" not in font:
            continue
        cmap_str = font["/ToUnicode"].get_object().get_data().decode("latin-1")
        mapping = _parse_cmap(cmap_str)
        reverse = {v: k for k, v in mapping.items()}
        if not all(c in reverse for c in old_text):
            continue

        # 从 FontFile2 读取字体度量
        char_width = 1000
        upem = 1000
        font_size = 12
        try:
            fd = font.get("/FontDescriptor")
            if fd:
                fd_obj = fd.get_object()
                if "/FontFile2" in fd_obj:
                    fdata = fd_obj["/FontFile2"].get_object().get_data()
                    tt = TTFont(io.BytesIO(fdata))
                    upem = tt["head"].unitsPerEm
                    hmtx = tt["hmtx"]
                    font_cmap_tables = tt["cmap"].tables
                    font_internal_cmap = {}
                    for tbl in font_cmap_tables:
                        if tbl.cmap:
                            font_internal_cmap = tbl.cmap
                            break
                    widths = []
                    for code_val in mapping:
                        gname = font_internal_cmap.get(code_val)
                        if gname and gname in hmtx.metrics:
                            widths.append(hmtx[gname][0])
                    if widths:
                        char_width = widths[0]
        except Exception as e:
            print(f"[L2] 字体度量读取失败，使用默认值: {e}")

        # 从 Tf 操作读取字体大小
        try:
            contents = page["/Contents"]
            if not isinstance(contents, list):
                contents = [contents]
            for cref in contents:
                raw = cref.get_object().get_data().decode("latin-1")
                for m in re.finditer(rf"{re.escape(fname)}\s+([\d.]+)\s+Tf", raw):
                    font_size = int(float(m.group(1)))
                    break
        except Exception:
            pass

        font_info = {
            "font_name": fname,
            "char_to_code": reverse,
            "code_to_char": mapping,
            "char_width": char_width,
            "upem": upem,
            "font_size": font_size,
        }
        break

    if font_info is None:
        print(f"[L2] 未找到包含 '{old_text}' 所有字符的字体")
        return False

    writer = PdfWriter()
    writer.append_pages_from_reader(reader)
    out_page = writer.pages[page_num]

    ok = _replace_variable_length_page(out_page, writer, old_text, new_text, font_info)
    if ok:
        with open(output_path, "wb") as f:
            writer.write(f)
    return ok
