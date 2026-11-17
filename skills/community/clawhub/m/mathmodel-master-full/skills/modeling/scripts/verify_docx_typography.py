#!/usr/bin/env python3
"""Audit DOCX typography for CUMCM modeling papers.

Default rule:
- Latin text, numbers, and headings use Times New Roman.
- Chinese / East Asian text uses SimSun / 宋体.
- Title and heading text must be black or automatic black.

The check is structural. It inspects styles, document body, headers, footers,
footnotes, and endnotes for explicit font declarations. It cannot replace a
rendered Word/PDF visual review.
"""

from __future__ import annotations

import argparse
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}

TEXT_PARTS = (
    "word/document.xml",
    "word/styles.xml",
    "word/footnotes.xml",
    "word/endnotes.xml",
)

DISALLOWED_DEFAULTS = {
    "Calibri",
    "Arial",
    "Aptos",
    "Cambria",
    "Microsoft YaHei",
    "微软雅黑",
    "等线",
    "DengXian",
    "SimHei",
    "黑体",
}

REQUIRED_STYLE_IDS = ("Normal", "Heading1", "Heading2", "Heading3")
TITLE_AND_HEADING_STYLE_IDS = ("Title", "Heading1", "Heading2", "Heading3")
BLACK_COLOR_VALUES = {None, "", "auto", "000000"}


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def read_xml(zf: zipfile.ZipFile, name: str) -> ET.Element | None:
    try:
        return ET.fromstring(zf.read(name))
    except KeyError:
        return None


def iter_xml_parts(zf: zipfile.ZipFile) -> list[tuple[str, ET.Element]]:
    names = list(TEXT_PARTS)
    names.extend(name for name in zf.namelist() if name.startswith("word/header") and name.endswith(".xml"))
    names.extend(name for name in zf.namelist() if name.startswith("word/footer") and name.endswith(".xml"))
    parts = []
    for name in dict.fromkeys(names):
        root = read_xml(zf, name)
        if root is not None:
            parts.append((name, root))
    return parts


def font_attrs(node: ET.Element) -> dict[str, str]:
    return {
        key: value
        for key, value in {
            "ascii": node.get(f"{{{NS['w']}}}ascii"),
            "hAnsi": node.get(f"{{{NS['w']}}}hAnsi"),
            "eastAsia": node.get(f"{{{NS['w']}}}eastAsia"),
            "cs": node.get(f"{{{NS['w']}}}cs"),
        }.items()
        if value
    }


def style_id(style: ET.Element) -> str | None:
    return style.get(f"{{{NS['w']}}}styleId")


def style_element_map(styles_root: ET.Element | None) -> dict[str, ET.Element]:
    if styles_root is None:
        return {}
    result: dict[str, ET.Element] = {}
    for style in styles_root.findall(".//w:style", NS):
        sid = style_id(style)
        if sid:
            result[sid] = style
    return result


def style_font_map(styles_root: ET.Element | None) -> dict[str, dict[str, str]]:
    if styles_root is None:
        return {}
    result: dict[str, dict[str, str]] = {}
    for style in styles_root.findall(".//w:style", NS):
        sid = style_id(style)
        r_fonts = style.find(".//w:rPr/w:rFonts", NS)
        if sid and r_fonts is not None:
            result[sid] = font_attrs(r_fonts)
    return result


def color_desc(color: ET.Element | None) -> str:
    if color is None:
        return "auto"
    val = color.get(f"{{{NS['w']}}}val")
    theme = color.get(f"{{{NS['w']}}}themeColor")
    shade = color.get(f"{{{NS['w']}}}themeShade")
    tint = color.get(f"{{{NS['w']}}}themeTint")
    parts = [f"val={val!r}"]
    if theme:
        parts.append(f"themeColor={theme!r}")
    if shade:
        parts.append(f"themeShade={shade!r}")
    if tint:
        parts.append(f"themeTint={tint!r}")
    return ", ".join(parts)


def is_black_or_auto(color: ET.Element | None) -> bool:
    if color is None:
        return True
    val = color.get(f"{{{NS['w']}}}val")
    if val is None:
        return False
    return val.lower() in BLACK_COLOR_VALUES


def paragraph_style_id(paragraph: ET.Element) -> str | None:
    p_style = paragraph.find("./w:pPr/w:pStyle", NS)
    if p_style is None:
        return None
    return p_style.get(f"{{{NS['w']}}}val")


def audit_docx(
    docx_path: Path,
    latin_font: str,
    east_asia_font: str,
    allow_missing_style_fonts: bool,
    allow_colored_headings: bool,
) -> tuple[bool, list[str]]:
    messages: list[str] = []
    failed = False

    with zipfile.ZipFile(docx_path) as zf:
        styles_root = read_xml(zf, "word/styles.xml")
        style_elements = style_element_map(styles_root)
        styles = style_font_map(styles_root)
        parts = iter_xml_parts(zf)

        for sid in REQUIRED_STYLE_IDS:
            attrs = styles.get(sid, {})
            if not attrs:
                message = f"STYLE WARNING: {sid} has no explicit w:rFonts declaration."
                if allow_missing_style_fonts:
                    messages.append(message)
                else:
                    failed = True
                    messages.append(message.replace("WARNING", "ERROR"))
                continue
            for key in ("ascii", "hAnsi"):
                if attrs.get(key) != latin_font:
                    failed = True
                    messages.append(f"STYLE ERROR: {sid} {key}={attrs.get(key)!r}, expected {latin_font!r}.")
            if attrs.get("eastAsia") not in {east_asia_font, "宋体"}:
                failed = True
                messages.append(f"STYLE ERROR: {sid} eastAsia={attrs.get('eastAsia')!r}, expected {east_asia_font!r}/'宋体'.")

        if not allow_colored_headings:
            for sid in TITLE_AND_HEADING_STYLE_IDS:
                style = style_elements.get(sid)
                if style is None:
                    continue
                color = style.find(".//w:rPr/w:color", NS)
                if not is_black_or_auto(color):
                    failed = True
                    messages.append(f"COLOR ERROR: {sid} style color {color_desc(color)}, expected black/auto.")

            heading_color_hits: list[str] = []
            for part_name, root in parts:
                if part_name == "word/styles.xml":
                    continue
                for index, paragraph in enumerate(root.findall(".//w:p", NS), start=1):
                    sid = paragraph_style_id(paragraph)
                    if sid not in TITLE_AND_HEADING_STYLE_IDS:
                        continue
                    for color in paragraph.findall(".//w:rPr/w:color", NS):
                        if not is_black_or_auto(color):
                            heading_color_hits.append(f"{part_name}: paragraph {index} style={sid} color {color_desc(color)}")
            if heading_color_hits:
                failed = True
                messages.append(f"COLOR ERROR: non-black title/heading runs found ({len(heading_color_hits)} hit(s)).")
                messages.extend(f"  {hit}" for hit in heading_color_hits[:20])

        explicit_font_count = 0
        disallowed_hits: list[str] = []
        unexpected_latin: list[str] = []
        unexpected_east_asia: list[str] = []

        for part_name, root in parts:
            for r_fonts in root.findall(".//w:rFonts", NS):
                explicit_font_count += 1
                if part_name == "word/styles.xml":
                    continue
                attrs = font_attrs(r_fonts)
                for key, value in attrs.items():
                    if value in DISALLOWED_DEFAULTS:
                        disallowed_hits.append(f"{part_name}: {key}={value}")
                for key in ("ascii", "hAnsi"):
                    value = attrs.get(key)
                    if value and value != latin_font and value not in DISALLOWED_DEFAULTS:
                        unexpected_latin.append(f"{part_name}: {key}={value}")
                value = attrs.get("eastAsia")
                if value and value not in {east_asia_font, "宋体"} and value not in DISALLOWED_DEFAULTS:
                    unexpected_east_asia.append(f"{part_name}: eastAsia={value}")

        if disallowed_hits:
            failed = True
            messages.append(f"FONT ERROR: disallowed default fonts found ({len(disallowed_hits)} hit(s)).")
            messages.extend(f"  {hit}" for hit in disallowed_hits[:20])
        if unexpected_latin:
            failed = True
            messages.append(f"FONT ERROR: unexpected Latin fonts found ({len(unexpected_latin)} hit(s)).")
            messages.extend(f"  {hit}" for hit in unexpected_latin[:20])
        if unexpected_east_asia:
            failed = True
            messages.append(f"FONT ERROR: unexpected East Asian fonts found ({len(unexpected_east_asia)} hit(s)).")
            messages.extend(f"  {hit}" for hit in unexpected_east_asia[:20])

        messages.insert(0, f"explicit_rFonts_nodes: {explicit_font_count}")
        messages.insert(0, f"docx: {docx_path}")

    return failed, messages


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify DOCX font declarations for CUMCM papers.")
    parser.add_argument("docx", help="Path to .docx file")
    parser.add_argument("--latin-font", default="Times New Roman", help="Expected Latin font")
    parser.add_argument("--east-asia-font", default="SimSun", help="Expected East Asian font")
    parser.add_argument("--allow-missing-style-fonts", action="store_true", help="Warn instead of fail when required styles omit rFonts")
    parser.add_argument("--allow-colored-headings", action="store_true", help="Do not fail on non-black title or heading colors")
    args = parser.parse_args()

    docx_path = Path(args.docx)
    if not docx_path.exists():
        print(f"ERROR: file not found: {docx_path}", file=sys.stderr)
        return 2

    failed, messages = audit_docx(
        docx_path=docx_path,
        latin_font=args.latin_font,
        east_asia_font=args.east_asia_font,
        allow_missing_style_fonts=args.allow_missing_style_fonts,
        allow_colored_headings=args.allow_colored_headings,
    )
    for message in messages:
        print(message)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
