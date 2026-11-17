#!/usr/bin/env python3
import json
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS = {"w": W}
VAL = f"{{{W}}}val"
DEFAULT_MAX_TWIPS = 1440  # 72 pt; larger values are normally a unit-conversion error.


def integer_attr(element, name):
    value = element.get(f"{{{W}}}{name}")
    try:
        return int(value) if value is not None else None
    except ValueError:
        return None


def main():
    if len(sys.argv) not in (2, 3):
        raise SystemExit("usage: check_paragraph_spacing.py <file.docx> [max_twips]")
    path = Path(sys.argv[1])
    max_twips = int(sys.argv[2]) if len(sys.argv) == 3 else DEFAULT_MAX_TWIPS
    issues = []
    with zipfile.ZipFile(path) as package:
        root = ET.fromstring(package.read("word/document.xml"))
    for index, paragraph in enumerate(root.findall(".//w:body/w:p", NS)):
        text = "".join(node.text or "" for node in paragraph.findall(".//w:t", NS)).strip()
        if not text:
            continue
        ppr = paragraph.find("w:pPr", NS)
        spacing = ppr.find("w:spacing", NS) if ppr is not None else None
        if spacing is None:
            continue
        for attribute in ("before", "after"):
            value = integer_attr(spacing, attribute)
            if value is not None and value > max_twips:
                issues.append(
                    {
                        "paragraph": index,
                        "attribute": attribute,
                        "twips": value,
                        "points": value / 20,
                        "text": text[:80],
                    }
                )
    result = {
        "status": "pass" if not issues else "fail",
        "max_twips": max_twips,
        "max_points": max_twips / 20,
        "issues": issues,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if not issues else 1)


if __name__ == "__main__":
    main()
