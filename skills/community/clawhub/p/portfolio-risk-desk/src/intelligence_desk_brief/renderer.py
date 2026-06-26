"""Render a human-readable Portfolio Risk Desk brief."""

from __future__ import annotations

from intelligence_desk_brief.contracts import CreateBriefResponse


def _line_list(items: list[str]) -> str:
    return ", ".join(items) if items else "None provided"


def render_markdown(brief: CreateBriefResponse) -> str:
    lines: list[str] = [
        f"# Portfolio Risk Desk - {brief.date}",
        "",
        "## 0) User focus",
        f"- Portfolio or watchlist in scope: {brief.user_focus.portfolio_or_watchlist}",
        f"- Interested industries or themes: {_line_list(brief.user_focus.interested_industries)}",
        f"- Brief objective: {brief.user_focus.brief_objective}",
        f"- Factor or exposure lens: {_line_list(brief.user_focus.factor_lens)}",
        f"- Comparison baseline: {brief.user_focus.comparison_baseline}",
        f"- Scenario questions being stress-tested: {_line_list(brief.user_focus.scenario_questions)}",
        "",
        "## 1) Executive summary",
        f"- {brief.summary}",
        "",
        "## 2) Current exposure map",
    ]

    for item in brief.current_exposure_map:
        lines.extend(
            [
                f"- {item['name']}: {item['assessment']}",
                f"  Names: {_line_list(item.get('names', []))}",
                f"  Confidence and assumptions: {item.get('confidence', 'unknown')} | {item.get('assumptions', 'n/a')}",
            ]
        )

    lines.extend(["", "### Dominant factors"])
    for item in brief.dominant_factors:
        lines.append(
            f"- {item['factor']}: {item['stance']} - {item['impact_summary']}"
        )

    lines.extend(["", "## 3) What changed since last brief"])
    for item in brief.risk_map_changes:
        lines.append(f"- {item['change']}: {item['effect']}")

    lines.extend(["", "## 4) Key drivers and cross-holding read-throughs"])
    for item in brief.key_drivers_and_readthroughs:
        lines.extend(
            [
                f"- Driver: {item['driver']}",
                f"  Touched names: {_line_list(item['affected_names'])}",
                f"  First-order effect: {item['first_order_effect']}",
                f"  Second-order read-through: {item['second_order_readthrough']}",
                f"  Confidence and evidence quality: {item['confidence']} | {item['evidence_quality']}",
            ]
        )

    lines.extend(["", "## 5) Scenario analysis"])
    for item in brief.scenario_analysis:
        lines.extend(
            [
                f"- Scenario: {item.scenario}",
                f"  Confidence level: {item.confidence_level}",
                f"  What likely breaks or holds: {_line_list(item.breaks_or_holds)}",
                f"  Affected names: {_line_list(item.affected_names)}",
                "  Supporting evidence:",
            ]
        )
        for evidence in item.supporting_evidence:
            lines.append(
                f"  - {evidence['title']} ({evidence['recency_note']}) - {evidence['url']}"
            )
        lines.append(f"  Falsifiers: {_line_list(item.falsifiers)}")

    lines.extend(["", "## 6) Signal vs noise"])
    for item in brief.signal_vs_noise:
        lines.append(f"- {item['bucket']}: {item['title']} - {item['reason']}")

    lines.extend(["", "## 7) Watchpoints"])
    for item in brief.watchpoints:
        lines.append(
            f"- {item['topic']}: {item['watchpoint']} (next check: {item['next_check']})"
        )

    lines.extend(["", "## 8) Evidence and sources"])
    for item in brief.evidence_and_sources:
        lines.extend(
            [
                f"- Source ID: {item.get('evidence_id', 'unknown')}",
                f"  Source title: {item['source_title']}",
                f"  URL or publisher: {item['url_or_publisher']}",
                f"  Timestamp or recency note: {item['timestamp_or_recency_note']}",
                f"  Why this source mattered to the analysis: {item['why_it_mattered']}",
            ]
        )

    lines.extend(["", "## 9) Audit trail"])
    for section_title, section_key in (
        ("Dominant factors", "dominant_factors"),
        ("Risk map changes", "risk_map_changes"),
        ("Key drivers", "key_drivers"),
        ("Scenarios", "scenarios"),
        ("Watchpoints", "watchpoints"),
    ):
        lines.append(f"### {section_title}")
        for item in brief.audit_trail.get(section_key, []):
            lines.extend(
                [
                    f"- {item['claim']}",
                    f"  Evidence refs: {_line_list(item.get('supporting_evidence_ids', []))}",
                    f"  Confidence reason: {item.get('confidence_reason', 'Not provided')}",
                ]
            )

    if brief.uncertainty_notes:
        lines.extend(["", "## Uncertainty notes"])
        for note in brief.uncertainty_notes:
            lines.append(f"- {note}")

    lines.extend(["", f"Delivery status: {brief.delivery_status.value}"])
    return "\n".join(lines).strip() + "\n"
