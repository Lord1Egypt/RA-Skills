"""
Nex Ghostwriter - Email template engine
Copyright 2026 Nex AI (Kevin Blancaflor)
"""
import json
import datetime as dt

SUBSEPARATOR = "-" * 40


def generate_subject(meeting_title, client_name=None):
    if client_name:
        return f"Follow-up: {meeting_title} - {client_name}"
    return f"Follow-up: {meeting_title}"


def _format_action_items(action_items_raw):
    if not action_items_raw:
        return ""

    items = []
    try:
        parsed = json.loads(action_items_raw)
        if isinstance(parsed, list):
            items = parsed
    except (json.JSONDecodeError, TypeError):
        items = [i.strip() for i in action_items_raw.split(',') if i.strip()]

    if not items:
        return ""

    lines = []
    for i, item in enumerate(items, 1):
        if isinstance(item, dict):
            owner = item.get('owner', '')
            task = item.get('task', str(item))
            deadline = item.get('deadline', '')
            line = f"   {i}. {task}"
            if owner:
                line += f" ({owner})"
            if deadline:
                line += f" - due {deadline}"
            lines.append(line)
        else:
            lines.append(f"   {i}. {item}")

    return "\n".join(lines)


def _greeting(client_name=None, preferred_greeting=None, tone="professional"):
    if preferred_greeting:
        return preferred_greeting

    if not client_name:
        if tone in ("casual", "friendly"):
            return "Hey,"
        return "Hi,"

    first_name = client_name.split()[0] if client_name else ""

    if tone == "formal":
        return f"Dear {client_name},"
    elif tone == "casual":
        return f"Hey {first_name},"
    elif tone == "friendly":
        return f"Hi {first_name},"
    else:
        return f"Hi {first_name},"


def _closing(tone="professional"):
    if tone == "formal":
        return "Kind regards,"
    elif tone == "casual":
        return "Cheers,"
    elif tone == "friendly":
        return "Talk soon,"
    elif tone == "direct":
        return "Best,"
    return "Best regards,"


def _opening(meeting_title, meeting_date=None, tone="professional"):
    date_str = ""
    if meeting_date:
        try:
            d = dt.date.fromisoformat(meeting_date[:10])
            today = dt.date.today()
            delta = (today - d).days

            if delta == 0:
                date_str = "earlier today"
            elif delta == 1:
                date_str = "yesterday"
            elif delta < 7:
                date_str = f"on {d.strftime('%A')}"
            else:
                date_str = f"on {d.strftime('%B %d')}"
        except (ValueError, TypeError):
            pass

    if tone == "casual":
        if date_str:
            return f"Good chatting {date_str}. Here's a quick recap of what we covered."
        return "Good chatting. Here's a quick recap of what we covered."
    elif tone == "formal":
        if date_str:
            return f"Thank you for taking the time to meet {date_str}. Please find below a summary of our discussion."
        return "Thank you for taking the time to meet. Please find below a summary of our discussion."
    elif tone == "direct":
        if date_str:
            return f"Recap from our meeting {date_str}:"
        return "Recap from our meeting:"
    else:
        if date_str:
            return f"Thanks for the meeting {date_str}. Here's a summary of what we discussed."
        return "Thanks for the meeting. Here's a summary of what we discussed."


def generate_email(meeting_title, notes=None, action_items=None, next_steps=None,
                   deadline=None, client_name=None, client_email=None,
                   attendees=None, preferred_greeting=None,
                   tone="professional", meeting_date=None):
    """Generate a complete follow-up email from meeting data."""

    parts = []

    # Greeting
    parts.append(_greeting(client_name, preferred_greeting, tone))
    parts.append("")

    # Opening
    parts.append(_opening(meeting_title, meeting_date, tone))
    parts.append("")

    # Discussion summary
    if notes:
        if tone == "direct":
            parts.append(f"Key points:")
            parts.append(f"   {notes}")
        else:
            parts.append(f"What we discussed:")
            parts.append(f"   {notes}")
        parts.append("")

    # Action items
    action_str = _format_action_items(action_items)
    if action_str:
        parts.append("Action items:")
        parts.append(action_str)
        parts.append("")

    # Next steps
    if next_steps:
        parts.append(f"Next steps:")
        parts.append(f"   {next_steps}")
        parts.append("")

    # Deadline
    if deadline:
        try:
            d = dt.date.fromisoformat(deadline[:10])
            parts.append(f"Target date: {d.strftime('%B %d, %Y')}")
            parts.append("")
        except (ValueError, TypeError):
            parts.append(f"Target date: {deadline}")
            parts.append("")

    # Closing prompt
    if tone == "casual":
        parts.append("Let me know if I missed anything.")
    elif tone == "formal":
        parts.append("Please do not hesitate to reach out should you have any questions or require further clarification.")
    elif tone == "direct":
        parts.append("Flag anything I missed.")
    else:
        parts.append("Let me know if anything needs adjusting.")

    parts.append("")
    parts.append(_closing(tone))

    return "\n".join(parts)


def generate_internal_recap(meeting_title, notes=None, action_items=None,
                            next_steps=None, attendees=None, meeting_date=None):
    """Generate an internal team recap (less formal than client emails)."""
    parts = []

    parts.append(f"Meeting Recap: {meeting_title}")
    if meeting_date:
        parts.append(f"Date: {meeting_date}")
    if attendees:
        parts.append(f"Attendees: {attendees}")
    parts.append(SUBSEPARATOR)
    parts.append("")

    if notes:
        parts.append(f"Summary:")
        parts.append(f"   {notes}")
        parts.append("")

    action_str = _format_action_items(action_items)
    if action_str:
        parts.append("Action items:")
        parts.append(action_str)
        parts.append("")

    if next_steps:
        parts.append(f"Next steps: {next_steps}")
        parts.append("")

    return "\n".join(parts)
