#!/usr/bin/env python3
import json
import os
import re
from typing import Any, Dict, List, Tuple

SKILL_SLUG = 'npc-dialogue-rehearser'
PROMPT_TEMPLATE = """Rehearse a real-world conversation.
Clarify the goal, choose likely counterpart styles, generate a natural opening line, three short response branches, risky phrase replacements, and a calm closing line. Keep the script non-manipulative and relationship-aware."""

HIGH_RISK_WORDS = ['abuse', 'violent', 'violence', 'threat', 'unsafe', 'self-harm', 'medical', 'legal', 'harassment']
NPC_STYLE_RULES = {
    'authority': ['teacher', 'boss', 'manager', 'doctor', 'coach', 'principal', 'authority', '家长', '老师', '领导'],
    'busy': ['busy', 'rushed', 'time', 'deadline', 'quick', '赶时间', '忙'],
    'defensive': ['defensive', 'blame', 'angry', 'upset', 'reject', '误会', '生气', '防御'],
    'friendly': ['friend', 'partner', 'classmate', 'family', 'supportive', '朋友', '家人', '同学'],
}

BRANCH_LIBRARY = {
    'authority': {
        'label': 'Authority NPC',
        'npc_line': 'What exactly are you requesting, and why?',
        'you_line': 'My request is: {ask}. The reason is: {reason}. I can also work with this fallback: {fallback}.',
        'repair': 'If the full request is not possible, what smaller option would you allow?'
    },
    'busy': {
        'label': 'Busy NPC',
        'npc_line': 'I only have a minute, what do you need?',
        'you_line': 'The short version is: {ask}. The one next step I am asking for is {next_step}.',
        'repair': 'If now is a bad time, can we set a specific moment to finish this conversation?'
    },
    'defensive': {
        'label': 'Defensive NPC',
        'npc_line': 'Why are you bringing this up now? Are you blaming me?',
        'you_line': 'I am not trying to blame you. I want to solve this clearly: {ask}. What matters most is {goal_focus}.',
        'repair': 'Let me restate it simply. I am making a request, not attacking you.'
    },
    'friendly': {
        'label': 'Friendly NPC',
        'npc_line': 'Okay, tell me more. What would help?',
        'you_line': 'Thanks for hearing me out. What would help most is {ask}. Even one small next step would make this easier.',
        'repair': 'If that is too much right now, what smaller version feels workable?'
    },
}


def _load_skill_meta(skill_name):
    path = os.path.join(os.path.dirname(__file__), 'SKILL.md')
    with open(path, 'r', encoding='utf-8') as handle:
        content = handle.read()
    match = re.search(r'^---\s*\n(.*?)\n---\s*', content, re.DOTALL | re.MULTILINE)
    meta = {}
    if match:
        for line in match.group(1).splitlines():
            if ':' in line:
                key, value = line.split(':', 1)
                meta[key.strip()] = value.strip()
    meta['skill_name'] = skill_name or meta.get('name', SKILL_SLUG)
    return meta


def _load_prompt_template(skill_name):
    return PROMPT_TEMPLATE


def _clean_text(value: Any) -> str:
    if value is None:
        return ''
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, (int, float)):
        return str(value)
    return json.dumps(value, ensure_ascii=False)


def _parse_text_map(raw: str) -> Dict[str, str]:
    data: Dict[str, str] = {}
    for line in raw.splitlines():
        if re.search(r'[:：]', line):
            key, value = re.split(r'[:：]', line, maxsplit=1)
            normalized = re.sub(r'\s+', '_', key.strip().lower())
            data[normalized] = value.strip()
    return data


def _coerce_input(user_input: Any) -> Tuple[str, Dict[str, Any]]:
    if isinstance(user_input, dict):
        return json.dumps(user_input, ensure_ascii=False), dict(user_input)
    raw = _clean_text(user_input)
    if raw.startswith('{') and raw.endswith('}'):
        try:
            parsed = json.loads(raw)
            if isinstance(parsed, dict):
                return raw, parsed
        except json.JSONDecodeError:
            pass
    return raw, _parse_text_map(raw)


def _pick(data: Dict[str, Any], keys: List[str], default: str = '') -> str:
    for key in keys:
        if key in data:
            text = _clean_text(data.get(key))
            if text:
                return text
    return default


def _detect_primary_style(counterpart: str, scenario: str, worry: str) -> str:
    combined = f'{counterpart} {scenario} {worry}'.lower()
    for style, words in NPC_STYLE_RULES.items():
        if any(word in combined for word in words):
            return style
    return 'busy'


def _branch_order(primary_style: str) -> List[str]:
    if primary_style == 'authority':
        return ['authority', 'busy', 'defensive']
    if primary_style == 'friendly':
        return ['friendly', 'busy', 'defensive']
    if primary_style == 'defensive':
        return ['defensive', 'busy', 'friendly']
    return ['busy', 'friendly', 'defensive']


def _opening_line(goal: str, tone: str) -> str:
    tone_lower = tone.lower()
    if 'firm' in tone_lower or 'direct' in tone_lower:
        return f'I want to be clear and respectful. My request is {goal}.'
    if 'brief' in tone_lower or 'short' in tone_lower:
        return f'Quick version: I am hoping to {goal}.'
    return f'I want to say this clearly and calmly. I am hoping to {goal}.'


def _risk_swaps(goal: str) -> List[Tuple[str, str]]:
    return [
        ('"You never listen."', '"I want to make sure my point is landing clearly."'),
        ('"Fine, whatever."', '"I want to be honest about what would help here."'),
        (f'"You have to {goal}."', f'"My request is {goal}, and I want to see what is workable."'),
    ]


def _safety_note(raw: str) -> str:
    lowered = raw.lower()
    if any(word in lowered for word in HIGH_RISK_WORDS):
        return 'This sounds higher risk than a normal rehearsal. Consider real-world support, documentation, or professional help before relying on phrasing alone.'
    return ''


def _build_result(raw: str, data: Dict[str, Any], template: str) -> str:
    scenario = _pick(data, ['scenario', 'context'], 'A conversation the user wants to handle better')
    counterpart = _pick(data, ['counterpart', 'person', 'other_person'], 'the other person')
    goal = _pick(data, ['goal', 'request', 'ask'], 'make a clear request')
    taboo = _pick(data, ['taboo', 'avoid', 'sensitive'], 'Avoid blame, pressure, and manipulative framing.')
    worry = _pick(data, ['worry', 'fear', 'concern'], 'The other person may react in a way that makes the user freeze or over-explain.')
    tone = _pick(data, ['tone', 'style'], 'gentle and direct')
    primary_style = _detect_primary_style(counterpart, scenario, worry)
    branches = _branch_order(primary_style)
    reason = scenario if scenario else 'it would reduce friction and confusion'
    fallback = 'one smaller step, a later time, or a partial yes'
    next_step = 'one clear yes, no, or alternative'
    goal_focus = goal
    safety_note = _safety_note(f'{raw} {scenario} {counterpart} {worry}')

    lines: List[str] = []
    lines.append('# NPC Dialogue Rehearsal')
    lines.append('')
    lines.append('## Dialogue Objective')
    lines.append(f'- Scenario: {scenario}')
    lines.append(f'- Counterpart: {counterpart}')
    lines.append(f'- Goal: {goal}')
    lines.append(f'- Tone: {tone}')
    lines.append(f'- Guardrail: {taboo}')
    lines.append(f'- Rehearsal frame: {template.splitlines()[0]}')
    lines.append('')
    lines.append('## Opening Line')
    lines.append(f'- {_opening_line(goal, tone)}')
    lines.append('')
    lines.append('## Three-Branch Script')
    for style in branches:
        branch = BRANCH_LIBRARY[style]
        lines.append(f"### {branch['label']}")
        lines.append(f"- Likely reply: {branch['npc_line']}")
        lines.append(f"- Your next line: {branch['you_line'].format(ask=goal, reason=reason, fallback=fallback, next_step=next_step, goal_focus=goal_focus)}")
        lines.append(f"- Repair line: {branch['repair']}")
        lines.append('')
    lines.append('## Risky Phrase Swaps')
    for risky, safer in _risk_swaps(goal):
        lines.append(f'- Risky: {risky}')
        lines.append(f'  - Better: {safer}')
    lines.append('')
    lines.append('## Closing Line')
    lines.append('- Thanks for hearing me out. Let’s confirm the next step so I know how to proceed.')
    if safety_note:
        lines.append('')
        lines.append('## Safety Note')
        lines.append(f'- {safety_note}')
    return '\n'.join(lines)


def handle(args):
    skill_name = args.get('skill_name', SKILL_SLUG) or SKILL_SLUG
    user_input = args.get('input', '')
    mode = args.get('mode', 'guide')
    meta = _load_skill_meta(skill_name)
    template = _load_prompt_template(skill_name)
    if mode == 'meta':
        return {'result': json.dumps(meta, ensure_ascii=False, indent=2)}
    if mode == 'prompt':
        return {'result': template}
    raw, data = _coerce_input(user_input)
    return {'result': _build_result(raw, data, template)}
