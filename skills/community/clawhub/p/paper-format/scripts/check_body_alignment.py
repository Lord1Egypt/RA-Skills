#!/usr/bin/env python3
import json
import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS = {"w": W}


def text_of(paragraph):
    return "".join(node.text or "" for node in paragraph.findall(".//w:t", NS)).strip()


def main():
    if len(sys.argv) != 2:
        raise SystemExit("usage: check_body_alignment.py <file.docx>")
    with zipfile.ZipFile(Path(sys.argv[1])) as package:
        root = ET.fromstring(package.read("word/document.xml"))
    paragraphs = root.findall(".//w:body/w:p", NS)
    in_body = False
    checked = 0
    issues = []
    for index, paragraph in enumerate(paragraphs):
        text = text_of(paragraph)
        compact = re.sub(r"\s+", "", text)
        if re.match(r"^第[一二三四五六七八九十百0-9]+章", compact) or compact in {"绪论", "引言"}:
            in_body = True
            continue
        if compact in {"参考文献", "致谢"} or compact.startswith("附录"):
            in_body = False
        if not in_body or len(text) < 20:
            continue
        if re.match(r"^\d+(?:\.\d+){0,4}\s*\D", text):
            continue
        ppr = paragraph.find("w:pPr", NS)
        if ppr is not None and (ppr.find("w:outlineLvl", NS) is not None or ppr.find("w:numPr", NS) is not None):
            continue
        checked += 1
        jc = ppr.find("w:jc", NS) if ppr is not None else None
        value = jc.get(f"{{{W}}}val") if jc is not None else None
        if value != "both":
            issues.append({"paragraph": index, "alignment": value, "text": text[:80]})
        ind = ppr.find("w:ind", NS) if ppr is not None else None
        first_line_chars = ind.get(f"{{{W}}}firstLineChars") if ind is not None else None
        if first_line_chars != "200":
            issues.append({"paragraph": index, "first_line_chars": first_line_chars, "issue": "body_first_line_indent_not_2_chars", "text": text[:80]})
    if checked == 0:
        issues.append({"issue": "no_body_paragraphs_checked"})
    result = {"status": "pass" if not issues else "fail", "checked": checked, "issues": issues}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if not issues else 1)


if __name__ == "__main__":
    main()
