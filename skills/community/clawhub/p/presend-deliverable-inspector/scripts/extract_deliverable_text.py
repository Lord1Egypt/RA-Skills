#!/usr/bin/env python3
from __future__ import annotations

import json
import posixpath
import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

NS_A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
NS_MAIN = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
NS_REL = "{http://schemas.openxmlformats.org/package/2006/relationships}"
NS_W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def pptx_text(path: Path) -> dict:
    entries = []
    with zipfile.ZipFile(path) as zf:
        slide_names = sorted(
            [name for name in zf.namelist() if re.match(r"ppt/slides/slide\d+\.xml$", name)],
            key=lambda name: int(re.search(r"slide(\d+)\.xml", name).group(1)),
        )
        for name in slide_names:
            number = int(re.search(r"slide(\d+)\.xml", name).group(1))
            root = ET.fromstring(zf.read(name))
            texts = [node.text or "" for node in root.iter(f"{NS_A}t")]
            clean = "\n".join(text for text in texts if text.strip())
            location = f"slide {number}"
            if root.attrib.get("show") == "0":
                location = f"{location} hidden"
            entries.append({"location": location, "text": clean})
        notes_names = sorted(
            [name for name in zf.namelist() if re.match(r"ppt/notesSlides/notesSlide\d+\.xml$", name)],
            key=lambda name: int(re.search(r"notesSlide(\d+)\.xml", name).group(1)),
        )
        for name in notes_names:
            number = int(re.search(r"notesSlide(\d+)\.xml", name).group(1))
            root = ET.fromstring(zf.read(name))
            texts = [node.text or "" for node in root.iter(f"{NS_A}t")]
            clean = "\n".join(text for text in texts if text.strip())
            if clean:
                entries.append({"location": f"slide {number} notes", "text": clean})
    return {"artifact_type": "ppt", "path": str(path), "entries": entries}


def workbook_sheet_map(zf: zipfile.ZipFile) -> list[dict]:
    root = ET.fromstring(zf.read("xl/workbook.xml"))
    sheets = []
    for idx, sheet in enumerate(root.findall(f".//{NS_MAIN}sheet"), start=1):
        sheets.append({
            "name": sheet.attrib["name"],
            "state": sheet.attrib.get("state", "visible"),
            "path": f"xl/worksheets/sheet{idx}.xml",
            "index": idx,
        })
    return sheets


def normalize_ooxml_target(base_dir: str, target: str) -> str:
    if target.startswith("/"):
        return target.lstrip("/")
    return posixpath.normpath(posixpath.join(base_dir, target))


def xlsx_comment_parts(zf: zipfile.ZipFile, sheets: list[dict]) -> list[tuple[str, str]]:
    parts = []
    names = set(zf.namelist())
    for sheet in sheets:
        rels_name = f"xl/worksheets/_rels/sheet{sheet['index']}.xml.rels"
        if rels_name not in names:
            continue
        rels_root = ET.fromstring(zf.read(rels_name))
        for rel in rels_root.findall(f"{NS_REL}Relationship"):
            if rel.attrib.get("Type", "").endswith("/comments"):
                comment_path = normalize_ooxml_target("xl/worksheets", rel.attrib["Target"])
                if comment_path in names:
                    parts.append((sheet["name"], comment_path))
    if not parts:
        for name in sorted(item for item in names if re.match(r"xl/comments\d+\.xml$", item)):
            parts.append(("workbook", name))
    return parts


def xlsx_comment_entries(zf: zipfile.ZipFile, sheets: list[dict]) -> list[dict]:
    entries = []
    for sheet_name, part_name in xlsx_comment_parts(zf, sheets):
        root = ET.fromstring(zf.read(part_name))
        for idx, comment in enumerate(root.findall(f".//{NS_MAIN}comment"), start=1):
            ref = comment.attrib.get("ref", str(idx))
            texts = [node.text or "" for node in comment.iter(f"{NS_MAIN}t")]
            clean = "".join(texts).strip()
            if clean:
                entries.append({"location": f"{sheet_name} comment {ref}", "text": clean})
    return entries


def xlsx_text(path: Path) -> dict:
    entries = []
    with zipfile.ZipFile(path) as zf:
        sheets = workbook_sheet_map(zf)
        for sheet in sheets:
            root = ET.fromstring(zf.read(sheet["path"]))
            values = []
            for cell in root.findall(f".//{NS_MAIN}c"):
                ref = cell.attrib.get("r", "")
                inline = cell.find(f"{NS_MAIN}is/{NS_MAIN}t")
                formula = cell.find(f"{NS_MAIN}f")
                value = cell.find(f"{NS_MAIN}v")
                parts = []
                if inline is not None and inline.text:
                    parts.append(inline.text)
                if formula is not None and formula.text:
                    parts.append(f"formula={formula.text}")
                if value is not None and value.text:
                    parts.append(value.text)
                if parts:
                    values.append(f"{ref}: {' | '.join(parts)}")
            state_note = f"sheet_state={sheet['state']}"
            entries.append({
                "location": sheet["name"],
                "text": "\n".join([state_note, *values]),
            })
        entries.extend(xlsx_comment_entries(zf, sheets))
    return {"artifact_type": "excel", "path": str(path), "entries": entries}


def pdf_text(path: Path) -> dict:
    try:
        from pypdf import PdfReader
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "PDF extraction requires optional pypdf; use the host PDF reader or rendering tools when unavailable."
        ) from exc

    reader = PdfReader(str(path))
    entries = []
    for idx, page in enumerate(reader.pages, start=1):
        entries.append({"location": f"page {idx}", "text": page.extract_text() or ""})
    return {"artifact_type": "pdf", "path": str(path), "entries": entries}


def pasted_text(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    blocks = [block.strip() for block in re.split(r"\n\s*\n", text) if block.strip()]
    entries = [{"location": f"paragraph {idx}", "text": block} for idx, block in enumerate(blocks, start=1)]
    if not entries and text.strip():
        entries.append({"location": "paragraph 1", "text": text.strip()})
    return {"artifact_type": "pasted_text", "path": str(path), "entries": entries}


def sorted_ooxml_parts(names: list[str], pattern: str) -> list[str]:
    return sorted(
        [name for name in names if re.match(pattern, name)],
        key=lambda name: int(re.search(r"(\d+)", name).group(1)),
    )


def word_part_entries(zf: zipfile.ZipFile, part_names: list[str], location_prefix: str) -> list[dict]:
    entries = []
    for part_idx, name in enumerate(part_names, start=1):
        root = ET.fromstring(zf.read(name))
        paragraph_texts = []
        for para in root.findall(f".//{NS_W}p"):
            texts = [node.text or "" for node in para.iter(f"{NS_W}t")]
            clean = "".join(texts).strip()
            if clean:
                paragraph_texts.append(clean)
        for para_idx, clean in enumerate(paragraph_texts, start=1):
            location = f"{location_prefix} {part_idx}"
            if len(paragraph_texts) > 1:
                location = f"{location} paragraph {para_idx}"
            entries.append({"location": location, "text": clean})
    return entries


def word_text(path: Path) -> dict:
    entries = []
    with zipfile.ZipFile(path) as zf:
        names = zf.namelist()
        root = ET.fromstring(zf.read("word/document.xml"))
        for idx, para in enumerate(root.findall(f".//{NS_W}p"), start=1):
            texts = [node.text or "" for node in para.iter(f"{NS_W}t")]
            clean = "".join(texts).strip()
            if clean:
                entries.append({"location": f"paragraph {idx}", "text": clean})

        for pattern, location_prefix in (
            (r"word/header\d+\.xml$", "header"),
            (r"word/footer\d+\.xml$", "footer"),
        ):
            entries.extend(word_part_entries(zf, sorted_ooxml_parts(names, pattern), location_prefix))

        if "word/footnotes.xml" in names:
            entries.extend(word_part_entries(zf, ["word/footnotes.xml"], "footnote"))

        if "word/endnotes.xml" in names:
            entries.extend(word_part_entries(zf, ["word/endnotes.xml"], "endnote"))

        if "word/comments.xml" in names:
            comments = ET.fromstring(zf.read("word/comments.xml"))
            for idx, comment in enumerate(comments.findall(f".//{NS_W}comment"), start=1):
                texts = [node.text or "" for node in comment.iter(f"{NS_W}t")]
                clean = "".join(texts).strip()
                if clean:
                    entries.append({"location": f"comment {idx}", "text": clean})

        if "word/settings.xml" in names:
            settings = zf.read("word/settings.xml").decode("utf-8", errors="ignore")
            if "trackRevisions" in settings:
                entries.append({"location": "settings", "text": "trackRevisions enabled"})
    return {"artifact_type": "word", "path": str(path), "entries": entries}


def extract(path: Path) -> dict:
    suffix = path.suffix.lower()
    if suffix == ".pptx":
        return pptx_text(path)
    if suffix == ".docx":
        return word_text(path)
    if suffix == ".xlsx":
        return xlsx_text(path)
    if suffix == ".pdf":
        return pdf_text(path)
    if suffix in {".txt", ".md"}:
        return pasted_text(path)
    raise ValueError(f"unsupported file type: {path}")


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit("usage: extract_deliverable_text.py <file> [<file> ...]")
    results = [extract(Path(arg)) for arg in sys.argv[1:]]
    print(json.dumps({"files": results}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
