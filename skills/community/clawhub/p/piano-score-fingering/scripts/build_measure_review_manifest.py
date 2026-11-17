#!/usr/bin/env python3
"""Build or apply an independent per-measure visual review manifest.

The build command reports current plan counts for discrepancy triage, but it
deliberately leaves expected counts blank.  A reviewer must enter those values
from the cited raw crop before the apply command accepts the evidence.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

from plan_io import load_plan, save_plan


def _key(record: dict) -> tuple[int, int, str]:
    return (
        int(record.get("page", 0) or 0),
        int(record.get("measure_index", record.get("measure", 0)) or 0),
        str(record.get("hand", "")).upper(),
    )


def build_manifest(plan: dict, source_path: Path) -> dict:
    regions = plan.get("recognition", {}).get("measure_regions", [])
    if not regions:
        raise ValueError(
            "recognition.measure_regions is empty; define every page/measure/hand crop, including rest-only measures"
        )
    note_counts: dict[tuple[int, int, str], int] = defaultdict(int)
    rest_counts: dict[tuple[int, int, str], int] = defaultdict(int)
    for note in plan.get("notes", []):
        note_counts[_key(note)] += 1
    for rest in plan.get("rests", []):
        rest_counts[_key(rest)] += 1

    reviews: list[dict] = []
    seen: set[str] = set()
    for index, region in enumerate(regions):
        if not isinstance(region, dict):
            raise ValueError(f"measure_regions[{index}] must be an object")
        region_id = str(region.get("region_id", "")).strip()
        if not region_id or region_id in seen:
            raise ValueError(f"measure_regions[{index}] has duplicate/empty region_id")
        seen.add(region_id)
        key = _key(region)
        crop = str(region.get("evidence_crop", "")).strip()
        if not crop:
            raise ValueError(f"{region_id}: evidence_crop is required")
        reviews.append({
            "review_id": f"measure:{region_id}",
            "region_id": region_id,
            "page": key[0],
            "measure": key[1],
            "hand": key[2],
            "evidence_crop": crop,
            "observed_plan_noteheads": note_counts[key],
            "observed_plan_rests": rest_counts[key],
            "expected_noteheads": None,
            "expected_rests": None,
            "expected_attack_events": None,
            "expected_chord_sizes": None,
            "duration_verified": False,
            "source": "independent_visual_review",
            "verified": False,
            "status": "open",
        })
    return {
        "schema_version": "measure-review-v1",
        "plan": str(source_path),
        "instruction": (
            "Open each evidence_crop first. Enter noteheads, rests, left-to-right attack-event count and "
            "ordered chord sizes from the raw crop without copying observed_plan_*; verify note/rest durations, "
            "then set verified=true and status=resolved. The chord sizes must sum to expected_noteheads."
        ),
        "reviews": reviews,
    }


def completed_checks(manifest: dict, plan: dict) -> list[dict]:
    if manifest.get("schema_version") != "measure-review-v1":
        raise ValueError("unsupported review manifest schema")
    reviews = manifest.get("reviews")
    if not isinstance(reviews, list):
        raise ValueError("manifest.reviews must be a list")
    regions = {
        str(region.get("region_id", "")): region
        for region in plan.get("recognition", {}).get("measure_regions", [])
        if isinstance(region, dict)
    }
    if not regions:
        raise ValueError("plan has no recognition.measure_regions")
    checks: list[dict] = []
    seen: set[str] = set()
    for index, review in enumerate(reviews):
        if not isinstance(review, dict):
            raise ValueError(f"reviews[{index}] must be an object")
        region_id = str(review.get("region_id", "")).strip()
        if region_id not in regions or region_id in seen:
            raise ValueError(f"reviews[{index}] has unknown/duplicate region_id {region_id!r}")
        seen.add(region_id)
        if review.get("verified") is not True or str(review.get("status", "")).lower() != "resolved":
            raise ValueError(f"{region_id}: review is not resolved and verified")
        if review.get("duration_verified") is not True:
            raise ValueError(f"{region_id}: duration_verified must be true")
        source = str(review.get("source", ""))
        if source not in {"independent_visual_review", "source_semantic"}:
            raise ValueError(f"{region_id}: source must be independent_visual_review or source_semantic")
        crop = str(review.get("evidence_crop", "")).strip()
        if not crop or crop != str(regions[region_id].get("evidence_crop", "")).strip():
            raise ValueError(f"{region_id}: evidence_crop must match the declared measure region")
        try:
            expected_notes = int(review["expected_noteheads"])
            expected_rests = int(review["expected_rests"])
            expected_events = int(review["expected_attack_events"])
            expected_sizes = [int(value) for value in review["expected_chord_sizes"]]
        except (KeyError, TypeError, ValueError):
            raise ValueError(f"{region_id}: expected counts and event topology must be independently entered") from None
        if expected_notes < 0 or expected_rests < 0 or expected_events < 0 or any(size < 1 for size in expected_sizes):
            raise ValueError(f"{region_id}: expected counts/topology are invalid")
        if expected_events != len(expected_sizes) or sum(expected_sizes) != expected_notes:
            raise ValueError(f"{region_id}: event topology must reconcile with expected_noteheads")
        region = regions[region_id]
        checks.append({
            "region_id": region_id,
            "page": int(region["page"]),
            "measure": int(region["measure"]),
            "hand": str(region["hand"]).upper(),
            "expected_noteheads": expected_notes,
            "expected_rests": expected_rests,
            "expected_attack_events": expected_events,
            "expected_chord_sizes": expected_sizes,
            "duration_verified": True,
            "source": source,
            "evidence_crop": crop,
            "verified": True,
        })
    missing = set(regions) - seen
    if missing:
        raise ValueError(f"completed manifest is missing {len(missing)} region(s): {sorted(missing)}")
    return checks


def command_build(args: argparse.Namespace) -> int:
    plan = load_plan(args.plan)
    manifest = build_manifest(plan, args.plan)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(manifest['reviews'])} open measure review(s): {args.output}")
    return 0


def command_apply(args: argparse.Namespace) -> int:
    plan = load_plan(args.plan)
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    checks = completed_checks(manifest, plan)
    recognition = plan.setdefault("recognition", {})
    recognition["measure_symbol_checks"] = checks
    recognition.pop("fact_lock", None)
    recognition["status"] = "review"
    save_plan(args.output, plan)
    print(f"Applied {len(checks)} independent measure check(s): {args.output}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    build = commands.add_parser("build", help="create an open review manifest with blank expected counts")
    build.add_argument("plan", type=Path)
    build.add_argument("-o", "--output", type=Path, required=True)
    build.set_defaults(func=command_build)
    apply = commands.add_parser("apply", help="apply a fully completed independent review manifest")
    apply.add_argument("plan", type=Path)
    apply.add_argument("manifest", type=Path)
    apply.add_argument("-o", "--output", type=Path, required=True)
    apply.set_defaults(func=command_apply)
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
