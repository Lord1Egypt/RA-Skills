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


def main():
    parser = argparse.ArgumentParser(description="检查 Word 页码字段结构及可见结果。")
    parser.add_argument("docx", type=Path)
    parser.add_argument(
        "--mode",
        choices=("structure", "visible"),
        default="visible",
        help="structure=只要求真实 PAGE 字段；visible=还要求字段已有刷新后的数字结果",
    )
    args = parser.parse_args()
    issues = []
    fields = 0
    numeric_results = 0
    with zipfile.ZipFile(args.docx) as package:
        for name in package.namelist():
            if not re.fullmatch(r"word/footer\d+\.xml", name):
                continue
            root = ET.fromstring(package.read(name))
            visible = "".join(node.text or "" for node in root.findall(".//w:t", NS))
            if re.search(r"\bPAGE\b|PAGE\\|PAGE\s*[~～]", visible, re.I):
                issues.append({"footer": name, "issue": "literal_page_field_text_visible", "text": visible[:80]})
            instructions = " ".join(node.text or "" for node in root.findall(".//w:instrText", NS))
            if re.search(r"\bPAGE\b", instructions, re.I):
                fields += 1
                if any(re.fullmatch(r"\d+", (node.text or "").strip()) for node in root.findall(".//w:t", NS)):
                    numeric_results += 1
    if fields == 0:
        issues.append({"issue": "real_page_field_not_found_in_footer"})
    warnings = []
    if fields and numeric_results == 0 and args.mode == "visible":
        issues.append({"issue": "page_field_has_no_refreshed_numeric_result"})
    elif fields and numeric_results == 0:
        warnings.append({"issue": "page_field_numeric_result_not_verified", "note": "需在 Word/WPS/LibreOffice 中刷新后检查显示结果。"})
    result = {"status": "pass" if not issues else "fail", "mode": args.mode, "page_fields": fields, "numeric_results": numeric_results, "issues": issues, "warnings": warnings}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if not issues else 1)


if __name__ == "__main__":
    main()
