"""
Чтение DOCX и PPTX напрямую из XML (zipfile + ElementTree) — без python-docx и python-pptx.

DOCX: абзацы по порядку, заголовки (по стилям и outlineLvl), списки, таблицы (с объединёнными
      ячейками), надписи (text box), содержимое элементов управления, колонтитул, диаграммы
      (данные из кэша), рисунки.
PPTX: слайды в порядке показа, текст фигур и групп, таблицы, диаграммы (числа), SmartArt,
      заметки докладчика, картинки и доля площади слайда, которую они занимают.
"""
from __future__ import annotations

import posixpath
import re
import zipfile
from xml.etree import ElementTree as ET

NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "c": "http://schemas.openxmlformats.org/drawingml/2006/chart",
    "mc": "http://schemas.openxmlformats.org/markup-compatibility/2006",
    "rel": "http://schemas.openxmlformats.org/package/2006/relationships",
    "dgm": "http://schemas.openxmlformats.org/drawingml/2006/diagram",
}
W = "{%s}" % NS["w"]
A = "{%s}" % NS["a"]
P = "{%s}" % NS["p"]
R = "{%s}" % NS["r"]
MC = "{%s}" % NS["mc"]


def _xml(z: zipfile.ZipFile, name: str):
    try:
        return ET.fromstring(z.read(name))
    except (KeyError, ET.ParseError):
        return None


def _rels(z: zipfile.ZipFile, part: str) -> dict[str, tuple[str, str]]:
    """id → (полный путь цели, тип) для части part."""
    folder, fname = posixpath.split(part)
    root = _xml(z, posixpath.join(folder, "_rels", fname + ".rels"))
    out = {}
    if root is None:
        return out
    for rel in root:
        tgt = rel.get("Target", "")
        if rel.get("TargetMode") == "External":
            continue
        path = posixpath.normpath(posixpath.join(folder, tgt)) if not tgt.startswith("/") else tgt.lstrip("/")
        out[rel.get("Id")] = (path, rel.get("Type", "").rsplit("/", 1)[-1])
    return out


def _drop_fallbacks(root):
    """mc:AlternateContent: оставляем mc:Choice, убираем mc:Fallback (иначе текст надписей дублируется)."""
    if root is None:
        return root
    for parent in root.iter():
        for child in list(parent):
            if child.tag == MC + "AlternateContent":
                fb = child.find(MC + "Fallback")
                if fb is not None:
                    child.remove(fb)
    return root


# ============================================================================ диаграммы
C_NS = {"c": NS["c"], "a": NS["a"]}


def chart_xml_to_text(xml_bytes: bytes) -> str:
    """Заголовок, категории и значения серий из кэша диаграммы Office."""
    try:
        root = ET.fromstring(xml_bytes)
    except ET.ParseError:
        return ""
    title = " ".join(t.text or "" for t in root.findall(".//c:title//a:t", C_NS)).strip()
    lines = [f"[Диаграмма] {title}" if title else "[Диаграмма]"]
    for ser in root.findall(".//c:ser", C_NS):
        name = " ".join(v.text or "" for v in ser.findall("./c:tx//c:v", C_NS)).strip() or "серия"
        cats = [v.text or "" for v in ser.findall("./c:cat//c:pt/c:v", C_NS)]
        vals = [v.text or "" for v in ser.findall("./c:val//c:pt/c:v", C_NS)]
        if not vals:
            vals = [v.text or "" for v in ser.findall("./c:yVal//c:pt/c:v", C_NS)]
            cats = cats or [v.text or "" for v in ser.findall("./c:xVal//c:pt/c:v", C_NS)]
        pairs = [f"{c}: {v}" for c, v in zip(cats, vals)] if cats else vals
        lines.append(f"  {name} — " + "; ".join(pairs[:60]) + (" …" if len(pairs) > 60 else ""))
    return "\n".join(lines) if len(lines) > 1 or title else ""


# ============================================================================ DOCX

def _ival(el, default: int | None = None) -> int | None:
    """Целое значение атрибута w:val (у элемента может не быть w:val)."""
    if el is None:
        return default
    v = el.get(W + "val")
    return int(v) if v is not None and v.lstrip("-").isdigit() else default


def _w_text(el) -> str:
    """Текст абзаца/ячейки: w:t, табуляции, переносы; удалённые правки и коды полей пропускаем.
    Вложенные абзацы (надписи, ячейки) отделяются переводом строки.
    """
    out = []
    for node in el.iter():
        tag = node.tag
        if tag == W + "p" and node is not el:
            out.append("\n")
        elif tag == W + "t":
            out.append(node.text or "")
        elif tag == W + "tab":
            out.append("\t")
        elif tag in (W + "br", W + "cr"):
            out.append("\n")
        elif tag == W + "noBreakHyphen":
            out.append("-")
    return "".join(out)


_WRAPPERS = (W + "sdt", W + "sdtContent", W + "customXml")


def _children(el, tag: str):
    """Дочерние элементы tag, в том числе обёрнутые в w:sdt / w:customXml (повторяющиеся разделы форм)."""
    for ch in el:
        if ch.tag == tag:
            yield ch
        elif ch.tag in _WRAPPERS:
            yield from _children(ch, tag)


def _table_rows(tbl) -> list[list[str]]:
    rows = []
    for tr in _children(tbl, W + "tr"):
        cells = []
        for tc in _children(tr, W + "tc"):
            tcpr = tc.find(W + "tcPr")
            vmerge = tcpr.find(W + "vMerge") if tcpr is not None else None
            if vmerge is not None and vmerge.get(W + "val", "continue") == "continue":
                cells.append("")  # продолжение вертикально объединённой ячейки
                continue
            paras = [_w_text(p).strip() for p in tc.iter(W + "p")]
            cells.append(" ".join(p for p in paras if p))
            span = _ival(tcpr.find(W + "gridSpan"), 1) if tcpr is not None else 1
            cells += [""] * max(0, min(span, 64) - 1)  # горизонтальное объединение
        rows.append(cells)
    return rows


def table_to_md(rows: list[list[str]]) -> str:
    rows = [[(c or "").replace("\n", " ").replace("|", "/").strip() for c in r] for r in rows]
    rows = [r for r in rows if any(r)]
    if not rows:
        return ""
    width = max(len(r) for r in rows)
    rows = [r + [""] * (width - len(r)) for r in rows]
    out = ["| " + " | ".join(rows[0]) + " |", "|" + "---|" * width]
    out += ["| " + " | ".join(r) + " |" for r in rows[1:]]
    return "\n".join(out)


def read_docx(path) -> dict:
    """→ {"text": markdown-подобный текст, "charts": [текст], "media": [(имя, bytes)], "header": str}"""
    with zipfile.ZipFile(path) as z:
        names = set(z.namelist())
        doc = _drop_fallbacks(_xml(z, "word/document.xml"))
        if doc is None:
            raise ValueError("нет word/document.xml")
        styles = _xml(z, "word/styles.xml")
        heading_level: dict[str, int] = {}
        list_styles: set[str] = set()
        if styles is not None:
            for st in styles.findall(W + "style"):
                sid = st.get(W + "styleId", "")
                nm = st.find(W + "name")
                name = (nm.get(W + "val", "") if nm is not None else "").lower()
                m = re.search(r"(heading|заголовок)\s*(\d)", name)
                ol = _ival(st.find(f"{W}pPr/{W}outlineLvl"), 9)
                if m:
                    heading_level[sid] = int(m.group(2))
                elif 0 <= ol < 9:
                    heading_level[sid] = ol + 1
                elif name == "title":
                    heading_level[sid] = 1
                if "list" in name or "спис" in name:
                    list_styles.add(sid)
        body = doc.find(W + "body")
        parts: list[str] = []

        def walk(container):
            for el in container:
                tag = el.tag
                if tag == W + "p":
                    t = _w_text(el).strip()
                    if not t:
                        continue
                    ppr = el.find(W + "pPr")
                    sid = ""
                    lvl = None
                    is_list = False
                    if ppr is not None:
                        ps = ppr.find(W + "pStyle")
                        sid = ps.get(W + "val", "") if ps is not None else ""
                        ol = _ival(ppr.find(W + "outlineLvl"), 9)
                        if 0 <= ol < 9:
                            lvl = ol + 1
                        is_list = ppr.find(W + "numPr") is not None
                    lvl = lvl or heading_level.get(sid)
                    if lvl:
                        parts.append("#" * min(lvl + 1, 6) + " " + t)
                    elif is_list or sid in list_styles:
                        parts.append("- " + t)
                    else:
                        parts.append(t)
                elif tag == W + "tbl":
                    md = table_to_md(_table_rows(el))
                    if md:
                        parts.append(md)
                elif tag == W + "sdt":
                    content = el.find(W + "sdtContent")
                    if content is not None:
                        walk(content)
                elif tag in (W + "sdtContent", W + "customXml", W + "smartTag"):
                    walk(el)

        walk(body if body is not None else [])
        header = ""
        for n in sorted(x for x in names if re.match(r"word/header\d*\.xml$", x)):
            h = _xml(z, n)
            if h is not None:
                header = " ".join(_w_text(p).strip() for p in h.iter(W + "p") if _w_text(p).strip())
                if header:
                    break
        # сноски и комментарии: в них часто цифры и источники
        for part, title in (("word/footnotes.xml", "Сноски"), ("word/endnotes.xml", "Концевые сноски"),
                            ("word/comments.xml", "Комментарии")):
            root = _drop_fallbacks(_xml(z, part)) if part in names else None
            if root is None:
                continue
            notes = []
            for note in root:
                if note.get(W + "type") in ("separator", "continuationSeparator", "continuationNotice"):
                    continue
                t = " ".join(_w_text(p).strip() for p in note.iter(W + "p") if _w_text(p).strip())
                if t:
                    author = note.get(W + "author")
                    notes.append(f"- {author + ': ' if author else ''}{t}")
            if notes:
                parts.append(f"[{title}]\n" + "\n".join(notes))
        charts, media = [], []
        for n in sorted(names):  # одна битая картинка/диаграмма не должна губить весь документ
            try:
                if re.match(r"word/charts/chart\d+\.xml$", n):
                    charts.append(chart_xml_to_text(z.read(n)))
                elif n.startswith("word/media/"):
                    media.append((n, z.read(n)))
            except Exception:  # noqa: BLE001
                continue
    return {"text": "\n\n".join(parts), "header": header, "charts": [c for c in charts if c], "media": media}


# ============================================================================ PPTX

def _a_text(el) -> str:
    """Текст DrawingML: абзацы a:p → строки."""
    lines = []
    for p in el.iter(A + "p"):
        buf = []
        for node in p.iter():
            if node.tag == A + "t":
                buf.append(node.text or "")
            elif node.tag == A + "br":
                buf.append("\n")
        line = "".join(buf).strip()
        if line:
            lines.append(line)
    return "\n".join(lines)


def read_pptx(path) -> dict:
    """→ {"size": (cx, cy), "slides": [{"text", "flags", "pictures": [(имя, bytes, доля)], "notes"}]}"""
    with zipfile.ZipFile(path) as z:
        pres = _xml(z, "ppt/presentation.xml")
        if pres is None:
            raise ValueError("нет ppt/presentation.xml")
        sz = pres.find(P + "sldSz")
        cx = int(sz.get("cx", 9144000)) if sz is not None else 9144000
        cy = int(sz.get("cy", 6858000)) if sz is not None else 6858000
        prels = _rels(z, "ppt/presentation.xml")
        order = []
        lst = pres.find(P + "sldIdLst")
        for sid in (lst if lst is not None else []):
            rid = sid.get(R + "id")
            if rid in prels:
                order.append(prels[rid][0])
        if not order:  # нет списка — по номерам файлов
            order = sorted((n for n in z.namelist() if re.match(r"ppt/slides/slide\d+\.xml$", n)),
                           key=lambda n: int(re.findall(r"\d+", n)[-1]))
        slides = []
        media_cache: dict[str, bytes] = {}
        for part in order:
            root = _drop_fallbacks(_xml(z, part))
            if root is None:
                continue
            rels = _rels(z, part)
            acc: list[str] = []
            flags: set[str] = set()
            pictures = []

            def walk(tree):
                for sh in tree:
                    tag = sh.tag
                    if tag == MC + "AlternateContent":  # фигуры с формулами и т.п. — берём вариант mc:Choice
                        for choice in sh.findall(MC + "Choice"):
                            walk(choice)
                    elif tag == P + "grpSp":
                        walk(sh)
                    elif tag == P + "sp":
                        tb = sh.find(P + "txBody")
                        if tb is not None:
                            t = _a_text(tb)
                            if t:
                                acc.append(t)
                    elif tag == P + "graphicFrame":
                        tbl = sh.find(".//" + A + "tbl")
                        if tbl is not None:
                            rows = [[_a_text(tc).replace("\n", " ") for tc in tr.findall(A + "tc")]
                                    for tr in tbl.findall(A + "tr")]
                            md = table_to_md(rows)
                            if md:
                                acc.append(md)
                        ch = sh.find(".//{%s}chart" % NS["c"])
                        if ch is not None:
                            flags.add("диаграмма")
                            target = rels.get(ch.get(R + "id"), ("", ""))[0]
                            try:
                                acc.append(chart_xml_to_text(z.read(target)) or "[Диаграмма]")
                            except Exception:  # noqa: BLE001
                                acc.append("[Диаграмма — данные не найдены]")
                        dm = sh.find(".//{%s}relIds" % NS["dgm"])
                        if dm is not None:  # SmartArt: текст в части data
                            target = rels.get(dm.get(R + "dm"), ("", ""))[0]
                            d = _xml(z, target)
                            if d is not None:
                                t = " · ".join(x.text.strip() for x in d.iter(A + "t") if x.text and x.text.strip())
                                if t:
                                    acc.append(t)
                    elif tag == P + "pic":
                        blip = sh.find(".//" + A + "blip")
                        ext = sh.find(f"{P}spPr/{A}xfrm/{A}ext")
                        share = 0.0
                        if ext is not None:
                            share = int(ext.get("cx", 0)) * int(ext.get("cy", 0)) / max(cx * cy, 1)
                        if blip is not None:
                            target = rels.get(blip.get(R + "embed"), ("", ""))[0]
                            try:
                                if target not in media_cache:  # одна и та же картинка на многих слайдах
                                    media_cache[target] = z.read(target)
                                pictures.append((target, media_cache[target], share))
                            except Exception:  # noqa: BLE001
                                pass
                        if share > 0.08:
                            flags.add("изображение")

            tree = root.find(f"{P}cSld/{P}spTree")
            walk(tree if tree is not None else [])
            notes = ""
            for path_, typ in rels.values():
                if typ == "notesSlide":
                    nroot = _xml(z, path_)
                    if nroot is not None:
                        texts = []
                        for sp in nroot.iter(P + "sp"):
                            ph = sp.find(f"{P}nvSpPr/{P}nvPr/{P}ph")
                            if ph is not None and ph.get("type") in ("sldImg", "sldNum", "hdr", "ftr", "dt"):
                                continue
                            tb = sp.find(P + "txBody")
                            if tb is not None and _a_text(tb):
                                texts.append(_a_text(tb))
                        notes = "\n".join(texts)
            slides.append({"text": "\n".join(acc), "flags": flags, "pictures": pictures, "notes": notes})
    return {"size": (cx, cy), "slides": slides}
