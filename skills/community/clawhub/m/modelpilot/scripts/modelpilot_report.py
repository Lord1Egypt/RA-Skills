#!/usr/bin/env python3
"""Create a Markdown report from ModelPilot benchmark JSON."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any


def decision_for_model(records: list[dict[str, Any]], rounds_required: int = 2) -> tuple[str, str]:
    rounds = {record.get("round") for record in records}
    if len(rounds) < rounds_required:
        return "candidate_only", "Only one benchmark round is complete."

    failures = [record for record in records if not record.get("success")]
    format_failures = [record for record in records if not record.get("format_pass")]
    think_leaks = [record for record in records if record.get("think_leak")]

    if failures:
        return "not_recommended", f"{len(failures)} prompt runs failed."
    if think_leaks:
        return "not_recommended", f"{len(think_leaks)} outputs show possible thinking leakage."
    if format_failures:
        return "observe", f"{len(format_failures)} outputs failed the expected format check."
    return "replace_ready", "Two rounds passed mechanical checks. Human semantic review is still required."


def summarize_model(records: list[dict[str, Any]]) -> dict[str, Any]:
    durations = [float(record.get("duration_seconds", 0)) for record in records]
    total = len(records)
    success = sum(1 for record in records if record.get("success"))
    format_pass = sum(1 for record in records if record.get("format_pass"))
    think_leak = sum(1 for record in records if record.get("think_leak"))
    return {
        "total": total,
        "success": success,
        "format_pass": format_pass,
        "think_leak": think_leak,
        "avg_seconds": round(sum(durations) / total, 3) if total else 0,
        "rounds": sorted({record.get("round") for record in records}),
    }


def load_results(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if "records" not in data or not isinstance(data["records"], list):
        raise ValueError("Benchmark JSON must contain a 'records' list.")
    return data


def render_report(data: dict[str, Any]) -> str:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in data["records"]:
        grouped[str(record.get("model", "unknown"))].append(record)

    lines: list[str] = []
    lines.append("# ModelPilot Benchmark Report")
    lines.append("")
    lines.append(f"- Version: {data.get('version', 'unknown')}")
    lines.append(f"- Generated at: {data.get('generated_at', 'unknown')}")
    lines.append(f"- Local only: {data.get('local_only', True)}")
    lines.append(f"- Rounds requested: {data.get('rounds_requested', 'unknown')}")
    lines.append(f"- Prompt count: {data.get('prompt_count', 'unknown')}")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append("| Model | Decision | Reason | Success | Format | Think leak | Avg seconds |")
    lines.append("| --- | --- | --- | ---: | ---: | ---: | ---: |")

    for model, records in sorted(grouped.items()):
        summary = summarize_model(records)
        decision, reason = decision_for_model(records)
        lines.append(
            "| {model} | {decision} | {reason} | {success}/{total} | {format_pass}/{total} | {think_leak} | {avg_seconds} |".format(
                model=model,
                decision=decision,
                reason=reason,
                success=summary["success"],
                total=summary["total"],
                format_pass=summary["format_pass"],
                think_leak=summary["think_leak"],
                avg_seconds=summary["avg_seconds"],
            )
        )

    lines.append("")
    lines.append("## Replacement Decision")
    lines.append("")
    lines.append("- `replace_ready` means both rounds passed mechanical checks.")
    lines.append("- A human must still review semantic quality before replacing a production workflow model.")
    lines.append("- Keep the previous model and config available for rollback.")
    lines.append("")
    lines.append("## Detailed Runs")
    lines.append("")
    lines.append("| Round | Model | Prompt | Success | Format | Think leak | Seconds | Error |")
    lines.append("| ---: | --- | --- | --- | --- | --- | ---: | --- |")

    for record in data["records"]:
        error = str(record.get("error", "")).replace("\n", " ").strip()
        lines.append(
            "| {round} | {model} | {prompt_id} | {success} | {format_pass} | {think_leak} | {seconds} | {error} |".format(
                round=record.get("round"),
                model=record.get("model"),
                prompt_id=record.get("prompt_id"),
                success=record.get("success"),
                format_pass=record.get("format_pass"),
                think_leak=record.get("think_leak"),
                seconds=record.get("duration_seconds"),
                error=error or "-",
            )
        )

    lines.append("")
    lines.append("## Risks and Limits")
    lines.append("")
    lines.append("- Mechanical checks do not prove semantic quality.")
    lines.append("- Results are comparable only when the same prompt set and runtime conditions are used.")
    lines.append("- Do not delete old models based only on this report.")
    lines.append("")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render a ModelPilot benchmark report.")
    parser.add_argument("--input", required=True, type=Path, help="Benchmark JSON path.")
    parser.add_argument("--output", required=True, type=Path, help="Markdown report path.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    data = load_results(args.input)
    report = render_report(data)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(report, encoding="utf-8")
    print(f"Wrote report to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

