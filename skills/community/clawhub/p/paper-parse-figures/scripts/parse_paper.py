#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "PyMuPDF>=1.23.0",
#     "pymupdf4llm>=0.0.10",
# ]
# ///
"""
Parse academic PDF papers into markdown with figure extraction.

Usage:
    uv run parse_paper.py --pdf /path/to/paper.pdf [--output-dir ./output]
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


def parse_paper(
    pdf_path: Path,
    output_dir: Path,
    figure_x_pad: float = 28.0,
    figure_y_pad: float = 16.0,
    figure_width_mode: str = "auto",
) -> dict[str, Any]:
    """Parse a PDF into markdown with figure screenshots and captions."""
    try:
        import fitz  # PyMuPDF
    except ImportError:
        raise RuntimeError("PyMuPDF is required. Install with: pip install PyMuPDF")

    try:
        import pymupdf4llm
    except ImportError:
        raise RuntimeError("pymupdf4llm is required. Install with: pip install pymupdf4llm")

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    if pdf_path.suffix.lower() != ".pdf":
        raise ValueError(f"Expected a PDF file, got: {pdf_path.name}")

    # Create output directories
    output_dir.mkdir(parents=True, exist_ok=True)
    fig_dir = output_dir / "figures"
    fig_dir.mkdir(exist_ok=True)

    # 1. Convert PDF to markdown
    markdown = pymupdf4llm.to_markdown(str(pdf_path), page_chunks=False)
    md_path = output_dir / f"{pdf_path.stem}_content.md"
    md_path.write_text(markdown, encoding="utf-8")

    # 2. Extract figures with captions
    doc = fitz.open(str(pdf_path))
    num_pages = len(doc)
    title = doc.metadata.get("title", "") or pdf_path.stem
    figures = extract_figures(
        doc,
        fig_dir,
        x_pad=figure_x_pad,
        y_pad=figure_y_pad,
        width_mode=figure_width_mode,
    )
    cover_snapshot_path = extract_cover_snapshot(doc, output_dir)
    doc.close()

    # 3. Save structured JSON
    parsed = {
        "paper_name": pdf_path.stem,
        "title": title,
        "num_pages": num_pages,
        "figures": figures,
        "cover_snapshot_path": str(cover_snapshot_path) if cover_snapshot_path else "",
    }
    json_path = output_dir / f"{pdf_path.stem}_parsed.json"
    json_path.write_text(
        json.dumps(parsed, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    return {
        "status": "ok",
        "paper_name": pdf_path.stem,
        "title": title,
        "parsed_json_path": str(json_path),
        "markdown_path": str(md_path),
        "figures_dir": str(fig_dir),
        "figures_count": len(figures),
        "cover_snapshot_path": str(cover_snapshot_path) if cover_snapshot_path else "",
        "figures": [
            {"num": f["figure_num"], "caption": f["caption"][:120], "path": f["path"]}
            for f in figures
        ],
        "num_pages": num_pages,
    }


def _extract_text(blk: dict[str, Any]) -> str:
    return "".join(
        span.get("text", "")
        for line in blk.get("lines", [])
        for span in line.get("spans", [])
    ).strip()


def _caption_match(text: str) -> re.Match[str] | None:
    """Match figure captions while reducing accidental inline hits."""
    caption_re = re.compile(
        r"^\s*(?:Figure|Fig(?:ure)?\.?|Extended\s+Data\s+Fig(?:ure)?\.?|"
        r"Supplementary\s+Fig(?:ure)?\.?)\s*([A-Za-z]?\d+[A-Za-z]?)\b[:.\-]?\s*",
        re.IGNORECASE,
    )
    return caption_re.search(text[:180])


def _column_bounds(pw: float, center_x: float) -> tuple[float, float]:
    mid = pw / 2.0
    return (0.0, mid) if center_x <= mid else (mid, pw)


def _best_image_for_caption(
    caption_rect: Any, image_rects: list[Any], pw: float, ph: float
) -> Any | None:
    best = None
    best_score = -1e9
    for rect in image_rects:
        if rect.width < pw * 0.06 or rect.height < ph * 0.025:
            continue
        overlap_x = max(0.0, min(caption_rect.x1, rect.x1) - max(caption_rect.x0, rect.x0))
        overlap_ratio = overlap_x / max(1.0, min(caption_rect.width, rect.width))

        # Prefer images above caption, but allow below-caption layouts with penalty.
        if rect.y1 <= caption_rect.y0 + 12:
            vertical_gap = caption_rect.y0 - rect.y1
            dir_bonus = 1.0
        elif rect.y0 >= caption_rect.y1 - 6:
            vertical_gap = rect.y0 - caption_rect.y1
            dir_bonus = 0.3
        else:
            vertical_gap = 0.0
            dir_bonus = 0.6

        same_column = False
        cap_col = _column_bounds(pw, (caption_rect.x0 + caption_rect.x1) / 2.0)
        img_center = (rect.x0 + rect.x1) / 2.0
        if cap_col[0] <= img_center <= cap_col[1]:
            same_column = True

        area_ratio = (rect.width * rect.height) / max(1.0, pw * ph)

        score = (
            2.6 * overlap_ratio
            + 0.7 * dir_bonus
            + (0.25 if same_column else 0.0)
            + 1.8 * area_ratio
            - (vertical_gap / max(1.0, ph))
        )
        if score > best_score:
            best_score = score
            best = rect
    return best


def _union_rect(rects: list[Any]) -> Any | None:
    if not rects:
        return None
    import fitz

    x0 = min(r.x0 for r in rects)
    y0 = min(r.y0 for r in rects)
    x1 = max(r.x1 for r in rects)
    y1 = max(r.y1 for r in rects)
    return fitz.Rect(x0, y0, x1, y1)


def _vertical_overlap_ratio(a: Any, b: Any) -> float:
    overlap = max(0.0, min(a.y1, b.y1) - max(a.y0, b.y0))
    denom = max(1.0, min(a.height, b.height))
    return overlap / denom


def _expand_to_dual_column_cluster(
    base_rect: Any, image_rects: list[Any], pw: float, ph: float, caption_rect: Any
) -> Any:
    """If a figure spans two columns, merge sibling image blocks from the other column."""
    peers: list[Any] = [base_rect]
    mid = pw / 2.0
    base_center = (base_rect.x0 + base_rect.x1) / 2.0
    base_left_col = base_center <= mid

    for rect in image_rects:
        if rect == base_rect:
            continue
        center = (rect.x0 + rect.x1) / 2.0
        rect_left_col = center <= mid
        # Only look for the opposite-column sibling with similar vertical band.
        if rect_left_col == base_left_col:
            continue
        if rect.y1 > caption_rect.y1 + 20:
            continue
        close_band = (
            abs(rect.y0 - base_rect.y0) <= ph * 0.11
            or abs(rect.y1 - base_rect.y1) <= ph * 0.11
        )
        if _vertical_overlap_ratio(rect, base_rect) < 0.2 and not close_band:
            continue
        # Avoid pulling tiny icons or unrelated tiny blocks.
        if rect.width < pw * 0.08 or rect.height < ph * 0.03:
            continue
        peers.append(rect)

    merged = _union_rect(peers)
    return merged if merged is not None else base_rect


def _cross_column_union_hint(
    caption_rect: Any, candidate_rects: list[Any], pw: float, ph: float
) -> Any | None:
    """If both columns contain substantial graphics above caption, union them."""
    significant = [
        r for r in candidate_rects
        if r.width >= pw * 0.12 and r.height >= ph * 0.05 and r.y1 <= caption_rect.y1 + 20
    ]
    if not significant:
        return None

    mid = pw / 2.0
    left = [r for r in significant if (r.x0 + r.x1) / 2.0 <= mid]
    right = [r for r in significant if (r.x0 + r.x1) / 2.0 > mid]
    if not left or not right:
        return None

    # Keep near-caption band to avoid absorbing unrelated headers/footers.
    band_top = max(0.0, caption_rect.y0 - ph * 0.62)
    band = [r for r in significant if r.y1 >= band_top]
    if len(band) < 2:
        # Dense-vector fallback: many small drawing blocks distributed in both columns.
        dense = [r for r in candidate_rects if r.width > 1 and r.height > 1]
        left_dense = [r for r in dense if (r.x0 + r.x1) / 2.0 <= mid and r.y1 <= caption_rect.y0 + 8]
        right_dense = [r for r in dense if (r.x0 + r.x1) / 2.0 > mid and r.y1 <= caption_rect.y0 + 8]
        if len(left_dense) < 18 or len(right_dense) < 18:
            return None
        # Use quantiles to avoid outliers pulling the crop too far.
        ys0 = sorted(r.y0 for r in (left_dense + right_dense))
        ys1 = sorted(r.y1 for r in (left_dense + right_dense))
        q10 = ys0[max(0, int(len(ys0) * 0.10) - 1)]
        q95 = ys1[min(len(ys1) - 1, int(len(ys1) * 0.95))]
        import fitz

        return fitz.Rect(0.0, max(0.0, q10 - 8), pw, min(ph, q95 + 8))
    return _union_rect(band)


def _auto_fullwidth_top(
    caption_rect: Any, candidate_rects: list[Any], pw: float, ph: float
) -> float | None:
    """Recover top boundary for wide multi-panel figures without manual parameters."""
    band_top = max(0.0, caption_rect.y0 - ph * 0.78)
    upper = [
        r
        for r in candidate_rects
        if r.y1 <= caption_rect.y0 + 10
        and r.y0 >= band_top
        and r.width > pw * 0.05
        and r.height > ph * 0.01
    ]
    if not upper:
        return None

    # Filter page separators/noise: very thin full-width lines are not figure content.
    filtered = [
        r for r in upper
        if not (r.width >= pw * 0.62 and r.height <= ph * 0.008)
    ]
    if not filtered:
        return None

    mid = pw / 2.0
    left = [r for r in filtered if (r.x0 + r.x1) / 2.0 <= mid]
    right = [r for r in filtered if (r.x0 + r.x1) / 2.0 > mid]
    if len(left) < 3 or len(right) < 3:
        return None

    # Use very low-percentile per-column tops to capture earliest panel rows.
    left_tops = sorted(r.y0 for r in left)
    right_tops = sorted(r.y0 for r in right)
    q = 0.005 if (len(left_tops) + len(right_tops)) >= 260 else 0.01
    li = max(0, int(len(left_tops) * q) - 1)
    ri = max(0, int(len(right_tops) * q) - 1)
    baseline = min(left_tops[li], right_tops[ri])
    return max(0.0, baseline - ph * 0.006)


def _map_rect_between_pages(rect: Any, src_w: float, src_h: float, dst_w: float, dst_h: float) -> Any:
    import fitz

    sx = 1.0 if src_w <= 0 else dst_w / src_w
    sy = 1.0 if src_h <= 0 else dst_h / src_h
    return fitz.Rect(rect.x0 * sx, rect.y0 * sy, rect.x1 * sx, rect.y1 * sy)


def _best_prev_page_image_for_top_caption(
    caption_rect: Any,
    caption_pw: float,
    prev_image_rects: list[Any],
    prev_pw: float,
    prev_ph: float,
) -> Any | None:
    """When caption starts a new page, try matching figure blocks near bottom of previous page."""
    if not prev_image_rects:
        return None

    cap_mapped = _map_rect_between_pages(caption_rect, caption_pw, 1.0, prev_pw, 1.0)
    cap_center = (cap_mapped.x0 + cap_mapped.x1) / 2.0
    cap_col = _column_bounds(prev_pw, cap_center)

    best = None
    best_score = -1e9
    for rect in prev_image_rects:
        if rect.width < prev_pw * 0.06 or rect.height < prev_ph * 0.025:
            continue
        # Cross-page figures are typically at lower half of previous page.
        if rect.y1 < prev_ph * 0.45:
            continue

        overlap_x = max(0.0, min(cap_mapped.x1, rect.x1) - max(cap_mapped.x0, rect.x0))
        overlap_ratio = overlap_x / max(1.0, min(cap_mapped.width, rect.width))
        same_column = cap_col[0] <= (rect.x0 + rect.x1) / 2.0 <= cap_col[1]
        area_ratio = (rect.width * rect.height) / max(1.0, prev_pw * prev_ph)
        bottom_ratio = rect.y1 / max(1.0, prev_ph)

        score = (
            2.4 * overlap_ratio
            + (0.30 if same_column else 0.0)
            + 1.8 * area_ratio
            + 0.9 * bottom_ratio
        )
        if score > best_score:
            best_score = score
            best = rect
    return best


def extract_figures(
    doc: Any,
    img_dir: Path,
    scale: int = 3,
    x_pad: float = 28.0,
    y_pad: float = 16.0,
    width_mode: str = "auto",
) -> list[dict]:
    """Locate figure captions, match nearby image blocks, and crop with wider margins."""
    import fitz  # Import here for use in this function

    figures: list[dict] = []
    seq_id = 0

    page_graphics: list[dict[str, Any]] = []
    for page_num in range(len(doc)):
        page = doc[page_num]
        pw, ph = page.rect.width, page.rect.height
        blocks = page.get_text("dict")["blocks"]
        image_rects = [fitz.Rect(*blk["bbox"]) for blk in blocks if blk.get("type") == 1]
        drawing_rects = []
        for d in page.get_drawings():
            rect = d.get("rect")
            if rect is None:
                continue
            # Keep small vector pieces for dense-figure clustering logic.
            if rect.width <= 1 or rect.height <= 1:
                continue
            drawing_rects.append(rect)
        graphic_rects = image_rects + drawing_rects
        page_graphics.append(
            {
                "pw": pw,
                "ph": ph,
                "blocks": blocks,
                "graphic_rects": graphic_rects,
            }
        )

    for page_num in range(len(doc)):
        page = doc[page_num]
        pw = page_graphics[page_num]["pw"]
        ph = page_graphics[page_num]["ph"]
        blocks = page_graphics[page_num]["blocks"]
        graphic_rects = page_graphics[page_num]["graphic_rects"]
        caption_candidates: list[dict[str, Any]] = []

        for blk in blocks:
            if blk.get("type") != 0:  # Skip non-text blocks
                continue
            text = _extract_text(blk)
            m = _caption_match(text)
            if not m:
                continue
            cap_rect = fitz.Rect(*blk["bbox"])
            caption_candidates.append(
                {
                    "rect": cap_rect,
                    "text": text[m.start():].strip(),
                    "label": m.group(1),
                }
            )

        caption_candidates.sort(key=lambda c: (c["rect"].y0, c["rect"].x0))
        for cap in caption_candidates:
            seq_id += 1
            cap_rect = cap["rect"]
            source_page_num = page_num
            source_page = page
            source_pw, source_ph = pw, ph
            source_cap_rect = cap_rect
            source_graphics = graphic_rects

            nearby_graphics = [
                r for r in graphic_rects
                if r.y1 <= cap_rect.y1 + 20 and r.y0 >= cap_rect.y0 - ph * 0.72
            ]
            matched_img = _best_image_for_caption(cap_rect, nearby_graphics, pw, ph)
            if (
                matched_img is None
                and page_num > 0
                and cap_rect.y0 <= ph * 0.30
            ):
                prev_ctx = page_graphics[page_num - 1]
                prev_pw = prev_ctx["pw"]
                prev_ph = prev_ctx["ph"]
                prev_graphics = prev_ctx["graphic_rects"]
                prev_match = _best_prev_page_image_for_top_caption(
                    cap_rect, pw, prev_graphics, prev_pw, prev_ph
                )
                if prev_match is not None:
                    source_page_num = page_num - 1
                    source_page = doc[source_page_num]
                    source_pw, source_ph = prev_pw, prev_ph
                    source_graphics = prev_graphics
                    source_cap_rect = _map_rect_between_pages(
                        cap_rect, pw, ph, source_pw, source_ph
                    )
                    # Emulate a "caption below figure" relationship on previous page.
                    source_cap_rect.y0 = max(source_cap_rect.y0, source_ph - 6)
                    source_cap_rect.y1 = source_ph
                    nearby_graphics = [
                        r
                        for r in source_graphics
                        if r.y1 <= source_cap_rect.y1 + 20
                        and r.y0 >= source_cap_rect.y0 - source_ph * 0.72
                    ]
                    matched_img = prev_match

            base_rect = matched_img if matched_img is not None else cap_rect
            if matched_img is not None:
                base_rect = _expand_to_dual_column_cluster(
                    base_rect, nearby_graphics, source_pw, source_ph, source_cap_rect
                )
            cross_hint = _cross_column_union_hint(source_cap_rect, nearby_graphics, source_pw, source_ph)
            if cross_hint is not None:
                base_rect = _union_rect([base_rect, cross_hint]) or base_rect

            # Wider horizontal crop to avoid truncating multi-column figures.
            cx = (source_cap_rect.x0 + source_cap_rect.x1) / 2.0
            is_wide_caption = source_cap_rect.width >= source_pw * 0.56
            cap_left_col = cx <= source_pw / 2.0
            opposite_dense = [
                r
                for r in nearby_graphics
                if (((r.x0 + r.x1) / 2.0 <= source_pw / 2.0) != cap_left_col)
                and r.y1 <= source_cap_rect.y0 + 10
                and r.width > 2
                and r.height > 2
            ]
            force_full_width = len(opposite_dense) >= 24
            if width_mode == "page":
                left, right = 0.0, source_pw
            elif width_mode == "column":
                left, right = _column_bounds(source_pw, cx)
            else:  # auto
                if (
                    is_wide_caption
                    or force_full_width
                    or (cross_hint is not None and cross_hint.width >= source_pw * 0.75)
                    or (matched_img is not None and base_rect.width >= source_pw * 0.62)
                ):
                    left, right = 0.0, source_pw
                else:
                    left, right = _column_bounds(source_pw, cx)

            top = min(base_rect.y0, source_cap_rect.y0)
            bottom = max(base_rect.y1, source_cap_rect.y1)

            # In full-width multi-panel figures, recover earlier top subpanels (e.g., panel "a").
            if left == 0.0 and right == source_pw:
                upper_graphics = [
                    r
                    for r in nearby_graphics
                    if r.y1 <= source_cap_rect.y0 + 8
                    and r.y0 >= source_cap_rect.y0 - source_ph * 0.60
                    and r.width > 2
                    and r.height > 2
                ]
                if len(upper_graphics) >= 20:
                    ys = sorted(r.y0 for r in upper_graphics)
                    q01_idx = max(0, int(len(ys) * 0.01) - 1)
                    recovered_top = ys[q01_idx]
                    top = min(top, recovered_top - y_pad * 1.8)
                auto_top = _auto_fullwidth_top(source_cap_rect, nearby_graphics, source_pw, source_ph)
                if auto_top is not None:
                    top = min(top, auto_top - y_pad * 2.4)

            crop = fitz.Rect(
                max(0.0, left - x_pad),
                max(0.0, top - y_pad),
                min(source_pw, right + x_pad),
                min(source_ph, bottom + y_pad),
            )

            if crop.height < 30:
                continue
            mat = fitz.Matrix(scale, scale)
            pix = source_page.get_pixmap(matrix=mat, clip=crop)
            fname = f"figure_seq_{seq_id:03d}.png"
            pix.save(str(img_dir / fname))
            label_raw = cap["label"]
            label_numeric = int(label_raw) if label_raw.isdigit() else None
            figures.append({
                "figure_num": seq_id,
                "figure_seq_id": seq_id,
                "figure_label_id": label_numeric if label_numeric is not None else label_raw,
                "page": source_page_num + 1,
                "caption_page": page_num + 1,
                "image_page": source_page_num + 1,
                "caption": cap["text"],
                "path": str(img_dir / fname),
                "width": pix.width,
                "height": pix.height,
                "bbox": {
                    "x0": round(crop.x0, 2),
                    "y0": round(crop.y0, 2),
                    "x1": round(crop.x1, 2),
                    "y1": round(crop.y1, 2),
                },
            })

    figures.sort(key=lambda f: f["figure_seq_id"])
    return figures


def extract_cover_snapshot(doc: Any, output_dir: Path, scale: int = 2) -> Path | None:
    """Extract a first-page title+authors snapshot and save as PNG."""
    import fitz

    if len(doc) == 0:
        return None

    page = doc[0]
    pw, ph = page.rect.width, page.rect.height
    blocks = page.get_text("dict")["blocks"]

    text_blocks: list[dict[str, Any]] = []
    for blk in blocks:
        if blk.get("type") != 0:
            continue
        text = "".join(
            span.get("text", "")
            for line in blk.get("lines", [])
            for span in line.get("spans", [])
        ).strip()
        if not text:
            continue
        spans = [
            span
            for line in blk.get("lines", [])
            for span in line.get("spans", [])
            if span.get("text", "").strip()
        ]
        sizes = [float(span.get("size", 0.0)) for span in spans if span.get("size")]
        avg_size = (sum(sizes) / len(sizes)) if sizes else 0.0
        x0, y0, x1, y1 = blk.get("bbox", (0.0, 0.0, pw, 0.0))
        text_blocks.append(
            {
                "text": text,
                "bbox": fitz.Rect(x0, y0, x1, y1),
                "avg_size": avg_size,
            }
        )

    if not text_blocks:
        return None

    # Title candidates are usually large-font text near the top of the first page.
    top_blocks = [b for b in text_blocks if b["bbox"].y0 <= ph * 0.45]
    title_candidates = [
        b for b in top_blocks if b["avg_size"] >= 0.95 * max(tb["avg_size"] for tb in top_blocks)
    ] or top_blocks
    title_block = max(title_candidates, key=lambda b: (b["avg_size"], len(b["text"])))

    abstract_y = None
    for b in text_blocks:
        if b["bbox"].y0 > title_block["bbox"].y1 and re.search(r"\babstract\b", b["text"], re.IGNORECASE):
            abstract_y = b["bbox"].y0
            break

    margin = 8
    top = max(0.0, title_block["bbox"].y0 - margin)
    if abstract_y is not None:
        bottom = min(ph, abstract_y - margin)
    else:
        # Fallback: capture title + likely author rows in upper region.
        bottom = min(ph * 0.55, title_block["bbox"].y1 + ph * 0.22)

    if bottom <= top + 24:
        return None

    clip = fitz.Rect(0.0, top, pw, bottom)
    pix = page.get_pixmap(matrix=fitz.Matrix(scale, scale), clip=clip)
    out_path = output_dir / "cover_title_authors.png"
    pix.save(str(out_path))
    return out_path


def main():
    parser = argparse.ArgumentParser(
        description="Parse academic PDF papers into markdown with figure extraction"
    )
    parser.add_argument(
        "--pdf", "-p",
        required=True,
        type=Path,
        help="Path to the PDF file to parse"
    )
    parser.add_argument(
        "--output-dir", "-o",
        type=Path,
        default=Path("./parsed_paper"),
        help="Output directory (default: ./parsed_paper)"
    )
    parser.add_argument(
        "--figure-x-pad",
        type=float,
        default=28.0,
        help="Horizontal padding for figure crop (default: 28)"
    )
    parser.add_argument(
        "--figure-y-pad",
        type=float,
        default=16.0,
        help="Vertical padding for figure crop (default: 16)"
    )
    parser.add_argument(
        "--figure-width-mode",
        choices=["auto", "column", "page"],
        default="auto",
        help="Crop width strategy: auto/column/page (default: auto)"
    )

    args = parser.parse_args()

    try:
        result = parse_paper(
            args.pdf,
            args.output_dir,
            figure_x_pad=args.figure_x_pad,
            figure_y_pad=args.figure_y_pad,
            figure_width_mode=args.figure_width_mode,
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error parsing paper: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
