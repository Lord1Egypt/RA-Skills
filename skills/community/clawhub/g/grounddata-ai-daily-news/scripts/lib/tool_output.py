"""
tool_output.py — Tool output formatting

Responsibilities:
- Format dataset structure into LLM-readable Markdown
- Keep thin: rely on _data_dictionary for field explanations, don't hardcode too much
- Preserve full record data so LLM can use source-specific extension fields
"""

import json
from typing import Dict, Any, List, Optional, Tuple

from lib.engagement_delivery import load_engagement_state, render_engagement_item, select_engagement_item


def _format_scalar(value) -> str:
    """Format scalar values for markdown output."""
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, str):
        return value
    return json.dumps(value, ensure_ascii=False)


def _flatten_markdown_fields(value, prefix: str = "") -> List[Tuple[str, Any]]:
    """
    Flatten nested dict/list data into dotted markdown field paths.

    Examples:
    - {"a": {"b": 1}} -> [("a.b", "1")]
    - {"tags": ["x", "y"]} -> [("tags", "[\"x\", \"y\"]")]
    """
    if isinstance(value, dict):
        rows = []
        for key, nested_value in value.items():
            key_str = str(key)
            next_prefix = f"{prefix}.{key_str}" if prefix else key_str
            rows.extend(_flatten_markdown_fields(nested_value, next_prefix))
        if not rows and prefix:
            rows.append((prefix, "{}"))
        return rows

    if isinstance(value, list):
        if not prefix:
            return [("value", json.dumps(value, ensure_ascii=False))]

        simple_list = all(not isinstance(item, (dict, list)) for item in value)
        if simple_list:
            return [(prefix, json.dumps(value, ensure_ascii=False))]

        rows = []
        for idx, item in enumerate(value):
            next_prefix = f"{prefix}[{idx}]"
            rows.extend(_flatten_markdown_fields(item, next_prefix))
        if not rows:
            rows.append((prefix, "[]"))
        return rows

    if not prefix:
        return [("value", _format_scalar(value))]
    return [(prefix, _format_scalar(value))]


def _render_record_with_priority(record: Dict[str, Any]) -> List[str]:
    """
    Render a record with priority fields first (for Top News).

    Priority order:
    - presentation_group_label
    - top_news_position
    - title_normalized
    - categories
    - secondary_class_l1
    - secondary_class_l2
    - strategic_explainer
    - ranking_rationale
    - ... rest of the fields
    """
    # Define priority order
    priority_fields = [
        "presentation_group_label",
        "top_news_position",
        "title_normalized",
        "categories",
        "secondary_class_l1",
        "secondary_class_l2",
        "strategic_explainer",
        "ranking_rationale",
    ]

    # Get all flattened fields
    all_fields = dict(_flatten_markdown_fields(record))

    lines = []

    # Render priority fields first (if present)
    for field in priority_fields:
        if field in all_fields:
            value = all_fields.pop(field)
            lines.append(f"- {field}: {_format_scalar(value)}")

    # Render remaining fields sorted
    for field, value in sorted(all_fields.items()):
        lines.append(f"- {field}: {_format_scalar(value)}")

    return lines


def _group_records_by_section_and_group(records: List[Dict[str, Any]]) -> Dict[str, Dict[str, List[Dict[str, Any]]]]:
    """Group records by presentation_section and presentation_group."""
    result: Dict[str, Dict[str, List[Dict[str, Any]]]] = {}

    for record in records:
        section = record.get("presentation_section")
        group = record.get("presentation_group", "unknown")

        if section not in result:
            result[section] = {}
        if group not in result[section]:
            result[section][group] = []

        result[section][group].append(record)

    return result


def _has_presentation_fields(records: List[Dict[str, Any]]) -> bool:
    """Check if records have presentation fields (for backward compatibility)."""
    if not records:
        return False
    first_record = records[0]
    return "presentation_section" in first_record


def _render_section(
    section_name: str,
    section_label: str,
    groups: Dict[str, List[Dict[str, Any]]],
    presentation_groups: List[Dict[str, Any]] = None,
    use_priority_order: bool = False,
) -> List[str]:
    """Render a section with its groups and records.
    Group display is driven by _meta.presentation.groups if available.
    """
    lines = [f"## {section_label}"]
    lines.append("")

    # Build group meta lookup for quick access
    group_meta_map = {}
    if presentation_groups:
        for gm in presentation_groups:
            group_name = gm.get("name")
            if group_name:
                group_meta_map[group_name] = gm

    # Sort groups: first try using meta order, then fallback to record fields
    def get_group_order(group_name: str, group_records: List[Dict[str, Any]]) -> int:
        # First try from presentation.groups
        if group_name in group_meta_map:
            return group_meta_map[group_name].get("order", 999)
        # Fallback to record fields
        if group_records:
            return group_records[0].get("presentation_group_order", 999)
        return 999

    sorted_groups = sorted(groups.items(), key=lambda g: get_group_order(g[0], g[1]))

    for group_name, group_records in sorted_groups:
        if not group_records:
            continue

        # Get group label: first try from presentation.groups, then fallback to record
        group_label = group_name
        group_description = None

        if group_name in group_meta_map:
            group_label = group_meta_map[group_name].get("label", group_name)
            group_description = group_meta_map[group_name].get("description")
        else:
            if group_records:
                group_label = group_records[0].get("presentation_group_label", group_name)

        if len(sorted_groups) > 1:
            lines.append(f"### {group_label}")
            if group_description:
                lines.append(f"_{group_description}_")
            lines.append("")

        # Sort records within group by presentation_item_order
        def get_item_order(record: Dict[str, Any]) -> int:
            return record.get("presentation_item_order", 999)

        sorted_records = sorted(group_records, key=get_item_order)

        for idx, record in enumerate(sorted_records, 1):
            if len(sorted_groups) > 1:
                lines.append(f"#### Item {idx}")
            else:
                lines.append(f"#### Record {idx}")
            lines.append("")

            if use_priority_order:
                lines.extend(_render_record_with_priority(record))
            else:
                for field, value in _flatten_markdown_fields(record):
                    lines.append(f"- {field}: {_format_scalar(value)}")

            lines.append("")

    return lines


def _render_full_dataset_markdown(data: dict) -> list[str]:
    """Render the full dataset as schema-preserving markdown."""
    lines = [
        "## Full Dataset Markdown",
        "",
        "This section preserves the full dataset content in markdown field form.",
        "",
    ]

    sections = [
        ("Dataset Meta", data.get("_meta", {})),
        ("Data Dictionary", data.get("_data_dictionary", {})),
        ("Ads", data.get("_ads", {})),
    ]

    for heading, section_value in sections:
        lines.append(f"### {heading}")
        lines.append("")
        for field_path, field_value in _flatten_markdown_fields(section_value):
            lines.append(f"- {field_path}: {_format_scalar(field_value)}")
        lines.append("")

    records = data.get("data", [])
    lines.append("### Records")
    lines.append("")
    for idx, record in enumerate(records, 1):
        lines.append(f"#### Record {idx}")
        lines.append("")
        for field_path, field_value in _flatten_markdown_fields(record):
            lines.append(f"- {field_path}: {_format_scalar(field_value)}")
        lines.append("")

    return lines


def _render_dataset_content_new(data: dict) -> list[str]:
    """Render the shared dataset body using new section-based format."""
    meta = data.get("_meta", {})
    records = data.get("data", [])

    lines = []
    lines.append(f"- Source: {meta.get('source', meta.get('dataset_name', 'news_dataset'))}")
    lines.append(f"- Schema: {meta.get('schema_version', 'v1')}")
    lines.append(f"- Language: {meta.get('normalization_language', 'en')}")
    lines.append(f"- Records: {len(records)}")
    generated_at = meta.get("generated_at")
    if generated_at:
        lines.append(f"- Generated At: {generated_at}")
    lines.append("")

    if not _has_presentation_fields(records):
        # Fallback to old format
        lines.extend(_render_full_dataset_markdown(data))
        return lines

    # Group records by section and group
    grouped = _group_records_by_section_and_group(records)

    # Get presentation metadata if available
    presentation = meta.get("presentation", {})

    # Determine section order from meta, or fallback to hardcoded
    section_order = presentation.get("section_order", ["top_news", "source_updates", "remaining_news"])

    # Build section label map from meta, or fallback to hardcoded
    section_label_map = {}
    sections_meta = presentation.get("sections", [])
    for section_meta in sections_meta:
        section_name = section_meta.get("name")
        if section_name:
            section_label_map[section_name] = section_meta.get("label", section_name)

    # Fallback labels for compatibility
    fallback_section_labels = {
        "top_news": "Top News",
        "source_updates": "Source Updates",
        "remaining_news": "Remaining News",
    }

    # Get groups meta for rendering
    presentation_groups = presentation.get("groups", [])

    # Render sections in order
    for section in section_order:
        if section in grouped:
            # Use label from meta if available, otherwise fallback
            section_label = section_label_map.get(section, fallback_section_labels.get(section, section))
            lines.extend(_render_section(
                section,
                section_label,
                grouped[section],
                presentation_groups=presentation_groups,
                use_priority_order=(section == "top_news"),
            ))

    # Render meta, data dictionary, ads
    lines.append("---")
    lines.append("")
    lines.append("## Metadata & Dictionary")
    lines.append("")
    lines.append("### Dataset Meta")
    lines.append("")
    for field_path, field_value in _flatten_markdown_fields(meta):
        lines.append(f"- {field_path}: {_format_scalar(field_value)}")
    lines.append("")

    lines.append("### Data Dictionary")
    lines.append("")
    data_dict = data.get("_data_dictionary", {})
    for field_path, field_value in _flatten_markdown_fields(data_dict):
        lines.append(f"- {field_path}: {_format_scalar(field_value)}")
    lines.append("")

    return lines


def _render_dataset_content(data: dict) -> list[str]:
    """Render the shared dataset body (for backward compatibility)."""
    return _render_dataset_content_new(data)


def _render_engagement_section(result: dict) -> List[str]:
    """Render the selected engagement section for automation-safe markdown."""
    state = load_engagement_state()
    item = select_engagement_item(result.get("engagement_delivery"), state)
    if not item:
        return []

    rendered = render_engagement_item(item)
    if not rendered:
        return []

    return [rendered, ""]


def format_dataset(data: dict, date: str, tier: str) -> str:
    """
    Format news_dataset.v1 into Markdown output.

    Parameters:
        data: Full dataset JSON (contains _meta, _data_dictionary, _ads, data)
        date: Date string
        tier: Tier name

    Returns:
        Markdown string
    """
    lines = []
    lines.append(f"# AI Daily News — {date} ({tier})")
    lines.append("")
    lines.extend(_render_dataset_content(data))

    return "\n".join(lines)


def format_error(error_msg: str) -> str:
    """Format error output"""
    return f"Error: {error_msg}"


def format_latest_dataset(result: dict, tier: str) -> str:
    """
    Format the wrapped latest dataset response.

    Parameters:
        result: The wrapped response from L2 (contains dataset_ref, resolved_date,
                freshness_status, days_behind, notice_for_user, data)
        tier: Tier name

    Returns:
        Markdown string with freshness metadata and dataset content
    """
    dataset_ref = result.get("dataset_ref", "latest")
    resolved_date = result.get("resolved_date", "")
    freshness_status = result.get("freshness_status", "")
    days_behind = result.get("days_behind", 0)
    notice_for_user = result.get("notice_for_user", "")
    data = result.get("data", {})

    # Check for local time enhancement
    display_notice = result.get("display_notice")
    generated_at_local = result.get("generated_at_local")
    client_timezone = result.get("client_timezone")
    resolved_source_date = result.get("resolved_source_date", resolved_date)
    display_mode = result.get("display_mode")

    # First, format the freshness metadata section (IMPORTANT: LLM must see this first)
    lines = []
    lines.append(f"# AI Daily News — Latest Available ({tier})")
    lines.append("")

    if display_mode == "local_time" and display_notice:
        # Prefer local time display for enhanced responses
        lines.append("## Freshness Information (Local Time)")
        lines.append("")
        lines.append(f"- **Notice**: {display_notice}")
        if generated_at_local:
            lines.append(f"- **Generated At (Local)**: {generated_at_local}")
        if client_timezone:
            lines.append(f"- **Your Timezone**: {client_timezone}")
        lines.append(f"- **Resolved Canonical Date**: {resolved_source_date}")
        lines.append("")
    else:
        # Legacy display mode
        lines.append("## Freshness Information")
        lines.append("")
        lines.append(f"- **Resolved Date**: {resolved_date}")
        lines.append(f"- **Freshness Status**: {freshness_status}")
        lines.append(f"- **Days Behind**: {days_behind}")
        lines.append(f"- **Notice**: {notice_for_user}")
        lines.append(f"- **Dataset Ref**: {dataset_ref}")
        lines.append("")

    lines.extend(_render_dataset_content(data))

    return "\n".join(lines)


def format_resolved_date_dataset(result: dict, tier: str) -> str:
    """
    Format the wrapped local date resolved dataset response.

    Parameters:
        result: The wrapped response from L2 (contains requested_local_date,
                resolved_source_date, display_notice, data)
        tier: Tier name

    Returns:
        Markdown string with local date metadata and dataset content
    """
    requested_local_date = result.get("requested_local_date", "")
    resolved_source_date = result.get("resolved_source_date", "")
    client_timezone = result.get("client_timezone", "")
    generated_at_local = result.get("generated_at_local", "")
    display_notice = result.get("display_notice", "")
    data = result.get("data", {})

    lines = []
    lines.append(f"# AI Daily News — {requested_local_date} (Local Time, {tier})")
    lines.append("")
    lines.append("## Date Resolution Information")
    lines.append("")
    lines.append(f"- **Notice**: {display_notice}")
    lines.append(f"- **Requested Local Date**: {requested_local_date}")
    lines.append(f"- **Your Timezone**: {client_timezone}")
    lines.append(f"- **Resolved Canonical Date**: {resolved_source_date}")
    if generated_at_local:
        lines.append(f"- **Generated At (Local)**: {generated_at_local}")
    lines.append("")

    lines.extend(_render_dataset_content(data))

    return "\n".join(lines)


def _safe_str(value: Any) -> str:
    if not isinstance(value, str):
        return ""
    return value.replace("\r", " ").strip()


def _render_automation_preferences(preferences: Optional[dict], summary: str = "") -> List[str]:
    if not isinstance(preferences, dict):
        return [
            "- Preference Summary: No preferences set",
            "- Preferences Set: false",
        ]

    def _format_list(name: str, items: Any) -> str:
        if not isinstance(items, list) or not items:
            return f"- {name}: (not set)"
        normalized = [str(item) for item in items]
        return f"- {name}: {', '.join(normalized)}"

    lines = [
        f"- Preference Summary: {summary or 'No preferences set'}",
        _format_list("Preferred Topics", preferences.get("topics")),
        _format_list("Preferred Entities", preferences.get("entities")),
        _format_list("Preferred Source Types", preferences.get("source_types")),
        _format_list("User Role Perspective", preferences.get("roles")),
        _format_list("Exclude Topics", preferences.get("exclude_topics")),
        _format_list("Exclude Entities", preferences.get("exclude_entities")),
        f"- Preferred Depth: {preferences.get('depth', 'standard')}",
        f"- Output Format: {preferences.get('output_format', 'standard')}",
        f"- Language: {preferences.get('language', 'zh-CN')}",
        f"- Strict Filtering: {bool(preferences.get('strict_filtering', False))}",
    ]

    notes = _safe_str(preferences.get("notes"))
    if notes:
        lines.append(f"- Additional Notes: {notes}")

    return lines


def _extract_notice_lines(result: dict) -> Tuple[List[str], List[str]]:
    sponsor_lines: List[str] = []
    update_lines: List[str] = []

    delivery = result.get("notice_delivery")
    if not isinstance(delivery, dict):
        return sponsor_lines, update_lines

    items = delivery.get("items")
    if not isinstance(items, list):
        return sponsor_lines, update_lines

    for item in items:
        if not isinstance(item, dict):
            continue

        kind = item.get("kind")
        payload = item.get("payload")
        if not isinstance(payload, dict):
            payload = {}

        url = _safe_str(payload.get("url"))

        if kind == "sponsor_notice":
            brand = _safe_str(payload.get("brand"))
            message = _safe_str(payload.get("message"))
            text = brand or message
            if not text:
                continue
            if url:
                sponsor_lines.append(f"- {text} ({url})")
            else:
                sponsor_lines.append(f"- {text}")
            continue

        if kind == "upgrade_notice":
            message = _safe_str(payload.get("message")) or "Update available."
            min_version = _safe_str(payload.get("min_version_to_hide"))
            suffix = f" (min_version_to_hide: {min_version})" if min_version else ""
            if url:
                update_lines.append(f"- {message}{suffix} ({url})")
            else:
                update_lines.append(f"- {message}{suffix}")

    return sponsor_lines, update_lines


def format_context_only_dataset(
    result: dict,
    tier: str,
    query_type: str,
    preferences: Optional[dict] = None,
    preference_summary: str = "",
) -> str:
    """
    Format context-only markdown for loading news data into conversation context only.

    This mode is intended for isolated session continuation scenarios where the user
    wants to ask follow-up questions about previously delivered scheduled news,
    but does NOT want the news to be rendered again as a user-facing response.

    Output includes:
    - Freshness/date resolution metadata
    - Full dataset content (for LLM context)
    - Local user preferences
    - Data dictionary
    - Agent handoff context

    Output EXCLUDES:
    - Engagement content (survey, feedback prompts)
    - Growth tips / onboarding suggestions
    - Notice delivery (upgrade, sponsor)
    - Sponsor ads
    - Rendering instructions
    """
    data = result.get("data", {})
    lines: List[str] = [
        "# AI Daily News - Context Only (Do NOT Render to User)",
        "",
        "IMPORTANT: This is context data for the Agent/LLM only. Do NOT render this content to the user.",
        "This data is loaded to provide context for follow-up questions about news delivered earlier.",
        f"- Query Type: {query_type}",
        f"- Tier: {tier}",
        "",
    ]

    if query_type == "latest":
        lines.append("## Freshness Information (Context Only)")
        lines.append("")
        lines.append(f"- Notice: {result.get('display_notice', result.get('notice_for_user', ''))}")
        lines.append(f"- Generated At (Local): {result.get('generated_at_local', '')}")
        lines.append(f"- Your Timezone: {result.get('client_timezone', '')}")
        lines.append(f"- Resolved Canonical Date: {result.get('resolved_source_date', result.get('resolved_date', ''))}")
    else:
        lines.append("## Date Resolution Information (Context Only)")
        lines.append("")
        lines.append(f"- Notice: {result.get('display_notice', '')}")
        lines.append(f"- Requested Local Date: {result.get('requested_local_date', '')}")
        lines.append(f"- Your Timezone: {result.get('client_timezone', '')}")
        lines.append(f"- Generated At (Local): {result.get('generated_at_local', '')}")
        lines.append(f"- Resolved Canonical Date: {result.get('resolved_source_date', '')}")

    lines.append("")
    lines.append("## Local User Preferences (Context Only)")
    lines.append("")
    lines.extend(_render_automation_preferences(preferences, preference_summary))
    lines.append("")

    lines.append("## Dataset Content (Context Only)")
    lines.append("")
    lines.extend(_render_dataset_content(data))
    lines.append("")

    lines.append("## Data Dictionary (Context Only)")
    lines.append("")
    lines.extend(_render_data_dictionary(data))
    lines.append("")

    lines.append("## Agent Handoff Instructions (Context Only)")
    lines.append("")
    lines.append("The user may ask follow-up questions about this news data.")
    lines.append("Use the dataset content above to answer their questions.")
    lines.append("Do NOT mention that you 'loaded context' - simply answer based on the news data.")
    lines.append("Available workflows: AI Coding Tech Radar, Content Creation Materials, Knowledge Base Capture, Product Opportunity Scan, Investment/Strategy Brief")
    lines.append("")
    lines.append("---")
    lines.append("")

    return "\n".join(lines)


def _render_dataset_ads(data: dict) -> List[str]:
    ads = data.get("_ads")
    if not isinstance(ads, dict) or not ads:
        return ["- None"]
    lines: List[str] = []
    for field_path, field_value in _flatten_markdown_fields(ads):
        lines.append(f"- {field_path}: {_format_scalar(field_value)}")
    return lines


def format_automation_safe_dataset(
    result: dict,
    tier: str,
    query_type: str,
    preferences: Optional[dict] = None,
    preference_summary: str = "",
) -> str:
    """
    Format automation-safe markdown for scheduled task generation.

    Output keeps news content, preferences, sponsor/update notices, and data dictionary
    while omitting interactive-only guidance from caller scripts.
    """
    data = result.get("data", {})
    lines: List[str] = [
        "# AI Daily News Automation Input",
        "",
        "This markdown is intended for scheduled-task rendering and delivery.",
        f"- Query Type: {query_type}",
        f"- Tier: {tier}",
        "",
    ]

    if query_type == "latest":
        lines.append("## Freshness Information")
        lines.append("")
        lines.append(f"- Notice: {result.get('display_notice', result.get('notice_for_user', ''))}")
        lines.append(f"- Generated At (Local): {result.get('generated_at_local', '')}")
        lines.append(f"- Your Timezone: {result.get('client_timezone', '')}")
        lines.append(f"- Resolved Canonical Date: {result.get('resolved_source_date', result.get('resolved_date', ''))}")
    else:
        lines.append("## Date Resolution Information")
        lines.append("")
        lines.append(f"- Notice: {result.get('display_notice', '')}")
        lines.append(f"- Requested Local Date: {result.get('requested_local_date', '')}")
        lines.append(f"- Your Timezone: {result.get('client_timezone', '')}")
        lines.append(f"- Generated At (Local): {result.get('generated_at_local', '')}")
        lines.append(f"- Resolved Canonical Date: {result.get('resolved_source_date', '')}")

    lines.extend(_render_engagement_section(result))

    lines.append("## Local User Preferences")
    lines.append("")
    lines.extend(_render_automation_preferences(preferences, preference_summary))
    lines.append("")

    lines.append("## Dataset Content")
    lines.append("")
    lines.extend(_render_dataset_content(data))
    lines.append("")

    lines.append("## Sponsor Data")
    lines.append("")
    lines.extend(_render_dataset_ads(data))
    lines.append("")

    sponsor_lines, update_lines = _extract_notice_lines(result)
    
    lines.append("---")
    lines.append("")
    lines.append("## 💡 Have follow-up questions?")
    lines.append("")
    lines.append("If you want to ask questions about this news later (e.g., \"Tell me more about the Gemini updates\"):")
    lines.append("")
    lines.append("**Step 1:** In your new conversation, run this command first:")
    lines.append("```")
    lines.append("ai-daily-news: get latest news context only")
    lines.append("```")
    lines.append("")
    lines.append("**Step 2:** Then ask your question — I'll be able to answer based on today's news!")
    lines.append("")
    lines.append("*This loads the news data without re-displaying the entire briefing.*")
    lines.append("")
    lines.append("---")

    lines.append("## Sponsor Information")
    lines.append("")
    lines.append("Rendering instruction: if sponsor information is present below, keep it visible in the same final reply as the news result.")
    lines.append("")
    lines.extend(sponsor_lines or ["- None"])
    lines.append("")

    lines.append("## Update Available")
    lines.append("")
    lines.append("Rendering instruction: if an update notice is present below, include it in the same final reply after the news content.")
    lines.append("")
    lines.extend(update_lines or ["- None"])
    lines.append("")

    return "\n".join(lines)
