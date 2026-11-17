#!/usr/bin/env python3
import argparse
import json
import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS = {"w": W}


def enabled(element):
    if element is None:
        return False
    value = element.get(f"{{{W}}}val", "1").lower()
    return value not in {"0", "false", "off", "no"}


def text_of(element):
    return "".join(node.text or "" for node in element.findall(".//w:t", NS)).strip()


def normalized(text):
    return re.sub(r"[\s\u3000:：]", "", text).upper()


def has_page_boundary(element):
    if element.tag != f"{{{W}}}p":
        return False
    ppr = element.find("w:pPr", NS)
    if ppr is not None and enabled(ppr.find("w:pageBreakBefore", NS)):
        return True
    if any(node.get(f"{{{W}}}type", "textWrapping") == "page" for node in element.findall(".//w:br", NS)):
        return True
    sect = ppr.find("w:sectPr", NS) if ppr is not None else None
    if sect is not None:
        section_type = sect.find("w:type", NS)
        value = section_type.get(f"{{{W}}}val", "nextPage") if section_type is not None else "nextPage"
        return value in {"nextPage", "oddPage", "evenPage"}
    return False


def boundary_before(children, target_index):
    if has_page_boundary(children[target_index]):
        return True
    index = target_index - 1
    while index >= 0:
        element = children[index]
        if has_page_boundary(element):
            return True
        if text_of(element):
            return False
        if element.tag == f"{{{W}}}tbl":
            return False
        index -= 1
    return False


def main():
    parser = argparse.ArgumentParser(description="检查论文前置部分的分页边界。")
    parser.add_argument("docx", type=Path)
    parser.add_argument(
        "--mode",
        choices=("auto", "required"),
        default="required",
        help="auto=只检查原稿已有部分；required=中文摘要、英文摘要和目录均必须存在",
    )
    args = parser.parse_args()
    path = args.docx
    with zipfile.ZipFile(path) as package:
        root = ET.fromstring(package.read("word/document.xml"))
    body = root.find("w:body", NS)
    children = list(body) if body is not None else []
    targets = {"中文摘要": {"摘要", "中文摘要"}, "英文摘要": {"ABSTRACT"}, "目录": {"目录"}}
    issues = []
    warnings = []
    found = {}
    for label, names in targets.items():
        match = None
        for index, element in enumerate(children):
            if element.tag == f"{{{W}}}p" and normalized(text_of(element)) in names:
                match = index
                break
        found[label] = match
        if match is None:
            target = issues if args.mode == "required" else warnings
            target.append({"part": label, "issue": "missing_or_nested_in_table"})
        elif not boundary_before(children, match):
            issues.append({"part": label, "issue": "no_page_or_next_page_section_break_before", "body_index": match})
    result = {"status": "pass" if not issues else "fail", "mode": args.mode, "found": found, "issues": issues, "warnings": warnings}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if not issues else 1)


if __name__ == "__main__":
    main()
