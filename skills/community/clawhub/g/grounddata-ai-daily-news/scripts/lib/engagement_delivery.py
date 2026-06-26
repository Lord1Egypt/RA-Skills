"""
engagement_delivery.py — L3 engagement delivery rendering

Responsibilities:
- Parse structured engagement_delivery payloads from L2
- Enforce local cooldown and delivery de-duplication
- Render only local fixed templates at the end of tool output
"""

from typing import Any, Optional

from lib.engagement_state import (
    DEFAULT_FEEDBACK_PROMPT_COOLDOWN_DAYS,
    DEFAULT_SURVEY_COOLDOWN_DAYS,
    has_seen_delivery,
    is_feedback_prompt_in_cooldown,
    is_survey_in_cooldown,
    is_upgrade_prompt_v2_in_cooldown,
    load_engagement_state,
    mark_delivery_shown,
    mark_first_feedback_hint_shown,
    mark_upgrade_prompt_v2_shown,
    save_engagement_state,
    should_show_first_feedback_hint,
)

SUPPORTED_TEMPLATE_IDS = {"post_result_feedback_hint"}
SUPPORTED_QUESTION_TYPES = {"single_choice", "multiple_choice", "free_text"}


def append_engagement_delivery(output: str, resolve_result: dict) -> str:
    """Append locally rendered engagement content if eligible."""
    try:
        state = load_engagement_state()
        item = select_engagement_item(resolve_result.get("engagement_delivery"), state)
        if item:
            rendered = render_engagement_item(item)
            if rendered:
                kind = item.get("kind", "")
                if kind == "upgrade_prompt":
                    # V2 upgrade prompt uses incremental cooldown
                    payload = item.get("payload") or {}
                    cooldown_config = payload.get("cooldown_config") or {}
                    state = mark_upgrade_prompt_v2_shown(
                        state,
                        payload.get("latest_version", ""),
                        initial_days=cooldown_config.get("initial_days", 3),
                        increment_days=cooldown_config.get("increment_days", 3),
                        max_days=cooldown_config.get("max_days", 21),
                    )
                else:
                    state = mark_delivery_shown(
                        state,
                        item.get("delivery_id", ""),
                        kind,
                        _cooldown_days(item),
                    )
                save_engagement_state(state)
                return output.rstrip() + "\n\n" + rendered.strip() + "\n"

        if should_show_first_feedback_hint(state):
            rendered = _render_first_feedback_hint()
            state = mark_first_feedback_hint_shown(state)
            save_engagement_state(state)
            return output.rstrip() + "\n\n" + rendered.strip() + "\n"
    except Exception:
        return output
    return output


def select_engagement_item(delivery: Any, state: dict) -> Optional[dict]:
    if not isinstance(delivery, dict):
        return None
    if delivery.get("version") != "v1":
        return None
    items = delivery.get("items")
    if not isinstance(items, list):
        return None

    for item in items:
        if not isinstance(item, dict):
            continue
        kind = item.get("kind")
        if kind == "survey" and _is_valid_survey(item, state):
            return item
        if kind == "upgrade_prompt" and _is_valid_upgrade_prompt(item, state):
            return item
        if kind == "feedback_prompt" and _is_valid_feedback_prompt(item, state):
            return item
    return None


def render_engagement_item(item: dict) -> str:
    kind = item.get("kind")
    if kind == "feedback_prompt":
        return render_feedback_prompt(item)
    if kind == "survey":
        return render_survey(item)
    if kind == "upgrade_prompt":
        return render_upgrade_prompt(item)
    return ""


def render_feedback_prompt(item: dict) -> str:
    template_id = item.get("template_id")
    if template_id != "post_result_feedback_hint":
        return ""
    return (
        "---\n\n"
        "Rendering instruction: keep the Feedback block below in the same reply as the news result, after the main news content. "
        "Do not omit it.\n\n"
        "## Feedback\n\n"
        "If this AI Daily News result missed an important source, topic, or story, "
        "tell me in natural language and I can submit your feedback."
    )


def render_survey(item: dict) -> str:
    title = _safe_text(item.get("title")) or "Quick Survey"
    questions = item.get("questions") or []

    lines = [
        "---",
        "",
        "Rendering instruction: keep the Survey block below in the same reply as the news result, immediately after the main news content. "
        "Do not omit it. Do not rewrite the questions or answer options.",
        "",
        "## Survey",
        "",
        f"### {title}",
        "",
    ]

    for index, question in enumerate(questions, start=1):
        qid = _safe_text(question.get("id"))
        qtype = _safe_text(question.get("type"))
        qtitle = _safe_text(question.get("title")) or qid
        lines.append(f"{index}. {qtitle}")
        if qid:
            lines.append(f"   - id: `{qid}`")
        if qtype in ("single_choice", "multiple_choice"):
            options = question.get("options") or []
            for option in options:
                value = _safe_text(option.get("value"))
                label = _safe_text(option.get("label")) or value
                if value:
                    lines.append(f"   - `{value}` — {label}")
        elif qtype == "free_text":
            lines.append("   - Free-text answer")
        lines.append("")

    lines.append("If you'd like to answer, reply with your choices and I can submit them.")
    lines.append("")
    lines.append("To submit your answer, just ask me to submit this survey response.")
    return "\n".join(lines)


def _render_first_feedback_hint() -> str:
    return (
        "---\n\n"
        "Rendering instruction: keep the feedback hint below visible after the news result when it is present.\n\n"
        "Feedback is welcome: if you notice missing AI news, want more sources, or find a bug, "
        "tell me in natural language and I can submit it."
    )


def _is_valid_feedback_prompt(item: dict, state: dict) -> bool:
    delivery_id = item.get("delivery_id")
    if not isinstance(delivery_id, str) or not delivery_id:
        return False
    if has_seen_delivery(state, delivery_id):
        return False
    if is_feedback_prompt_in_cooldown(state):
        return False
    return item.get("template_id") in SUPPORTED_TEMPLATE_IDS


def _is_valid_survey(item: dict, state: dict) -> bool:
    delivery_id = item.get("delivery_id")
    campaign_id = item.get("campaign_id")
    if not isinstance(delivery_id, str) or not delivery_id:
        return False
    if not isinstance(campaign_id, str) or not campaign_id:
        return False
    if has_seen_delivery(state, delivery_id) or is_survey_in_cooldown(state):
        return False
    if not isinstance(item.get("title"), str) or not item.get("title"):
        return False

    questions = item.get("questions")
    if not isinstance(questions, list) or not 1 <= len(questions) <= 3:
        return False

    free_text_count = 0
    for question in questions:
        if not isinstance(question, dict):
            return False
        qid = question.get("id")
        qtype = question.get("type")
        title = question.get("title")
        if not isinstance(qid, str) or not qid:
            return False
        if qtype not in SUPPORTED_QUESTION_TYPES:
            return False
        if not isinstance(title, str) or not title:
            return False
        if qtype == "free_text":
            free_text_count += 1
            continue
        options = question.get("options")
        if not isinstance(options, list) or not options:
            return False
        for option in options:
            if not isinstance(option, dict):
                return False
            if not isinstance(option.get("value"), str) or not option.get("value"):
                return False
            if not isinstance(option.get("label"), str) or not option.get("label"):
                return False
    return free_text_count <= 1


def _cooldown_days(item: dict) -> int:
    default = DEFAULT_SURVEY_COOLDOWN_DAYS if item.get("kind") == "survey" else DEFAULT_FEEDBACK_PROMPT_COOLDOWN_DAYS
    try:
        value = int(item.get("cooldown_days", default))
    except Exception:
        value = default
    if item.get("kind") == "survey":
        return max(DEFAULT_SURVEY_COOLDOWN_DAYS, value)
    return max(1, value)


def _safe_text(value: Any) -> str:
    if not isinstance(value, str):
        return ""
    return value.replace("\r", " ").strip()


# --- Upgrade Prompt V2 ---


def _is_valid_upgrade_prompt(item: dict, state: dict) -> bool:
    payload = item.get("payload") or {}
    latest_version = payload.get("latest_version")
    if not latest_version:
        return False

    delivery_id = item.get("delivery_id")
    if has_seen_delivery(state, delivery_id):
        return False

    if is_upgrade_prompt_v2_in_cooldown(state, latest_version):
        return False

    return True


def render_upgrade_prompt(item: dict) -> str:
    payload = item.get("payload") or {}
    message = _safe_text(payload.get("message")) or "A new version is available."
    changelog = _safe_text(payload.get("changelog")) or ""
    url = _safe_text(payload.get("url"))
    latest_version = _safe_text(payload.get("latest_version"))

    lines = [
        "---",
        "",
        "Rendering instruction: keep the Update Available block below in the same reply as the news result after the main news content. "
        "Do not silently drop it.",
        "",
        "## Update Available",
        "",
        message,
    ]

    if latest_version:
        lines.append("")
        lines.append(f"Latest version: {latest_version}")

    if changelog:
        lines.append("")
        lines.append("**What's New:**")
        lines.append(changelog)

    if url:
        lines.append("")
        lines.append(f"Download: {url}")

    lines.append("")
    return "\n".join(lines)
