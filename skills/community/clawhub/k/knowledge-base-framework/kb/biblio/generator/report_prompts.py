#!/usr/bin/env python3
"""
Report Prompt Building and Data Analysis

Builds LLM prompts for daily, weekly, and monthly reports.
Includes hotspot detection and default template fallback.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

from kb.base.logger import get_logger

logger = get_logger("kb.llm.generator.report.prompts")


def default_template() -> str:
    """Fallback template if file is missing."""
    return """# {{ title }}

> **Abfrage:** {{ query }}

## Zusammenfassung

{{ summary }}

---

## Detailanalyse

{{ content }}

---

## Quellen

{% for source in source_list %}
- {{ source }}
{% endfor %}

---

## Metadaten

- **Erstellt:** {{ generated_at }}
- **Modell:** {{ model }}
- **Typ:** {{ report_type }}
- **Quellen:** {{ sources | length }} Dokumente

---

*Automatisch generiert vom kb-framework LLM-System*"""


def load_template(templates_path: Path) -> str:
    """Load the report prompt template from file, or return default."""
    template_path = templates_path / "report_template.md"
    if template_path.exists():
        return template_path.read_text(encoding="utf-8")
    logger.warning(f"Report template not found at {template_path}, using default")
    return default_template()


def compute_hotspots(
    essences: List[Dict[str, Any]],
    essences_path: Path,
) -> List[Dict[str, str]]:
    """
    Identify hotspot topics that appear in multiple essences.

    A hotspot is a topic/keyword referenced by 2+ essences.

    Args:
        essences: List of essence metadata dicts
        essences_path: Path to the essences directory

    Returns:
        List of hotspot dicts with topic and count, sorted by count desc
    """
    keyword_counts: Dict[str, int] = {}
    entity_counts: Dict[str, int] = {}

    for essence in essences:
        hash_val = essence.get("hash", "")

        # Try to read full data for keywords/entities
        json_path = essences_path / hash_val / "essence.json"
        if not json_path.exists():
            continue

        try:
            data = json.loads(json_path.read_text(encoding="utf-8"))
            full_data = data.get("essence", {})
        except (json.JSONDecodeError, IOError):
            continue

        for kw in full_data.get("keywords", []):
            kw_lower = kw.lower()
            keyword_counts[kw_lower] = keyword_counts.get(kw_lower, 0) + 1

        for entity in full_data.get("entities", []):
            entity_lower = entity.lower()
            entity_counts[entity_lower] = entity_counts.get(entity_lower, 0) + 1

    hotspots = []

    for kw, count in keyword_counts.items():
        if count >= 2:
            hotspots.append({"topic": kw, "count": count, "type": "keyword"})

    for entity, count in entity_counts.items():
        if count >= 2:
            hotspots.append({"topic": entity, "count": count, "type": "entity"})

    hotspots.sort(key=lambda x: x["count"], reverse=True)
    return hotspots[:20]  # Top 20


def build_daily_prompt(
    essences: List[Dict[str, Any]],
    hotspots: List[Dict[str, str]],
    period_start: datetime,
    period_end: datetime,
    essences_path: Path,
) -> str:
    """
    Build the LLM prompt for daily report generation.

    Args:
        essences: List of essences from the period
        hotspots: List of hotspot topics
        period_start: Period start
        period_end: Period end
        essences_path: Path to essences directory

    Returns:
        Formatted prompt string
    """
    period_str = (
        f"{period_start.strftime('%Y-%m-%d %H:%M')} – "
        f"{period_end.strftime('%Y-%m-%d %H:%M')} UTC"
    )

    prompt_parts = [
        "Du bist ein Wissensmanagement-Analyst. Erstelle einen täglichen "
        "Zusammenfassungsbericht der Knowledge Base.\n\n",
        f"## Berichtszeitraum: {period_str}\n\n",
        f"## Datenbasis:\n",
        f"- Neue Essenzen: {len(essences)}\n",
        f"- Hotspots (mehrfach referenzierte Themen): {len(hotspots)}\n\n",
    ]

    # Essence summaries
    if essences:
        prompt_parts.append("## Neue Essenzen (letzten 24h):\n\n")
        for i, essence in enumerate(essences[:15], 1):
            title = essence.get("title", "Unbenannt")
            prompt_parts.append(f"{i}. **{title}**\n")

            # Add summary if available
            hash_val = essence.get("hash", "")
            json_path = essences_path / hash_val / "essence.json"
            if json_path.exists():
                try:
                    data = json.loads(json_path.read_text(encoding="utf-8"))
                    summary = data.get("essence", {}).get("summary", "")
                    if summary:
                        prompt_parts.append(f"   _{summary}_\n")
                    kps = data.get("essence", {}).get("key_points", [])[:3]
                    for kp in kps:
                        prompt_parts.append(f"   - {kp}\n")
                except (json.JSONDecodeError, IOError):
                    pass

        prompt_parts.append("\n")

    # Hotspots
    if hotspots:
        prompt_parts.append("## Hotspots:\n\n")
        for hs in hotspots[:10]:
            prompt_parts.append(
                f"- **{hs['topic']}** ({hs['count']}× referenziert, {hs['type']})\n"
            )
        prompt_parts.append("\n")

    # Output format
    prompt_parts.append(
        "## Anforderungen an den Bericht:\n\n"
        "1. **Zusammenfassung**: Kurze Übersicht der letzten 24h (2-3 Sätze)\n"
        "2. **Neue Erkenntnisse**: Die wichtigsten neuen Themen und Punkte\n"
        "3. **Trends**: Auffällige Muster oder Entwicklungen\n"
        "4. **Hotspot-Analyse**: Welche Themen werden besonders häufig referenziert?\n"
        "5. **Empfehlungen**: Vorschläge für weitere Recherche oder Aktionen\n\n"
        "Schreibe den Bericht als Markdown. Verwende Überschriften, "
        "Aufzählungen und **Fett** für wichtige Punkte.\n"
    )

    return "".join(prompt_parts)


def build_weekly_prompt(
    daily_reports: List[Dict[str, Any]],
    essences: List[Dict[str, Any]],
    hotspots: List[Dict[str, str]],
    period_start: datetime,
    period_end: datetime,
) -> str:
    """
    Build the LLM prompt for weekly report generation.

    Aggregates daily reports and adds trend analysis.

    Args:
        daily_reports: List of daily report data
        essences: All essences from the week
        hotspots: Hotspot topics
        period_start: Period start
        period_end: Period end

    Returns:
        Formatted prompt string
    """
    period_str = (
        f"{period_start.strftime('%Y-%m-%d')} – "
        f"{period_end.strftime('%Y-%m-%d')}"
    )

    prompt_parts = [
        "Du bist ein Wissensmanagement-Analyst. Erstelle einen wöchentlichen "
        "Zusammenfassungsbericht der Knowledge Base.\n\n",
        f"## Berichtszeitraum: {period_str}\n\n",
        f"## Datenbasis:\n",
        f"- Daily Reports: {len(daily_reports)}\n",
        f"- Neue Essenzen gesamt: {len(essences)}\n",
        f"- Hotspots: {len(hotspots)}\n\n",
    ]

    # Daily report summaries
    if daily_reports:
        prompt_parts.append("## Tagesberichte der Woche:\n\n")
        for i, report in enumerate(daily_reports[:7], 1):
            title = report.get("title", "Unbenannt")
            body = report.get("body", "")[:800]
            generated = report.get("generated_at", "")
            prompt_parts.append(
                f"### Tag {i} ({generated[:10] if generated else '?'}): {title}\n\n"
                f"{body}\n\n"
            )

    # Hotspots
    if hotspots:
        prompt_parts.append("## Wöchentliche Hotspots:\n\n")
        for hs in hotspots[:15]:
            prompt_parts.append(
                f"- **{hs['topic']}** ({hs['count']}× referenziert)\n"
            )
        prompt_parts.append("\n")

    # Essence count per day (for trend detection)
    if essences:
        prompt_parts.append("## Essenzen pro Tag:\n\n")
        day_counts: Dict[str, int] = {}
        for e in essences:
            at = e.get("extracted_at", "")
            day_key = at[:10] if at else "unknown"
            day_counts[day_key] = day_counts.get(day_key, 0) + 1

        for day, count in sorted(day_counts.items()):
            prompt_parts.append(f"- {day}: {count} Essenzen\n")
        prompt_parts.append("\n")

    # Output format
    prompt_parts.append(
        "## Anforderungen an den Wochenbericht:\n\n"
        "1. **Wochenzusammenfassung**: Gesamtüberblick (3-5 Sätze)\n"
        "2. **Trend-Analyse**: Welche Themen sind aufsteigend/absteigend?\n"
        "3. **Wöchentliche Highlights**: Die 3-5 wichtigsten Erkenntnisse\n"
        "4. **Hotspot-Entwicklung**: Wie haben sich Hotspots verändert?\n"
        "5. **Aktivitäts-Übersicht**: Essenz-Erstellung pro Tag\n"
        "6. **Empfehlungen**: Nächste Schritte und Fokus-Themen\n\n"
        "Schreibe den Bericht als Markdown mit klaren Überschriften.\n"
    )

    return "".join(prompt_parts)


def build_monthly_prompt(
    weekly_reports: List[Dict[str, Any]],
    essences: List[Dict[str, Any]],
    hotspots: List[Dict[str, str]],
    period_start: datetime,
    period_end: datetime,
) -> str:
    """
    Build the LLM prompt for monthly report generation.

    Aggregates weekly reports and adds graph visualization data.

    Args:
        weekly_reports: List of weekly report data
        essences: All essences from the month
        hotspots: Hotspot topics
        period_start: Period start
        period_end: Period end

    Returns:
        Formatted prompt string
    """
    period_str = (
        f"{period_start.strftime('%Y-%m')} – "
        f"{period_end.strftime('%Y-%m')}"
    )

    prompt_parts = [
        "Du bist ein Wissensmanagement-Analyst. Erstelle einen monatlichen "
        "Analysebericht der Knowledge Base.\n\n",
        f"## Berichtszeitraum: {period_str}\n\n",
        f"## Datenbasis:\n",
        f"- Weekly Reports: {len(weekly_reports)}\n",
        f"- Essenzen gesamt: {len(essences)}\n",
        f"- Hotspots: {len(hotspots)}\n\n",
    ]

    # Weekly report summaries
    if weekly_reports:
        prompt_parts.append("## Wochenberichte des Monats:\n\n")
        for i, report in enumerate(weekly_reports[:4], 1):
            title = report.get("title", "Unbenannt")
            body = report.get("body", "")[:1000]
            generated = report.get("generated_at", "")
            prompt_parts.append(
                f"### Woche {i} ({generated[:10] if generated else '?'}): {title}\n\n"
                f"{body}\n\n"
            )

    # Hotspots
    if hotspots:
        prompt_parts.append("## Monatliche Hotspots:\n\n")
        for hs in hotspots[:20]:
            prompt_parts.append(
                f"- **{hs['topic']}** ({hs['count']}× referenziert)\n"
            )
        prompt_parts.append("\n")

    # Activity breakdown per week
    if essences:
        prompt_parts.append("## Essenzen pro Woche:\n\n")
        week_counts: Dict[str, int] = {}
        for e in essences:
            at = e.get("extracted_at", "")
            try:
                dt = datetime.fromisoformat(at.replace("Z", "+00:00"))
                week_key = f"KW{dt.isocalendar()[1]}"
            except (ValueError, AttributeError):
                week_key = "unknown"
            week_counts[week_key] = week_counts.get(week_key, 0) + 1

        for week, count in sorted(week_counts.items()):
            prompt_parts.append(f"- {week}: {count} Essenzen\n")
        prompt_parts.append("\n")

    # Output format
    prompt_parts.append(
        "## Anforderungen an den Monatsbericht:\n\n"
        "1. **Monatszusammenfassung**: Gesamtüberblick (5-8 Sätze)\n"
        "2. **Langfristige Trends**: Übergeordnete Entwicklungen\n"
        "3. **Monats-Highlights**: Top 5-10 Erkenntnisse\n"
        "4. **Hotspot-Netzwerk**: Beziehungen zwischen wiederkehrenden Themen\n"
        "5. **Wissensgraph-Entwicklung**: Wie hat sich das Netzwerk erweitert?\n"
        "6. **Empfehlungen**: Strategische Vorschläge für den nächsten Monat\n\n"
        "Schreibe den Bericht als Markdown mit umfassender Struktur.\n"
    )

    return "".join(prompt_parts)