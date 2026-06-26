#!/usr/bin/env python3
import argparse
import re
import sys
from pathlib import Path


PREVIEW_TEXT_FRAGMENTS = [
    "首页默认展示的是空态预览",
    "载入真实的 share-card 数据和最终图片后",
    "The home page starts in an empty preview state.",
    "Real content appears only after a valid share-card payload",
]


REMOVED_UI_FRAGMENTS = [
    'id="langZh"',
    'id="langEn"',
    'id="exportCardBtn"',
    "html2canvas.min.js",
]


def fail(message: str):
    print("[FAIL] " + message)
    sys.exit(1)


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception as exc:
        fail(f"cannot read {path}: {exc}")


def extract_element_text(html: str, tag: str, element_id: str) -> str:
    pattern = rf'<{tag}[^>]*id="{re.escape(element_id)}"[^>]*>(.*?)</{tag}>'
    match = re.search(pattern, html, flags=re.DOTALL)
    if not match:
        fail(f"missing visible element #{element_id}")
    text = re.sub(r"<[^>]+>", "", match.group(1))
    return " ".join(text.split())


def validate_rendered_html(html: str):
    if 'id="photoId"' in html:
        fail("rendered HTML must not expose the internal card_id marker on the poster face")

    for fragment in REMOVED_UI_FRAGMENTS:
        if fragment in html:
            fail(f"rendered HTML must not include removed language-toggle or export UI (`{fragment}`)")

    badge = extract_element_text(html, "span", "posterBadge")
    if badge in {"Agent Selfie", "CARD"}:
        fail(f"posterBadge must not fall back to a generic internal label (`{badge}`)")

    headline = extract_element_text(html, "h2", "sideHeadline")
    if headline in {"Agent Share Card Preview", "Share Card Preview"}:
        fail(f"sideHeadline must come from real card data, got preview text `{headline}`")

    subheadline = extract_element_text(html, "p", "subheadline")
    for fragment in PREVIEW_TEXT_FRAGMENTS:
        if fragment in subheadline:
            fail(f"subheadline still exposes preview copy (`{fragment}`)")


def main():
    parser = argparse.ArgumentParser(description="Validate rendered final HTML does not expose preview-only or internal poster fields")
    parser.add_argument("html_file", help="Path to rendered selfie-card HTML")
    args = parser.parse_args()

    html_path = Path(args.html_file)
    validate_rendered_html(read_text(html_path))
    print("[OK] Rendered HTML is valid")


if __name__ == "__main__":
    main()
