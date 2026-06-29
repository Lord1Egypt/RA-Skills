#!/usr/bin/env python3
"""
Gxpcode Markdown — generate bilingual Markdown from paddleocr elements + translated.json.

Usage:
  python Gxpcode_markdown.py --elements recognition.json --translated translated.json --out-dir output/ --title "ISPE Guide"
"""

import json, sys, re
from pathlib import Path
from datetime import datetime

if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")


def flatten_elements(data: dict) -> list:
    flat = []
    for page in data.get("pages", []):
        pn = page["page_number"]
        for el in page.get("elements", []):
            flat.append({
                "label": el["label"],
                "text": el["text"],
                "page": pn,
                "reading_order": el.get("reading_order", 0),
            })
    flat.sort(key=lambda x: (x["page"], x["reading_order"]))
    return flat


def load_translated_json(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_zh_lookup(tj: dict) -> dict:
    return {el["index"]: el["zh"] for el in tj.get("elements", [])}


def is_heading(label: str) -> bool:
    return label in ("sec", "sub_sec", "sub_sub_sec")


def build_markdown(data: dict, translated_json: dict, title: str) -> str:
    elements = flatten_elements(data)
    zh_lookup = build_zh_lookup(translated_json)
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")

    lines = [
        f"# {title}",
        "",
        f"> 双语对照 | {ts} | EN → ZH",
        "",
        "---",
        "",
    ]

    for i, el in enumerate(elements):
        en = el["text"]
        zh = zh_lookup.get(i, "")

        if is_heading(el["label"]):
            lines.append(f"## {en}")
            if zh:
                lines.append(f"**{zh}**")
            lines.append("")
        else:
            lines.append(f"| EN | ZH |")
            lines.append(f"| --- | --- |")
            # Escape pipes in content
            en_safe = en.replace("|", "\\|").replace("\n", " ")
            zh_safe = zh.replace("|", "\\|").replace("\n", " ")
            lines.append(f"| {en_safe} | {zh_safe} |")
            lines.append("")

    return "\n".join(lines)


def main():
    import argparse
    p = argparse.ArgumentParser(description="Generate Gxpcode bilingual Markdown")
    p.add_argument("--elements", required=True)
    p.add_argument("--translated", required=True)
    p.add_argument("--out-dir", required=True)
    p.add_argument("--title", default="Gxpcode Translation")
    args = p.parse_args()

    data = None
    with open(args.elements, "r", encoding="utf-8-sig") as f:
        data = json.load(f)
    tj = load_translated_json(args.translated)

    md = build_markdown(data, tj, args.title)

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    import re
    safe_title = re.sub(r'[\\/*?:"<>|]', '', args.title).replace(' ', '_')[:80]
    out_path = out_dir / f"Gxpcode-{safe_title}.md"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(md)

    print(f"Gxpcode-{safe_title}.md written to {out_path}")


if __name__ == "__main__":
    main()
