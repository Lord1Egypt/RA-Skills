#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from zipfile import ZipFile

from lxml import etree


NS = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}


def local_name(tag: str) -> str:
    if "}" in tag:
        return tag.rsplit("}", 1)[1]
    return tag


def parse_xml(blob: bytes) -> etree._Element:
    parser = etree.XMLParser(remove_blank_text=False, recover=True)
    return etree.fromstring(blob, parser=parser)


def get_slide_size(presentation_root: etree._Element) -> dict[str, int]:
    node = presentation_root.find(".//p:sldSz", namespaces=NS)
    if node is None:
        raise ValueError("presentation.xml 中未找到 p:sldSz")
    return {"width": int(node.get("cx")), "height": int(node.get("cy"))}


def parse_theme(theme_root: etree._Element) -> dict[str, object]:
    colors: dict[str, str] = {}
    fonts: dict[str, str] = {}

    for scheme in theme_root.xpath(".//a:clrScheme/*", namespaces=NS):
        color_node = scheme.find(".//a:srgbClr", namespaces=NS)
        if color_node is not None and color_node.get("val"):
            colors[local_name(scheme.tag)] = color_node.get("val")

    font_scheme = theme_root.find(".//a:fontScheme", namespaces=NS)
    if font_scheme is not None:
        for group_name in ("majorFont", "minorFont"):
            group = font_scheme.find(f"./a:{group_name}", namespaces=NS)
            if group is None:
                continue
            for child_name in ("latin", "ea", "cs"):
                child = group.find(f"./a:{child_name}", namespaces=NS)
                if child is not None and child.get("typeface"):
                    fonts[f"{group_name}.{child_name}"] = child.get("typeface")

    return {"colors": colors, "fonts": fonts}


def find_xfrm(shape: etree._Element) -> etree._Element | None:
    xfrm = shape.find("./p:spPr/a:xfrm", namespaces=NS)
    if xfrm is not None:
        return xfrm
    return shape.find("./p:grpSpPr/a:xfrm", namespaces=NS)


def get_box(shape: etree._Element) -> dict[str, int] | None:
    xfrm = find_xfrm(shape)
    if xfrm is None:
        return None
    off = xfrm.find("./a:off", namespaces=NS)
    ext = xfrm.find("./a:ext", namespaces=NS)
    if off is None or ext is None:
        return None
    return {
        "x": int(off.get("x", "0")),
        "y": int(off.get("y", "0")),
        "width": int(ext.get("cx", "0")),
        "height": int(ext.get("cy", "0")),
    }


def collect_text(shape: etree._Element) -> list[str]:
    texts = shape.xpath(".//a:t/text()", namespaces=NS)
    return [t.strip() for t in texts if t and t.strip()]


def unique_ordered(values: list[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for value in values:
        if value not in seen:
            seen.add(value)
            ordered.append(value)
    return ordered


def collect_font_sizes(shape: etree._Element) -> list[int]:
    sizes: list[int] = []
    for node in shape.xpath(".//a:rPr[@sz] | .//a:endParaRPr[@sz]", namespaces=NS):
        raw = node.get("sz")
        if raw:
            sizes.append(int(raw))
    return sizes


def collect_typefaces(shape: etree._Element) -> list[str]:
    faces: list[str] = []
    for node in shape.xpath(
        ".//a:rPr | .//a:endParaRPr | .//a:defRPr", namespaces=NS
    ):
        for child_name in ("ea", "latin", "cs"):
            child = node.find(f"./a:{child_name}", namespaces=NS)
            if child is not None and child.get("typeface"):
                faces.append(child.get("typeface"))
    return unique_ordered(faces)


def collect_colors(shape: etree._Element) -> list[str]:
    colors: list[str] = []
    for node in shape.xpath(".//a:solidFill", namespaces=NS):
        srgb = node.find("./a:srgbClr", namespaces=NS)
        if srgb is not None and srgb.get("val"):
            colors.append(srgb.get("val"))
        scheme = node.find("./a:schemeClr", namespaces=NS)
        if scheme is not None and scheme.get("val"):
            colors.append(f"scheme:{scheme.get('val')}")
    return unique_ordered(colors)


def summarize_shape(shape: etree._Element, slide_size: dict[str, int]) -> dict[str, object]:
    box = get_box(shape)
    texts = collect_text(shape)
    sizes = collect_font_sizes(shape)
    typefaces = collect_typefaces(shape)
    colors = collect_colors(shape)

    summary: dict[str, object] = {
        "shape_type": local_name(shape.tag),
        "name": None,
    }

    c_nv_pr = shape.find("./p:nvSpPr/p:cNvPr", namespaces=NS)
    if c_nv_pr is None:
        c_nv_pr = shape.find("./p:nvPicPr/p:cNvPr", namespaces=NS)
    if c_nv_pr is not None:
        summary["name"] = c_nv_pr.get("name")

    if box is not None:
        summary["box"] = box
        slide_w = slide_size["width"]
        slide_h = slide_size["height"]
        summary["box_ratio"] = {
            "x": round(box["x"] / slide_w, 4) if slide_w else 0,
            "y": round(box["y"] / slide_h, 4) if slide_h else 0,
            "width": round(box["width"] / slide_w, 4) if slide_w else 0,
            "height": round(box["height"] / slide_h, 4) if slide_h else 0,
        }

    if texts:
        summary["text"] = " | ".join(texts[:8])
        summary["text_count"] = len(texts)

    if sizes:
        summary["font_size_stats"] = {
            "min": min(sizes),
            "max": max(sizes),
            "distinct": sorted(set(sizes)),
        }

    if typefaces:
        summary["typefaces"] = typefaces

    if colors:
        summary["colors"] = colors

    return summary


def slide_sort_key(name: str) -> int:
    match = re.search(r"slide(\d+)\.xml$", name)
    return int(match.group(1)) if match else 0


def build_report(pptx_path: Path) -> dict[str, object]:
    with ZipFile(pptx_path) as zf:
        presentation = parse_xml(zf.read("ppt/presentation.xml"))
        slide_size = get_slide_size(presentation)

        theme = {}
        if "ppt/theme/theme1.xml" in zf.namelist():
            theme = parse_theme(parse_xml(zf.read("ppt/theme/theme1.xml")))

        slide_names = sorted(
            [name for name in zf.namelist() if re.match(r"ppt/slides/slide\d+\.xml$", name)],
            key=slide_sort_key,
        )

        slides: list[dict[str, object]] = []
        for slide_name in slide_names:
            root = parse_xml(zf.read(slide_name))
            sp_tree = root.find(".//p:spTree", namespaces=NS)
            shape_summaries: list[dict[str, object]] = []
            slide_texts: list[str] = []

            if sp_tree is not None:
                for child in sp_tree:
                    if local_name(child.tag) not in {"sp", "pic", "grpSp", "graphicFrame"}:
                        continue
                    summary = summarize_shape(child, slide_size)
                    shape_summaries.append(summary)
                    text = summary.get("text")
                    if isinstance(text, str):
                        slide_texts.extend([part.strip() for part in text.split("|") if part.strip()])

            slides.append(
                {
                    "slide": slide_name,
                    "headline": " | ".join(slide_texts[:8]),
                    "shape_count": len(shape_summaries),
                    "shapes": shape_summaries,
                }
            )

    return {
        "file": str(pptx_path),
        "slide_size": slide_size,
        "aspect_ratio": round(slide_size["width"] / slide_size["height"], 4)
        if slide_size["height"]
        else None,
        "theme": theme,
        "slide_count": len(slides),
        "slides": slides,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Dump PPTX layout and theme details as JSON.")
    parser.add_argument("pptx", type=Path, help="Path to a .pptx file")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output")
    args = parser.parse_args()

    report = build_report(args.pptx)
    print(json.dumps(report, ensure_ascii=False, indent=2 if args.pretty else None))


if __name__ == "__main__":
    main()
