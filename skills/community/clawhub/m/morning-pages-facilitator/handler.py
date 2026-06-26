#!/usr/bin/env python3
import json
import os
import re
from typing import Any, Dict, List, Sequence


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


OBSTACLE_RULES = {
    'Freeze on page one': ['freeze', 'frozen', 'blank page', 'page one', 'cannot start'],
    'Self-editing': ['self-edit', 'editing', 'polish', 'perfect', 'sound good'],
    'Over-analysis': ['overthink', 'analyze', 'ruminate', 'spiral'],
    'Low time': ['5 minutes', 'five minutes', 'short', 'busy', 'little time'],
}


def _extract_container(data: Dict[str, Any], raw: str) -> str:
    page_target = _pick_text(data, ['page_target', 'pages'])
    if page_target:
        return page_target if 'page' in page_target.lower() else f'{page_target} pages'

    time_target = _pick_text(data, ['time', 'minutes', 'duration'])
    if time_target:
        lower = time_target.lower()
        if 'minute' in lower or 'page' in lower:
            return time_target
        return f'{time_target} minutes'

    lowered = raw.lower()
    minute_match = re.search(r'(\d+)\s*(minutes?|mins?)', lowered)
    if minute_match:
        return f"{minute_match.group(1)} minutes"

    page_match = re.search(r'(\d+)\s*pages?', lowered)
    if page_match:
        return f"{page_match.group(1)} pages"

    if 'five-minute' in lowered or '5-minute' in lowered:
        return '5 minutes'
    return '10 minutes or about 2 pages'


def _build_cues(obstacle: str, focus: str) -> List[str]:
    cue_one = 'Right now my mind is full of...'
    cue_two = 'If I am honest, I keep thinking about...'
    cue_three = 'What I do not want to write is...'

    if obstacle == 'Self-editing':
        cue_two = 'If this never had to sound smart, I would say...'
    elif obstacle == 'Over-analysis':
        cue_two = 'The loop I keep replaying is...'
    elif obstacle == 'Low time':
        cue_one = 'In the next five minutes, I need to unload...'

    if focus:
        cue_one = f'Right now my mind is full of {focus}, and the first honest sentence is...'
    return [cue_one, cue_two, cue_three]


def handle(inputs):
    meta = _load_skill_meta('skill')
    data = _coerce_dict(inputs)
    raw = _normalize_inputs(inputs)

    focus = _pick_text(data, ['focus', 'theme', 'topic'])
    obstacle = _pick_text(data, ['obstacle', 'stuckness'], _detect_one(raw, OBSTACLE_RULES, 'Freeze on page one'))
    container = _extract_container(data, raw)
    writing_rule = 'Keep the pen or cursor moving, do not edit while writing, and write the next honest sentence even if it feels repetitive.'
    if obstacle == 'Self-editing':
        writing_rule = 'Write without polishing or crossing out, and let awkward sentences stay awkward until the session ends.'
    elif obstacle == 'Over-analysis':
        writing_rule = 'Stay with raw observation, not interpretation, until the timer or page target ends.'

    cues = _build_cues(obstacle, focus)
    gentle_focus = focus if focus else 'Whatever feels loudest in your mind this morning.'

    return f"""# Morning Pages Session
## Container
- Time or page target: {container}
- Writing rule: {writing_rule}
- Gentle focus, if helpful: {gentle_focus}

## Starter Cues
- {cues[0]}
- {cues[1]}
- {cues[2]}

## After Writing
- One phrase that stood out: Circle or copy one line that surprised you.
- One feeling I notice: Name the clearest feeling in one or two words.
- One next action, if any: Pull only one gentle next step if it feels obvious.
- Restart note: Missing days does not break the practice; restart with one honest sentence tomorrow.
"""
