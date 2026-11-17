#!/usr/bin/env python3
"""Standard-library PDF text extraction for packet-audit.

The audit has to read the documents people actually submit, and those are PDFs. Requiring
`pypdf` meant a PDF was either readable or reported unreadable depending on whether someone
happened to have a third-party package installed — a silent difference in what the audit
checked. This module reads the text layer itself:

  - objects, including those packed inside object streams (/Type /ObjStm)
  - FlateDecode, ASCIIHexDecode and ASCII85Decode filters
  - page order from the page tree (/Catalog -> /Pages -> /Kids), not file order
  - text-showing operators Tj, TJ, ' and " with per-font /ToUnicode CMaps

It is deliberately not a renderer and not OCR. An encrypted PDF, a scanned page and a PDF
whose text lives only in an image all raise the same honest error the caller already reports
as `PA-R01`, and the message says which case it is.

No third-party imports: zlib, base64 and re only.
"""

from __future__ import annotations

import base64
import re
import zlib
from pathlib import Path

OBJ_RE = re.compile(rb"(?<![0-9])(\d+)\s+(\d+)\s+obj\b")
STREAM_RE = re.compile(rb"stream\r?\n")
REF_RE = re.compile(rb"(\d+)\s+\d+\s+R")

WHITESPACE = b"\x00\t\n\x0c\r "
DELIMITERS = b"()<>[]{}/%"


class PDFError(RuntimeError):
    """Raised when the text layer cannot be read; the message is shown to the user."""


# ---------------------------------------------------------------------------
# object layer
# ---------------------------------------------------------------------------

def _objects(data: bytes) -> dict[int, tuple[bytes, bytes | None]]:
    """Map object number -> (dictionary bytes, decoded-or-raw stream bytes)."""
    found: dict[int, tuple[bytes, bytes | None]] = {}
    for match in OBJ_RE.finditer(data):
        num = int(match.group(1))
        start = match.end()
        end = data.find(b"endobj", start)
        if end == -1:
            end = len(data)
        head_end = end
        stream = None
        stream_at = data.find(b"stream", start, end)
        if stream_at != -1:
            header = data[start:stream_at]
            body_start = stream_at + len(b"stream")
            # the keyword is followed by CRLF or LF (or a lone CR in the wild)
            while body_start < len(data) and data[body_start:body_start + 1] in (b"\r", b"\n"):
                body_start += 1
            stream_end = data.find(b"endstream", body_start)
            if stream_end == -1:
                stream_end = end
            stream = data[body_start:stream_end]
            head_end = stream_at
            end = data.find(b"endobj", stream_end)
            if end == -1:
                end = len(data)
            header = data[start:head_end]
        else:
            header = data[start:end]
        found.setdefault(num, (header, stream))
    return found


def _decode_filter(header: bytes, raw: bytes | None) -> bytes:
    if raw is None:
        return b""
    filters = re.findall(rb"/(FlateDecode|Fl|ASCIIHexDecode|AHx|ASCII85Decode|A85)", header)
    data = raw
    for name in filters:
        try:
            if name in (b"FlateDecode", b"Fl"):
                try:
                    data = zlib.decompress(data)
                except zlib.error:
                    data = zlib.decompressobj().decompress(data)
            elif name in (b"ASCIIHexDecode", b"AHx"):
                hexed = re.sub(rb"[^0-9A-Fa-f]", b"", data.split(b">")[0])
                if len(hexed) % 2:
                    hexed += b"0"
                data = bytes.fromhex(hexed.decode("ascii"))
            elif name in (b"ASCII85Decode", b"A85"):
                payload = data.strip()
                if payload.startswith(b"<~"):
                    payload = payload[2:]
                if payload.endswith(b"~>"):
                    payload = payload[:-2]
                data = base64.a85decode(re.sub(rb"\s", b"", payload))
        except Exception:  # noqa: BLE001 - an undecodable filter means "no text here"
            return b""
    return data


def _expand_object_streams(objs: dict[int, tuple[bytes, bytes | None]]) -> None:
    """Unpack /Type /ObjStm containers so page dictionaries inside them are visible."""
    for _num, (head, stream) in list(objs.items()):
        if not re.search(rb"/Type\s*/ObjStm", head) or not stream:
            continue
        body = _decode_filter(head, stream)
        count = re.search(rb"/N\s+(\d+)", head)
        first = re.search(rb"/First\s+(\d+)", head)
        if not body or not count or not first:
            continue
        n, offset0 = int(count.group(1)), int(first.group(1))
        header = body[:offset0].split()
        pairs = []
        for i in range(0, min(len(header), 2 * n) - 1, 2):
            try:
                pairs.append((int(header[i]), int(header[i + 1])))
            except ValueError:
                break
        for idx, (obj_num, offset) in enumerate(pairs):
            end = pairs[idx + 1][1] if idx + 1 < len(pairs) else len(body) - offset0
            objs.setdefault(obj_num, (body[offset0 + offset: offset0 + end], None))


def _object_ref(header: bytes, key: bytes) -> int | None:
    match = re.search(key + rb"\s+(\d+)\s+\d+\s+R", header)
    return int(match.group(1)) if match else None


def _object_refs(header: bytes, key: bytes) -> list[int]:
    inline = re.search(key + rb"\s*\[(.*?)\]", header, re.S)
    if inline:
        return [int(m.group(1)) for m in REF_RE.finditer(inline.group(1))]
    single = _object_ref(header, key)
    return [single] if single is not None else []


def _page_order(objs: dict[int, tuple[bytes, bytes | None]]) -> list[int]:
    catalog = next((n for n, (head, _s) in objs.items()
                    if re.search(rb"/Type\s*/Catalog", head)), None)
    order: list[int] = []
    seen: set[int] = set()

    def walk(num: int, depth: int = 0) -> None:
        if depth > 64 or num in seen or num not in objs:
            return
        seen.add(num)
        head, _stream = objs[num]
        if re.search(rb"/Type\s*/Pages\b", head):
            for kid in _object_refs(head, rb"/Kids"):
                walk(kid, depth + 1)
        elif re.search(rb"/Type\s*/Page(?![s\w])", head):
            order.append(num)

    if catalog is not None:
        walk(_object_ref(objs[catalog][0], rb"/Pages") or -1)
    if not order:
        order = sorted(n for n, (head, _s) in objs.items()
                       if re.search(rb"/Type\s*/Page(?![s\w])", head))
    return order


# ---------------------------------------------------------------------------
# font maps
# ---------------------------------------------------------------------------

def _parse_tounicode(data: bytes) -> dict[int, str]:
    text = data.decode("latin-1", errors="replace")
    mapping: dict[int, str] = {}
    for block in re.findall(r"beginbfchar(.*?)endbfchar", text, re.S):
        for src, dst in re.findall(r"<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>", block):
            try:
                mapping[int(src, 16)] = bytes.fromhex(dst).decode("utf-16-be", errors="replace")
            except ValueError:
                continue
    for block in re.findall(r"beginbfrange(.*?)endbfrange", text, re.S):
        pattern = re.compile(r"<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>\s*(?:<([0-9A-Fa-f]+)>|\[(.*?)\])", re.S)
        for lo, hi, dst, lst in pattern.findall(block):
            try:
                low, high = int(lo, 16), int(hi, 16)
            except ValueError:
                continue
            if high - low > 65535:
                continue
            if dst:
                base = bytes.fromhex(dst)
                for step, code in enumerate(range(low, high + 1)):
                    value = int.from_bytes(base, "big") + step
                    raw = value.to_bytes(max(len(base), 1), "big")
                    mapping[code] = (raw.decode("utf-16-be", errors="replace")
                                     if len(raw) % 2 == 0 else raw.decode("latin-1"))
            else:
                hexes = re.findall(r"<([0-9A-Fa-f]+)>", lst or "")
                for step, code in enumerate(range(low, high + 1)):
                    if step >= len(hexes):
                        break
                    try:
                        mapping[code] = bytes.fromhex(hexes[step]).decode("utf-16-be", errors="replace")
                    except ValueError:
                        continue
    return mapping


def _parse_widths(font_head: bytes, objs: dict[int, tuple[bytes, bytes | None]]) -> tuple[dict[int, float], float]:
    """Character code -> advance width in 1/1000 em, plus the default width."""
    # Type0: /W [ start [w1 w2 ...] | start end w ], default /DW (1000)
    w_ref = _object_ref(font_head, rb"/DW")
    default = 1000.0
    if w_ref is not None and w_ref in objs:
        default = _first_number(objs[w_ref][0]) or default
    widths: dict[int, float] = {}
    w_array = re.search(rb"/W\s*\[(.*?)\]\s*(?:/|>>)", font_head, re.S)
    if w_array:
        tokens = re.findall(rb"\[|\]|[0-9.]+", w_array.group(1))
        i = 0
        while i < len(tokens):
            if not tokens[i].isdigit():
                i += 1
                continue
            start = int(tokens[i])
            if i + 1 < len(tokens) and tokens[i + 1] == b"[":
                i += 2
                code = start
                while i < len(tokens) and tokens[i] != b"]":
                    try:
                        widths[code] = float(tokens[i])
                    except ValueError:
                        pass
                    code += 1
                    i += 1
                i += 1
            elif i + 2 < len(tokens):
                try:
                    end, width = int(tokens[i + 1]), float(tokens[i + 2])
                except ValueError:
                    i += 1
                    continue
                if 0 <= end - start <= 4096:
                    for code in range(start, end + 1):
                        widths[code] = width
                i += 3
            else:
                i += 1
        if widths:
            return widths, default

    # simple fonts: /FirstChar + /Widths
    first = re.search(rb"/FirstChar\s+(\d+)", font_head)
    array_ref = _object_ref(font_head, rb"/Widths")
    array_text = font_head
    if array_ref is not None and array_ref in objs:
        array_text = objs[array_ref][0]
    widths_body = re.search(rb"/Widths\s*\[(.*?)\]", array_text, re.S)
    if first and widths_body:
        start = int(first.group(1))
        for offset, value in enumerate(re.findall(rb"[0-9.]+", widths_body.group(1))):
            try:
                widths[start + offset] = float(value)
            except ValueError:
                pass
    missing = re.search(rb"/MissingWidth\s+(\d+)", font_head)
    if missing:
        default = float(missing.group(1))
    return widths, default


def _first_number(data: bytes) -> float | None:
    match = re.search(rb"[-+]?[0-9]*\.?[0-9]+", data)
    if not match:
        return None
    try:
        return float(match.group(0))
    except ValueError:
        return None


def _page_fonts(head: bytes, objs: dict[int, tuple[bytes, bytes | None]]) -> dict[str, dict]:
    """font resource name (/F1) -> {cmap, wide, widths, default_width}."""
    resources = head
    res_ref = _object_ref(head, rb"/Resources")
    if res_ref is not None and res_ref in objs:
        resources = objs[res_ref][0]
    fonts: dict[str, dict] = {}
    font_ref = _object_ref(resources, rb"/Font")
    if font_ref is not None and font_ref in objs:
        resources = objs[font_ref][0]
    table = re.search(rb"/Font\s*<<(.*?)>>", resources, re.S)
    block = table.group(1) if table else resources
    for name, num in re.findall(rb"/([A-Za-z0-9#+.-]+)\s+(\d+)\s+\d+\s+R", block):
        entry = objs.get(int(num))
        if not entry:
            continue
        font_head = entry[0]
        # Type0 / Identity encodings address glyphs with two-byte codes even when every
        # code in the CMap happens to be below 0x100 (Identity-H does exactly that).
        wide = bool(re.search(rb"/Subtype\s*/Type0|/Identity-[HV]", font_head))
        to_unicode = _object_ref(font_head, rb"/ToUnicode")
        cmap: dict[int, str] = {}
        if to_unicode is not None and to_unicode in objs:
            target_head, target_stream = objs[to_unicode]
            cmap = _parse_tounicode(_decode_filter(target_head, target_stream))
        if cmap and max(cmap) > 0xFF:
            wide = True
        widths, default_width = _parse_widths(font_head, objs)
        fonts[name.decode("latin-1")] = {
            "cmap": cmap, "wide": wide, "widths": widths, "default_width": default_width,
        }
    return fonts


# ---------------------------------------------------------------------------
# content streams
# ---------------------------------------------------------------------------

def _read_string(data: bytes, index: int) -> tuple[bytes, int]:
    """Read a PDF literal string starting after '('; returns (bytes, next index)."""
    out = bytearray()
    depth = 1
    i = index
    while i < len(data):
        ch = data[i:i + 1]
        if ch == b"\\":
            nxt = data[i + 1:i + 2]
            simple = {b"n": b"\n", b"r": b"\r", b"t": b"\t", b"b": b"\b", b"f": b"\f",
                      b"(": b"(", b")": b")", b"\\": b"\\"}
            if nxt in simple:
                out += simple[nxt]
                i += 2
                continue
            octal = re.match(rb"[0-7]{1,3}", data[i + 1:i + 4])
            if octal:
                out.append(int(octal.group(0), 8) & 0xFF)
                i += 1 + len(octal.group(0))
                continue
            if nxt in (b"\n", b"\r"):
                i += 2
                continue
            i += 1
            continue
        if ch == b"(":
            depth += 1
        elif ch == b")":
            depth -= 1
            if depth == 0:
                return bytes(out), i + 1
        out += ch
        i += 1
    return bytes(out), i


def _decode_pdf_string(raw: bytes, font: dict | None) -> str:
    cmap = (font or {}).get("cmap") or {}
    if cmap:
        if (font or {}).get("wide"):
            chars = [cmap.get(int.from_bytes(raw[i:i + 2], "big"), "")
                     for i in range(0, len(raw) - 1, 2)]
        else:
            chars = [cmap.get(byte, chr(byte)) for byte in raw]
        joined = "".join(chars)
        if joined.strip():
            return joined
    return raw.decode("latin-1", errors="replace")


def _string_width(raw: bytes, font: dict | None, size: float, hscale: float) -> float:
    """Advance width of a shown string in text-space units."""
    font = font or {}
    widths = font.get("widths") or {}
    default = font.get("default_width", 1000.0)
    if font.get("wide"):
        codes = [int.from_bytes(raw[i:i + 2], "big") for i in range(0, len(raw) - 1, 2)]
    else:
        codes = list(raw)
    total = sum(widths.get(code, default) for code in codes)
    return total / 1000.0 * size * hscale


def _content_text(content: bytes, fonts: dict[str, dict]) -> str:
    """Walk a content stream and return the text it draws.

    Words and lines are reconstructed from the text-positioning operators, because plenty of
    PDFs position every glyph individually (`(T) Tj 33 0 Td (D) Tj`): emitting a separator for
    every positioning move turns "TD Canada Trust" into "T D C a n a d a". The pen advances by
    the font's own /Widths (or /W) for each shown string, and a separator is only written when
    the next string starts measurably beyond that pen.
    """
    out: list[str] = []
    operands: list[object] = []
    font: dict | None = None
    size = 12.0
    hscale = 1.0
    leading = 0.0
    line_x = line_y = 0.0
    pen_x = pen_y = 0.0
    drawn = False
    i = 0
    length = len(content)

    def separator(target_x: float, target_y: float) -> str:
        if not drawn:
            return ""
        if abs(target_y - pen_y) > 0.5 * size or target_x < pen_x - 0.6 * size:
            return "\n"
        if target_x - pen_x > 0.15 * size:
            return " "
        return ""

    while i < length:
        ch = content[i:i + 1]
        if ch in b" \t\r\n\x0c\x00":
            i += 1
            continue
        if ch == b"%":
            nl = content.find(b"\n", i)
            i = length if nl == -1 else nl + 1
            continue
        if ch == b"(":
            raw, i = _read_string(content, i + 1)
            operands.append(raw)
            continue
        if ch == b"<":
            if content[i:i + 2] == b"<<":
                depth, i = 1, i + 2
                while i < length and depth:
                    if content[i:i + 2] == b"<<":
                        depth, i = depth + 1, i + 2
                    elif content[i:i + 2] == b">>":
                        depth, i = depth - 1, i + 2
                    else:
                        i += 1
                operands.append(b"")
                continue
            close = content.find(b">", i)
            if close == -1:
                break
            hexed = re.sub(rb"[^0-9A-Fa-f]", b"", content[i + 1:close])
            if len(hexed) % 2:
                hexed += b"0"
            operands.append(bytes.fromhex(hexed.decode("ascii")) if hexed else b"")
            i = close + 1
            continue
        if ch == b"[":
            operands.append("[")
            i += 1
            continue
        if ch == b"]":
            items: list[object] = []
            while operands and operands[-1] != "[":
                items.append(operands.pop())
            if operands:
                operands.pop()
            operands.append(list(reversed(items)))
            i += 1
            continue
        if ch == b"/":
            end = i + 1
            while end < length and content[end:end + 1] not in WHITESPACE + DELIMITERS:
                end += 1
            operands.append(content[i:end].decode("latin-1"))
            i = end
            continue
        match = re.match(rb"[-+]?[0-9]*\.?[0-9]+", content[i:i + 24])
        if match:
            try:
                operands.append(float(match.group(0)))
            except ValueError:
                operands.append(0.0)
            i += len(match.group(0))
            continue
        end = i
        while end < length and content[end:end + 1] not in WHITESPACE + DELIMITERS:
            end += 1
        operator = content[i:end]
        i = end if end > i else i + 1

        if operator == b"Tf" and len(operands) >= 2:
            name = operands[-2]
            font = fonts.get(name.lstrip("/")) if isinstance(name, str) else None
            size = operands[-1] if isinstance(operands[-1], float) else size
        elif operator == b"Tz" and operands and isinstance(operands[-1], float):
            hscale = operands[-1] / 100.0
        elif operator == b"TL" and operands and isinstance(operands[-1], float):
            leading = operands[-1]
        elif operator == b"Tm" and len(operands) >= 6:
            x, y = operands[-2], operands[-1]
            if isinstance(x, float) and isinstance(y, float):
                line_x, line_y = x, y
        elif operator in (b"Td", b"TD") and len(operands) >= 2:
            tx, ty = operands[-2], operands[-1]
            if isinstance(tx, float) and isinstance(ty, float):
                line_x += tx
                line_y += ty
                if operator == b"TD":
                    leading = -ty
        elif operator == b"T*":
            line_y -= leading
        elif operator in (b"Tj", b"'", b'"', b"TJ") and operands:
            if operator in (b"'", b'"'):
                line_y -= leading
                out.append("\n")
            start = separator(line_x, line_y)
            if start:
                out.append(start)
            if operator == b"TJ":
                items = operands[-1]
                if isinstance(items, list):
                    for item in items:
                        if isinstance(item, bytes):
                            out.append(_decode_pdf_string(item, font))
                            pen_x = line_x + _string_width(item, font, size, hscale)
                        elif isinstance(item, float):
                            pen_x -= item / 1000.0 * size * hscale
                            if item <= -150:
                                out.append(" ")
            else:
                raw = operands[-1]
                if isinstance(raw, bytes):
                    out.append(_decode_pdf_string(raw, font))
                    pen_x = line_x + _string_width(raw, font, size, hscale)
            pen_y = line_y
            drawn = True
        if operator != b"[":
            operands = []
    return "".join(out)


# ---------------------------------------------------------------------------
# pages
# ---------------------------------------------------------------------------

def _page_content(head: bytes, objs: dict[int, tuple[bytes, bytes | None]]) -> bytes:
    chunks: list[bytes] = []
    for num in _object_refs(head, rb"/Contents"):
        entry = objs.get(num)
        if entry:
            chunks.append(_decode_filter(entry[0], entry[1]))
    return b"\n".join(chunks)


def extract_pages(path: Path | str) -> list[str]:
    """Return the text layer of each page, in page order.

    Raises PDFError when the file is encrypted, has no text layer, or cannot be parsed;
    the message is the reason the report shows for `PA-R01`.
    """
    path = Path(path)
    try:
        data = path.read_bytes()
    except OSError as exc:
        raise PDFError(f"cannot read file ({exc.strerror or exc})") from exc
    if not data.lstrip().startswith(b"%PDF"):
        raise PDFError("not a PDF file (no %PDF header)")
    if re.search(rb"/Encrypt\s", data):
        raise PDFError("pdf is encrypted; its text cannot be read without the password")

    objs = _objects(data)
    if not objs:
        raise PDFError("pdf structure could not be parsed (no objects found)")
    _expand_object_streams(objs)

    pages = _page_order(objs)
    if not pages:
        raise PDFError("pdf has no pages")

    texts: list[str] = []
    for num in pages:
        head, _stream = objs[num]
        try:
            fonts = _page_fonts(head, objs)
            texts.append(_content_text(_page_content(head, objs), fonts))
        except Exception:  # noqa: BLE001 - one unreadable page must not lose the rest
            texts.append("")
    if not any(t.strip() for t in texts):
        raise PDFError("pdf has no extractable text layer (scan or image-only)")
    return texts
