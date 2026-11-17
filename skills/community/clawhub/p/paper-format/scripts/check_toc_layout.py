#!/usr/bin/env python3
"""Audit DOCX table-of-contents placement and leader-tab formatting."""

from __future__ import annotations

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


def compact(text):
    return re.sub(r"[\s\u3000:：]", "", text).upper()


def style_id(paragraph):
    ppr = paragraph.find("w:pPr", NS)
    style = ppr.find("w:pStyle", NS) if ppr is not None else None
    return style.get(f"{{{W}}}val", "") if style is not None else ""


def has_page_boundary(element):
    ppr = element.find("w:pPr", NS)
    if ppr is not None:
        page_before = ppr.find("w:pageBreakBefore", NS)
        if page_before is not None and page_before.get(f"{{{W}}}val", "1").lower() not in {"0", "false", "off", "no"}:
            return True
        sect = ppr.find("w:sectPr", NS)
        if sect is not None:
            section_type = sect.find("w:type", NS)
            value = section_type.get(f"{{{W}}}val", "nextPage") if section_type is not None else "nextPage"
            if value in {"nextPage", "oddPage", "evenPage"}:
                return True
    return any(node.get(f"{{{W}}}type", "textWrapping") == "page" for node in element.findall(".//w:br", NS))


def boundary_before(children, target):
    if has_page_boundary(children[target]):
        return True
    index = target - 1
    while index >= 0:
        element = children[index]
        if has_page_boundary(element):
            return True
        if text_of(element) or element.tag == f"{{{W}}}tbl":
            return False
        index -= 1
    return False


def style_properties(styles_root):
    result = {}
    for style in styles_root.findall("w:style", NS):
        identifier = style.get(f"{{{W}}}styleId", "")
        result[identifier] = style.find("w:pPr", NS)
    return result


def effective_ppr(paragraph, styles):
    direct = paragraph.find("w:pPr", NS)
    inherited = styles.get(style_id(paragraph))
    return direct, inherited


def right_dot_tab(paragraph, styles):
    tabs = []
    for ppr in effective_ppr(paragraph, styles):
        if ppr is not None:
            tabs.extend(ppr.findall("w:tabs/w:tab", NS))
    return any(
        tab.get(f"{{{W}}}val") == "right" and tab.get(f"{{{W}}}leader") in {"dot", "middleDot"}
        for tab in tabs
    )


def main():
    if len(sys.argv) != 2:
        raise SystemExit("usage: check_toc_layout.py <file.docx>")
    path = Path(sys.argv[1])
    issues = []
    warnings = []
    with zipfile.ZipFile(path) as package:
        document = ET.fromstring(package.read("word/document.xml"))
        styles = style_properties(ET.fromstring(package.read("word/styles.xml")))

    body = document.find("w:body", NS)
    children = list(body) if body is not None else []
    paragraphs = [(i, element) for i, element in enumerate(children) if element.tag == f"{{{W}}}p"]

    toc_title = next((i for i, p in paragraphs if compact(text_of(p)) == "目录"), None)
    if toc_title is None:
        payload = {"status": "fail", "issues": [{"issue": "toc_title_not_found"}], "warnings": []}
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        raise SystemExit(1)

    if not boundary_before(children, toc_title):
        issues.append({"issue": "toc_not_started_on_new_page", "body_index": toc_title})

    # The TOC belongs after all available title/abstract front matter and before body chapters.
    for index, paragraph in paragraphs:
        normalized = compact(text_of(paragraph))
        sid = style_id(paragraph).lower()
        if index > toc_title and (
            normalized in {"摘要", "中文摘要", "ABSTRACT"}
            or sid in {"title", "论文标题", "papertitle"}
        ):
            issues.append({"issue": "toc_precedes_title_or_abstract", "later_body_index": index, "text": text_of(paragraph)[:80]})
    first_body = next(
        (
            i
            for i, paragraph in paragraphs
            if re.match(r"^(第[一二三四五六七八九十百0-9]+章|\d+(?:\.\d+)*\s*\D|绪论|引言)", text_of(paragraph).strip())
        ),
        None,
    )
    if first_body is not None and toc_title > first_body:
        issues.append({"issue": "toc_appears_after_body", "toc_index": toc_title, "first_body_index": first_body})

    toc_entries = []
    for index, paragraph in paragraphs:
        sid = style_id(paragraph)
        if re.fullmatch(r"TOC[1-9]", sid, re.I):
            toc_entries.append((index, paragraph, sid))
    if not toc_entries:
        issues.append({"issue": "no_toc_entry_paragraphs_found"})
    for index, paragraph, sid in toc_entries:
        if not paragraph.findall(".//w:tab", NS):
            issues.append({"issue": "toc_entry_missing_tab_character", "body_index": index, "style": sid, "text": text_of(paragraph)[:80]})
        if not right_dot_tab(paragraph, styles):
            issues.append({"issue": "toc_entry_missing_right_dot_leader_tab", "body_index": index, "style": sid, "text": text_of(paragraph)[:80]})
        if not re.search(r"\d+\s*$", text_of(paragraph)):
            warnings.append({"issue": "toc_entry_page_number_not_visible", "body_index": index, "style": sid, "text": text_of(paragraph)[:80]})

    instructions = " ".join(node.text or "" for node in document.findall(".//w:instrText", NS))
    if not re.search(r"\bTOC\b", instructions, re.I):
        issues.append({"issue": "real_toc_field_not_found"})

    payload = {
        "status": "pass" if not issues else "fail",
        "toc_title_body_index": toc_title,
        "toc_entries": len(toc_entries),
        "issues": issues,
        "warnings": warnings,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    raise SystemExit(0 if not issues else 1)


if __name__ == "__main__":
    main()
