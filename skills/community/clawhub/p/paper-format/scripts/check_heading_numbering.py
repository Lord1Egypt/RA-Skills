#!/usr/bin/env python3
import json
import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS = {"w": W}
PATTERNS = {
    0: re.compile(r"^第[一二三四五六七八九十百0-9]+章  \S"),
    1: re.compile(r"^\d+\.\d+\s+\S"),
    2: re.compile(r"^\d+\.\d+\.\d+\s+\S"),
}


def text_of(paragraph):
    return "".join(node.text or "" for node in paragraph.findall(".//w:t", NS)).strip()


def main():
    if len(sys.argv) != 2:
        raise SystemExit("usage: check_heading_numbering.py <file.docx>")
    with zipfile.ZipFile(Path(sys.argv[1])) as package:
        root = ET.fromstring(package.read("word/document.xml"))
    issues = []
    checked = 0
    for index, paragraph in enumerate(root.findall(".//w:body/w:p", NS)):
        ppr = paragraph.find("w:pPr", NS)
        outline = ppr.find("w:outlineLvl", NS) if ppr is not None else None
        if outline is None:
            continue
        try:
            level = int(outline.get(f"{{{W}}}val"))
        except (TypeError, ValueError):
            continue
        if level not in PATTERNS:
            continue
        checked += 1
        text = text_of(paragraph)
        num_pr = ppr.find("w:numPr", NS) if ppr is not None else None
        if num_pr is None and not PATTERNS[level].match(text):
            issues.append({"paragraph": index, "outline_level": level, "issue": "missing_or_invalid_visible_number", "text": text[:80]})
    if checked == 0:
        issues.append({"issue": "no_level_1_to_3_headings_found"})
    result = {"status": "pass" if not issues else "fail", "checked": checked, "issues": issues}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if not issues else 1)


if __name__ == "__main__":
    main()
