#!/usr/bin/env python3
import json
import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
NS = {"w": W}
DATE = re.compile(r"\d{4} 年 \d{1,2} 月 \d{1,2} 日")


def text_of(element):
    return "".join(node.text or "" for node in element.findall(".//w:t", NS)).strip()


def main():
    if len(sys.argv) != 2:
        raise SystemExit("usage: check_cover_layout.py <file.docx>")
    issues = []
    with zipfile.ZipFile(Path(sys.argv[1])) as package:
        document = ET.fromstring(package.read("word/document.xml"))
        body = document.find("w:body", NS)
        children = list(body) if body is not None else []
        abstract_index = next((i for i, e in enumerate(children) if re.sub(r"[\s\u3000]", "", text_of(e)) in {"摘要", "中文摘要"}), len(children))
        cover_children = children[:abstract_index]
        if any(element.tag == f"{{{W}}}tbl" for element in cover_children):
            issues.append({"issue": "cover_identity_fields_must_not_use_table"})
        required_labels = {"姓名": False, "专业": False, "学校": False}
        optional_labels = {"学号", "学院", "指导教师"}
        for paragraph in (e for e in cover_children if e.tag == f"{{{W}}}p"):
            raw = text_of(paragraph)
            compact = re.sub(r"[\s\u3000:：]", "", raw)
            label = next((name for name in tuple(required_labels) + tuple(optional_labels) if compact.startswith(name)), None)
            if label is None:
                continue
            if label in required_labels:
                required_labels[label] = True
            ppr = paragraph.find("w:pPr", NS)
            jc = ppr.find("w:jc", NS) if ppr is not None else None
            if jc is None or jc.get(f"{{{W}}}val") != "center":
                issues.append({"issue": "cover_field_not_centered", "label": label})
            runs = paragraph.findall("w:r", NS)
            for run in runs:
                rpr = run.find("w:rPr", NS)
                fonts = rpr.find("w:rFonts", NS) if rpr is not None else None
                size = rpr.find("w:sz", NS) if rpr is not None else None
                east_asia = fonts.get(f"{{{W}}}eastAsia") if fonts is not None else None
                points = size.get(f"{{{W}}}val") if size is not None else None
                if east_asia != "宋体" or points != "28":
                    issues.append({"issue": "cover_field_not_14pt_simsun", "label": label, "font": east_asia, "half_points": points})
                    break
            has_underline = any(run.find("w:rPr/w:u", NS) is not None for run in runs) or "_" in raw
            if not has_underline:
                issues.append({"issue": "cover_field_fill_line_missing", "label": label})
        for label, present in required_labels.items():
            if not present:
                issues.append({"issue": "required_cover_field_missing", "label": label})
        cover_text = "".join(text_of(element) for element in cover_children)
        if "日期" in cover_text or "提交日期" in cover_text:
            issues.append({"issue": "date_label_must_not_be_shown_in_cover_body"})
        if DATE.search(cover_text):
            issues.append({"issue": "date_must_be_in_cover_footer_not_cover_body"})
        rels = ET.fromstring(package.read("word/_rels/document.xml.rels"))
        rel_map = {rel.get("Id"): "word/" + rel.get("Target", "").lstrip("/") for rel in list(rels)}
        sections = document.findall(".//w:sectPr", NS)
        footer_ids = []
        for section in sections[:2]:
            ref = section.find("w:footerReference[@w:type='default']", NS)
            footer_ids.append(ref.get(f"{{{R}}}id") if ref is not None else None)
        if not footer_ids or footer_ids[0] is None:
            issues.append({"issue": "cover_footer_reference_not_found"})
        elif len(footer_ids) < 2 or footer_ids[1] in {None, footer_ids[0]}:
            issues.append({"issue": "section_after_cover_inherits_date_footer", "footer_ids": footer_ids})
        footer_matches = []
        cover_footer = rel_map.get(footer_ids[0]) if footer_ids and footer_ids[0] else None
        if cover_footer in package.namelist():
            footer = ET.fromstring(package.read(cover_footer))
            for paragraph in footer.findall(".//w:p", NS):
                text = text_of(paragraph)
                if DATE.fullmatch(text):
                    ppr = paragraph.find("w:pPr", NS)
                    jc = ppr.find("w:jc", NS) if ppr is not None else None
                    footer_matches.append({"part": cover_footer, "text": text, "centered": jc is not None and jc.get(f"{{{W}}}val") == "center"})
        if not footer_matches:
            issues.append({"issue": "centered_cover_date_footer_not_found"})
        elif not any(match["centered"] for match in footer_matches):
            issues.append({"issue": "cover_date_footer_not_centered", "matches": footer_matches})
    result = {"status": "pass" if not issues else "fail", "footer_dates": footer_matches, "issues": issues}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if not issues else 1)


if __name__ == "__main__":
    main()
