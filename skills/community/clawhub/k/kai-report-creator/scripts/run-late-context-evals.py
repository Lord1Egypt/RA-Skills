#!/usr/bin/env python3
"""Run late-context isolation evals on repo-contained cases."""

from __future__ import annotations

import argparse
import csv
import json
import sys
import time
from dataclasses import asdict, dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.context_isolation import (  # noqa: E402
    build_context_snapshot,
    build_ir_snapshot,
    build_naive_context_snapshot,
    compare_snapshots,
)


@dataclass(frozen=True)
class LateContextCaseResult:
    case_id: str
    ok: bool
    isolated_drift_fields: list[str]
    baseline_drift_fields: list[str]
    extraction_ms: float
    expected_snapshot: dict[str, object]
    isolated_snapshot: dict[str, object]
    baseline_snapshot: dict[str, object]


def load_manifest(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def resolve(root: Path, relative_path: str) -> Path:
    return (root / relative_path).resolve()


def read_required(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(path)
    return path.read_text(encoding="utf-8")


def evaluate_case(root: Path, case: dict[str, str]) -> LateContextCaseResult:
    ir_text = read_required(resolve(root, case["ir_path"]))
    context_path = case.get("context_path", "").strip()
    if not context_path:
        raise ValueError(f"Case {case['case_id']} missing context_path for late-context eval.")
    context_text = read_required(resolve(root, context_path))

    expected_snapshot = build_ir_snapshot(ir_text)

    started = time.perf_counter()
    isolated_snapshot = build_context_snapshot(context_text)
    extraction_ms = (time.perf_counter() - started) * 1000

    baseline_snapshot = build_naive_context_snapshot(context_text)

    isolated_drift_fields = compare_snapshots(expected_snapshot, isolated_snapshot)
    baseline_drift_fields = compare_snapshots(
        expected_snapshot,
        baseline_snapshot,
        keys=[
            "resolved_report_class",
            "resolved_theme",
            "resolved_archetype",
            "required_refs",
        ],
    )

    return LateContextCaseResult(
        case_id=case["case_id"],
        ok=not isolated_drift_fields,
        isolated_drift_fields=isolated_drift_fields,
        baseline_drift_fields=baseline_drift_fields,
        extraction_ms=round(extraction_ms, 3),
        expected_snapshot=expected_snapshot,
        isolated_snapshot=isolated_snapshot,
        baseline_snapshot=baseline_snapshot,
    )


def print_text(results: list[LateContextCaseResult]) -> int:
    failures = 0
    for case in results:
        status = "PASS" if case.ok else "FAIL"
        print(f"{status} {case.case_id}")
        print(f"  - isolated drift: {case.isolated_drift_fields or 'none'}")
        print(f"  - baseline drift: {case.baseline_drift_fields or 'none'}")
        print(f"  - extraction_ms: {case.extraction_ms}")
        if not case.ok:
            failures += 1
    print()
    print(f"Summary: {len(results) - failures} passed, {failures} failed.")
    return 0 if failures == 0 else 1


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Repository root.")
    parser.add_argument("--manifest", default="evals/report-cases.csv", help="Relative path to the case manifest.")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="Output format.")
    parser.add_argument("--json-out", help="Optional path to write the full JSON result.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()
    manifest = resolve(root, args.manifest)
    cases = load_manifest(manifest)
    results = [evaluate_case(root, case) for case in cases if case.get("context_path", "").strip()]

    baseline_drift_cases = sum(1 for result in results if result.baseline_drift_fields)
    isolated_drift_cases = sum(1 for result in results if result.isolated_drift_fields)
    payload = {
        "cases": [asdict(result) for result in results],
        "summary": {
            "total": len(results),
            "passed": sum(1 for result in results if result.ok),
            "failed": sum(1 for result in results if not result.ok),
            "baseline_cases_with_drift": baseline_drift_cases,
            "isolated_cases_with_drift": isolated_drift_cases,
            "baseline_total_drift_fields": sum(len(result.baseline_drift_fields) for result in results),
            "isolated_total_drift_fields": sum(len(result.isolated_drift_fields) for result in results),
            "drift_reduction": sum(len(result.baseline_drift_fields) for result in results)
            - sum(len(result.isolated_drift_fields) for result in results),
            "avg_extraction_ms": round(
                sum(result.extraction_ms for result in results) / len(results), 3
            )
            if results
            else 0.0,
        },
    }

    if args.json_out:
        target = Path(args.json_out).resolve()
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0 if payload["summary"]["failed"] == 0 else 1
    return print_text(results)


if __name__ == "__main__":
    sys.exit(main())
