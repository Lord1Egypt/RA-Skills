#!/usr/bin/env python3
import json
import os
import re
import sys
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
        parts: List[str] = []
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
        if isinstance(value, (list, tuple, set)):
            text = ', '.join(str(item) for item in value if str(item).strip())
        else:
            text = str(value).strip()
        if text:
            return text
    return default


def _listify(value: Any) -> List[str]:
    if value in (None, '', [], {}, ()):  # type: ignore[comparison-overlap]
        return []
    if isinstance(value, str):
        clean = value.replace(';', '\n').replace(',', '\n')
        return [chunk.strip() for chunk in clean.splitlines() if chunk.strip()]
    if isinstance(value, (list, tuple, set)):
        return [str(item).strip() for item in value if str(item).strip()]
    return [str(value).strip()]


def _detect_one(text: str, rules: Dict[str, Sequence[str]], default: str) -> str:
    lower = text.lower()
    for label, keywords in rules.items():
        if any(keyword in lower for keyword in keywords):
            return label
    return default


def _detect_many(text: str, rules: Dict[str, Sequence[str]], default: List[str], limit: int = 4) -> List[str]:
    lower = text.lower()
    found = [label for label, keywords in rules.items() if any(keyword in lower for keyword in keywords)]
    ordered: List[str] = []
    for item in found + default:
        if item not in ordered:
            ordered.append(item)
    return ordered[:limit]


def _shorten(text: str, limit: int = 140) -> str:
    clean = ' '.join(text.split())
    if len(clean) <= limit:
        return clean
    return clean[: limit - 3].rstrip() + '...'

GOAL_TYPE_RULES = {
'Learning or study': ['learn', 'study', 'course', 'exam', 'practice', 'certification', 'class'],
'Writing or shipping': ['write', 'book', 'essay', 'article', 'draft', 'publish', 'portfolio', 'newsletter'],
'Health or fitness': ['exercise', 'fitness', 'run', 'sleep', 'health', 'workout', 'diet', 'training'],
'Business or launch': ['launch', 'business', 'product', 'client', 'sales', 'marketing', 'offer', 'startup'],
'Family or home': ['family', 'home', 'parent', 'kid', 'child', 'house', 'routine'],
}

BLOCKER_RULES = {
'Clarity gap around what done looks like': ['unclear', 'not sure', 'vague', 'confused'],
'Time availability and calendar protection': ['busy', 'time', 'schedule', 'calendar'],
'Missing information, research, or examples': ['research', 'information', 'data', 'example'],
'Skill or confidence gap': ['new', 'learn', 'practice', 'confidence', 'skill'],
'Budget, tools, or resource access': ['money', 'budget', 'tool', 'software', 'equipment'],
'Coordination with other people': ['team', 'manager', 'client', 'partner', 'family'],
}


def _extract_time_horizon(text: str) -> str:
    lower = text.lower()
    patterns = [
        r'by ([a-z0-9\- ]+)',
        r'in (\d+\s+(?:day|days|week|weeks|month|months))',
        r'within (\d+\s+(?:day|days|week|weeks|month|months))',
    ]
    for pattern in patterns:
        match = re.search(pattern, lower)
        if match:
            return match.group(0)
    for token in ['today', 'tomorrow', 'this week', 'next week', 'this month', 'next month', 'this quarter', 'next quarter']:
        if token in lower:
            return token
    return ''


def _goal_milestones(goal_type: str, unclear: bool) -> List[str]:
    if unclear:
        return [
            'Clarify the outcome, success criteria, and review horizon before doing more work.',
            'Name the first milestone and the minimum resources needed to start it.',
            'Run a short execution cycle, then review scope, pace, and blockers.',
        ]
    mapping = {
        'Learning or study': [
            'Define the exact skill target, scope, and baseline level.',
            'Build a repeatable practice plan and complete the first learning block.',
            'Test understanding in a real output, drill, or exam-style checkpoint.',
        ],
        'Writing or shipping': [
            'Lock the core message, audience, and outline of the deliverable.',
            'Complete a rough draft or first shippable version without over-editing.',
            'Revise, polish, and deliver or publish with a feedback checkpoint.',
        ],
        'Health or fitness': [
            'Define the target behavior and the smallest repeatable routine.',
            'Set up the environment, schedule, and tracking needed for consistency.',
            'Review results after the first week and adjust load or frequency.',
        ],
        'Business or launch': [
            'Define the offer, audience, and concrete launch outcome.',
            'Build the minimum assets, process, or prototype needed to test it.',
            'Run a first launch or outreach cycle and review the signal honestly.',
        ],
        'Family or home': [
            'Clarify the desired outcome, who is affected, and what must change first.',
            'Prepare the first small system, routine, or decision that reduces friction.',
            'Review what held up in real life and simplify the next round.',
        ],
    }
    return mapping.get(goal_type, [
        'Define what success looks like and what the first milestone actually is.',
        'Complete the first milestone with a simple, time-bounded plan.',
        'Review progress, blockers, and the next stretch of work.',
    ])


def _goal_actions(goal_type: str, unclear: bool, goal: str) -> List[str]:
    if unclear:
        return [
            'Clarify the outcome by writing one sentence that defines what done looks like.',
            'List the first milestone, the time available this week, and the main blocker.',
            'Schedule one 25-minute session to start the smallest useful action.',
        ]
    mapping = {
        'Learning or study': [
            'Define the exact topic, level, and review date for the learning goal.',
            'Choose one resource and complete the first focused study block.',
            'Practice by solving one exercise, quiz, or mini-project today.',
        ],
        'Writing or shipping': [
            'Define the audience, promise, and rough outline of the deliverable.',
            'Draft the ugliest usable first version of the opening or core section.',
            'Schedule one revision pass with a clear finish line.',
        ],
        'Health or fitness': [
            'Define the smallest version of the routine you can repeat this week.',
            'Prepare the environment, gear, or trigger that removes startup friction.',
            'Start one short session today and log how it felt afterward.',
        ],
        'Business or launch': [
            'Define the offer, audience, and success metric for the first test.',
            'List the minimum assets or conversations needed before launch.',
            'Start one concrete build or outreach task that creates real signal.',
        ],
        'Family or home': [
            'Define the one outcome that would make daily life feel easier.',
            'List who needs to be involved and what decision must happen first.',
            'Start one small setup task that reduces friction today.',
        ],
    }
    return mapping.get(goal_type, [
        'Define the first milestone in one sentence.',
        'List the smallest actions that move the milestone forward.',
        'Schedule the first work block on the calendar.',
    ])


def handle(inputs):
    meta = _load_skill_meta('goal-chunking-helper')
    data = _coerce_dict(inputs)
    text = _normalize_inputs(inputs)
    lower = text.lower()

    goal = _pick_text(data, ['goal', 'outcome', 'objective', 'project'], _shorten(text, 120) or 'Clarify the real goal before execution')
    why = _pick_text(data, ['why', 'reason', 'importance', 'motivation'], 'Reduce overwhelm and create a path that is easier to start.')
    horizon = _pick_text(data, ['deadline', 'time_horizon', 'review_horizon', 'review', 'by'], _extract_time_horizon(text)) or 'Set a review point within the next 1 to 4 weeks.'
    goal_type = _detect_one(text, GOAL_TYPE_RULES, 'General')
    unclear = len(goal.split()) < 4 or any(token in goal.lower() for token in ['something', 'better', 'figure it out', 'improve life'])
    milestones = _goal_milestones(goal_type, unclear)
    actions = _goal_actions(goal_type, unclear, goal)
    dependencies = _listify(data.get('dependencies')) or _detect_many(text, BLOCKER_RULES, [
        'Time availability and calendar protection',
        'Missing information, research, or examples',
        'A realistic review checkpoint',
    ], limit=4)
    if any(token in lower for token in ['today', 'tomorrow', 'this week']) and goal_type in ['Learning or study', 'Writing or shipping', 'Business or launch']:
        if 'Timeline compression, which may require a smaller first milestone' not in dependencies:
            dependencies.append('Timeline compression, which may require a smaller first milestone')

    lines: List[str] = []
    lines.append('# Goal Breakdown')
    lines.append('')
    lines.append('## Goal Definition')
    lines.append(f'- Goal: {goal}')
    lines.append(f'- Why it matters: {why}')
    lines.append(f'- Time horizon: {horizon}')
    lines.append('')
    lines.append('## Milestone Ladder')
    for idx, milestone in enumerate(milestones, 1):
        lines.append(f'{idx}. {milestone}')
    lines.append('')
    lines.append('## Next Actions')
    for idx, action in enumerate(actions[:3], 1):
        lines.append(f'- Action {idx}: {action}')
    lines.append('')
    lines.append('## Dependencies and Risks')
    for item in dependencies[:5]:
        lines.append(f'- {item}')
    if 'Set a review point within the next 1 to 4 weeks.' in horizon:
        checkpoint = 'the next review date'
    else:
        checkpoint = horizon
    lines.append('')
    lines.append('## Review Checkpoint')
    lines.append(f'- Progress is real if, by {checkpoint}, milestone 1 is complete, the next actions are scheduled, and the main blocker is named.')
    return '\n'.join(lines)

if __name__ == "__main__":
    payload = sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read()
    print(handle(payload))
