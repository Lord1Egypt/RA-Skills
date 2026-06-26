"""
Nex Voice - Action Item Extraction
"""

import re
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any
import subprocess

from .config import ACTION_KEYWORDS


def _parse_relative_date(text: str) -> Optional[str]:
    """Parse relative dates like morgen, overmorgen, vrijdag, etc."""
    text_lower = text.lower().strip()

    today = datetime.now().date()
    tomorrow = today + timedelta(days=1)
    day_after_tomorrow = today + timedelta(days=2)

    # Dutch relative dates
    if text_lower in ["morgen", "tomorrow"]:
        return tomorrow.isoformat()
    if text_lower in ["overmorgen", "day after tomorrow"]:
        return day_after_tomorrow.isoformat()
    if text_lower in ["vandaag", "today"]:
        return today.isoformat()

    # Day names (Dutch and English)
    day_map = {
        "maandag": 0, "monday": 0,
        "dinsdag": 1, "tuesday": 1,
        "woensdag": 2, "wednesday": 2,
        "donderdag": 3, "thursday": 3,
        "vrijdag": 4, "friday": 4,
        "zaterdag": 5, "saturday": 5,
        "zondag": 6, "sunday": 6,
    }

    if text_lower in day_map:
        target_day = day_map[text_lower]
        current_day = today.weekday()
        days_ahead = target_day - current_day

        if days_ahead <= 0:  # Target day already happened this week
            days_ahead += 7

        target_date = today + timedelta(days=days_ahead)
        return target_date.isoformat()

    # Time formats: "14u", "2pm", "14:30", "14h30"
    time_match = re.search(r"(\d{1,2})[u:h](\d{2})?", text_lower)
    if time_match:
        hour = int(time_match.group(1))
        minute = int(time_match.group(2)) if time_match.group(2) else 0

        # Infer date context from surrounding text
        if any(d in text_lower for d in ["morgen", "tomorrow"]):
            date = tomorrow
        elif any(d in text_lower for d in ["overmorgen", "day after tomorrow"]):
            date = day_after_tomorrow
        else:
            # Try to parse day name from text
            for day_name, day_num in day_map.items():
                if day_name in text_lower:
                    current_day = today.weekday()
                    days_ahead = day_num - current_day
                    if days_ahead <= 0:
                        days_ahead += 7
                    date = today + timedelta(days=days_ahead)
                    break
            else:
                date = today

        return f"{date.isoformat()}T{hour:02d}:{minute:02d}:00"

    return None


def _extract_actions_regex(text: str) -> List[Dict[str, Any]]:
    """Extract actions using regex patterns"""
    actions = []

    # Normalize text
    lines = text.split("\n")

    for line in lines:
        line = line.strip()
        if not line:
            continue

        action = None

        # Task patterns
        task_patterns = [
            r"(moet\s+(?:nog\s+)?)?([^.!?]+?)(\s+naar\s+|\s+voor\s+)?$",
            r"^([A-Z][a-z]+)\s+(said\s+)?(?:he\'ll|will|said he)\s+([^.!?]+)",
            r"(must|need to|do|handle|prepare|review)\s+([^.!?]+)",
        ]

        for pattern in task_patterns:
            match = re.search(pattern, line, re.IGNORECASE)
            if match:
                action = {
                    "type": "task",
                    "description": match.group(0).strip(),
                    "assigned_to": None,
                    "due_date": None,
                    "priority": "medium",
                }
                break

        # Decision patterns
        if not action:
            decision_patterns = [
                r"(?:besloten|decided)[\s:]\s*([^.!?]+)",
                r"(?:we\s+)?(?:agree|agreed)\s+(?:on\s+)?([^.!?]+)",
            ]

            for pattern in decision_patterns:
                match = re.search(pattern, line, re.IGNORECASE)
                if match:
                    action = {
                        "type": "decision",
                        "description": match.group(1).strip() if match.groups() else line.strip(),
                        "priority": "high",
                    }
                    break

        # Reminder patterns
        if not action:
            reminder_patterns = [
                r"(?:vergeet niet|don't forget)[\s:]\s*([^.!?]+)",
                r"(?:remember|herinnering)[\s:]\s*([^.!?]+)",
            ]

            for pattern in reminder_patterns:
                match = re.search(pattern, line, re.IGNORECASE)
                if match:
                    description = match.group(1).strip() if match.groups() else line.strip()

                    action = {
                        "type": "reminder",
                        "description": description,
                        "priority": "high",
                    }

                    # Try to extract date
                    date_match = re.search(
                        r"(morgen|overmorgen|vandaag|maandag|dinsdag|woensdag|donderdag|vrijdag|zaterdag|zondag|tomorrow|today|monday|tuesday|wednesday|thursday|friday|saturday|sunday|^\d{1,2}[u:h]\d{2}?)",
                        line,
                        re.IGNORECASE
                    )
                    if date_match:
                        action["due_date"] = _parse_relative_date(date_match.group(1))

                    break

        # Call patterns
        if not action:
            call_patterns = [
                r"(?:bel|call|belt|calling|contact)\s+([A-Z][a-z]+)(?:\s+([^.!?]+))?",
                r"([A-Z][a-z]+)(?:\s+terug\s+bellen|\s+call back)(?:\s+([^.!?]+))?",
            ]

            for pattern in call_patterns:
                match = re.search(pattern, line)
                if match:
                    assigned_to = match.group(1).strip()
                    description = f"Call {assigned_to}"
                    if match.group(2):
                        description += f": {match.group(2).strip()}"

                    action = {
                        "type": "call",
                        "description": description,
                        "assigned_to": assigned_to,
                        "priority": "high",
                    }

                    # Try to extract when
                    when_match = re.search(
                        r"(morgen|overmorgen|vandaag|tomorrow|today)",
                        line,
                        re.IGNORECASE
                    )
                    if when_match:
                        action["due_date"] = _parse_relative_date(when_match.group(1))

                    break

        # Email/Send patterns
        if not action:
            email_patterns = [
                r"(?:mail|email|stuur|send)\s+([^.!?]+?)(?:\s+naar\s+([A-Z][a-z\s]+))?",
            ]

            for pattern in email_patterns:
                match = re.search(pattern, line, re.IGNORECASE)
                if match:
                    description = match.group(1).strip()
                    assigned_to = match.group(2).strip() if match.group(2) else None

                    action = {
                        "type": "email",
                        "description": description,
                        "assigned_to": assigned_to,
                        "priority": "medium",
                    }
                    break

        # Meeting patterns
        if not action:
            meeting_patterns = [
                r"(?:afspraak|meeting|vergadering|overleg|presentatie|demo)(?:\s+(?:met|with)\s+([^.!?]+))?(?:\s+(morgen|overmorgen|maandag|dinsdag|woensdag|donderdag|vrijdag|zaterdag|zondag|tomorrow|monday|tuesday|wednesday|thursday|friday|saturday|sunday))?",
            ]

            for pattern in meeting_patterns:
                match = re.search(pattern, line, re.IGNORECASE)
                if match:
                    description = f"Meeting"
                    if match.group(1):
                        description += f" with {match.group(1).strip()}"

                    action = {
                        "type": "meeting",
                        "description": description,
                        "assigned_to": match.group(1).strip() if match.group(1) else None,
                        "priority": "high",
                    }

                    if match.group(2):
                        action["due_date"] = _parse_relative_date(match.group(2))

                    break

        # Deadline patterns
        if not action:
            deadline_patterns = [
                r"(?:deadline|voor|by|until)\s+([^.!?]+?)(?:\s+voor\s+)?([^.!?]+)?",
            ]

            for pattern in deadline_patterns:
                match = re.search(pattern, line, re.IGNORECASE)
                if match:
                    description = match.group(1).strip()

                    action = {
                        "type": "deadline",
                        "description": description,
                        "priority": "high",
                    }

                    if match.group(2):
                        action["due_date"] = _parse_relative_date(match.group(2))

                    break

        if action:
            actions.append(action)

    return actions


def _extract_actions_llm(
    text: str,
    api_key: str,
    api_base: str,
    model: str,
) -> List[Dict[str, Any]]:
    """Extract actions using LLM"""
    prompt = f"""Extract action items from this transcript. For each action, identify:
- type: task, reminder, call, email, meeting, decision, or deadline
- description: what needs to be done
- assigned_to: who is responsible (if mentioned)
- due_date: when it's due (ISO format YYYY-MM-DD or full timestamp, or null)
- priority: low, medium, or high

Return a JSON array of action items.

Transcript:
{text}

JSON output:"""

    try:
        response = subprocess.run(
            [
                "curl",
                "-s",
                f"{api_base}/chat/completions",
                "-H", f"Authorization: Bearer {api_key}",
                "-H", "Content-Type: application/json",
                "-d", json.dumps({
                    "model": model,
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are an expert at extracting action items from transcripts. Always return valid JSON.",
                        },
                        {
                            "role": "user",
                            "content": prompt,
                        }
                    ],
                    "temperature": 0.7,
                })
            ],
            capture_output=True,
            text=True,
        )

        if response.returncode != 0:
            raise RuntimeError(f"API request failed: {response.stderr}")

        result = json.loads(response.stdout)
        content = result["choices"][0]["message"]["content"]

        # Extract JSON from response
        json_match = re.search(r"\[.*\]", content, re.DOTALL)
        if json_match:
            actions = json.loads(json_match.group())
            return actions

        return []

    except (subprocess.CalledProcessError, json.JSONDecodeError, KeyError) as e:
        # Fall back to regex extraction
        return _extract_actions_regex(text)


def extract_actions(
    transcript: str,
    use_llm: bool = False,
    api_key: Optional[str] = None,
    api_base: Optional[str] = None,
    model: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Extract action items from transcript.

    Args:
        transcript: The transcript text
        use_llm: Whether to use LLM for extraction
        api_key: API key for LLM
        api_base: API base URL for LLM
        model: LLM model name

    Returns:
        List of action items with type, description, assigned_to, due_date, priority
    """
    if use_llm and api_key and api_base and model:
        try:
            return _extract_actions_llm(transcript, api_key, api_base, model)
        except Exception:
            # Fall back to regex
            pass

    return _extract_actions_regex(transcript)


def generate_summary(transcript: str) -> str:
    """Generate a brief summary of the transcript"""
    lines = transcript.split("\n")

    # Get first meaningful line
    summary_lines = []
    for line in lines:
        line = line.strip()
        if line and not line.startswith("..."):
            summary_lines.append(line)
            if len(summary_lines) >= 2:
                break

    summary = " ".join(summary_lines)

    # Limit to ~200 characters
    if len(summary) > 200:
        summary = summary[:197] + "..."

    return summary
