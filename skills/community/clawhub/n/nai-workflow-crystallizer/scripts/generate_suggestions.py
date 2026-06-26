#!/usr/bin/env python3
"""
Workflow Crystallizer — Suggestion Generator

Takes cluster analysis output (from analyze_patterns.py) and generates
actionable suggestions: cron job definitions, skill drafts, workflow
shortcuts, or monitoring proposals.

Usage:
    python3 analyze_patterns.py --memory-dir PATH | python3 generate_suggestions.py
    
    Or standalone:
    python3 generate_suggestions.py --clusters clusters.json [--state-file PATH]

Outputs a JSON array of suggestions to stdout.
Updates state.json with new suggestions.
"""

import argparse
import hashlib
import json
import sys
from datetime import datetime
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from state import (
    load_state, save_state, add_suggestion, is_duplicate_suggestion,
    get_active_suggestions
)

# ── Existing automation detection ─────────────────────────────────────

def load_existing_crons(cron_path: str = None) -> list[dict]:
    """Load existing cron jobs to avoid duplicate suggestions."""
    if cron_path is None:
        cron_path = Path.home() / ".openclaw" / "cron" / "jobs.json"
    else:
        cron_path = Path(cron_path)

    if not cron_path.exists():
        return []

    try:
        with open(cron_path) as f:
            data = json.load(f)
        return data.get("jobs", [])
    except (json.JSONDecodeError, KeyError):
        return []


def load_existing_skills(skills_dirs: list[str] = None) -> list[str]:
    """Load names of existing skills to avoid duplicate suggestions."""
    if skills_dirs is None:
        skills_dirs = [
            str(Path.home() / ".openclaw" / "workspace" / "skills"),
            "/opt/homebrew/lib/node_modules/openclaw/skills",
        ]

    names = []
    for d in skills_dirs:
        p = Path(d)
        if not p.exists():
            continue
        for skill_dir in p.iterdir():
            if skill_dir.is_dir():
                skill_md = skill_dir / "SKILL.md"
                if skill_md.exists():
                    names.append(skill_dir.name.lower())

    return names


def cron_covers_cluster(crons: list[dict], cluster: dict) -> bool:
    """Check if an existing cron job already covers this cluster's pattern.
    
    Uses entity-focused matching to avoid false positives from generic keywords.
    A cron "covers" a cluster only if they share specific named entities, not
    just common words like 'web', 'api', 'dashboard'.
    """
    # Only match on entities (proper nouns / project names), not generic keywords
    cluster_entities = set(e.lower() for e in cluster.get("top_entities", []))

    # Filter out generic entity names that cause false matches
    # These appear in many contexts and don't indicate a specific purpose
    generic_entities = {"api", "web", "built", "code", "day", "build", "setup",
                        "config", "update", "fix", "test", "run", "new",
                        "claude", "openai", "google", "discord", "github",
                        "react", "python", "rust", "sqlite", "openclaw",
                        "obsidian", "ollama", "anthropic"}
    specific_entities = cluster_entities - generic_entities

    if not specific_entities:
        return False

    for job in crons:
        job_name = job.get("name", "").lower()
        job_msg = job.get("payload", {}).get("message", "").lower()
        job_text = job_name + " " + job_msg

        # Require at least 2 specific entity matches
        entity_matches = sum(1 for e in specific_entities if e in job_text)
        if entity_matches >= 2:
            return True
        # Single match only for highly specific names (>7 chars, not a common tool)
        if entity_matches == 1:
            matched = [e for e in specific_entities if e in job_text]
            if any(len(e) > 7 for e in matched):
                return True

    return False


def skill_covers_cluster(skill_names: list[str], cluster: dict) -> bool:
    """Check if an existing skill already covers this cluster's pattern."""
    cluster_keywords = set(k.lower() for k in cluster.get("top_keywords", []))
    cluster_entities = set(e.lower() for e in cluster.get("top_entities", []))

    for name in skill_names:
        # Fuzzy match: skill name tokens overlap with cluster keywords
        name_tokens = set(name.replace("-", " ").replace("_", " ").split())
        if len(name_tokens & cluster_keywords) >= 1:
            return True
        if name in cluster_entities:
            return True

    return False


# ── Suggestion ID generation ──────────────────────────────────────────

def make_suggestion_id(cluster: dict) -> str:
    """Generate a stable ID for a suggestion based on cluster content."""
    key = f"{cluster['label']}:{cluster['pattern_type']}:{','.join(cluster['dates'])}"
    return "sugg-" + hashlib.md5(key.encode()).hexdigest()[:8]


# ── Suggestion generators by type ─────────────────────────────────────

def generate_cron_suggestion(cluster: dict) -> dict:
    """Generate a cron job suggestion for a time-correlated pattern."""
    dates = cluster.get("dates", [])
    events = cluster.get("events", [])
    entities = cluster.get("top_entities", [])
    keywords = cluster.get("top_keywords", [])

    # Determine schedule from time correlation
    # Check day-of-week pattern
    days_of_week = []
    for ev in events:
        if "day_of_week" in ev:
            days_of_week.append(ev["day_of_week"])

    # Build a human-readable description of what was detected
    event_descriptions = []
    for ev in events:
        event_descriptions.append(f"- {ev.get('date', '?')}: {ev.get('section', '?')}")

    evidence = "\n".join(event_descriptions)
    label = cluster["label"]

    # Default to weekly schedule
    cron_expr = "0 10 * * 1"  # Monday 10 AM
    schedule_desc = "weekly on Monday at 10:00 AM ET"

    # Try to infer a better schedule
    if len(dates) >= 3:
        # Check if it's daily
        if cluster["unique_days"] >= 4:
            cron_expr = "0 10 * * *"
            schedule_desc = "daily at 10:00 AM ET"
        # Check if events cluster on a specific day
        elif days_of_week:
            from collections import Counter
            dow_counts = Counter(days_of_week)
            top_day, top_count = dow_counts.most_common(1)[0]
            if top_count >= 2:
                dow_map = {
                    "Monday": "1", "Tuesday": "2", "Wednesday": "3",
                    "Thursday": "4", "Friday": "5", "Saturday": "6", "Sunday": "0"
                }
                cron_num = dow_map.get(top_day, "1")
                cron_expr = f"0 10 * * {cron_num}"
                schedule_desc = f"weekly on {top_day} at 10:00 AM ET"

    task_desc = f"Review and handle: {label}"
    if entities:
        task_desc = f"Check on {', '.join(entities[:2])} — recurring pattern detected"

    return {
        "id": make_suggestion_id(cluster),
        "type": "cron",
        "title": f"Scheduled: {label}",
        "confidence": cluster["confidence"],
        "evidence_dates": dates,
        "evidence": evidence,
        "description": (
            f"This pattern appeared {cluster['count']} times across "
            f"{cluster['unique_days']} days. It looks schedulable."
        ),
        "implementation": {
            "cron_definition": {
                "name": f"Auto: {label}",
                "schedule": {
                    "kind": "cron",
                    "expr": cron_expr,
                    "tz": "America/New_York"
                },
                "payload": {
                    "kind": "agentTurn",
                    "message": task_desc
                }
            },
            "schedule_description": schedule_desc,
        }
    }


def generate_skill_suggestion(cluster: dict) -> dict:
    """Generate a skill suggestion for a multi-step workflow pattern."""
    events = cluster.get("events", [])
    entities = cluster.get("top_entities", [])
    keywords = cluster.get("top_keywords", [])
    dates = cluster.get("dates", [])

    event_descriptions = []
    for ev in events:
        event_descriptions.append(f"- {ev.get('date', '?')}: {ev.get('section', '?')}")
    evidence = "\n".join(event_descriptions)

    label = cluster["label"]
    skill_name = label.lower().replace(" + ", "-").replace(" / ", "-").replace(" ", "-")
    skill_name = "".join(c for c in skill_name if c.isalnum() or c == "-")[:30]

    # Build a draft SKILL.md
    keyword_str = ", ".join(keywords[:5])
    skill_draft = (
        f"---\n"
        f"name: {skill_name}\n"
        f"description: \"Automates the recurring workflow: {label}. "
        f"Detected from {cluster['count']} occurrences across "
        f"{cluster['unique_days']} days. Trigger words: {keyword_str}.\"\n"
        f"---\n\n"
        f"# {label} Skill\n\n"
        f"Auto-generated skill draft from Workflow Crystallizer.\n"
        f"This pattern was detected {cluster['count']} times.\n\n"
        f"## Workflow\n\n"
        f"1. [Step 1 — fill in based on the pattern]\n"
        f"2. [Step 2]\n"
        f"3. [Step 3]\n\n"
        f"## When to Use\n\n"
        f"Trigger phrases: {keyword_str}\n\n"
        f"## Evidence\n\n"
        f"{evidence}\n"
    )

    return {
        "id": make_suggestion_id(cluster),
        "type": "skill",
        "title": f"Skill: {label}",
        "confidence": cluster["confidence"],
        "evidence_dates": dates,
        "evidence": evidence,
        "description": (
            f"This multi-step workflow appeared {cluster['count']} times across "
            f"{cluster['unique_days']} days. It could be formalized as a skill."
        ),
        "implementation": {
            "skill_name": skill_name,
            "skill_draft": skill_draft,
        }
    }


def generate_workflow_suggestion(cluster: dict) -> dict:
    """Generate a workflow shortcut suggestion."""
    events = cluster.get("events", [])
    entities = cluster.get("top_entities", [])
    keywords = cluster.get("top_keywords", [])
    dates = cluster.get("dates", [])

    event_descriptions = []
    for ev in events:
        event_descriptions.append(f"- {ev.get('date', '?')}: {ev.get('section', '?')}")
    evidence = "\n".join(event_descriptions)

    label = cluster["label"]

    # Generate a composite prompt suggestion
    entity_str = ", ".join(entities[:3]) if entities else "this topic"
    prompt = f"Run the standard {label.lower()} workflow: [describe the steps you usually take]"

    return {
        "id": make_suggestion_id(cluster),
        "type": "workflow",
        "title": f"Shortcut: {label}",
        "confidence": cluster["confidence"],
        "evidence_dates": dates,
        "evidence": evidence,
        "description": (
            f"You do this {cluster['count']} times regularly. "
            f"Consider a saved prompt or composite workflow."
        ),
        "implementation": {
            "suggested_prompt": prompt,
            "components": keywords[:5],
        }
    }


def generate_monitor_suggestion(cluster: dict) -> dict:
    """Generate a proactive monitoring suggestion."""
    events = cluster.get("events", [])
    entities = cluster.get("top_entities", [])
    dates = cluster.get("dates", [])

    event_descriptions = []
    for ev in events:
        event_descriptions.append(f"- {ev.get('date', '?')}: {ev.get('section', '?')}")
    evidence = "\n".join(event_descriptions)

    label = cluster["label"]
    entity_str = ", ".join(entities[:2]) if entities else label

    return {
        "id": make_suggestion_id(cluster),
        "type": "monitor",
        "title": f"Monitor: {entity_str}",
        "confidence": cluster["confidence"],
        "evidence_dates": dates,
        "evidence": evidence,
        "description": (
            f"You've checked on {entity_str} {cluster['count']} times across "
            f"{cluster['unique_days']} days. Want automated monitoring?"
        ),
        "implementation": {
            "monitor_target": entity_str,
            "suggested_frequency": "every 6 hours" if cluster["count"] >= 5 else "daily",
            "cron_definition": {
                "name": f"Monitor: {entity_str}",
                "schedule": {
                    "kind": "cron",
                    "expr": "0 */6 * * *" if cluster["count"] >= 5 else "0 9 * * *",
                    "tz": "America/New_York"
                },
                "payload": {
                    "kind": "agentTurn",
                    "message": f"Check on {entity_str} — automated monitoring. Report any issues or notable changes."
                }
            }
        }
    }


# ── Main pipeline ─────────────────────────────────────────────────────

GENERATORS = {
    "cron": generate_cron_suggestion,
    "skill": generate_skill_suggestion,
    "workflow": generate_workflow_suggestion,
    "monitor": generate_monitor_suggestion,
    "none": lambda c: None,
}


def generate_suggestions(clusters: list[dict], state_path: str = None,
                         cron_path: str = None) -> list[dict]:
    """Generate suggestions from scored clusters."""
    state = load_state(state_path)
    config = state.get("config", {})
    min_confidence = config.get("min_confidence", 0.6)
    max_suggestions = config.get("max_suggestions_per_run", 3)
    min_days = config.get("min_days_of_data", 3)

    total_days = len(state.get("event_cache", {}))

    # Load existing automations
    crons = load_existing_crons(cron_path)
    skills = load_existing_skills()

    suggestions = []

    for cluster in clusters:
        # Skip low confidence
        if cluster["confidence"] < min_confidence:
            continue

        # Skip projects (not patterns)
        if cluster.get("is_project", False):
            sys.stderr.write(
                f"  Skipping project (not pattern): {cluster['label']}\n"
            )
            continue

        # Skip already-formalized patterns
        if cluster.get("is_formalized", False):
            sys.stderr.write(
                f"  Skipping already-formalized: {cluster['label']}\n"
            )
            continue

        # Skip if covered by existing cron
        if cron_covers_cluster(crons, cluster):
            sys.stderr.write(
                f"  Skipping (existing cron covers it): {cluster['label']}\n"
            )
            continue

        # Skip if covered by existing skill
        if skill_covers_cluster(skills, cluster):
            sys.stderr.write(
                f"  Skipping (existing skill covers it): {cluster['label']}\n"
            )
            continue

        # Skip if already suggested
        suggestion_type = cluster.get("suggestion_type", "workflow")
        if is_duplicate_suggestion(state, cluster["label"], suggestion_type):
            sys.stderr.write(
                f"  Skipping duplicate suggestion: {cluster['label']}\n"
            )
            continue

        # Require minimum unique days for non-burst patterns
        min_required_days = config.get("min_unique_days", 2)
        if cluster["unique_days"] < min_required_days:
            sys.stderr.write(
                f"  Skipping (only {cluster['unique_days']} unique days): {cluster['label']}\n"
            )
            continue

        # Generate the suggestion
        generator = GENERATORS.get(suggestion_type)
        if generator is None:
            continue

        suggestion = generator(cluster)
        if suggestion is None:
            continue

        suggestions.append(suggestion)
        add_suggestion(state, suggestion)

        if len(suggestions) >= max_suggestions:
            break

    # Adjust min_confidence if we have very little data
    if total_days < min_days:
        sys.stderr.write(
            f"  Note: Only {total_days} days of data (min recommended: {min_days}). "
            f"Suggestions are provisional.\n"
        )
        for s in suggestions:
            s["provisional"] = True

    save_state(state, state_path)
    return suggestions


def main():
    parser = argparse.ArgumentParser(
        description="Generate suggestions from pattern clusters"
    )
    parser.add_argument(
        "--clusters",
        default=None,
        help="Path to clusters JSON file (default: read from stdin)"
    )
    parser.add_argument(
        "--state-file",
        default=None,
        help="Path to state.json"
    )
    parser.add_argument(
        "--cron-path",
        default=None,
        help="Path to cron jobs.json"
    )
    args = parser.parse_args()

    if args.clusters:
        with open(args.clusters) as f:
            clusters = json.load(f)
    else:
        clusters = json.load(sys.stdin)

    suggestions = generate_suggestions(clusters, args.state_file, args.cron_path)
    print(json.dumps(suggestions, indent=2))


if __name__ == "__main__":
    main()
