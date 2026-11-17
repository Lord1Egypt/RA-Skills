#!/usr/bin/env python3
"""Compare Jev harness reports only when their evaluation inputs match."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def read_report(path: Path) -> dict[str, Any]:
    try:
        report = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"report not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid report JSON in {path}: {exc}") from exc
    if not isinstance(report, dict) or not isinstance(report.get("summary"), dict):
        raise ValueError(f"{path} is not a Jev harness report")
    return report


def comparable_identity(report: dict[str, Any]) -> tuple[Any, Any, Any]:
    config = report.get("config", {})
    return config.get("question_sha256"), config.get("case_sha256") or config.get("case_id_sha256"), config.get("tag_filter", [])


def row(path: Path, report: dict[str, Any]) -> dict[str, Any]:
    config = report.get("config", {})
    summary = report["summary"]
    provider_caps = summary.get("provider_capabilities", config.get("provider_capabilities", {}))
    by_type = summary.get("by_type", {})
    return {
        "report": str(path),
        "provider": config.get("provider"),
        "model": config.get("model"),
        "protocol": provider_caps.get("protocol") if isinstance(provider_caps, dict) else None,
        "architecture": provider_caps.get("architecture") if isinstance(provider_caps, dict) else None,
        "probability_semantics": provider_caps.get("probability_semantics") if isinstance(provider_caps, dict) else None,
        "calibration_status": provider_caps.get("calibration_status") if isinstance(provider_caps, dict) else None,
        "status": report.get("status"),
        "exact_accuracy": summary.get("exact_accuracy"),
        "accuracy_ci95": summary.get("accuracy_ci95"),
        "noul_brier": by_type.get("noul", {}).get("brier"),
        "noul_ece": by_type.get("noul", {}).get("ece"),
        "choice_ece": by_type.get("choice", {}).get("ece"),
        "score_mae": by_type.get("score", {}).get("mae"),
        "review_rate": summary.get("review_rate"),
        "warning_rate": summary.get("warnings", {}).get("rate"),
        "latency_ms_p95": summary.get("latency_ms", {}).get("p95"),
        "input_tokens": summary.get("usage", {}).get("input_tokens"),
        "output_tokens": summary.get("usage", {}).get("output_tokens"),
    }


def markdown(rows: list[dict[str, Any]]) -> str:
    columns = [
        "provider", "model", "protocol", "architecture", "probability_semantics",
        "exact_accuracy", "noul_brier", "noul_ece", "choice_ece", "score_mae",
        "review_rate", "warning_rate", "latency_ms_p95",
    ]
    labels = {
        "probability_semantics": "probability semantics",
        "exact_accuracy": "accuracy",
        "noul_brier": "Noul Brier",
        "noul_ece": "Noul ECE",
        "choice_ece": "Choice ECE",
        "score_mae": "Score MAE",
        "review_rate": "review rate",
        "warning_rate": "warning rate",
        "latency_ms_p95": "p95 ms",
    }
    header = "| " + " | ".join(labels.get(column, column) for column in columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(str(row.get(column, "—")) if row.get(column) is not None else "—" for column in columns) + " |"
        for row in rows
    ]
    return "\n".join(["# Jev Harness Comparison", "", header, divider, *body, ""])


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare reports from the same Jev question/case manifest")
    parser.add_argument("reports", nargs="+", type=Path)
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON instead of Markdown")
    parser.add_argument("--allow-mismatch", action="store_true", help="Show reports even when input hashes differ")
    args = parser.parse_args()
    try:
        loaded = [(path, read_report(path)) for path in args.reports]
        identities = {comparable_identity(report) for _, report in loaded}
        if len(identities) != 1 and not args.allow_mismatch:
            raise ValueError("reports do not share the same question hash, case hash, or tag filter; refusing an unfair comparison")
        rows = [row(path, report) for path, report in loaded]
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps({"comparable": len(identities) == 1, "reports": rows}, indent=2, ensure_ascii=False))
    else:
        print(markdown(rows))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
