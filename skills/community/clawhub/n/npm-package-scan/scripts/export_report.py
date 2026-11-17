#!/usr/bin/env python3
"""Export a structured npm-package-scan result as Markdown or JSON."""

from __future__ import annotations

import argparse
from datetime import datetime
import json
from pathlib import Path
import re
from typing import Any


SCHEMA_VERSION = "1.0"


def slugify(value: str) -> str:
    value = re.sub(r"[^A-Za-z0-9._-]+", "-", value.strip()).strip("-")
    return value or "project"


def load_model(path: Path, project_name: str | None = None) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("scan result must be a JSON object")
    scan = data.setdefault("scan", {})
    if not isinstance(scan, dict):
        raise ValueError("scan must be a JSON object")
    if project_name:
        scan["projectName"] = project_name
    scan.setdefault("projectName", "project")
    scan.setdefault("completedAt", datetime.now().astimezone().isoformat())
    scan.setdefault("packageManager", "unknown")
    scan.setdefault("scope", "repository")
    scan.setdefault("networkChecks", {"executed": False, "commands": [], "note": ""})
    data.setdefault("schemaVersion", SCHEMA_VERSION)
    data.setdefault("dependencies", [])
    data.setdefault("findings", [])
    data.setdefault("actions", [])
    return data


def text(value: Any) -> str:
    if value is None:
        return "-"
    if isinstance(value, bool):
        return "yes" if value else "no"
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    return str(value)


def render_markdown(data: dict[str, Any]) -> str:
    scan = data["scan"]
    network = scan.get("networkChecks", {})
    lines = [
        "# Dependency risk review", "", "## Scope and confidence", "",
        f"- Project: {text(scan.get('projectName'))}",
        f"- Scope: {text(scan.get('scope'))}",
        f"- Package manager: {text(scan.get('packageManager'))}",
        f"- Completed: {text(scan.get('completedAt'))}",
        f"- Network checks executed: {text(network.get('executed', False))}",
        f"- Network check note: {text(network.get('note'))}", "",
        "## Dependencies", "",
    ]
    dependencies = data.get("dependencies", [])
    if dependencies:
        lines.extend(["| Name | Version | Kind | Path |", "| --- | --- | --- | --- |"])
        for item in dependencies:
            lines.append(
                f"| {text(item.get('name'))} | {text(item.get('version'))} | "
                f"{text(item.get('kind'))} | {text(item.get('path'))} |"
            )
    else:
        lines.append("No dependency entries were recorded.")
    lines.extend(["", "## Findings", ""])
    findings = data.get("findings", [])
    if not findings:
        lines.append("No actionable findings were recorded.")
    else:
        for finding in findings:
            severity = text(finding.get("severity", "Info"))
            title = text(finding.get("title", finding.get("ruleId", "Finding")))
            lines.extend([
                f"### [{severity}] {title}", "",
                f"- **Finding ID:** {text(finding.get('id'))}",
                f"- **Package/path:** {text(finding.get('packagePath', finding.get('path')))}",
                f"- **Evidence:** {text(finding.get('evidence'))}",
                f"- **Impact:** {text(finding.get('impact'))}",
                f"- **Confidence:** {text(finding.get('confidence'))}",
                f"- **Action:** {text(finding.get('action'))}",
                f"- **Verify:** `{text(finding.get('verify'))}`",
                f"- **Blast radius:** {text(finding.get('blastRadius'))}", "",
            ])
    lines.extend(["## Action plan", ""])
    actions = data.get("actions", [])
    if actions:
        lines.extend(f"{index}. {text(action)}" for index, action in enumerate(actions, 1))
    else:
        lines.append("No follow-up actions were recorded.")
    lines.append("")
    return "\n".join(lines)


def default_output(data: dict[str, Any], fmt: str, output_dir: Path) -> Path:
    scan = data["scan"]
    completed = scan.get("completedAt", "")
    try:
        timestamp = datetime.fromisoformat(completed).astimezone().strftime("%Y%m%d-%H%M")
    except (TypeError, ValueError):
        timestamp = datetime.now().astimezone().strftime("%Y%m%d-%H%M")
    suffix = "md" if fmt == "markdown" else "json"
    filename = f"npm-package-scan-{slugify(str(scan.get('projectName', 'project')))}-{timestamp}.{suffix}"
    return output_dir / filename


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path, help="Structured scan result JSON")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--output", type=Path, help="Output file; defaults to a timestamped report name")
    parser.add_argument("--output-dir", type=Path, default=Path("."))
    parser.add_argument("--project-name", help="Override the project name used in the report filename")
    args = parser.parse_args()

    data = load_model(args.input, args.project_name)
    destination = args.output or default_output(data, args.format, args.output_dir)
    destination.parent.mkdir(parents=True, exist_ok=True)
    if args.format == "markdown":
        destination.write_text(render_markdown(data), encoding="utf-8")
    else:
        destination.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(destination)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
