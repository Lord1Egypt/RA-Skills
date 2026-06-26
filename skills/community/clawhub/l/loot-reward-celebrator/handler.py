#!/usr/bin/env python3
import json
import os
import re
from typing import Any, Dict, List, Tuple

SKILL_SLUG = 'loot-reward-celebrator'
PROMPT_TEMPLATE = """Celebrate a completed task like earned loot.
Name the visible and invisible rewards, suggest one immediate and one richer celebration option, include a way to record the win, and keep the reward aligned with budget and long-term goals."""

GROWTH_MAP = [
    ('study', ['study', 'essay', 'exam', 'read', 'learn'], 'knowledge, consistency, and follow-through'),
    ('health', ['exercise', 'walk', 'workout', 'sleep', 'meal', 'run'], 'discipline, body trust, and recovery skills'),
    ('admin', ['application', 'form', 'paperwork', 'email', 'submit', 'tax'], 'follow-through, tolerance for friction, and completion energy'),
    ('care', ['family', 'child', 'parent', 'home', 'care'], 'care capacity, patience, and reliability'),
]


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


def _budget_level(budget: str) -> str:
    lowered = budget.lower()
    if not lowered:
        return 'low'
    match = re.search(r'(\d+)', lowered)
    if match:
        amount = int(match.group(1))
        if amount <= 30:
            return 'low'
        if amount <= 120:
            return 'medium'
        return 'high'
    if any(word in lowered for word in ['low', 'tight', 'limited', 'small', 'budget']):
        return 'low'
    if any(word in lowered for word in ['medium', 'moderate']):
        return 'medium'
    if any(word in lowered for word in ['high', 'generous']):
        return 'high'
    return 'low'


def _growth_gain(task: str) -> str:
    lowered = task.lower()
    for _, words, gain in GROWTH_MAP:
        if any(word in lowered for word in words):
            return gain
    return 'follow-through, proof of effort, and a stronger completion loop'


def _reward_options(task: str, budget_level: str, values: str) -> Tuple[str, str, str, str]:
    values_lower = values.lower()
    health_guard = any(word in values_lower for word in ['health', 'sleep', 'diet', 'fitness'])
    money_guard = any(word in values_lower for word in ['save', 'saving', 'budget', 'money']) or budget_level == 'low'
    if money_guard or health_guard:
        immediate = 'A low-cost reset, such as favorite tea, a quiet walk, stretching, music, or 20 guilt-free minutes off duty.'
        chest = 'A modest ritual reward, such as a library visit, a fresh notebook page, a favorite podcast, or a family shout-out.'
        keepsake = 'Record the win with a photo, journal note, sticker, or shared message so the reward is visible without being expensive.'
        guardrail = 'Keep the reward restorative and low-cost, and avoid celebrations that create money stress or health backlash.'
        return immediate, chest, keepsake, guardrail
    if budget_level == 'medium':
        immediate = 'A short enjoyable reward you can do today, such as favorite coffee, a long shower, or protected leisure time.'
        chest = 'A slightly bigger treat, such as a small purchase, a meaningful outing, or a dedicated hobby block.'
        keepsake = 'Mark the milestone in your notes, tracker, or calendar so the win does not disappear.'
        guardrail = 'Keep the reward proportional so celebration supports momentum instead of becoming the new source of pressure.'
        return immediate, chest, keepsake, guardrail
    immediate = 'A satisfying immediate reward, such as a favorite meal, a longer rest block, or an intentional splurge within your limit.'
    chest = 'A richer milestone reward, such as a day trip, a meaningful item, or a larger shared celebration.'
    keepsake = 'Create a visible milestone record so the reward is not only consumed but also remembered.'
    guardrail = 'Even high-budget rewards should protect sleep, recovery, and the next day’s stability.'
    return immediate, chest, keepsake, guardrail


def _next_unlock(task: str) -> str:
    lowered = task.lower()
    if any(word in lowered for word in ['day', 'streak', 'habit', 'daily', 'week']):
        return 'Unlock the next chest after the next repeatable streak milestone, not after a random hard day.'
    if any(word in lowered for word in ['project', 'milestone', 'essay', 'application', 'submit']):
        return 'Unlock the next bigger reward when the next milestone is shipped, not merely planned.'
    return 'Set the next unlock condition as one visible repeat of this behavior or the next meaningful milestone.'


def _display_idea(task: str, values: str) -> str:
    values_lower = values.lower()
    if 'family' in values_lower or 'child' in values_lower:
        return 'Share the win with family, add it to a shared board, or let someone celebrate it with you.'
    if 'private' in values_lower:
        return 'Keep it private but visible with a journal entry, habit tracker mark, or screenshot archive.'
    return f'Write a one-line victory log for {task} and store it somewhere you will actually revisit.'


def _build_result(raw: str, data: Dict[str, Any], template: str) -> str:
    task = _pick(data, ['completed_task', 'task', 'milestone', 'win'], 'a meaningful completed task')
    effort = _pick(data, ['effort', 'cost', 'energy'], 'real effort was invested, even if it looked small from the outside')
    mood = _pick(data, ['mood', 'emotion', 'state'], 'ready for a fair celebration')
    budget = _pick(data, ['budget', 'reward_budget'], 'low')
    values = _pick(data, ['values', 'constraints', 'guardrails'], '')
    budget_level = _budget_level(budget)
    growth_gain = _growth_gain(task)
    immediate, chest, keepsake, guardrail = _reward_options(task, budget_level, values)
    display_idea = _display_idea(task, values)
    next_unlock = _next_unlock(task)

    lines: List[str] = []
    lines.append('# Loot Reward Celebration')
    lines.append('')
    lines.append('## Loot Table')
    lines.append(f'- Mission cleared: {task}')
    lines.append(f'- Visible reward already earned: progress, relief, and a completed checkpoint linked to {task}.')
    lines.append(f'- Invisible growth gained: {growth_gain}.')
    lines.append(f'- Proof you earned it: {effort}.')
    lines.append(f'- Celebration frame: {template.splitlines()[0]}')
    lines.append('')
    lines.append('## Reward Suggestions')
    lines.append(f'- Immediate drop: {immediate}')
    lines.append(f'- Treasure chest option: {chest}')
    lines.append(f'- Keepsake loot: {keepsake}')
    lines.append(f'- Current mood note: {mood}')
    lines.append('')
    lines.append('## How to Display the Win')
    lines.append(f'- {display_idea}')
    lines.append('')
    lines.append('## Next Unlock Condition')
    lines.append(f'- {next_unlock}')
    lines.append('')
    lines.append('## Sustainability Guardrails')
    lines.append(f'- {guardrail}')
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
