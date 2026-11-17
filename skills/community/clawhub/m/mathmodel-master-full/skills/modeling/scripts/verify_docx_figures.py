#!/usr/bin/env python3
"""Audit figures in a DOCX for captions and nearby explanations."""

import argparse
import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
}

CAPTION_RE = re.compile(r"^\s*图\s*\d+[\s\.．、:：-]")
HEADING_RE = re.compile(r"^\s*(摘要|[一二三四五六七八九十]+、|\d+(?:\.\d+)+|参考文献|附录)")


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def paragraph_text(p: ET.Element) -> str:
    return "".join(t.text or "" for t in p.findall(".//w:t", NS)).strip()


def paragraph_has_image(p: ET.Element) -> bool:
    return any(local_name(node.tag) in {"drawing", "pict"} for node in p.iter())


def read_document_xml(docx_path: Path) -> ET.Element:
    with zipfile.ZipFile(docx_path) as zf:
        try:
            return ET.fromstring(zf.read("word/document.xml"))
        except KeyError as exc:
            raise RuntimeError("word/document.xml not found; file may not be a valid DOCX") from exc


def is_explanation(text: str, min_chars: int) -> bool:
    if len(text) < min_chars:
        return False
    if CAPTION_RE.search(text) or HEADING_RE.search(text):
        return False
    if text.startswith(("表", "代码", "附图")):
        return False
    return True


def audit(docx_path: Path, min_explanation_chars: int) -> dict:
    root = read_document_xml(docx_path)
    paragraphs = []
    for p in root.findall(".//w:p", NS):
        text = paragraph_text(p)
        has_image = paragraph_has_image(p)
        if text or has_image:
            paragraphs.append({"text": text, "has_image": has_image})

    image_indices = [i for i, item in enumerate(paragraphs) if item["has_image"]]
    caption_indices = [i for i, item in enumerate(paragraphs) if CAPTION_RE.search(item["text"])]

    captioned_images = 0
    caption_explanations = []
    missing_caption_images = []
    for image_idx in image_indices:
        nearby_caption = None
        for j in range(image_idx + 1, min(len(paragraphs), image_idx + 5)):
            if CAPTION_RE.search(paragraphs[j]["text"]):
                nearby_caption = j
                break
        if nearby_caption is None:
            missing_caption_images.append(image_idx)
            continue
        captioned_images += 1

    for caption_idx in caption_indices:
        explanation = None
        for j in range(caption_idx + 1, min(len(paragraphs), caption_idx + 5)):
            text = paragraphs[j]["text"]
            if not text:
                continue
            if is_explanation(text, min_explanation_chars):
                explanation = text
                break
            if CAPTION_RE.search(text) or HEADING_RE.search(text):
                break
        caption_explanations.append((caption_idx, paragraphs[caption_idx]["text"], explanation))

    explained = [item for item in caption_explanations if item[2]]
    unexplained = [item for item in caption_explanations if not item[2]]
    return {
        "images": len(image_indices),
        "captions": len(caption_indices),
        "captioned_images": captioned_images,
        "explained_captions": len(explained),
        "missing_caption_images": missing_caption_images,
        "unexplained_captions": unexplained,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify DOCX figure captions and explanations.")
    parser.add_argument("docx", help="Path to .docx file")
    parser.add_argument("--min-figures", type=int, default=1, help="Minimum image count expected")
    parser.add_argument("--min-captions", type=int, default=None, help="Minimum figure caption count expected")
    parser.add_argument("--min-explained", type=int, default=None, help="Minimum captions with nearby explanations")
    parser.add_argument("--min-explanation-chars", type=int, default=35, help="Minimum characters for a nearby explanation paragraph")
    args = parser.parse_args()

    docx_path = Path(args.docx)
    if not docx_path.exists():
        print(f"ERROR: file not found: {docx_path}", file=sys.stderr)
        return 2

    result = audit(docx_path, args.min_explanation_chars)
    min_captions = args.min_captions if args.min_captions is not None else result["images"]
    min_explained = args.min_explained if args.min_explained is not None else min_captions

    print(f"docx: {docx_path}")
    print(f"images: {result['images']}")
    print(f"figure_captions: {result['captions']}")
    print(f"captioned_images: {result['captioned_images']}")
    print(f"explained_captions: {result['explained_captions']}")

    failed = False
    if result["images"] < args.min_figures:
        print(f"ERROR: expected at least {args.min_figures} image(s).", file=sys.stderr)
        failed = True
    if result["captions"] < min_captions:
        print(f"ERROR: expected at least {min_captions} figure caption(s).", file=sys.stderr)
        failed = True
    if result["captioned_images"] < result["images"]:
        print("ERROR: at least one image lacks a nearby figure caption.", file=sys.stderr)
        failed = True
    if result["explained_captions"] < min_explained:
        examples = "; ".join(item[1][:60] for item in result["unexplained_captions"][:3])
        print(f"ERROR: figure caption(s) lack nearby explanation: {examples}", file=sys.stderr)
        failed = True

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
