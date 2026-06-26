#!/usr/bin/env python3
"""
report.py — Markdown report generator for UXR Observer.

Reads an analysis JSON object (from analyze.py) and a Markdown template,
then renders a structured daily ethnographic research report.

Usage:
  python3 report.py --analysis <analysis.json> --template <template.md> --output <report.md>

If --output is omitted, the report is printed to stdout.
"""

import argparse
import json
import os
import sys
from datetime import datetime


def format_duration(seconds: float) -> str:
    """Format seconds into a human-readable duration string."""
    if seconds < 60:
        return f"{seconds:.0f}s"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f}m"
    else:
        hours = seconds / 3600
        remaining_min = (seconds % 3600) / 60
        return f"{hours:.0f}h {remaining_min:.0f}m"


def format_cost(cost: float) -> str:
    """Format cost into a readable string."""
    if cost < 0.01:
        return f"${cost:.6f}"
    elif cost < 1.0:
        return f"${cost:.4f}"
    else:
        return f"${cost:.2f}"


def severity_label(severity: int) -> str:
    """Convert severity number to descriptive label."""
    labels = {1: "Minor", 2: "Low", 3: "Moderate", 4: "High", 5: "Critical"}
    return labels.get(severity, f"Level {severity}")


def render_executive_summary(analysis: dict) -> str:
    """Generate a 2-3 sentence executive summary."""
    stats = analysis.get("session_stats", {})
    session_count = stats.get("session_count", 0)
    total_cost = stats.get("total_cost", 0)
    total_messages = stats.get("total_messages", 0)
    friction_count = len(analysis.get("friction_log", []))
    delight_count = len(analysis.get("delight_log", []))
    archetype = analysis.get("behavioral_archetype", {})
    tasks = analysis.get("task_distribution", {})

    if session_count == 0:
        return "No sessions recorded for this date."

    # Top task category
    top_task = max(tasks, key=tasks.get) if tasks else "general"
    top_pct = tasks.get(top_task, 0)

    summary_parts = []
    summary_parts.append(
        f"The user engaged in {session_count} session{'s' if session_count != 1 else ''} "
        f"with {total_messages} total messages, spending {format_cost(total_cost)} in API costs."
    )

    if top_task != "uncategorized":
        summary_parts.append(
            f"Primary focus was **{top_task}** ({top_pct}% of classified activity)."
        )

    if friction_count > 0 and delight_count > 0:
        summary_parts.append(
            f"Detected {friction_count} friction signal{'s' if friction_count != 1 else ''} "
            f"alongside {delight_count} delight signal{'s' if delight_count != 1 else ''}."
        )
    elif friction_count > 0:
        summary_parts.append(f"Detected {friction_count} friction signal{'s' if friction_count != 1 else ''} worth investigating.")
    elif delight_count > 0:
        summary_parts.append(f"A smooth day with {delight_count} positive signal{'s' if delight_count != 1 else ''}.")

    return " ".join(summary_parts)


def render_session_stats(stats: dict) -> str:
    """Render the session statistics section."""
    lines = []
    lines.append(f"| Metric | Value |")
    lines.append(f"|--------|-------|")
    lines.append(f"| Sessions | {stats.get('session_count', 0)} |")
    lines.append(f"| Total Duration | {format_duration(stats.get('total_duration_seconds', 0))} |")
    lines.append(f"| Avg Duration | {format_duration(stats.get('average_duration_seconds', 0))} |")
    lines.append(f"| Total Messages | {stats.get('total_messages', 0)} |")
    lines.append(f"| User Messages | {stats.get('total_user_messages', 0)} |")
    lines.append(f"| Assistant Messages | {stats.get('total_assistant_messages', 0)} |")
    lines.append(f"| Total Cost | {format_cost(stats.get('total_cost', 0))} |")

    # Busiest hours
    patterns = stats.get("_patterns", {})
    hours = patterns.get("session_timing", {}).get("hours", {})
    if hours:
        busiest = sorted(hours.items(), key=lambda x: int(x[1]), reverse=True)[:3]
        busiest_str = ", ".join(f"{h}:00 ({c})" for h, c in busiest)
        lines.append(f"| Busiest Hours | {busiest_str} |")

    return "\n".join(lines)


def render_task_breakdown(tasks: dict) -> str:
    """Render the task distribution breakdown."""
    if not tasks:
        return "_No task data available._"

    lines = []
    for category, pct in sorted(tasks.items(), key=lambda x: x[1], reverse=True):
        bar_len = int(pct / 5)  # Scale bar to max ~20 chars
        bar = "\u2588" * bar_len
        lines.append(f"- **{category}**: {pct}% {bar}")

    return "\n".join(lines)


def render_friction_log(friction: list) -> str:
    """Render the friction log section."""
    if not friction:
        return "_No friction signals detected. Smooth sailing!_"

    lines = []
    for i, f in enumerate(friction[:10], 1):
        severity = f.get("severity", 0)
        lines.append(f"**{i}. [{severity_label(severity)}] {f.get('type', 'unknown').replace('_', ' ').title()}**")
        lines.append(f"> {f.get('context', '')}")
        ts = f.get("timestamp", "")
        if ts:
            lines.append(f"_Timestamp: {ts}_")
        lines.append("")

    return "\n".join(lines)


def render_delight_log(delight: list) -> str:
    """Render the delight log section."""
    if not delight:
        return "_No explicit delight signals detected._"

    lines = []
    for i, d in enumerate(delight[:10], 1):
        dtype = d.get("type", "unknown").replace("_", " ").title()
        lines.append(f"**{i}. {dtype}**")
        lines.append(f"> {d.get('context', '')}")
        ts = d.get("timestamp", "")
        if ts:
            lines.append(f"_Timestamp: {ts}_")
        lines.append("")

    return "\n".join(lines)


def render_quotes(quotes: list) -> str:
    """Render the verbatim quotes section."""
    if not quotes:
        return "_No notable quotes extracted._"

    lines = []
    for i, q in enumerate(quotes[:5], 1):
        sentiment = q.get("sentiment", "neutral")
        emoji = {"positive": "+", "frustration": "!", "confusion": "?", "neutral": "-"}.get(sentiment, "-")
        lines.append(f"**{i}.** [{emoji}] _{sentiment}_")
        lines.append(f'> "{q.get("text", "")}"')
        ts = q.get("timestamp", "")
        if ts:
            lines.append(f"_Timestamp: {ts}_")
        lines.append("")

    return "\n".join(lines)


def render_tool_usage(tool_stats: dict) -> str:
    """Render tool/skill usage statistics."""
    lines = []
    lines.append(f"| Metric | Value |")
    lines.append(f"|--------|-------|")
    lines.append(f"| Total Tool Calls | {tool_stats.get('total_tool_calls', 0)} |")
    lines.append(f"| Successful | {tool_stats.get('successful', 0)} |")
    lines.append(f"| Failed | {tool_stats.get('failed', 0)} |")
    lines.append(f"| Success Rate | {tool_stats.get('success_rate', 0)}% |")

    return "\n".join(lines)


def render_trends(comparison: dict) -> str:
    """Render behavioral trends compared to history."""
    if not comparison.get("has_history"):
        return "_Not enough historical data yet. Trends will appear after a few days of usage._"

    notes = comparison.get("notes", [])
    if not notes:
        return "_Today's usage is within normal ranges compared to the past week._"

    lines = []
    for note in notes:
        lines.append(f"- {note}")

    return "\n".join(lines)


def render_recommendations(recs: list) -> str:
    """Render actionable recommendations."""
    if not recs:
        return "_No specific recommendations at this time._"

    lines = []
    for i, rec in enumerate(recs, 1):
        priority = rec.get("priority", "info").upper()
        lines.append(f"**{i}. [{priority}]** {rec.get('recommendation', '')}")
        lines.append("")

    return "\n".join(lines)


def render_archetype(archetype: dict) -> str:
    """Render the behavioral archetype section."""
    name = archetype.get("archetype", "unknown").replace("_", " ").title()
    desc = archetype.get("description", "")
    traits = archetype.get("traits", [])

    lines = [f"**{name}**: {desc}"]
    if traits:
        lines.append("")
        lines.append("Key traits observed:")
        for trait in traits:
            lines.append(f"- {trait}")

    return "\n".join(lines)


def render_report(analysis: dict, template: str) -> str:
    """Render the full report by substituting placeholders in the template."""
    report_date = analysis.get("date", datetime.now().strftime("%Y-%m-%d"))
    stats = analysis.get("session_stats", {})

    # Inject patterns into stats for rendering
    stats["_patterns"] = analysis.get("interaction_patterns", {})

    replacements = {
        "{{DATE}}": report_date,
        "{{EXECUTIVE_SUMMARY}}": render_executive_summary(analysis),
        "{{SESSION_STATS}}": render_session_stats(stats),
        "{{TASK_BREAKDOWN}}": render_task_breakdown(analysis.get("task_distribution", {})),
        "{{TOP_FINDINGS}}": render_top_findings(analysis),
        "{{FRICTION_LOG}}": render_friction_log(analysis.get("friction_log", [])),
        "{{DELIGHT_LOG}}": render_delight_log(analysis.get("delight_log", [])),
        "{{VERBATIM_QUOTES}}": render_quotes(analysis.get("verbatim_quotes", [])),
        "{{TOOL_USAGE}}": render_tool_usage(analysis.get("tool_usage", {})),
        "{{BEHAVIORAL_TRENDS}}": render_trends(analysis.get("trend_comparison", {})),
        "{{ARCHETYPE}}": render_archetype(analysis.get("behavioral_archetype", {})),
        "{{RECOMMENDATIONS}}": render_recommendations(analysis.get("recommendations", [])),
    }

    report = template
    for placeholder, content in replacements.items():
        report = report.replace(placeholder, content)

    return report


def render_top_findings(analysis: dict) -> str:
    """Synthesize top 3-5 findings ranked by significance."""
    findings = []

    # Finding from friction
    friction = analysis.get("friction_log", [])
    if friction:
        high_friction = [f for f in friction if f.get("severity", 0) >= 4]
        if high_friction:
            findings.append({
                "significance": 5,
                "finding": f"**High-severity friction detected**: {len(high_friction)} instance(s) of {high_friction[0]['type'].replace('_', ' ')}. Users encountering repeated friction at this level often indicate a systemic UX issue.",
            })
        elif len(friction) >= 3:
            findings.append({
                "significance": 3,
                "finding": f"**Moderate friction accumulation**: {len(friction)} friction signals across sessions suggest the agent struggled with certain request types today.",
            })

    # Finding from delight
    delight = analysis.get("delight_log", [])
    if delight:
        rapid_completions = [d for d in delight if d["type"] == "rapid_completion"]
        if rapid_completions:
            findings.append({
                "significance": 3,
                "finding": f"**Rapid task completion**: {len(rapid_completions)} task(s) completed efficiently, indicating well-matched capabilities for these request types.",
            })

    # Finding from task distribution
    tasks = analysis.get("task_distribution", {})
    if tasks:
        top = list(tasks.items())[:1]
        if top and top[0][1] > 60:
            findings.append({
                "significance": 2,
                "finding": f"**Concentrated usage**: {top[0][1]}% of activity was {top[0][0]}-related. This specialization could benefit from a dedicated skill or workflow.",
            })

    # Finding from archetype
    archetype = analysis.get("behavioral_archetype", {})
    if archetype.get("traits"):
        findings.append({
            "significance": 2,
            "finding": f"**User archetype — {archetype['archetype'].replace('_', ' ').title()}**: {archetype.get('description', '')}",
        })

    # Finding from tool usage
    tool_stats = analysis.get("tool_usage", {})
    if tool_stats.get("failed", 0) > 0:
        findings.append({
            "significance": 4,
            "finding": f"**Tool reliability concern**: {tool_stats['failed']} tool call(s) failed out of {tool_stats['total_tool_calls']} ({100 - tool_stats.get('success_rate', 100):.1f}% failure rate).",
        })

    # Sort by significance and take top 5
    findings.sort(key=lambda x: x["significance"], reverse=True)
    findings = findings[:5]

    if not findings:
        return "_Insufficient data for significant findings._"

    lines = []
    for i, f in enumerate(findings, 1):
        lines.append(f"{i}. {f['finding']}")
        lines.append("")

    return "\n".join(lines)


def load_template(template_path: str) -> str:
    """Load the report template, or use a default if not found."""
    try:
        with open(template_path, "r") as f:
            return f.read()
    except FileNotFoundError:
        # Fallback default template
        return """# UXR Daily Report — {{DATE}}

## Executive Summary

{{EXECUTIVE_SUMMARY}}

## Session Statistics

{{SESSION_STATS}}

## Task Breakdown

{{TASK_BREAKDOWN}}

## Top Findings

{{TOP_FINDINGS}}

## Friction Log

{{FRICTION_LOG}}

## Delight Log

{{DELIGHT_LOG}}

## Verbatim Quotes

{{VERBATIM_QUOTES}}

## Tool & Skill Usage

{{TOOL_USAGE}}

## Behavioral Archetype

{{ARCHETYPE}}

## Behavioral Trends

{{BEHAVIORAL_TRENDS}}

## Recommendations

{{RECOMMENDATIONS}}

---
_Generated by [UXR Observer](https://clawhub.com/skills/uxr-observer) — Ethnographic UX research for OpenClaw_
"""


def update_trends(analysis: dict, trends_file: str):
    """Append today's summary to the rolling trends file."""
    try:
        with open(trends_file, "r") as f:
            trends = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        trends = {"daily": [], "weekly": [], "monthly": []}

    stats = analysis.get("session_stats", {})
    daily_entry = {
        "date": analysis.get("date", ""),
        "session_count": stats.get("session_count", 0),
        "total_messages": stats.get("total_messages", 0),
        "total_cost": stats.get("total_cost", 0),
        "total_duration_seconds": stats.get("total_duration_seconds", 0),
        "friction_count": len(analysis.get("friction_log", [])),
        "delight_count": len(analysis.get("delight_log", [])),
        "top_task": max(analysis.get("task_distribution", {"unknown": 0}),
                        key=analysis.get("task_distribution", {"unknown": 0}).get),
        "archetype": analysis.get("behavioral_archetype", {}).get("archetype", "unknown"),
        "tool_success_rate": analysis.get("tool_usage", {}).get("success_rate", 0),
    }

    # Avoid duplicate entries for the same date
    trends["daily"] = [d for d in trends["daily"] if d.get("date") != daily_entry["date"]]
    trends["daily"].append(daily_entry)

    # Keep last 90 days
    trends["daily"] = trends["daily"][-90:]

    # Compute weekly summary if we have 7+ days
    if len(trends["daily"]) >= 7:
        last_7 = trends["daily"][-7:]
        weekly_summary = {
            "week_ending": last_7[-1]["date"],
            "avg_sessions": round(sum(d["session_count"] for d in last_7) / 7, 1),
            "total_cost": round(sum(d["total_cost"] for d in last_7), 6),
            "avg_friction": round(sum(d["friction_count"] for d in last_7) / 7, 1),
            "avg_delight": round(sum(d["delight_count"] for d in last_7) / 7, 1),
        }
        # Only add if different week
        if not trends["weekly"] or trends["weekly"][-1].get("week_ending") != weekly_summary["week_ending"]:
            trends["weekly"].append(weekly_summary)
            trends["weekly"] = trends["weekly"][-12:]  # Keep 12 weeks

    os.makedirs(os.path.dirname(trends_file) or ".", exist_ok=True)
    with open(trends_file, "w") as f:
        json.dump(trends, f, indent=2)


def main():
    parser = argparse.ArgumentParser(description="UXR Report Generator")
    parser.add_argument("--analysis", required=True, help="Path to analysis JSON file")
    parser.add_argument("--template", required=True, help="Path to report template")
    parser.add_argument("--output", default=None, help="Output file path (stdout if omitted)")
    parser.add_argument("--trends", default=None, help="Path to trends.json to update after report generation")
    args = parser.parse_args()

    try:
        with open(args.analysis, "r") as f:
            analysis = json.load(f)
    except FileNotFoundError:
        print(f"Error: Analysis file not found: {args.analysis}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in analysis file: {e}", file=sys.stderr)
        sys.exit(1)

    template = load_template(args.template)
    report = render_report(analysis, template)

    if args.output:
        os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
        with open(args.output, "w") as f:
            f.write(report)
        print(f"Report saved to: {args.output}", file=sys.stderr)
    else:
        print(report)

    # Update trends if path provided
    if args.trends:
        update_trends(analysis, args.trends)
        print(f"Trends updated: {args.trends}", file=sys.stderr)


if __name__ == "__main__":
    main()
