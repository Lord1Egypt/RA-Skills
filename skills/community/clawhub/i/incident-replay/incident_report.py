#!/usr/bin/env python3
"""
Incident Replay — Report Generation
======================================
Generate markdown or JSON reports from incidents.

Usage:
    from incident_report import ReportGenerator
    gen = ReportGenerator(config)
    md = gen.incident_report(incident)
    md = gen.summary_report(incidents)

CLI:
    python3 incident_report.py --config incident_config.json --incident INC-0001
    python3 incident_report.py --config incident_config.json --summary
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any, List, Optional


def _load_config(path: str) -> Any:
    """Load configuration from a JSON file."""
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Config not found: {path}")
    if not path.endswith(".json"):
        raise ValueError(f"Config must be a .json file: {path}")
    if os.path.getsize(path) > 1_000_000:
        raise ValueError(f"Config file too large (>1MB): {path}")
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def _get(cfg: Any, name: str, default: Any = None) -> Any:
    if isinstance(cfg, dict):
        return cfg.get(name, default)
    return getattr(cfg, name, default)


class ReportGenerator:
    """Generate incident reports."""

    def __init__(self, config: Any):
        self.data_dir = _get(config, "DATA_DIR", "incident_data")
        self.reports_dir = os.path.join(self.data_dir, _get(config, "REPORTS_DIR", "reports"))
        self.include_diffs = _get(config, "INCLUDE_FULL_DIFFS", False)
        self.include_decisions = _get(config, "INCLUDE_DECISION_CHAIN", True)
        self.max_diff_lines = _get(config, "MAX_DIFF_LINES", 100)
        self.root_causes = _get(config, "ROOT_CAUSE_CATEGORIES", {})

    def incident_report_md(self, incident: dict) -> str:
        """Generate a full markdown incident report."""
        lines: list[str] = []
        inc_id = incident.get("id", "UNKNOWN")
        severity = incident.get("severity", "unknown").upper()
        resolved = incident.get("resolved", False)

        lines.append(f"# Incident Report — {inc_id}")
        lines.append("")
        lines.append(f"**Created:** {incident.get('created', 'N/A')}")
        lines.append(f"**Title:** {incident.get('title', 'N/A')}")
        lines.append(f"**Severity:** {severity}")
        lines.append(f"**Status:** {'Resolved ✅' if resolved else 'Open 🔴'}")
        lines.append("")

        # Root cause
        lines.append("## Root Cause Analysis")
        lines.append("")
        rc = incident.get("root_cause", "unknown")
        lines.append(f"**Category:** {rc}")
        lines.append(f"**Description:** {incident.get('root_cause_description', 'N/A')}")
        lines.append("")

        # Remediation
        remediation = incident.get("remediation", [])
        if remediation:
            lines.append("## Recommended Remediation")
            lines.append("")
            for i, step in enumerate(remediation, 1):
                lines.append(f"{i}. {step}")
            lines.append("")

        # Timeline
        timeline = incident.get("timeline", [])
        if timeline:
            lines.append("## Timeline")
            lines.append("")
            for event in timeline:
                ts = event.get("timestamp", "")[:19] or "—"
                etype = event.get("event_type", "")
                desc = event.get("description", "")
                icon = {
                    "snapshot": "📸",
                    "file_change": "📝",
                    "trigger": "🚨",
                    "decision": "🧠",
                }.get(etype, "•")
                lines.append(f"- {icon} **{ts}** [{etype}] {desc}")
            lines.append("")

        # File Changes
        file_changes = incident.get("file_changes", [])
        if file_changes:
            lines.append("## File Changes")
            lines.append("")
            lines.append("| File | Change | Size Delta |")
            lines.append("|------|--------|------------|")
            for ch in file_changes:
                path = ch.get("path", "")
                ctype = ch.get("change_type", "")
                delta = ch.get("size_delta", 0)
                symbol = {"added": "➕", "deleted": "❌", "modified": "✏️"}.get(ctype, "")
                lines.append(f"| {path} | {symbol} {ctype} | {delta:+d} bytes |")
            lines.append("")

            # Diffs
            if self.include_diffs:
                for ch in file_changes:
                    diff = ch.get("content_diff")
                    if diff:
                        lines.append(f"### Diff: {ch.get('path', '')}")
                        lines.append("```diff")
                        diff_lines = diff.split("\n")
                        lines.extend(diff_lines[:self.max_diff_lines])
                        if len(diff_lines) > self.max_diff_lines:
                            lines.append(f"... ({len(diff_lines) - self.max_diff_lines} more lines)")
                        lines.append("```")
                        lines.append("")

        # Decision Chain
        decisions = incident.get("decisions", [])
        if decisions and self.include_decisions:
            lines.append("## Decision Chain")
            lines.append("")
            lines.append("Extracted decision points leading to the incident:")
            lines.append("")
            for dp in decisions:
                ts = dp.get("timestamp", "")[:19] or "—"
                src = dp.get("source", dp.get("source_file", ""))
                ln = dp.get("line", dp.get("line_number", ""))
                text = dp.get("text", "")
                dtype = dp.get("type", dp.get("decision_type", ""))
                lines.append(f"- **[{dtype}]** {ts} ({src}:{ln}): {text}")
            lines.append("")

        # Triggers
        triggers = incident.get("triggers", [])
        if triggers:
            lines.append("## Triggers Fired")
            lines.append("")
            for t in triggers:
                sev = t.get("severity", "").upper()
                name = t.get("trigger", t.get("trigger_name", ""))
                desc = t.get("description", "")
                lines.append(f"- **[{sev}] {name}:** {desc}")
                for e in t.get("evidence", [])[:5]:
                    lines.append(f"  - {e}")
            lines.append("")

        # Notes
        notes = incident.get("notes", "")
        if notes:
            lines.append("## Notes")
            lines.append("")
            lines.append(notes)
            lines.append("")

        return "\n".join(lines)

    def summary_report_md(self, incidents: List[dict]) -> str:
        """Generate a summary report across all incidents."""
        lines: list[str] = []
        lines.append("# Incident Summary Report")
        lines.append("")
        lines.append(f"**Total Incidents:** {len(incidents)}")

        if not incidents:
            lines.append("\nNo incidents recorded.")
            return "\n".join(lines)

        # Severity breakdown
        sev_counts: dict[str, int] = {}
        rc_counts: dict[str, int] = {}
        open_count = 0
        for inc in incidents:
            sev = inc.get("severity", "unknown")
            sev_counts[sev] = sev_counts.get(sev, 0) + 1
            rc = inc.get("root_cause", "unknown")
            rc_counts[rc] = rc_counts.get(rc, 0) + 1
            if not inc.get("resolved", False):
                open_count += 1

        lines.append(f"**Open:** {open_count}  |  **Resolved:** {len(incidents) - open_count}")
        lines.append("")

        lines.append("## By Severity")
        lines.append("")
        for sev in ["critical", "high", "medium", "low"]:
            count = sev_counts.get(sev, 0)
            if count:
                bar = "█" * count
                lines.append(f"- **{sev.upper()}:** {count} {bar}")
        lines.append("")

        lines.append("## By Root Cause")
        lines.append("")
        for rc, count in sorted(rc_counts.items(), key=lambda x: -x[1]):
            desc = self.root_causes.get(rc, {}).get("description", "")
            lines.append(f"- **{rc}** ({count}): {desc}")
        lines.append("")

        # Recent incidents
        lines.append("## All Incidents")
        lines.append("")
        lines.append("| ID | Severity | Title | Root Cause | Status |")
        lines.append("|----|----------|-------|------------|--------|")
        for inc in incidents:
            status = "✅" if inc.get("resolved") else "🔴"
            lines.append(
                f"| {inc.get('id', '')} "
                f"| {inc.get('severity', '').upper()} "
                f"| {inc.get('title', '')} "
                f"| {inc.get('root_cause', '')} "
                f"| {status} |"
            )
        lines.append("")

        return "\n".join(lines)

    def save_report(self, content: str, filename: str) -> str:
        os.makedirs(self.reports_dir, exist_ok=True)
        path = os.path.join(self.reports_dir, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return path


# ── CLI ───────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description="Incident Replay — report generation")
    parser.add_argument("--config", required=True, help="Path to config .json file")
    parser.add_argument("--incident", default=None, help="Generate report for incident ID")
    parser.add_argument("--summary", action="store_true", help="Generate summary of all incidents")
    parser.add_argument("--output", default=None, help="Save to file instead of stdout")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    args = parser.parse_args()

    try:
        cfg = _load_config(args.config)
    except Exception as exc:
        print(f"Error loading config: {exc}", file=sys.stderr)
        sys.exit(1)

    gen = ReportGenerator(cfg)

    if args.incident:
        try:
            from incident_replay import Analyzer
            analyzer = Analyzer(cfg)
            inc = analyzer.load_incident(args.incident)
            if inc is None:
                print(f"Incident {args.incident} not found.", file=sys.stderr)
                sys.exit(1)
            inc_dict = inc.to_dict()
        except Exception as exc:
            print(f"Error: {exc}", file=sys.stderr)
            sys.exit(1)

        if args.format == "json":
            content = json.dumps(inc_dict, indent=2, default=str)
        else:
            content = gen.incident_report_md(inc_dict)

    elif args.summary:
        try:
            from incident_replay import Analyzer
            analyzer = Analyzer(cfg)
            incidents = analyzer.list_incidents()
        except Exception as exc:
            print(f"Error: {exc}", file=sys.stderr)
            sys.exit(1)

        if args.format == "json":
            content = json.dumps(incidents, indent=2)
        else:
            content = gen.summary_report_md(incidents)
    else:
        parser.print_help()
        return

    if args.output:
        path = gen.save_report(content, args.output)
        print(f"Report saved to {path}")
    else:
        print(content)


if __name__ == "__main__":
    main()
