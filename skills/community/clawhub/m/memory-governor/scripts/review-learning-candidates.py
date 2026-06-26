#!/usr/bin/env python3

from __future__ import annotations

import argparse
import importlib.util
import pathlib
import sys
from dataclasses import dataclass
from datetime import UTC, datetime


SCRIPT_DIR = pathlib.Path(__file__).resolve().parent
VALIDATOR_PATH = SCRIPT_DIR / "validate-memory-frontmatter.py"


@dataclass
class ReviewReport:
    path: pathlib.Path
    target_class: str
    candidate_status: str
    updated_at: str
    candidate_count: int
    structured_candidate_count: int
    unstructured_candidate_count: int
    incomplete_candidates: list[str]
    stage_counts: dict[str, int]
    age_days: int
    is_stale: bool


def load_validator():
    spec = importlib.util.spec_from_file_location("memory_validator", VALIDATOR_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load validator from {VALIDATOR_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


VALIDATOR = load_validator()


def parse_iso8601(value: str) -> datetime:
    normalized = value.replace("Z", "+00:00")
    parsed = datetime.fromisoformat(normalized)
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=UTC)
    return parsed.astimezone(UTC)


def extract_candidates_section(body: str) -> str:
    heading = "## Candidates"
    start = body.find(heading)
    if start == -1:
        return ""
    section = body[start + len(heading) :]
    next_heading = section.find("\n## ")
    if next_heading != -1:
        section = section[:next_heading]
    return section


def analyze_candidate_entries(body: str) -> tuple[int, int, list[str], dict[str, int]]:
    section = extract_candidates_section(body)
    required_fields = {
        "summary:",
        "why_it_matters:",
        "promotion_signals:",
        "lifecycle_stage:",
        "evidence_count:",
        "next_review:",
    }
    valid_stages = {
        "collecting_evidence",
        "ready_for_promotion",
        "promoted",
        "discarded",
    }

    structured_count = 0
    unstructured_count = 0
    incomplete: list[str] = []
    stage_counts = {stage: 0 for stage in sorted(valid_stages)}
    current_title: str | None = None
    current_fields: set[str] = set()
    current_values: dict[str, str] = {}

    def flush_current() -> None:
        nonlocal structured_count, current_title, current_fields, current_values
        if current_title is None:
            return
        missing = sorted(required_fields - current_fields)
        if missing:
            incomplete.append(f"{current_title} missing {', '.join(missing)}")
        else:
            current_errors: list[str] = []
            stage = current_values.get("lifecycle_stage:", "")
            if stage not in valid_stages:
                current_errors.append(
                    f"{current_title} has invalid lifecycle_stage {stage!r}; expected one of "
                    f"{', '.join(sorted(valid_stages))}"
                )
            else:
                stage_counts[stage] += 1

            evidence_count = current_values.get("evidence_count:", "")
            if not evidence_count.isdigit() or int(evidence_count) < 1:
                current_errors.append(
                    f"{current_title} has invalid evidence_count {evidence_count!r}; expected integer >= 1"
                )

            next_review = current_values.get("next_review:", "")
            if not next_review:
                current_errors.append(f"{current_title} is missing a concrete next_review value")

            if current_errors:
                incomplete.extend(current_errors)
            else:
                structured_count += 1
        current_title = None
        current_fields = set()
        current_values = {}

    for raw_line in section.splitlines():
        line = raw_line.strip()
        if line.startswith("### "):
            flush_current()
            current_title = line[4:].strip()
            continue
        if current_title is not None:
            lowered = line.lower()
            for field in required_fields:
                if lowered.startswith(f"- {field}") or lowered.startswith(f"* {field}"):
                    current_fields.add(field)
                    current_values[field] = line.split(":", 1)[1].strip() if ":" in line else ""
                    break
        elif line.startswith("- ") or line.startswith("* "):
            unstructured_count += 1

    flush_current()
    return structured_count, unstructured_count, incomplete, stage_counts


def review_file(path: pathlib.Path, stale_days: int, now: datetime) -> ReviewReport:
    errors = VALIDATOR.validate_file(path)
    if errors:
        raise ValueError("\n".join(errors))

    text = path.read_text(encoding="utf-8")
    frontmatter, body = VALIDATOR.extract_frontmatter(text)
    updated_at = str(frontmatter["updated_at"])
    updated = parse_iso8601(updated_at)
    age_days = max(0, (now - updated).days)
    structured_count, unstructured_count, incomplete_candidates, stage_counts = analyze_candidate_entries(body)

    return ReviewReport(
        path=path,
        target_class=str(frontmatter["target_class"]),
        candidate_status=str(frontmatter["candidate_status"]),
        updated_at=updated_at,
        candidate_count=structured_count + unstructured_count,
        structured_candidate_count=structured_count,
        unstructured_candidate_count=unstructured_count,
        incomplete_candidates=incomplete_candidates,
        stage_counts=stage_counts,
        age_days=age_days,
        is_stale=age_days > stale_days,
    )


def describe_status(report: ReviewReport) -> tuple[str, list[str]]:
    notes: list[str] = []
    level = "OK"

    if report.target_class != "learning_candidates":
        return "ERROR", ["file is not a learning_candidates target"]

    if report.candidate_count == 0:
        level = "WARN"
        notes.append("no candidate items found under ## Candidates")

    if report.unstructured_candidate_count > 0:
        level = "WARN" if level == "OK" else level
        notes.append("some candidate items are still unstructured; prefer ### Candidate blocks with review fields")

    if report.incomplete_candidates:
        level = "WARN" if level == "OK" else level
        for item in report.incomplete_candidates:
            notes.append(item)

    if report.stage_counts.get("ready_for_promotion", 0) > 0:
        notes.append("one or more candidates are marked ready_for_promotion; review whether they should move into reusable_lessons")

    if report.stage_counts.get("discarded", 0) > 0:
        notes.append("discarded candidates are still present; clear them when the file is next refreshed")

    if report.stage_counts.get("promoted", 0) > 0:
        notes.append("promoted candidates are still present; archive or replace them after migration")

    if report.is_stale:
        level = "WARN" if level == "OK" else level
        notes.append("review overdue")

    if report.candidate_status == "promoted":
        notes.append("ready to archive or replace with fresh candidates")
    elif report.candidate_status == "discarded":
        notes.append("review complete; clear stale discarded items when convenient")
    else:
        notes.append("keep, promote, or discard during the next review pass")

    return level, notes


def main() -> int:
    parser = argparse.ArgumentParser(description="Review learning_candidates files for freshness and workflow state.")
    parser.add_argument("paths", nargs="+", help="learning_candidates markdown files to review")
    parser.add_argument(
        "--stale-days",
        type=int,
        default=7,
        help="warn when updated_at is older than this many days (default: 7)",
    )
    parser.add_argument(
        "--now",
        help="override current UTC time for deterministic checks, e.g. 2026-04-06T00:00:00Z",
    )
    args = parser.parse_args()

    now = parse_iso8601(args.now) if args.now else datetime.now(UTC)
    overall_ok = True

    for raw_path in args.paths:
        path = pathlib.Path(raw_path)
        if not path.exists():
            print(f"ERROR: missing file {path}", file=sys.stderr)
            overall_ok = False
            continue

        try:
            report = review_file(path, args.stale_days, now)
        except Exception as exc:  # noqa: BLE001
            print(str(exc), file=sys.stderr)
            overall_ok = False
            continue

        level, notes = describe_status(report)
        if level == "ERROR":
            overall_ok = False

        print(f"FILE: {path}")
        print(f"STATUS: {level}")
        print(f"target_class: {report.target_class}")
        print(f"candidate_status: {report.candidate_status}")
        print(f"updated_at: {report.updated_at}")
        print(f"candidate_items: {report.candidate_count}")
        print(f"structured_candidates: {report.structured_candidate_count}")
        print(f"unstructured_candidates: {report.unstructured_candidate_count}")
        print(f"stage_collecting_evidence: {report.stage_counts['collecting_evidence']}")
        print(f"stage_ready_for_promotion: {report.stage_counts['ready_for_promotion']}")
        print(f"stage_promoted: {report.stage_counts['promoted']}")
        print(f"stage_discarded: {report.stage_counts['discarded']}")
        print(f"age_days: {report.age_days}")
        for note in notes:
            print(f"- {note}")

    return 0 if overall_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
