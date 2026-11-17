"""Measure a final document against requirements read from its reference.

These checks supplement, never replace, page-by-page visual comparison.
"""
from __future__ import annotations

import html
import math
import re
import unicodedata
import zipfile
from xml.etree import ElementTree as ET

_FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})")
_COMMENT = re.compile(r"<!--.*?-->", re.S)
_IMAGE = re.compile(r"!\[[^\]]*\]\([^)]*\)")
_LINK = re.compile(r"\[([^\]]*)\]\([^)]*\)")
_REF_LINK = re.compile(r"\[([^\]]+)\]\[[^\]]*\]")
_REF_DEF = re.compile(r"^ {0,3}\[(?!\^)[^\]]+\]:\s*\S")
_FOOTNOTE_DEF = re.compile(r"^ {0,3}\[\^[^\]]+\]:\s*")
_FOOTNOTE_REF = re.compile(r"\[\^[^\]]+\]")
_AUTOLINK = re.compile(r"<(https?://[^\s>]+)>")
_TAG = re.compile(r"</?[A-Za-z][^>]*>")
_HEADING = re.compile(r"^ {0,3}#{1,6}\s+")
_LIST = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+(?:\[[ xX]\]\s+)?")
_QUOTE = re.compile(r"^\s*>\s?")
_NUMBERING = re.compile(r"^\s*\d+(?:\.\d+)*[.)、]?\s+")
_TABLE_SEP = re.compile(r"^\s*\|?\s*:?-{3,}:?\s*(?:\|\s*:?-{3,}:?\s*)*\|?\s*$")
_ATTRIBUTES = re.compile(r"\s*\{[#.][^}]*\}\s*$")     # pandoc heading attributes
_RAW_MACRO = re.compile(r"^\s*\\[a-zA-Z]+\*?(?:\[[^\]]*\])?(?:\{[^}]*\})*\s*$")
_BLOCK_TAG = re.compile(r"^\s*<(style|script)\b", re.I)
_BLOCK_END = re.compile(r"</(style|script)>", re.I)
_MARKER = re.compile(r"^(?:\d{0,4}|[ivxlcdm]{1,6}|[a-z]|[一二三四五六七八九十百]{1,3})$")
_GAP = r"\d{0,4}"     # a footnote number or superscript printed inside a line
_PAGE_REACH = 300     # letters/digits of page furniture tolerated around a page break
_LINK_PREFIXES = ("链接", "link", "リンク", "링크", "enlace")


# Characters that occupy a line without printing: whitespace, format characters
# (ZWSP, BOM) and the blank "filler" letters used to pad a line.
_BLANK_LETTERS = {"\u2800", "\u3164", "\uffa0", "\u115f", "\u1160"}


def is_ink(char):
    """Whether a text character paints anything on the page."""
    return not (char.isspace() or char in _BLANK_LETTERS
                or unicodedata.category(char) in ("Cf", "Cc", "Zs", "Zl", "Zp"))


def _ink_key(text):
    """Letters and digits only: layout, hyphenation, ligatures and quotes vary."""
    return "".join(ch for ch in unicodedata.normalize("NFKC", text).casefold() if ch.isalnum())


def _fragments(text):
    """Ink keys of visible inline text, split where a footnote number prints."""
    text = _LINK.sub(r"\1", _REF_LINK.sub(r"\1", _AUTOLINK.sub(r"\1", _IMAGE.sub(" ", text))))
    text = html.unescape(_TAG.sub(" ", text))
    return [k for k in (_ink_key(part) for part in _FOOTNOTE_REF.split(text)) if k]


def _report_blocks(markdown):
    """Visible report.md blocks in reading order: para, note, row or header."""
    lines = _COMMENT.sub("", markdown).splitlines()
    if lines and lines[0].strip() == "---":                  # YAML front matter
        closing = next((n for n, l in enumerate(lines[1:], 1) if l.strip() in ("---", "...")), None)
        if closing:
            lines = lines[closing + 1:]
    blocks, para, fence, raw = [], None, None, None

    def flush():
        nonlocal para
        if para is not None:
            blocks.append(para)
        para = None

    for index, line in enumerate(lines):
        if raw:
            if _BLOCK_END.search(line):
                raw = None
            continue
        if _BLOCK_TAG.match(line):
            flush()
            raw = True
            if _BLOCK_END.search(line):
                raw = None
            continue
        if _RAW_MACRO.match(line):
            flush()
            continue
        opening = _FENCE.match(line)
        if fence:
            if opening and opening[1][0] == fence[0] and len(opening[1]) >= len(fence):
                fence = None
            continue
        if opening:
            flush()
            fence = opening[1]
            continue
        if not line.strip() or _REF_DEF.match(line) or ("|" in line and _TABLE_SEP.match(line)):
            flush()
            continue
        if line.count("|") >= 2:
            flush()
            following = lines[index + 1] if index + 1 < len(lines) else ""
            kind = "header" if "|" in following and _TABLE_SEP.match(following) else "row"
            cells = line.strip().strip("|").split("|")
            blocks.append({"kind": kind, "text": line.strip(), "raw_cells": cells,
                           "cells": [_fragments(c) for c in cells]})
            continue
        note, heading, item = _FOOTNOTE_DEF.match(line), _HEADING.match(line), _LIST.match(line)
        if note or heading or item:
            flush()
            # A heading keeps its own numbering (an edited "1." matters); a list
            # item loses its marker, which renderers renumber legitimately.
            text = (line[note.end():] if note else _ATTRIBUTES.sub("", line[heading.end():])
                    if heading else line[item.end():])
            para = {"kind": "note" if note else "para", "text": text}
            if heading:
                flush()
            continue
        line = _QUOTE.sub("", line)
        if para is None:
            para = {"kind": "para", "text": line}
        else:
            para["text"] += " " + line
    flush()
    for block in blocks:
        if block["kind"] in ("para", "note"):
            block["fragments"] = _fragments(block["text"])
    return [b for b in blocks if b.get("fragments") or any(b.get("cells", []))]


def report_text_problems(markdown, pages):
    """Current report.md text the PDF does not carry, in order, as snippets.

    ``pages`` holds each PDF page's extracted text, one PDF line per newline.
    Every block must match at word boundaries of the PDF's own text, so an edit
    hidden beside what is printed ("14 of the 25" read as "4 of the 25") does
    not pass. Paragraphs, headings and list items must occupy whole PDF lines,
    beside at most a list marker or the preceding block's label; table cells
    must sit beside their own row's other cells. Header rows are required only
    when the PDF prints them, since card layouts drop the labels. A block may
    cross a page break, but only over furniture: page numbers and lines that
    repeat on other pages, such as a running header or a repeated table header.
    A row must consume all of its cells, in their original column order. Wrapped
    columns may interleave after they start, but no partial cell is evidence for
    the whole value. Ambiguous or unsupported extraction fails closed. Deleting
    whole blocks and changing link targets also require the render-time source
    binding; visible text alone cannot prove those changes reached the PDF.
    """
    import bisect
    lines, starts, ends, page_start, offset = [], set(), set(), [], 0
    for number, page in enumerate(pages):
        page_start.append(offset)
        for text in page.splitlines():
            key, fresh = "", True
            for char in text:
                part = "".join(c for c in unicodedata.normalize("NFKC", char).casefold()
                               if c.isalnum())
                if part:
                    if fresh:
                        starts.add(offset + len(key))
                    key, fresh = key + part, False
                elif not fresh:
                    ends.add(offset + len(key))
                    fresh = True
            if not fresh:
                ends.add(offset + len(key))
            if key:
                lines.append({"key": key, "text": text, "start": offset,
                              "end": offset + len(key), "page": number})
                offset += len(key)
    page_start.append(offset)
    stream = "".join(line["key"] for line in lines)
    line_starts = [line["start"] for line in lines]
    word_start, word_end, edge = [0] * len(stream), [len(stream)] * len(stream), 0
    for position in range(len(stream)):
        if position in starts:
            edge = position
        word_start[position] = edge
    edge = len(stream)
    for position in reversed(range(len(stream))):
        if position + 1 in ends:
            edge = position + 1
        word_end[position] = edge
    seen = {}
    for line in lines:
        seen.setdefault(re.sub(r"\d+", "#", line["key"]), set()).add(line["page"])
    furniture = [line["key"].isdigit() or len(seen[re.sub(r"\d+", "#", line["key"])]) > 1
                 for line in lines]

    def at(position):
        return bisect.bisect_right(line_starts, position) - 1

    def opens(position, glued=False):
        """A word starts here; a footnote definition may carry a glued number."""
        return position in starts or (glued and stream[word_start[position]:position].isdigit())

    def closes(position):
        return position in ends or (position < len(stream)
                                    and stream[position:word_end[position]].isdigit())

    blocks = _report_blocks(markdown)
    # A footnote prints at the foot of its page, between a paragraph and the
    # page break, so it is page furniture for the purpose of a hop.
    footnotes = "".join("".join(b["fragments"]) for b in blocks if b["kind"] == "note")

    def skippable(index):
        text = lines[index]["key"].lstrip("0123456789")
        return furniture[index] or bool(text) and text in footnotes

    def between(start, end):
        """Whether only page furniture lies between two matched halves."""
        return all(skippable(i) for i in range(at(start - 1) + 1, at(end)))

    def across_breaks(start, key, breaks):
        same = 0
        while same < len(key) and start + same < len(stream) and stream[start + same] == key[same]:
            same += 1
        if same == len(key):
            return start + same
        if not breaks:
            return None
        # The page may end with furniture that happens to continue the text.
        for used in range(same, max(same - 8, 1), -1):
            boundary = next((b for b in page_start[1:-1] if b >= start + used), None)
            if boundary is None or boundary - (start + used) > _PAGE_REACH:
                continue
            rest = key[used:]
            resume = stream.find(rest[:3], boundary, boundary + _PAGE_REACH + 1)
            while resume >= 0:
                if (start + used == lines[at(start + used - 1)]["end"]
                        and resume in starts and between(start + used, resume)):
                    end = across_breaks(resume, rest, breaks - 1)
                    if end is not None:
                        return end
                resume = stream.find(rest[:3], resume + 1, boundary + _PAGE_REACH + 1)
        return None

    def beside(fragments, cursor, accept, glued=False):
        """First match at or after ``cursor`` whose neighbours ``accept``."""
        pattern = re.compile(_GAP.join(re.escape(f) for f in fragments))
        key, contiguous = "".join(fragments), None
        found = pattern.search(stream, cursor)
        while found:
            if opens(found.start(), glued) and closes(found.end()) and accept(found.start(), found.end()):
                contiguous = found.start(), found.end()
                break
            found = pattern.search(stream, found.start() + 1)
        if len(key) < 4 or len(pages) < 2:
            return contiguous
        # A nearer copy split by a page break wins over a later contiguous copy.
        limit = contiguous[0] if contiguous else len(stream)
        for start in sorted({p for p in starts if cursor <= p < limit}):
            if stream.startswith(key[:1], start):
                end = across_breaks(start, key, 3)
                if end is not None and closes(end) and accept(start, end):
                    return start, end
        return contiguous

    def row_end(keys, cursor, header):
        """Match a complete row, including interleaved wrapped columns.

        States track how many characters each cell has consumed. A new column
        can start only after the preceding column has started; continuation
        lines may return to an earlier column. Every character must belong to
        this row, so a negation or salary from another row cannot be ignored.
        PDF lines bound the match, including when CJK cells have no spaces.
        """
        keys = tuple(key for key in keys if key)
        if not keys:
            return cursor
        goal = tuple(map(len, keys))
        zero = (0,) * len(keys)
        for first in range(max(0, at(cursor)), len(lines)):
            if lines[first]["start"] < cursor:
                continue
            states, work = {(zero, -1)}, 0
            for index in range(first, len(lines)):
                line = lines[index]
                saved = states
                for position, char in enumerate(line["key"]):
                    following = set()
                    for state, active in states:
                        for column, key in enumerate(keys):
                            used = state[column]
                            switch = (position == 0 or column == active or active < 0
                                      or column > active and (state[active] == goal[active]
                                          or line["start"] + position in starts))
                            if (used < len(key) and key[used] == char
                                    and switch and (used or column == 0 or state[column - 1])):
                                advanced = list(state)
                                advanced[column] += 1
                                following.add((tuple(advanced), column))
                    states = following
                    work += len(states)
                    if not states or len(states) > 2048 or work > 200000:
                        states = set()
                        break
                # Only page-edge furniture may interrupt a row. Repeated body
                # cells are not generally skippable just because they repeat.
                edge = (index < 2 or index >= len(lines) - 2
                        or lines[max(0, index - 2)]["page"] != line["page"]
                        or lines[min(len(lines) - 1, index + 2)]["page"] != line["page"])
                if index > first and edge and (line["key"] == header or skippable(index)):
                    states |= saved
                if any(state == goal for state, _ in states):
                    return line["end"]
                if not states:
                    break
        return None

    def match_row(cells, cursor, headers, merged=0, raw_cells=()):
        from itertools import product
        keys = ["".join(cell) for cell in cells]
        header = "".join("".join(cell) for cell in headers)
        variants = []
        for index, key in enumerate(keys):
            links = _LINK.findall(raw_cells[index]) if index < len(raw_cells) else []
            choices = [key]
            if links:
                labels = [_ink_key(label) for label in links]
                for prefix in _LINK_PREFIXES:
                    decorated = "".join(prefix + label for label in labels)
                    choices.append(decorated if key == "".join(labels) else key + decorated)
            variants.append(choices)
        # Default tables, and externally rendered tables with a leading merged
        # company cell. Only leading cells proved in the previous row may merge.
        for choice in product(*variants):
            for omitted in range(merged + 1):
                spot = row_end(choice[omitted:], cursor, header)
                if spot is not None:
                    return spot
        # Wide/tall tables can be rendered as labeled entries. Labels are known
        # source headers, never arbitrary intervening PDF text.
        for title_columns in (1, 2):
            labeled = [key if n < title_columns else "".join(headers[n]) + key
                       for n, key in enumerate(keys)] if len(headers) == len(keys) else []
            if labeled:
                spot = row_end(labeled, cursor, header)
                if spot is not None:
                    return spot
        return None

    def whole_line(before, after):
        def accept(start, end):
            head = stream[lines[at(start)]["start"]:start]
            tail = stream[end:lines[at(end - 1)]["end"]]
            return ((_MARKER.match(head) or head in before)
                    and (_MARKER.match(tail) or tail in after))
        return accept

    problems, cursor, above, labels, headers = [], 0, None, {""}, []
    for index, block in enumerate(blocks):
        if block["kind"] in ("row", "header"):
            cells = [(c, column) for column, c in enumerate(block["cells"]) if c]
            labels |= {"".join(c) for c, _ in cells}
            if block["kind"] == "header":
                headers = block["cells"]
            merged = 0
            if block["kind"] == "row" and above:
                for previous, current in zip(above, block["cells"]):
                    if previous != current:
                        break
                    merged += 1
                merged = min(merged, max(0, len(block["cells"]) - 1))
            spot = match_row(block["cells"], cursor, headers, merged, block["raw_cells"])
            if spot is None and block["kind"] == "header":
                names = {"".join(c) for c, _ in cells}
                printed = any(len(names & {_ink_key(word) for word in line["text"].split()}) > 1
                              or (line["key"] in names and n + 1 < len(lines)
                                  and lines[n + 1]["key"] in names)
                              for n, line in enumerate(lines) if line["start"] >= cursor)
                if not printed:
                    above = None    # a card layout prints no header row
                    continue
            if spot is None:
                problems.append(block["text"])
                above = None
            else:
                cursor = spot
                above = block["cells"] if block["kind"] == "row" else None
            continue
        above = None
        note = block["kind"] == "note"
        following = blocks[index + 1] if index + 1 < len(blocks) else None
        after = {"".join(following["fragments"])} if following and following.get("fragments") else set()
        before = labels
        standalone = block["text"].strip().rstrip("。．.,，、;；:：!！?？ \t")
        if _LINK.fullmatch(standalone) or _AUTOLINK.fullmatch(standalone):
            # The default renderer decorates a standalone link in the report
            # language. Permit that known label only for a source link, never
            # as arbitrary extra prose beside an ordinary paragraph.
            before = labels | set(_LINK_PREFIXES)
        spot = beside(block["fragments"], 0 if note else cursor,
                      whole_line(before, after | {""}), glued=note)
        if spot is None:
            problems.append(block["text"].strip())
        elif not note:
            cursor = spot[1]
        labels = {"".join(block["fragments"]), ""}
    return [p[:60] for p in problems]


def _sample_range(text, needle):
    """Find literal sample ink while allowing exporter spacing beside CJK.

    Word/PDF font changes can turn '访谈6位' into '访谈6 位'. Keep the
    original offsets so every intersecting font span is still measured. Do not
    remove English word boundaries or accept changed digits/punctuation.
    """
    start = text.find(needle)
    if start >= 0:
        return start, start + len(needle)
    cjk = lambda ch: '\u3400' <= ch <= '\u9fff' or '\u3040' <= ch <= '\u30ff' or '\uac00' <= ch <= '\ud7af'
    pattern = []
    for index, char in enumerate(needle):
        if index and not char.isspace() and not needle[index - 1].isspace() and (
                cjk(char) or cjk(needle[index - 1])):
            pattern.append(r"\s*")
        pattern.append(re.escape(char))
    match = re.search("".join(pattern), text)
    return match.span() if match else None


def measure(ws, requirements, report=False):
    findings = []

    def fail(detail):
        findings.append("FORMAT_MISMATCH: " + detail + "; fix and render/review again")

    def close(actual, expected):
        return (type(expected) in (int, float) and math.isfinite(expected)
                and abs(actual - expected) <= 0.6)

    def font_name(value):
        # PDF subset prefixes and PostScript separators are not font changes.
        return str(value).split("+")[-1].replace("-", "").replace(" ", "").lower()

    def painted(doc):
        """(text, ink box) per span, from its non-whitespace glyphs only.

        A span's own box includes its spaces: exporters end wrapped lines with a
        trailing space past the last glyph, and NBSP-only paragraphs occupy a
        line without printing anything. Neither is text on the page. Known
        limit: text painted in the background colour is not detected.
        """
        for page in doc:
            for block in page.get_text("rawdict")["blocks"]:
                for line in block.get("lines", []):
                    for span in line["spans"]:
                        ink = [c["bbox"] for c in span["chars"] if is_ink(c["c"])]
                        if ink:
                            yield ("".join(c["c"] for c in span["chars"]).strip(),
                                   (min(b[0] for b in ink), min(b[1] for b in ink),
                                    max(b[2] for b in ink), max(b[3] for b in ink)))

    pdf = ws / ("report.pdf" if report else "cv.pdf")
    if pdf.is_file():
        try:
            import pymupdf
            with pymupdf.open(pdf) as doc:
                size = requirements.get("page_size_pt")
                if not isinstance(size, list) or len(size) != 2:
                    fail("page_size_pt must specify width and height")
                else:
                    for page in doc:
                        if not all(close(a, b) for a, b in zip(page.rect[2:], size)):
                            fail(f"page {page.number + 1} paper size")
                samples = requirements.get("text_samples")
                roles = {"title", "heading", "body"} if report else {"name", "heading", "body"}
                if not isinstance(samples, list):
                    samples = []
                if not roles <= {s.get("role") for s in samples if isinstance(s, dict)}:
                    fail("text_samples must measure " + ", ".join(sorted(roles)))
                lines = [line for page in doc for block in page.get_text("dict")["blocks"]
                         for line in block.get("lines", [])]
                minimum_bottom = requirements.get("minimum_content_bottom_pt")
                if minimum_bottom is not None:
                    if len(doc) != 1:
                        fail("minimum_content_bottom_pt requires a one-page document")
                    if type(minimum_bottom) not in (int, float) or not math.isfinite(minimum_bottom) or minimum_bottom <= 0:
                        fail("minimum_content_bottom_pt must be a positive finite number")
                    else:
                        bottom = max((box[3] for _, box in painted(doc)), default=0)
                        if bottom < minimum_bottom - .6:
                            fail(f"content ends at {bottom:.2f} pt, required at least {minimum_bottom:.2f} pt; excessive lower-page whitespace")
                for sample in samples:
                    if not isinstance(sample, dict):
                        fail("invalid text sample")
                        continue
                    needle, fonts = sample.get("text"), sample.get("fonts")
                    if not isinstance(needle, str) or not needle.strip() or not isinstance(fonts, list) or not fonts:
                        fail("every text sample needs literal text and expected fonts")
                        continue
                    matches = []
                    region = sample.get("region_pt")
                    if region is not None and (not isinstance(region, list) or len(region) != 4
                                               or any(type(v) not in (int, float) or not math.isfinite(v) for v in region)):
                        fail("region_pt must specify left, top, right, bottom")
                        continue
                    for line in lines:
                        if region is not None and not pymupdf.Rect(region).contains(pymupdf.Rect(line["bbox"])):
                            continue
                        spans = line["spans"]
                        text = "".join(s["text"] for s in spans)
                        sample_range = _sample_range(text, needle)
                        if sample_range is None:
                            continue
                        start, stop = sample_range
                        offset = 0
                        for span in spans:
                            end = offset + len(span["text"])
                            if end > start and offset < stop:
                                matches.append(span)
                            offset = end
                    if not matches:
                        fail(f"sample {needle!r} missing from final PDF")
                    for span in matches:
                        if not close(span["size"], sample.get("size_pt")):
                            fail(f"{needle!r} size {span['size']:.2f} pt, expected {sample.get('size_pt')}")
                        if font_name(span["font"]) not in {font_name(f) for f in fonts}:
                            fail(f"{needle!r} font {span['font']}, expected {fonts}")
                        if "color" in sample and span["color"] != sample["color"]:
                            fail(f"{needle!r} text color")
                bounds = requirements.get("text_bounds_pt")
                if not isinstance(bounds, list) or len(bounds) != 4 or any(type(v) not in (int, float) or not math.isfinite(v) for v in bounds):
                    fail("text_bounds_pt must specify left, top, right, bottom")
                else:
                    for text, (x0, y0, x1, y1) in painted(doc):
                        if (x0 < bounds[0] - .6 or y0 < bounds[1] - .6
                                or x1 > bounds[2] + .6 or y1 > bounds[3] + .6):
                            fail(f"text outside required bounds: {text[:30]!r}")
        except Exception as exc:
            fail(f"cannot measure PDF: {exc}")
    elif report:
        fail("report.pdf is missing")

    docx = ws / "cv.docx"
    if not report and docx.is_file():
        try:
            ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
            prefix = "{" + ns["w"] + "}"
            with zipfile.ZipFile(docx) as archive:
                root = ET.fromstring(archive.read("word/document.xml"))
            expected = requirements.get("docx_geometry_twips")
            keys = {"width", "height", "top", "bottom", "left", "right"}
            if not isinstance(expected, dict) or not keys <= expected.keys():
                fail("docx_geometry_twips needs paper width/height and four margins")
            else:
                for section in root.findall(".//w:sectPr", ns):
                    for key in sorted(keys):
                        node = section.find("w:pgSz" if key in {"width", "height"} else "w:pgMar", ns)
                        attr = {"width": "w", "height": "h"}.get(key, key)
                        actual = int(node.attrib[prefix + attr])
                        if actual != expected[key]:
                            fail(f"DOCX {key} {actual} twips, expected {expected[key]}")
        except Exception as exc:
            fail(f"cannot measure DOCX: {exc}")
    return findings
