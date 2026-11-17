#!/usr/bin/env python3
"""Create a non-authoritative MusicXML/OMR checklist for visual score review.

The output is deliberately a ledger, not a fingering plan.  It lets a model
compare each original page crop with a structured candidate's note/rest counts
and event timing, while making it impossible to promote OMR output directly
to ``verified`` visual facts.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
from collections import defaultdict
from pathlib import Path

from source_provenance import structured_asset_record


RISK_PAGE = re.compile(r"\[(?:[^\]]*#|[^\]]*?(?:page|sheet)[-_ ]?)(?P<page>\d+)\]", re.IGNORECASE)
RISK_MEASURE = re.compile(r"(?:Measure\{#|MeasureStack#)(?P<measure>\d+)\}?", re.IGNORECASE)
PAGE_PATH = re.compile(r"(?:^|[-_])(?:page|sheet|p)[-_ ]?0*(?P<page>\d+)(?:\D|$)", re.IGNORECASE)
PAGE_TEXT = re.compile(r"\b(?:page|sheet)\s*#?\s*(?P<page>\d+)\b", re.IGNORECASE)
MEASURE_TEXT = re.compile(r"\bmeasure\s*#?\s*(?P<measure>\d+)\b", re.IGNORECASE)
HAND_TEXT = re.compile(r"\b(?P<hand>RH|LH)\b", re.IGNORECASE)


def page_from_text(value: str) -> int | None:
    match = PAGE_PATH.search(value)
    return int(match.group("page")) if match else None


def scope_regions(template: dict) -> dict[tuple[int, int, str], str]:
    result: dict[tuple[int, int, str], str] = {}
    for region in template.get("recognition", {}).get("measure_regions", []):
        if not isinstance(region, dict):
            continue
        try:
            key = (int(region["page"]), int(region["measure"]), str(region["hand"]).upper())
        except (KeyError, TypeError, ValueError):
            continue
        region_id = str(region.get("region_id", "")).strip()
        if not region_id or key in result:
            raise ValueError("visual template must have one unique region_id for each page/measure/hand")
        result[key] = region_id
    if not result:
        raise ValueError("visual template has no measure_regions")
    return result


def run_extractor(candidate: Path, script_dir: Path) -> dict:
    with tempfile.TemporaryDirectory(prefix="piano-semantic-ledger-") as temporary:
        plan_path = Path(temporary) / "candidate-plan.json"
        completed = subprocess.run(
            [sys.executable, str(script_dir / "create_plan_from_musicxml.py"), str(candidate), "-o", str(plan_path)],
            text=True,
            capture_output=True,
        )
        if completed.returncode:
            detail = (completed.stderr or completed.stdout).strip()
            raise ValueError(f"candidate MusicXML could not be parsed: {detail}")
        return json.loads(plan_path.read_text(encoding="utf-8"))


def load_omr_risks(report_path: Path | None) -> list[dict]:
    """Read non-authoritative engine warnings and attach them to visual review."""
    if report_path is None:
        return []
    if not report_path.is_file():
        raise ValueError("--omr-report must be an existing local JSON report")
    report = json.loads(report_path.read_text(encoding="utf-8"))
    raw_signals = report.get("semantic_risk_signals", [])
    if not isinstance(raw_signals, list):
        raise ValueError("omr report semantic_risk_signals must be a list")
    risks: list[dict] = []
    default_page = page_from_text(str(report.get("input", "")))
    for signal in raw_signals:
        if not isinstance(signal, dict):
            continue
        code = str(signal.get("code", "unknown_omr_risk"))
        examples = [str(line) for line in signal.get("examples", []) if isinstance(line, str)]
        scopes: list[dict] = []
        for line in examples:
            page_match = RISK_PAGE.search(line)
            text_page = PAGE_TEXT.search(line)
            page = (
                int(page_match.group("page")) if page_match else
                int(text_page.group("page")) if text_page else
                (page_from_text(line) or default_page)
            )
            if page is None:
                continue
            scope = {"page": page}
            measure_match = RISK_MEASURE.search(line) or MEASURE_TEXT.search(line)
            if measure_match:
                scope["measure"] = int(measure_match.group("measure"))
            hand_match = HAND_TEXT.search(line)
            if hand_match:
                scope["hand"] = hand_match.group("hand").upper()
            if scope not in scopes:
                scopes.append(scope)
        risks.append({
            "code": code,
            "count": int(signal.get("count", len(examples)) or 0),
            "scopes": scopes,
            "examples": examples,
            "resolution": "Compare this original region before accepting candidate counts or events.",
        })
    return risks


def risks_for_region(risks: list[dict], page: int, measure: int, hand: str) -> list[dict]:
    selected: list[dict] = []
    for risk in risks:
        scopes = risk.get("scopes", [])
        for scope in scopes:
            # An engine warning without a measure is a page-level handoff,
            # not evidence that every measure is bad.  Repeating it on every
            # region used to turn a single octave-shift warning into forty
            # needless high-priority reviews.
            if (
                scope.get("page") == page and scope.get("measure") == measure
                and ("hand" not in scope or scope["hand"] == hand)
            ):
                selected.append(risk)
                break
    return selected


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("candidate", type=Path, help="locally produced MusicXML/MXL candidate, e.g. from an offline OMR")
    parser.add_argument("visual_template", type=Path, help="visual-facts template created from the original page images")
    parser.add_argument("--omr-report", type=Path, help="optional report from run_optional_omr.py; warnings become mandatory review context")
    parser.add_argument("-o", "--output", type=Path, required=True)
    args = parser.parse_args()
    if not args.candidate.is_file() or not args.visual_template.is_file():
        raise ValueError("candidate and visual_template must both be local files")
    template = json.loads(args.visual_template.read_text(encoding="utf-8"))
    if not isinstance(template, dict):
        raise ValueError("visual template must be a JSON object")
    regions = scope_regions(template)
    candidate = run_extractor(args.candidate, Path(__file__).resolve().parent)
    omr_risks = load_omr_risks(args.omr_report)
    notes: dict[tuple[int, str], list[dict]] = defaultdict(list)
    rests: dict[tuple[int, str], list[dict]] = defaultdict(list)
    for note in candidate.get("notes", []):
        notes[(int(note["measure_index"]), str(note["hand"]).upper())].append(note)
    for rest in candidate.get("rests", []):
        rests[(int(rest["measure_index"]), str(rest["hand"]).upper())].append(rest)

    entries: list[dict] = []
    for (page, measure, hand), region_id in sorted(regions.items()):
        candidate_notes = sorted(notes[(measure, hand)], key=lambda row: (float(row["onset"]), int(row["chord_row"])))
        candidate_rests = sorted(rests[(measure, hand)], key=lambda row: float(row["onset"]))
        entry = {
            "region_id": region_id,
            "page": page,
            "measure": measure,
            "hand": hand,
            "candidate_noteheads": len(candidate_notes),
            "candidate_rests": len(candidate_rests),
            "candidate_events": [
                {
                    "onset": note["onset"], "duration": note["duration"],
                    "pitch": f"{note['pitch_step']}{int(note.get('pitch_alter', 0) or 0):+d}/{note['pitch_octave']}",
                    "chord_size": note["chord_size"],
                }
                for note in candidate_notes
            ],
            "visual_review": "required",
            "accepted": False,
        }
        local_risks = risks_for_region(omr_risks, page, measure, hand)
        if local_risks:
            entry["omr_risk_signals"] = local_risks
            entry["review_priority"] = "high"
        entries.append(entry)
    ledger = {
        "schema_version": "1.0",
        "purpose": "candidate semantic checklist; never a substitute for raw-page visual verification",
        "candidate_source": structured_asset_record(args.candidate),
        "acceptance_rule": "Copy counts only after comparing the cited original crop. Differences and omr_risk_signals must enter review_queue; this file cannot set recognition gates.",
        "omr_risk_signals": omr_risks,
        "unscoped_omr_risk_signals": [
            risk for risk in omr_risks
            if not any("measure" in scope for scope in risk.get("scopes", []))
        ],
        "entries": entries,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote semantic review ledger for {len(entries)} visual measure region(s): {args.output}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
