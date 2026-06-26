#!/usr/bin/env python3
import json
import os
import re
from typing import Any, Dict, Sequence


def _load_skill_meta(slug):
    path = os.path.join(os.path.dirname(__file__), 'SKILL.md')
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    meta = re.search(r'^---$(.*?)^---$', content, re.DOTALL | re.MULTILINE)
    return meta.group(1).strip() if meta else ''


def _normalize_inputs(inputs: Any) -> str:
    if inputs is None:
        return ''
    if isinstance(inputs, str):
        return inputs.strip()
    if isinstance(inputs, dict):
        parts = []
        for key, value in inputs.items():
            if value in (None, '', [], {}, ()):  # type: ignore[comparison-overlap]
                continue
            if isinstance(value, (list, tuple, set)):
                rendered = ', '.join(str(item) for item in value)
            else:
                rendered = str(value)
            parts.append(f"{key}: {rendered}")
        return ' | '.join(parts)
    if isinstance(inputs, (list, tuple, set)):
        return ' | '.join(str(item) for item in inputs)
    try:
        return json.dumps(inputs, ensure_ascii=False, sort_keys=True)
    except TypeError:
        return str(inputs)


def _coerce_dict(inputs: Any) -> Dict[str, Any]:
    return inputs if isinstance(inputs, dict) else {}


def _pick_text(data: Dict[str, Any], keys: Sequence[str], default: str = '') -> str:
    for key in keys:
        value = data.get(key)
        if value is None:
            continue
        text = str(value).strip()
        if text:
            return text
    return default


def _detect_one(text: str, rules: Dict[str, Sequence[str]], default: str) -> str:
    lower = text.lower()
    for label, keywords in rules.items():
        if any(keyword in lower for keyword in keywords):
            return label
    return default


def _shorten(text: str, limit: int = 120) -> str:
    clean = ' '.join(text.split())
    if len(clean) <= limit:
        return clean
    return clean[: limit - 3].rstrip() + '...'


CATEGORY_RULES = {
    'Consistency': ['streak', 'consistent', 'showed up', 'every day', 'kept at it', 'routine'],
    'Courage': ['spoke up', 'hard conversation', 'boundary', 'asked for', 'brave', 'fear'],
    'Recovery': ['recovered', 'came back', 'restarted', 'after missing', 'bounced back', 'reset'],
    'Learning': ['learned', 'practiced', 'studied', 'improved', 'figured out'],
}


def _what_changed(category: str) -> str:
    return {
        'Consistency': 'You repeated the behavior enough times to make it feel more like a pattern than a random exception.',
        'Courage': 'You acted while discomfort was still present instead of waiting to feel fearless.',
        'Recovery': 'You returned after disruption instead of letting the setback define the story.',
        'Learning': 'You turned effort into usable skill, not just more information.',
        'Effort': 'You kept moving in the right direction before the outcome was fully polished.',
    }[category]


def _identity_line(category: str) -> str:
    return {
        'Consistency': 'I am becoming someone who follows through in small, repeatable ways.',
        'Courage': 'I am becoming someone who can stay honest and steady under discomfort.',
        'Recovery': 'I am becoming someone who can return after setbacks without drama.',
        'Learning': 'I am becoming someone who turns practice into capability.',
        'Effort': 'I am becoming someone who keeps showing up before applause arrives.',
    }[category]


def _next_step(category: str) -> str:
    return {
        'Consistency': 'Repeat the same action at the next scheduled time so the pattern stays alive.',
        'Courage': 'Write down the brave move you want to repeat and the next situation where it matters.',
        'Recovery': 'Protect the restart cue that helped you come back and use it again this week.',
        'Learning': 'Practice the new skill again within 48 hours so it sticks.',
        'Effort': 'Name the next smallest step and put it somewhere visible or scheduled.',
    }[category]


def handle(inputs):
    meta = _load_skill_meta('skill')
    data = _coerce_dict(inputs)
    raw = _normalize_inputs(inputs)

    milestone = _pick_text(
        data,
        ['milestone', 'what_happened', 'win', 'growth'],
        _shorten(raw) if raw else 'You noticed a real sign of movement worth naming.',
    )
    category = _pick_text(data, ['category'], _detect_one(raw, CATEGORY_RULES, 'Effort'))
    evidence = _pick_text(data, ['evidence', 'proof'], milestone)
    small_celebration = _pick_text(
        data,
        ['small_celebration'],
        'Mark it in writing, take one full breath of recognition, and give yourself a small treat or pause that feels sincere.',
    )
    bigger_celebration = _pick_text(
        data,
        ['bigger_celebration'],
        'If it feels meaningful, share it with one supportive person or pair it with a slightly bigger ritual, meal, or outing.',
    )

    return f"""# Growth Milestone Record
## What Happened
- Milestone: {milestone}
- Category: {category}
- Evidence: {evidence}

## Why It Matters
- What changed: {_what_changed(category)}
- What this says about me: {_identity_line(category)}

## Celebration
- Small celebration: {small_celebration}
- Bigger celebration, if appropriate: {bigger_celebration}

## Next Step
- To build on this, I will: {_next_step(category)}
"""
