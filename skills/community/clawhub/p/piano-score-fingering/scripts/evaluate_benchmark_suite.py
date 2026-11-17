#!/usr/bin/env python3
"""Aggregate a declared fingering/visual benchmark suite without cherry-picking.

The manifest is deliberately explicit.  A piece contributes only when it is
declared ``eligible`` and carries the required evidence; a missing artifact is
reported as missing, never silently omitted from the denominator.
"""

from __future__ import annotations

import argparse
import json
import hashlib
from pathlib import Path

from plan_io import load_plan
from validate_recognition import validate_recognition


AUDITS = ("placement", "source_anchor", "source_clearance", "rendered")


def file_digest(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_json(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path}: expected a JSON object")
    return payload


def resolve(base: Path, value: object) -> Path:
    if not isinstance(value, str) or not value:
        raise ValueError("missing artifact path")
    path = Path(value)
    return path if path.is_absolute() else base / path


def fingering_reports(entry: dict, base: Path) -> list[Path]:
    """Resolve one whole-piece report or several non-overlapping piece ranges."""
    singular = entry.get("fingering_comparison")
    plural = entry.get("fingering_comparisons")
    if singular is not None and plural is not None:
        raise ValueError("use either fingering_comparison or fingering_comparisons, not both")
    if plural is not None:
        if not isinstance(plural, list) or not plural:
            raise ValueError("fingering_comparisons must be a non-empty list")
        return [resolve(base, value) for value in plural]
    return [resolve(base, singular)]


def _scope_rows(rows: object) -> set[tuple[int, int, int, tuple[str, ...]]]:
    if not isinstance(rows, list) or not rows:
        raise ValueError("whole-piece measure_scope must be a non-empty list")
    normalized: set[tuple[int, int, int, tuple[str, ...]]] = set()
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError("whole-piece measure_scope entries must be objects")
        try:
            page = int(row["page"])
            start = int(row["measure_start"])
            end = int(row["measure_end"])
            hands = tuple(sorted({str(hand).upper() for hand in row["hands"]}))
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError("whole-piece measure_scope entry is incomplete") from exc
        if page < 1 or start < 1 or end < start or hands != ("LH", "RH"):
            raise ValueError("whole-piece measure_scope must declare a valid page/range and both hands")
        normalized.add((page, start, end, hands))
    return normalized


def _source_identity(entry: dict, base: Path) -> tuple[bool, str]:
    source = entry.get("source")
    if not isinstance(source, dict) or source.get("type") != "pdf":
        return False, "eligible visual entry needs a PDF source identity"
    try:
        path = resolve(base, source["path"])
        expected_hash = str(source["sha256"])
        expected_bytes = int(source["bytes"])
        page_count = int(source["page_count"])
    except (KeyError, TypeError, ValueError) as exc:
        return False, f"incomplete PDF source identity: {exc}"
    if page_count < 1:
        return False, "source.page_count must be positive"
    if not path.is_file():
        return False, f"source PDF is missing: {path}"
    if path.stat().st_size != expected_bytes or file_digest(path) != expected_hash:
        return False, "source PDF content differs from the declared benchmark source"
    return True, "ready"


def _audit_counts(name: str, audit: dict) -> tuple[int, int]:
    """Return a real numerator/denominator for one visual audit.

    ``placement_accuracy`` alone is insufficient because the old aggregator
    converted every threshold-passing piece to 100%.  Require the audit's
    underlying counts so a 92/100 result remains 92/100 in the suite.
    """
    fields = {
        "placement": ("unambiguous_labels", "labels"),
        "source_anchor": ("valid_anchors", "anchors"),
        "source_clearance": ("clear_labels", "labels"),
        "rendered": ("recovered_labels", "labels"),
    }
    numerator_key, denominator_key = fields[name]
    numerator = int(audit[numerator_key])
    denominator = int(audit[denominator_key])
    accuracy = float(audit["placement_accuracy"])
    if denominator < 1 or not 0 <= numerator <= denominator:
        raise ValueError(f"{name} audit has invalid counts")
    if abs(accuracy - numerator / denominator) > 1.0e-6:
        raise ValueError(f"{name} audit accuracy disagrees with its counts")
    return numerator, denominator


def visual_ready(entry: dict, base: Path) -> tuple[bool, str, int, int]:
    source_ready, source_reason = _source_identity(entry, base)
    if not source_ready:
        return False, source_reason, 0, 0
    try:
        declared_scope = _scope_rows(entry["whole_piece_measure_scope"])
        declared_pages = {int(page) for page in entry["whole_piece_pages"]}
    except (KeyError, TypeError, ValueError) as exc:
        return False, f"missing whole-piece coverage evidence: {exc}", 0, 0
    if not declared_pages or min(declared_pages) < 1:
        return False, "whole_piece_pages must contain valid page numbers", 0, 0
    if declared_pages != set(range(1, int(entry["source"]["page_count"]) + 1)):
        return False, "whole_piece_pages must cover every source PDF page", 0, 0
    try:
        plan_path = resolve(base, entry["visual_plan"])
        audit_paths = entry["visual_audits"]
    except (KeyError, TypeError, ValueError) as exc:
        return False, f"visual artifact declaration is incomplete: {exc}", 0, 0
    plan = load_plan(plan_path)
    if plan.get("source", {}).get("type") not in {"pdf", "image"}:
        return False, "plan is not a PDF/image result", 0, 0
    recognition_errors, _ = validate_recognition(plan, strict=True)
    if recognition_errors:
        return False, f"recognition gate failed: {recognition_errors[0]}", 0, 0
    try:
        actual_scope = _scope_rows(plan.get("recognition", {}).get("measure_scope", []))
    except ValueError as exc:
        return False, f"visual plan scope is invalid: {exc}", 0, 0
    if actual_scope != declared_scope:
        return False, "visual plan measure scope does not equal the declared whole-piece scope", 0, 0
    plan_pages = {int(page.get("page", 0)) for page in plan.get("pages", []) if isinstance(page, dict)}
    if plan_pages != declared_pages:
        return False, "visual plan rendered pages do not cover every declared source page", 0, 0
    checks = plan.get("recognition", {}).get("measure_symbol_checks", [])
    if not checks or any(not isinstance(row, dict) or row.get("source") != "independent_visual_review" for row in checks):
        return False, "measure counts are not all independently visually reviewed", 0, 0
    labels = sum(1 for note in plan.get("notes", []) if int(note.get("finger", 0)) in {1, 2, 3, 4, 5})
    if not labels:
        return False, "no assigned labels", 0, 0
    conservative_passed = labels
    for name in AUDITS:
        try:
            audit = read_json(resolve(base, audit_paths.get(name)))
            passed, denominator = _audit_counts(name, audit)
        except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
            return False, f"{name} audit unavailable: {exc}", 0, 0
        if denominator != labels:
            return False, f"{name} audit covers {denominator} labels, expected {labels}", 0, 0
        conservative_passed = min(conservative_passed, passed)
    return True, "ready", conservative_passed, labels


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("-o", "--output", type=Path, required=True)
    parser.add_argument("--fingering-minimum", type=float, default=0.80)
    parser.add_argument("--visual-minimum", type=float, default=0.90)
    args = parser.parse_args()
    if not 0 < args.fingering_minimum <= 1 or not 0 < args.visual_minimum <= 1:
        raise ValueError("minimums must be in (0, 1]")

    manifest = read_json(args.manifest)
    pieces = manifest.get("pieces")
    if not isinstance(pieces, list) or not pieces:
        raise ValueError("manifest.pieces must be a non-empty list")
    requirements = manifest.get("requirements", {})
    if not isinstance(requirements, dict):
        raise ValueError("manifest.requirements must be an object")

    def minimum(name: str, default: int) -> int:
        value = requirements.get(name, default)
        if not isinstance(value, int) or value < 1:
            raise ValueError(f"requirements.{name} must be a positive integer")
        # A manifest may demand broader evidence, but cannot make a tiny
        # smoke test appear to satisfy the published whole-suite claim.
        return max(default, value)

    min_fingering_pieces = minimum("min_fingering_pieces", 3)
    min_fingering_anchors = minimum("min_fingering_anchors", 100)
    min_visual_pieces = minimum("min_visual_pieces", 3)
    min_visual_labels = minimum("min_visual_labels", 100)
    holdout_required = any(str(key).startswith("min_holdout_") for key in requirements)
    min_holdout_fingering_pieces = int(requirements.get("min_holdout_fingering_pieces", 0))
    min_holdout_fingering_anchors = int(requirements.get("min_holdout_fingering_anchors", 0))
    min_holdout_visual_pieces = int(requirements.get("min_holdout_visual_pieces", 0))
    min_holdout_visual_labels = int(requirements.get("min_holdout_visual_labels", 0))
    if holdout_required and min(
        min_holdout_fingering_pieces, min_holdout_fingering_anchors,
        min_holdout_visual_pieces, min_holdout_visual_labels,
    ) < 1:
        raise ValueError("all min_holdout_* requirements must be positive when holdout evaluation is enabled")
    base = args.manifest.parent
    rows: list[dict] = []
    fingering_match = fingering_total = visual_match = visual_total = 0
    fingering_complete = visual_complete = True
    eligible_fingering = eligible_visual = 0
    role_totals = {
        role: {"fingering_pieces": 0, "fingering_matches": 0, "fingering_anchors": 0,
               "visual_pieces": 0, "visual_verified": 0, "visual_labels": 0}
        for role in ("development", "holdout", "unassigned")
    }
    for entry in pieces:
        if not isinstance(entry, dict):
            raise ValueError("each piece must be an object")
        identifier = str(entry.get("id", "unnamed"))
        grade = str(entry.get("grade_band", "unclassified"))
        role = str(entry.get("benchmark_role", "unassigned")).lower()
        if role not in role_totals:
            raise ValueError(f"{identifier}: benchmark_role must be development or holdout")
        row: dict[str, object] = {"id": identifier, "grade_band": grade, "benchmark_role": role,
                                  "fingering": "diagnostic", "visual": "diagnostic"}
        if entry.get("fingering_status") == "eligible":
            eligible_fingering += 1
            try:
                reports = [read_json(path) for path in fingering_reports(entry, base)]
                # `compare_reference_fingerings.py` names the numerator
                # `matches`; editorial PDF-anchor comparison names it
                # `finger_matches` because it also reports notehead matching.
                matches = sum(int(report["finger_matches"] if "finger_matches" in report else report["matches"]) for report in reports)
                anchors = sum(int(report["anchors"]) for report in reports)
                if anchors <= 0:
                    raise ValueError("no editor anchors")
                fingering_match += matches
                fingering_total += anchors
                role_totals[role]["fingering_pieces"] += 1
                role_totals[role]["fingering_matches"] += matches
                role_totals[role]["fingering_anchors"] += anchors
                row["fingering"] = f"{matches}/{anchors} ({matches / anchors:.1%})"
            except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
                row["fingering"] = f"missing ({exc})"
                fingering_complete = False
        if entry.get("visual_status") == "eligible":
            eligible_visual += 1
            try:
                ready, reason, good, total = visual_ready(
                    entry, base
                )
                if not ready:
                    raise ValueError(reason)
                visual_match += good
                visual_total += total
                role_totals[role]["visual_pieces"] += 1
                role_totals[role]["visual_verified"] += good
                role_totals[role]["visual_labels"] += total
                row["visual"] = f"{good}/{total} ({good / total:.1%})"
            except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
                row["visual"] = f"missing ({exc})"
                visual_complete = False
        rows.append(row)

    # An empty eligible set is not "complete evidence".  Treating it as such
    # made a fresh, diagnostic-only private manifest look healthier than it
    # was, even though the final pass flag remained false.
    fingering_complete = fingering_complete and eligible_fingering > 0
    visual_complete = visual_complete and eligible_visual > 0
    fingering_accuracy = fingering_match / fingering_total if fingering_total and fingering_complete else None
    visual_accuracy = visual_match / visual_total if visual_total and visual_complete else None
    holdout = role_totals["holdout"]
    holdout_fingering_accuracy = (
        holdout["fingering_matches"] / holdout["fingering_anchors"]
        if holdout["fingering_anchors"] else None
    )
    holdout_visual_accuracy = (
        holdout["visual_verified"] / holdout["visual_labels"]
        if holdout["visual_labels"] else None
    )
    holdout_passed = (
        not holdout_required
        or (
            holdout["fingering_pieces"] >= min_holdout_fingering_pieces
            and holdout["fingering_anchors"] >= min_holdout_fingering_anchors
            and holdout_fingering_accuracy is not None
            and holdout_fingering_accuracy >= args.fingering_minimum
            and holdout["visual_pieces"] >= min_holdout_visual_pieces
            and holdout["visual_labels"] >= min_holdout_visual_labels
            and holdout_visual_accuracy is not None
            and holdout_visual_accuracy >= args.visual_minimum
        )
    )
    result = {
        "metric_policy": "Only explicitly eligible entries with all required evidence contribute; diagnostics remain listed.",
        "status": (
            "ready_for_threshold_evaluation"
            if eligible_fingering and eligible_visual else
            "insufficient_evidence"
        ),
        "pieces": rows,
        "by_role": {
            role: values | {
                "fingering_accuracy": (
                    values["fingering_matches"] / values["fingering_anchors"]
                    if values["fingering_anchors"] else None
                ),
                "visual_accuracy": (
                    values["visual_verified"] / values["visual_labels"]
                    if values["visual_labels"] else None
                ),
            }
            for role, values in role_totals.items()
        },
        "holdout": {
            "required": holdout_required,
            "requirements": {
                "min_fingering_pieces": min_holdout_fingering_pieces,
                "min_fingering_anchors": min_holdout_fingering_anchors,
                "min_visual_pieces": min_holdout_visual_pieces,
                "min_visual_labels": min_holdout_visual_labels,
            },
            "passed": holdout_passed,
        },
        "fingering": {
            "eligible_pieces": eligible_fingering, "matches": fingering_match, "anchors": fingering_total,
            "evidence_complete": fingering_complete, "accuracy": fingering_accuracy,
            "requirements": {"min_pieces": min_fingering_pieces, "min_anchors": min_fingering_anchors},
            "passed": (
                fingering_accuracy is not None
                and eligible_fingering >= min_fingering_pieces
                and fingering_total >= min_fingering_anchors
                and fingering_accuracy >= args.fingering_minimum
            ),
        },
        "visual": {
            "eligible_pieces": eligible_visual, "labels": visual_total, "verified": visual_match,
            "evidence_complete": visual_complete, "accuracy": visual_accuracy,
            "requirements": {"min_pieces": min_visual_pieces, "min_labels": min_visual_labels},
            "passed": (
                visual_accuracy is not None
                and eligible_visual >= min_visual_pieces
                and visual_total >= min_visual_labels
                and visual_accuracy >= args.visual_minimum
            ),
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["fingering"]["passed"] and result["visual"]["passed"] and holdout_passed else 2


if __name__ == "__main__":
    raise SystemExit(main())
