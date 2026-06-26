"""
preferences.py — L3 local news preference management

Responsibilities:
- Read/write preferences_state.json
- Write preferences from explicit parameters or structured patches extracted from natural language
- Format preference context for Agent use

Design Principles:
- Agent LLM is responsible for extracting preference patches from natural language
- L3 local tool validates, saves, reads, clears, and formats preference context
- L3 does not implement complex NLP or semantic classification logic
"""

import json
import os
import sys
from datetime import datetime, timezone
from typing import Optional, List

# Ensure lib directory is in path when run as standalone script
if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib.runtime_paths import get_preferences_state_path

TOPICS = [
    "agent", "ai_coding", "llm", "multimodal", "vision", "audio",
    "infrastructure", "chip", "hardware", "open_source", "product",
    "fundraising", "regulation", "research", "safety", "alignment",
]

ENTITIES = [
    "openai", "anthropic", "google", "meta", "microsoft", "nvidia",
    "hugging_face", "cursor", "jetbrains", "apple", "amazon",
]

SOURCE_TYPES = ["github", "news", "blog", "social", "research", "video"]

ROLES = ["engineer", "product", "founder", "investor", "researcher", "creator", "general"]

EXCLUDE_TOPICS = ["fundraising", "marketing", "announcement"]

OUTPUT_FORMATS = [
    "brief", "standard", "deep", "team_report", "markdown_brief", "markdown_briefing",
    "knowledge_note", "structured_summary",
]


_EMPTY_PREFERENCES = {
    "version": "v1",
    "updated_at_utc": None,
    "language": "zh-CN",
    "topics": [],
    "entities": [],
    "source_types": [],
    "roles": [],
    "exclude_topics": [],
    "exclude_entities": [],
    "depth": "standard",
    "output_format": "standard",
    "strict_filtering": False,
    "notes": "",
}


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _format_time(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _normalize_list(value, allowed: Optional[List[str]] = None) -> list:
    """
    Normalize a list of preference values.

    Supports removal syntax: "-topic" means remove "topic" from existing preferences.
    The "-" prefix is preserved for the update_preferences function to handle.
    """
    if not isinstance(value, list):
        return []
    result = []
    seen = set()
    for item in value:
        if not isinstance(item, str):
            continue
        item = item.strip().lower()
        if not item:
            continue
        if item in seen:
            continue

        # Handle removal syntax: "-topic" means remove "topic"
        is_removal = item.startswith("-")
        actual_value = item[1:] if is_removal else item

        # Validate against allowed list using the actual value (without "-")
        if allowed and actual_value not in allowed:
            continue

        seen.add(item)
        result.append(item)
    return result


def _normalize_preferences(raw) -> dict:
    pref = dict(_EMPTY_PREFERENCES)
    if not isinstance(raw, dict):
        return pref

    if raw.get("version") == "v1":
        pref["version"] = "v1"

    updated_at = raw.get("updated_at_utc")
    if isinstance(updated_at, str):
        pref["updated_at_utc"] = updated_at

    language = raw.get("language")
    if isinstance(language, str) and language in ("zh-CN", "en"):
        pref["language"] = language

    pref["topics"] = _normalize_list(raw.get("topics"), TOPICS)
    pref["entities"] = _normalize_list(raw.get("entities"), ENTITIES)
    pref["source_types"] = _normalize_list(raw.get("source_types"), SOURCE_TYPES)
    pref["roles"] = _normalize_list(raw.get("roles"), ROLES)
    pref["exclude_topics"] = _normalize_list(raw.get("exclude_topics"), EXCLUDE_TOPICS)
    pref["exclude_entities"] = _normalize_list(raw.get("exclude_entities"), ENTITIES)

    depth = raw.get("depth")
    if isinstance(depth, str) and depth in ("brief", "standard", "deep"):
        pref["depth"] = depth

    output_format = raw.get("output_format")
    if isinstance(output_format, str) and output_format in OUTPUT_FORMATS:
        # Normalize: markdown_brief -> markdown_briefing for consistency with docs
        if output_format == "markdown_brief":
            output_format = "markdown_briefing"
        pref["output_format"] = output_format

    strict_filtering = raw.get("strict_filtering")
    if isinstance(strict_filtering, bool):
        pref["strict_filtering"] = strict_filtering

    notes = raw.get("notes")
    if isinstance(notes, str):
        pref["notes"] = notes

    return pref


def load_preferences() -> dict:
    path = get_preferences_state_path()
    if not path.exists():
        pref = _normalize_preferences({})
        save_preferences(pref)
        return pref
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        raw = {}
    pref = _normalize_preferences(raw)
    return pref


def save_preferences(preferences: dict) -> None:
    path = get_preferences_state_path()
    normalized = _normalize_preferences(preferences)
    normalized["updated_at_utc"] = _format_time(_utc_now())
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    tmp_path.write_text(
        json.dumps(normalized, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    tmp_path.replace(path)


def has_preferences_set(preferences: dict) -> bool:
    """Check if user has set any meaningful preferences"""
    return any([
        preferences.get("topics"),
        preferences.get("entities"),
        preferences.get("roles"),
        preferences.get("exclude_topics"),
        preferences.get("source_types"),
        preferences.get("depth") != "standard",
        preferences.get("output_format") != "standard",
        preferences.get("strict_filtering"),
    ])


def update_preferences(patch: dict) -> dict:
    """Update preferences, merge instead of overwrite"""
    pref = load_preferences()

    # Merge list fields (deduplicate)
    list_fields = [
        "topics", "entities", "source_types", "roles",
        "exclude_topics", "exclude_entities",
    ]
    for field in list_fields:
        if field in patch:
            existing = set(pref.get(field, []))
            new_items = _normalize_list(patch[field])
            # If value in patch starts with -, it means remove
            to_remove = set()
            to_add = []
            for item in new_items:
                if item.startswith("-"):
                    to_remove.add(item[1:])
                else:
                    to_add.append(item)
            merged = [x for x in existing if x not in to_remove]
            for item in to_add:
                if item not in merged:
                    merged.append(item)
            pref[field] = merged

    # Update scalar fields directly
    scalar_fields = ["language", "depth", "output_format", "strict_filtering", "notes"]
    for field in scalar_fields:
        if field in patch:
            pref[field] = patch[field]

    save_preferences(pref)
    return pref


def clear_preferences() -> dict:
    """Clear all preferences and reset to default state"""
    pref = _normalize_preferences({})
    save_preferences(pref)
    return pref


def format_preferences_for_agent(preferences: dict) -> str:
    """
    Format preference context for Agent use.

    Explicitly tells the model:
    1. Preferences only affect presentation, not data truth
    2. Can use dataset fields to determine relevance
    3. When preferences are set, reorganize by preference first; matching Top News ranks higher
    4. Only strictly filter if strict_filtering=True or user explicitly requests it
    """
    lines = [
        "## Local User Preferences",
        "",
        "These preferences are stored locally and should only guide presentation, filtering, and summarization.",
        "When preferences are set, reorganize by user preference first; matching Top News should rank higher among relevant items.",
        "Non-matching Top News can move lower or be placed in a short 'other important AI news' section.",
        "Do not fully remove important Top News unless strict_filtering is true or the user explicitly asks for strict filtering.",
        "When applying preferences, use dataset fields such as: title_normalized, summary_normalized, categories, source_type, presentation_section, presentation_group, ranking_rationale, strategic_explainer, secondary_class_l1, secondary_class_l2.",
        "",
    ]

    def _format_list(name: str, items: list) -> str:
        if not items:
            return f"- {name}: (not set)"
        return f"- {name}: {', '.join(items)}"

    lines.append(_format_list("Preferred Topics", preferences.get("topics", [])))
    lines.append(_format_list("Preferred Entities", preferences.get("entities", [])))
    lines.append(_format_list("Preferred Source Types", preferences.get("source_types", [])))
    lines.append(_format_list("User Role Perspective", preferences.get("roles", [])))
    lines.append(_format_list("Exclude Topics", preferences.get("exclude_topics", [])))
    lines.append(_format_list("Exclude Entities", preferences.get("exclude_entities", [])))
    lines.append(f"- Preferred Depth: {preferences.get('depth', 'standard')}")
    lines.append(f"- Output Format: {preferences.get('output_format', 'standard')}")
    lines.append(f"- Language: {preferences.get('language', 'zh-CN')}")
    lines.append(f"- Strict Filtering: {preferences.get('strict_filtering', False)}")

    notes = preferences.get("notes")
    if notes:
        lines.append(f"- Additional Notes: {notes}")

    lines.append("")
    lines.append("### Preference Application Rules")
    lines.append("1. When preferences are set, rank and group news by user preference first.")
    lines.append("2. Prioritize Top News only when it matches user preferences; non-matching Top News may move lower or appear in a short 'other important AI news' section.")
    lines.append("3. Do not completely remove important Top News items unless strict_filtering is true.")
    lines.append("4. Use categories and secondary_class_* fields for topic matching.")
    lines.append("5. Use title_normalized and summary_normalized for entity matching.")
    lines.append("6. Use ranking_rationale and strategic_explainer to explain relevance to the user's interests.")

    return "\n".join(lines)


def get_preference_summary(preferences: dict) -> str:
    """
    Get brief preference summary for handoff context.

    Returns something like: "Agent, AI Coding; Less fundraising; Engineer perspective brief summary"
    """
    parts = []

    topics = preferences.get("topics", [])
    if topics:
        topic_labels = {
            "agent": "Agent",
            "ai_coding": "AI Coding",
            "llm": "LLM",
            "multimodal": "Multimodal",
            "open_source": "Open Source",
            "product": "Product",
            "research": "Research",
            "infrastructure": "Infrastructure",
            "chip": "Chip",
        }
        display_topics = [topic_labels.get(t, t) for t in topics[:3]]
        parts.append(", ".join(display_topics))

    exclude = preferences.get("exclude_topics", [])
    if exclude:
        exclude_labels = {"fundraising": "Fundraising", "marketing": "Marketing"}
        display_exclude = [exclude_labels.get(e, e) for e in exclude[:2]]
        parts.append("Less: " + ", ".join(display_exclude))

    depth = preferences.get("depth", "standard")
    roles = preferences.get("roles", [])
    if depth != "standard" or roles:
        format_desc = []
        if roles:
            format_desc.append(roles[0].capitalize() + " perspective")
        if depth == "brief":
            format_desc.append("brief summary")
        elif depth == "deep":
            format_desc.append("deep analysis")
        if format_desc:
            parts.append(", ".join(format_desc))

    if not parts:
        return "No preferences set"

    return "; ".join(parts)


# ===== CLI Interface (for Skill invocation) =====

def _print_json(data: dict) -> None:
    """Print JSON output for agent parsing"""
    import json
    print(json.dumps(data, ensure_ascii=False, indent=2))


def cli_show() -> None:
    """Show current preferences"""
    prefs = load_preferences()
    _print_json({
        "status": "success",
        "action": "show",
        "preferences": prefs,
        "summary": get_preference_summary(prefs),
        "preferences_set": has_preferences_set(prefs),
    })


def cli_update(patch_json: str) -> None:
    """Update preferences with a JSON patch"""
    import json
    try:
        patch = json.loads(patch_json)
    except json.JSONDecodeError as e:
        _print_json({
            "status": "error",
            "action": "update",
            "error": f"Invalid JSON: {e}",
        })
        return

    prefs = update_preferences(patch)
    _print_json({
        "status": "success",
        "action": "update",
        "preferences": prefs,
        "summary": get_preference_summary(prefs),
        "message": "Preferences saved locally",
    })


def cli_clear() -> None:
    """Clear all preferences"""
    prefs = clear_preferences()
    _print_json({
        "status": "success",
        "action": "clear",
        "preferences": prefs,
        "summary": get_preference_summary(prefs),
        "message": "All preferences cleared",
    })


def cli_format() -> None:
    """Format preferences for agent context"""
    prefs = load_preferences()
    print(format_preferences_for_agent(prefs))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Local News Preference Manager")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # show
    subparsers.add_parser("show", help="Show current preferences")

    # update
    update_parser = subparsers.add_parser("update", help="Update preferences")
    update_parser.add_argument("--patch", required=True, help="JSON patch object")

    # clear
    subparsers.add_parser("clear", help="Clear all preferences")

    # format
    subparsers.add_parser("format", help="Format preferences for agent context")

    args = parser.parse_args()

    if args.command == "show":
        cli_show()
    elif args.command == "update":
        cli_update(args.patch)
    elif args.command == "clear":
        cli_clear()
    elif args.command == "format":
        cli_format()
    else:
        parser.print_help()
