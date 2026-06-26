#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from lxml import etree


NS = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}


def parse_xml(blob: bytes) -> etree._Element:
    parser = etree.XMLParser(remove_blank_text=False, recover=True)
    return etree.fromstring(blob, parser=parser)


def serialize_xml(root: etree._Element) -> bytes:
    return etree.tostring(
        root, encoding="UTF-8", xml_declaration=True, standalone=True
    )


def local_name(tag: str) -> str:
    if "}" in tag:
        return tag.rsplit("}", 1)[1]
    return tag


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


def set_box(shape: etree._Element, box: dict[str, int]) -> None:
    xfrm = find_xfrm(shape)
    if xfrm is None:
        return
    off = xfrm.find("./a:off", namespaces=NS)
    ext = xfrm.find("./a:ext", namespaces=NS)
    if off is None or ext is None:
        return
    off.set("x", str(int(box["x"])))
    off.set("y", str(int(box["y"])))
    ext.set("cx", str(int(box["width"])))
    ext.set("cy", str(int(box["height"])))


def get_slide_size(presentation_root: etree._Element) -> tuple[int, int]:
    node = presentation_root.find(".//p:sldSz", namespaces=NS)
    if node is None:
        raise ValueError("presentation.xml 中未找到 p:sldSz")
    return int(node.get("cx")), int(node.get("cy"))


def set_slide_size(presentation_root: etree._Element, width: int, height: int) -> None:
    node = presentation_root.find(".//p:sldSz", namespaces=NS)
    if node is None:
        raise ValueError("presentation.xml 中未找到 p:sldSz")
    node.set("cx", str(width))
    node.set("cy", str(height))


def collect_text(shape: etree._Element) -> str:
    texts = [t.strip() for t in shape.xpath(".//a:t/text()", namespaces=NS) if t and t.strip()]
    return " ".join(texts)


def font_sizes(shape: etree._Element) -> list[int]:
    sizes: list[int] = []
    for node in shape.xpath(".//a:rPr[@sz] | .//a:endParaRPr[@sz]", namespaces=NS):
        raw = node.get("sz")
        if raw:
            sizes.append(int(raw))
    return sizes


def scale_fonts(shape: etree._Element, factor: float) -> None:
    if factor <= 0:
        return
    for node in shape.xpath(".//a:rPr[@sz] | .//a:endParaRPr[@sz]", namespaces=NS):
        raw = node.get("sz")
        if not raw:
            continue
        new_size = max(800, int(round(int(raw) * factor)))
        node.set("sz", str(new_size))


def enable_text_autofit(shape: etree._Element) -> None:
    tx_body = shape.find("./p:txBody", namespaces=NS)
    if tx_body is None:
        return
    body_pr = tx_body.find("./a:bodyPr", namespaces=NS)
    if body_pr is None:
        return

    for child in list(body_pr):
        if local_name(child.tag) in {"noAutofit", "normAutofit", "spAutoFit"}:
            body_pr.remove(child)

    autofit = etree.SubElement(body_pr, f"{{{NS['a']}}}normAutofit")
    autofit.set("fontScale", "100000")
    autofit.set("lnSpcReduction", "0")


def classify_slide(slide_root: etree._Element, slide_index: int, total_slides: int) -> str:
    texts = [t.strip().upper() for t in slide_root.xpath(".//a:t/text()", namespaces=NS) if t and t.strip()]
    joined = " ".join(texts)
    if slide_index == 1:
        return "cover"
    if slide_index == total_slides:
        return "closing"
    if "CHAPTER" in joined:
        return "chapter"
    if any(token in joined for token in ["CONTENTS", "目录"]):
        return "contents"
    return "content"


def is_text_shape(shape: etree._Element) -> bool:
    return shape.find("./p:txBody", namespaces=NS) is not None


def is_picture(shape: etree._Element) -> bool:
    return local_name(shape.tag) == "pic"


def is_full_bleed(box: dict[str, int], old_w: int, old_h: int) -> bool:
    return (
        box["x"] <= old_w * 0.03
        and box["y"] <= old_h * 0.03
        and box["width"] >= old_w * 0.94
        and box["height"] >= old_h * 0.94
    )


def is_horizontal_rule(box: dict[str, int], old_w: int, old_h: int) -> bool:
    return box["height"] <= old_h * 0.025 and box["width"] >= old_w * 0.05


def frame_scale_for_slide(slide_kind: str, old_w: int, new_w: int) -> float:
    growth = max(0.0, new_w / old_w - 1.0) if old_w else 0.0
    weight = {
        "cover": 0.10,
        "chapter": 0.09,
        "closing": 0.10,
        "contents": 0.14,
        "content": 0.16,
    }.get(slide_kind, 0.14)
    return min(1.0 + growth * weight, (new_w / old_w) * 0.92 if old_w else 1.0)


def clamp_box(box: dict[str, int], slide_w: int, slide_h: int) -> dict[str, int]:
    clamped = dict(box)
    clamped["width"] = max(1, min(clamped["width"], slide_w))
    clamped["height"] = max(1, min(clamped["height"], slide_h))
    clamped["x"] = max(0, min(clamped["x"], slide_w - clamped["width"]))
    clamped["y"] = max(0, min(clamped["y"], slide_h - clamped["height"]))
    return clamped


def adjust_box(
    shape: etree._Element,
    box: dict[str, int],
    old_w: int,
    old_h: int,
    new_w: int,
    new_h: int,
    slide_kind: str,
    target_mode: str,
) -> dict[str, int]:
    x_scale = new_w / old_w if old_w else 1.0
    y_scale = new_h / old_h if old_h else 1.0

    if is_full_bleed(box, old_w, old_h):
        return {"x": 0, "y": 0, "width": new_w, "height": new_h}

    frame_scale = frame_scale_for_slide(slide_kind, old_w, new_w)
    frame_w = int(round(old_w * frame_scale))
    frame_x = int(round((new_w - frame_w) / 2))

    new_box = {
        "x": int(round(frame_x + box["x"] * frame_scale)),
        "y": box["y"],
        "width": int(round(box["width"] * frame_scale)),
        "height": box["height"],
    }

    if target_mode == "exact-reference":
        new_box["y"] = int(round(box["y"] * y_scale))
        new_box["height"] = max(1, int(round(box["height"] * y_scale)))

    if is_horizontal_rule(box, old_w, old_h):
        new_box["width"] = int(round(box["width"] * max(frame_scale, 1.14)))

    if is_text_shape(shape):
        text = collect_text(shape)
        sizes = font_sizes(shape)
        max_size = max(sizes) if sizes else 0
        title_like = max_size >= 3000 or len(text) <= 30

        if title_like:
            new_box["width"] = int(round(box["width"] * min(frame_scale, 1.08)))
        else:
            new_box["width"] = int(round(box["width"] * min(frame_scale, 1.12)))
            if max_size and max_size <= 2200:
                enable_text_autofit(shape)

        if target_mode == "exact-reference":
            font_factor = min(x_scale, y_scale)
            if not title_like:
                font_factor *= 0.96
            scale_fonts(shape, font_factor)

    return clamp_box(new_box, new_w, new_h)


def slide_sort_key(name: str) -> int:
    match = re.search(r"slide(\d+)\.xml$", name)
    return int(match.group(1)) if match else 0


def transform_pptx(
    source: Path,
    reference: Path,
    output: Path,
    target_mode: str,
) -> dict[str, object]:
    with ZipFile(source) as src_zip, ZipFile(reference) as ref_zip:
        presentation_root = parse_xml(src_zip.read("ppt/presentation.xml"))
        old_w, old_h = get_slide_size(presentation_root)

        ref_presentation = parse_xml(ref_zip.read("ppt/presentation.xml"))
        ref_w, ref_h = get_slide_size(ref_presentation)
        ref_ratio = ref_w / ref_h

        if target_mode == "exact-reference":
            new_w, new_h = ref_w, ref_h
        else:
            new_h = old_h
            new_w = int(round(old_h * ref_ratio))

        set_slide_size(presentation_root, new_w, new_h)

        slide_names = sorted(
            [name for name in src_zip.namelist() if re.match(r"ppt/slides/slide\d+\.xml$", name)],
            key=slide_sort_key,
        )
        total_slides = len(slide_names)

        transformed: dict[str, bytes] = {
            "ppt/presentation.xml": serialize_xml(presentation_root)
        }
        slide_reports: list[dict[str, object]] = []

        for index, slide_name in enumerate(slide_names, start=1):
            root = parse_xml(src_zip.read(slide_name))
            sp_tree = root.find(".//p:spTree", namespaces=NS)
            slide_kind = classify_slide(root, index, total_slides)
            adjusted_shapes = 0

            if sp_tree is not None:
                for child in sp_tree:
                    if local_name(child.tag) not in {"sp", "pic", "grpSp", "graphicFrame"}:
                        continue
                    box = get_box(child)
                    if box is None:
                        continue
                    new_box = adjust_box(
                        child, box, old_w, old_h, new_w, new_h, slide_kind, target_mode
                    )
                    if new_box != box:
                        set_box(child, new_box)
                        adjusted_shapes += 1

            transformed[slide_name] = serialize_xml(root)
            slide_reports.append(
                {
                    "slide": slide_name,
                    "slide_kind": slide_kind,
                    "adjusted_shapes": adjusted_shapes,
                }
            )

        with ZipFile(output, "w", compression=ZIP_DEFLATED) as out_zip:
            for info in src_zip.infolist():
                data = transformed.get(info.filename)
                if data is None:
                    data = src_zip.read(info.filename)
                out_zip.writestr(info.filename, data)

    return {
        "source": str(source),
        "reference": str(reference),
        "output": str(output),
        "target_mode": target_mode,
        "old_size": {"width": old_w, "height": old_h},
        "new_size": {"width": new_w, "height": new_h},
        "aspect_ratio": round(new_w / new_h, 4) if new_h else None,
        "slides": slide_reports,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Retarget a PPTX to an ultra-wide aspect ratio without stretching text."
    )
    parser.add_argument("source", type=Path, help="Source PPTX")
    parser.add_argument("--reference", type=Path, required=True, help="Reference PPTX")
    parser.add_argument("--output", type=Path, required=True, help="Output PPTX path")
    parser.add_argument(
        "--target-mode",
        choices=["preserve-height", "exact-reference"],
        default="preserve-height",
        help="preserve-height: keep source height and use reference aspect ratio; exact-reference: use the reference canvas size exactly",
    )
    parser.add_argument("--report", action="store_true", help="Print JSON report")
    args = parser.parse_args()

    args.output.parent.mkdir(parents=True, exist_ok=True)
    report = transform_pptx(
        source=args.source,
        reference=args.reference,
        output=args.output,
        target_mode=args.target_mode,
    )

    if args.report:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
