#!/usr/bin/env python3
import json
import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS = {"w": W}


def text_of(element):
    return "".join(node.text or "" for node in element.findall(".//w:t", NS)).strip()


def section_properties(element):
    if element.tag == f"{{{W}}}sectPr":
        return element
    ppr = element.find("w:pPr", NS) if element.tag == f"{{{W}}}p" else None
    return ppr.find("w:sectPr", NS) if ppr is not None else None


def main():
    if len(sys.argv) != 2:
        raise SystemExit("usage: check_page_numbering.py <file.docx>")
    with zipfile.ZipFile(Path(sys.argv[1])) as package:
        root = ET.fromstring(package.read("word/document.xml"))
    body = root.find("w:body", NS)
    children = list(body) if body is not None else []
    first_chapter = None
    for index, element in enumerate(children):
        text = re.sub(r"\s+", "", text_of(element))
        if re.match(r"^第[一二三四五六七八九十百0-9]+章", text) or text in {"绪论", "引言"}:
            first_chapter = index
            break
    issues = []
    if first_chapter is None:
        issues.append({"issue": "first_body_chapter_not_found"})
    else:
        body_sections = []
        for index in range(first_chapter, len(children)):
            sect = section_properties(children[index])
            if sect is not None:
                body_sections.append((index, sect))
        if not body_sections:
            issues.append({"issue": "body_section_properties_not_found"})
        else:
            for number, (index, sect) in enumerate(body_sections):
                page = sect.find("w:pgNumType", NS)
                fmt = page.get(f"{{{W}}}fmt") if page is not None else None
                start = page.get(f"{{{W}}}start") if page is not None else None
                if fmt != "decimal":
                    issues.append({"issue": "body_page_format_not_decimal", "section_end": index, "format": fmt})
                if number == 0 and start != "1":
                    issues.append({"issue": "body_first_page_not_starting_at_1", "section_end": index, "start": start})
                if number > 0 and start is not None:
                    issues.append({"issue": "later_body_section_restarts_page_number", "section_end": index, "start": start})
    result = {"status": "pass" if not issues else "fail", "first_chapter_body_index": first_chapter, "issues": issues}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if not issues else 1)


if __name__ == "__main__":
    main()
