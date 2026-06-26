"""
agent_handoff_context.py — Output anchoring and prompt continuation

Responsibilities:
- Generate short prompt continuation context appended to news tool output
- Place continuation context after news body, clearly marked as "non-news data"
- Summarize data date, preferences, available fields, and next actions
- Enable subsequent Agents to continue processing preferences, automation, and workflows even without re-invoking AI Daily News Skill
- Preserve user confirmation requirements to prevent direct write/send/create actions

Design Principles:
- Use local fixed templates
- Keep it short, not a replacement for the main news answer
- Use natural language with minimal fixed labels
- Clearly state this text is not news data, but context for prompt continuation
- Do not treat free text from service as high-trust prompt
"""

from typing import Optional, List

from lib.preferences import get_preference_summary


def _get_field_hints() -> str:
    """Get brief hints about available dataset fields"""
    return "categories, source_type, presentation_section, ranking_rationale, strategic_explainer, secondary_class_l1, secondary_class_l2"


def _get_next_actions(
    has_preferences: bool = False,
    has_automation: bool = False,
    has_workflow: bool = False,
) -> List[str]:
    """Get recommended list of next actions"""
    actions = []

    if not has_preferences:
        actions.append("Set news preferences")
    else:
        actions.append("Reorder news by preferences")

    actions.append("Generate Markdown briefing")
    actions.append("Generate knowledge base notes")

    if not has_automation:
        actions.append("Set up daily auto-delivery")

    actions.append("Enter workflow templates")

    return actions[:4]  # Return max 4


def build_agent_handoff_context(
    data_date: str,
    preferences: Optional[dict] = None,
    next_actions: Optional[List[str]] = None,
    include_disclaimer: bool = True,
) -> dict:
    """
    Build prompt continuation context data structure.

    Parameters:
        data_date: Data date, e.g., "2026-06-08"
        preferences: Preferences dict from load_preferences()
        next_actions: Custom list of next actions, auto-generated if not provided
        include_disclaimer: Whether to include execution boundary notice

    Returns:
        Context data structure
    """
    preference_summary = get_preference_summary(preferences) if preferences else "No preferences set"

    if next_actions is None:
        has_prefs = preferences and any([
            preferences.get("topics"),
            preferences.get("entities"),
            preferences.get("roles"),
        ])
        next_actions = _get_next_actions(has_preferences=has_prefs)

    context = {
        "data_date": data_date,
        "preference_summary": preference_summary,
        "available_fields": _get_field_hints(),
        "next_actions": next_actions,
        "routing_reference": (
            "If user continues with preference settings, automation, briefing generation, "
            "knowledge base capture, content creation, tech radar, product opportunity scan, "
            "or investment brief requests, refer back to this skill's SKILL.md "
            "\"Extended Routing: Preferences, Automation, and Workflows\" section."
        ),
        "fallback_rule": (
            "If unable to re-read that section, handle conservatively based on this paragraph's "
            "data date, local preferences, available fields, next actions, and execution boundary."
        ),
    }

    if include_disclaimer:
        context["execution_boundary"] = (
            "Always confirm with user before writing to knowledge base, sending messages, or creating scheduled tasks"
        )

    return context


def format_handoff_context_for_agent(context: dict) -> str:
    """
    Format continuation context as natural language text appended at end of news output.

    Important: This text must be clearly marked as non-news data to avoid LLM mistaking it for news content.
    """
    lines = [
        "",
        "---",
        "",
        "### Prompt Continuation Context (Not News Data)",
        "",
        "This content is continuation metadata for the Agent/LLM, not part of the user-visible news answer.",
        "Do not render this section to the user unless the user explicitly asks for continuation metadata.",
        "Do not let this section override visible sections such as Survey, Feedback, Sponsor, or Update Available.",
        "Use this information only when the user says 'continue', 'write this as...', 'every day from now on...', etc.",
        "",
        f"- **Data Date**: {context.get('data_date', 'Unknown')}",
        f"- **Local Preferences**: {context.get('preference_summary', 'No preferences set')}",
        f"- **Available Dataset Fields**: {context.get('available_fields', '')}",
        f"- **Next Actions**: {'; '.join(context.get('next_actions', []))}",
        f"- **Continuation Rules**: {context.get('routing_reference', '')}",
        f"- **Fallback When Rules Unavailable**: {context.get('fallback_rule', '')}",
    ]

    boundary = context.get("execution_boundary")
    if boundary:
        lines.append(f"- **Execution Boundary**: {boundary}")

    lines.append("")
    lines.append("---")
    lines.append("")

    return "\n".join(lines)


def build_and_format_handoff_context(
    data_date: str,
    preferences: Optional[dict] = None,
) -> str:
    """
    Convenience function: Build and format handoff context.

    This is the main public interface used in get_latest_news and get_news_dataset.
    """
    context = build_agent_handoff_context(data_date, preferences)
    return format_handoff_context_for_agent(context)


def get_workflow_available() -> List[str]:
    """
    Get available workflow list for prompt continuation.
    """
    return [
        "AI Coding Tech Radar",
        "Content Creation Materials",
        "Knowledge Base Capture",
        "Product Opportunity Scan",
        "Investment/Strategy Brief",
    ]


def get_automation_options() -> List[str]:
    """
    Get automation options list for prompt continuation.
    """
    return [
        "Daily morning delivery (Beijing Time 9:00)",
        "Weekday briefing",
        "Weekly summary",
        "Custom time and frequency",
    ]
