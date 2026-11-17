#!/usr/bin/env python3
"""Create a multi-page visual-facts template from reviewed page-region proposals."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def load_regions(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("systems"), list):
        raise ValueError(f"{path}: expected proposed-regions.json with systems")
    try:
        page = int(data["page"])
        width = float(data["width"])
        height = float(data["height"])
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError(f"{path}: page, width and height are required") from exc
    if page < 1 or width <= 0 or height <= 0:
        raise ValueError(f"{path}: invalid page dimensions")
    return data


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("regions", nargs="+", type=Path, help="one proposed-regions.json per source page")
    parser.add_argument("-o", "--output", required=True, type=Path)
    parser.add_argument("--source", required=True, help="original PDF or image path")
    parser.add_argument("--source-type", choices=("pdf", "image"), required=True)
    parser.add_argument("--coordinate-unit", default="pixel_top_left", choices=("pixel_top_left", "pdf_point"))
    parser.add_argument("--render-dpi", type=float, default=144.0,
                        help="DPI used to create the page PNGs (default: 144)")
    args = parser.parse_args()
    if args.render_dpi < 36 or args.render_dpi > 600:
        parser.error("--render-dpi must be between 36 and 600")

    pages: list[dict] = []
    systems: list[dict] = []
    regions: list[dict] = []
    scopes: list[dict] = []
    seen_pages: set[int] = set()
    measure_pages: dict[int, int] = {}
    for region_path in args.regions:
        data = load_regions(region_path)
        page = int(data["page"])
        if page in seen_pages:
            raise ValueError(f"duplicate page proposal: {page}")
        seen_pages.add(page)
        pages.append({
            "page": page, "width": data["width"], "height": data["height"],
            "image": str(data.get("source_image", "")),
        })
        measures: list[int] = []
        for system_index, system in enumerate(data["systems"], 1):
            if not isinstance(system, dict):
                raise ValueError(f"{region_path}: systems[{system_index - 1}] must be an object")
            system_id = str(system.get("system_id", f"p{page}-system-{system_index}"))
            for hand, clef, staff, lines_key in (("RH", "treble", 1, "treble_staff_line_y"), ("LH", "bass", 2, "bass_staff_line_y")):
                lines = system.get(lines_key)
                if not isinstance(lines, list) or len(lines) != 5:
                    raise ValueError(f"{region_path}: {system_id} has no five-line {hand} geometry")
                systems.append({
                    "system_id": f"{system_id}-{hand.lower()}", "page": page, "staff": staff,
                    "clef": clef, "staff_line_y": lines,
                })
            for measure in system.get("measures", []):
                if not isinstance(measure, dict):
                    raise ValueError(f"{region_path}: invalid measure proposal")
                try:
                    measure_index = int(measure["measure_index"])
                except (KeyError, TypeError, ValueError) as exc:
                    raise ValueError(f"{region_path}: measure_index is required") from exc
                previous_page = measure_pages.get(measure_index)
                if previous_page is not None and previous_page != page:
                    raise ValueError(
                        f"measure {measure_index} appears on pages {previous_page} and {page}; "
                        "rerun extract_score_regions.py with the correct --first-measure for each later page"
                    )
                measure_pages[measure_index] = page
                measures.append(measure_index)
                for hand in ("RH", "LH"):
                    hand_region = measure.get(hand)
                    if not isinstance(hand_region, dict):
                        raise ValueError(f"{region_path}: measure {measure_index} lacks {hand} crop")
                    crop_name = str(hand_region.get("evidence_crop", ""))
                    if not crop_name:
                        raise ValueError(f"{region_path}: measure {measure_index} {hand} lacks evidence_crop")
                    regions.append({
                        "region_id": f"p{page}-m{measure_index:03d}-{hand.lower()}",
                        "page": page, "measure": measure_index, "hand": hand,
                        "bbox": hand_region.get("bbox"),
                        "evidence_crop": str(region_path.parent / crop_name),
                    })
        if measures:
            scopes.append({"page": page, "measure_start": min(measures), "measure_end": max(measures), "hands": ["RH", "LH"]})

    if not regions:
        raise ValueError("no usable measure regions found; review page crop proposals first")
    template = {
        "source": {
            "type": args.source_type, "path": args.source,
            "coordinate_unit": args.coordinate_unit, "render_dpi": args.render_dpi,
        },
        "pages": sorted(pages, key=lambda item: item["page"]),
        "recognition": {
            "scope": "visual score facts pending model review",
            "measure_scope": sorted(scopes, key=lambda item: item["page"]),
            "systems": systems,
            "measure_regions": sorted(regions, key=lambda item: (item["page"], item["measure"], item["hand"])),
            "measure_symbol_checks": [],
            "event_count_checks": [],
            "key_signatures": [],
        },
        "notes": [],
        "rests": [],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(template, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote visual-facts template for {len(pages)} page(s), {len(regions)} hand-measure region(s): {args.output}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
