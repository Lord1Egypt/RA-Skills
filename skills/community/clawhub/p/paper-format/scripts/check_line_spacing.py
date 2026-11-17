#!/usr/bin/env python3
import json
import sys
from pathlib import Path

from docx import Document
from docx.oxml.ns import qn


TARGET_STYLES = {"Normal", "正文", "摘要正文", "学术摘要正文"}


def spacing_value(paragraph):
    ppr = paragraph._p.pPr
    spacing = ppr.find(qn("w:spacing")) if ppr is not None else None
    if spacing is not None and spacing.get(qn("w:line")):
        line = int(spacing.get(qn("w:line")))
        rule = spacing.get(qn("w:lineRule"), "auto")
        return line / 240 if rule == "auto" else None
    style = paragraph.style
    while style is not None:
        ppr = style.element.pPr
        spacing = ppr.find(qn("w:spacing")) if ppr is not None else None
        if spacing is not None and spacing.get(qn("w:line")):
            line = int(spacing.get(qn("w:line")))
            rule = spacing.get(qn("w:lineRule"), "auto")
            return line / 240 if rule == "auto" else None
        style = style.base_style
    return None


def main():
    path = Path(sys.argv[1])
    doc = Document(path)
    issues = []
    checked = 0
    for i, p in enumerate(doc.paragraphs):
        if not p.text.strip() or p.style.name not in TARGET_STYLES:
            continue
        checked += 1
        value = spacing_value(p)
        if value is None or abs(value - 1.5) > 0.01:
            issues.append({"paragraph": i, "style": p.style.name, "line_spacing": value, "text": p.text[:80]})
    status = "fail" if issues else ("pass" if checked else "skipped")
    result = {
        "status": status,
        "checked": checked,
        "issues": issues,
        "reason": None if checked else "未找到可识别的正文或摘要正文样式，未执行行距断言。",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if not issues else 1)


if __name__ == "__main__":
    main()
