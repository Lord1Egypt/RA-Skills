from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def normalize_status(value: str | None) -> str:
    if not value:
        return "failed"
    normalized = value.strip().lower()
    aliases = {
        "pass": "passed",
        "passed": "passed",
        "ok": "passed",
        "success": "passed",
        "fail": "failed",
        "failed": "failed",
        "error": "failed",
        "skip": "skipped",
        "skipped": "skipped",
    }
    return aliases.get(normalized, "failed")


def collect_result_files(results_dir: Path) -> list[Path]:
    return sorted(path for path in results_dir.glob("*.json") if path.is_file())


def summarize(results: list[dict[str, Any]]) -> dict[str, Any]:
    counts = Counter(item["status"] for item in results)
    return {
        "total": len(results),
        "passed": counts.get("passed", 0),
        "failed": counts.get("failed", 0),
        "skipped": counts.get("skipped", 0),
    }


def format_markdown(report: dict[str, Any]) -> str:
    summary = report["summary"]
    lines = [
        "# API Test Report",
        "",
        "## Executive Summary",
        f"- Environment: {report['environment'].get('name', 'unknown')}",
        f"- Base URL: {report['environment'].get('base_url', 'unknown')}",
        f"- Runner: {report['environment'].get('runner', 'unknown')}",
        f"- Total: {summary['total']}",
        f"- Passed: {summary['passed']}",
        f"- Failed: {summary['failed']}",
        f"- Skipped: {summary['skipped']}",
        "",
        "## Source Artifacts",
    ]
    for artifact in report["source_artifacts"]:
        lines.append(f"- {artifact}")

    lines.extend(["", "## Execution Results"])
    if not report["results"]:
        lines.append("- No test results were found.")
    else:
        for item in report["results"]:
            lines.append(
                f"- [{item['status'].upper()}] {item.get('case_id', 'unknown-case')} | {item.get('endpoint', 'unknown endpoint')} | {item.get('message', '')}".rstrip()
            )

    lines.extend(["", "## Coverage and Gaps"])
    uncovered = report.get("uncovered_cases", [])
    if uncovered:
        for item in uncovered:
            lines.append(f"- Unexecuted case: {item}")
    else:
        lines.append("- All manifest cases were observed in the execution results, or no manifest cases were defined.")

    lines.extend(["", "## Failure Diagnostics"])
    failures = [item for item in report["results"] if item["status"] == "failed"]
    if failures:
        for item in failures:
            details = item.get("details") or item.get("message") or "No details provided"
            lines.append(f"- {item.get('case_id', 'unknown-case')}: {details}")
    else:
        lines.append("- No failures recorded.")

    lines.extend(["", "## Assumptions and Blockers"])
    assumptions = report.get("assumptions", [])
    if assumptions:
        for item in assumptions:
            lines.append(f"- {item}")
    else:
        lines.append("- None recorded by the report builder.")

    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a complete API test report from result JSON files.")
    parser.add_argument("--manifest", required=True, help="Path to case-manifest.json")
    parser.add_argument("--results-dir", required=True, help="Directory containing JSON result files")
    parser.add_argument("--output-md", required=True, help="Output markdown report path")
    parser.add_argument("--output-json", required=True, help="Output JSON report path")
    args = parser.parse_args()

    manifest_path = Path(args.manifest).expanduser().resolve()
    results_dir = Path(args.results_dir).expanduser().resolve()
    output_md = Path(args.output_md).expanduser().resolve()
    output_json = Path(args.output_json).expanduser().resolve()

    manifest = load_json(manifest_path)
    result_files = collect_result_files(results_dir)

    merged_results: list[dict[str, Any]] = []
    env: dict[str, Any] = {
        "name": manifest.get("environment", "unknown"),
        "base_url": "unknown",
        "runner": manifest.get("runner", "unknown"),
    }
    source_artifacts = [str(manifest_path)] + [str(path) for path in result_files]

    for result_path in result_files:
        payload = load_json(result_path)
        if isinstance(payload, dict):
            env.update(payload.get("environment", {}))
            for item in payload.get("results", []):
                if not isinstance(item, dict):
                    continue
                normalized = dict(item)
                normalized["status"] = normalize_status(item.get("status"))
                merged_results.append(normalized)

    summary = summarize(merged_results)
    manifest_case_ids = [item.get("case_id") for item in manifest.get("cases", []) if isinstance(item, dict) and item.get("case_id")]
    executed_case_ids = {item.get("case_id") for item in merged_results if item.get("case_id")}
    uncovered_cases = [case_id for case_id in manifest_case_ids if case_id not in executed_case_ids]

    report = {
        "environment": env,
        "summary": summary,
        "results": merged_results,
        "source_artifacts": source_artifacts,
        "uncovered_cases": uncovered_cases,
        "assumptions": [],
    }

    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_md.write_text(format_markdown(report), encoding="utf-8")
    output_json.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(json.dumps({
        "markdown_report": str(output_md),
        "json_report": str(output_json),
        "summary": summary,
        "uncovered_cases": uncovered_cases,
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

