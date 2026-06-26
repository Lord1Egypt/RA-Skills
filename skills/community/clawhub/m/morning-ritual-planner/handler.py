#!/usr/bin/env python3
import json
import os
import re
import sys
from typing import Any, List, Tuple


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
    try:
        return json.dumps(inputs, ensure_ascii=False, sort_keys=True)
    except TypeError:
        return str(inputs)


def _dedupe(items: List[str]) -> List[str]:
    seen = set()
    ordered: List[str] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            ordered.append(item)
    return ordered


FEELING_RULES = {
    'calm and grounded': ['calm', 'peace', 'grounded', 'gentle', 'steady', 'soft'],
    'focused and clear': ['focus', 'focused', 'clarity', 'clear', 'productive', 'sharp'],
    'energized and upbeat': ['energ', 'active', 'wake up', 'wake-up', 'strong', 'workout', 'upbeat'],
}

ANCHOR_RULES = [
    ('after school drop-off', ['drop-off', 'school run', 'school drop off']),
    ('brush teeth', ['brush teeth', 'toothbrush', 'brushing']),
    ('make coffee', ['coffee', 'espresso']),
    ('make tea', ['tea', 'kettle']),
    ('drink water', ['drink water', 'water bottle', 'glass of water']),
    ('get out of bed', ['get out of bed', 'wake up', 'alarm']),
]

CONSTRAINT_RULES = [
    ('Caregiving or school logistics may interrupt the flow.', ['kids', 'kid', 'child', 'children', 'caregiver', 'school']),
    ('The morning needs a fast handoff into commute or work.', ['commute', 'office', 'train', 'out the door', 'meeting']),
    ('Energy may be limited after poor sleep.', ['poor sleep', 'tired', 'exhausted', 'sleep deprived', 'slept poorly']),
    ('A rotating or variable schedule may need multiple versions.', ['rotating', 'shift', 'variable schedule', 'different every day']),
]

RITUAL_TEMPLATES = {
    'calm and grounded': [
        ('Drink water and open the curtains', 'It wakes the body gently and gives the morning a visible starting point.'),
        ('Take two slow minutes for breathing, prayer, or silence', 'It lowers mental noise before the day begins to pull on you.'),
        ('Do light stretching or slow mobility', 'It turns stiffness into steadiness without needing much willpower.'),
        ('Write the one thing that matters most today', 'It keeps the day intentional instead of reactive.'),
        ('Have tea and read one quiet page or journal a few lines', 'It adds a human rhythm instead of a rushed mechanical start.'),
        ('Take a longer walk or reflective journaling block', 'It deepens the sense of grounded momentum when time allows.'),
    ],
    'focused and clear': [
        ('Drink water and stand in bright light', 'It helps the brain switch into awake mode quickly.'),
        ('Review today\'s top priority', 'It protects focus before notifications take over.'),
        ('Do quick mobility or a brisk walk', 'It raises alertness without turning the morning into a full workout.'),
        ('Write three lines in a notebook', 'It clears mental tabs and reduces background clutter.'),
        ('Preview the first work or study block', 'It makes the next meaningful action obvious.'),
        ('Do a longer planning or learning block', 'It converts spare time into deliberate progress.'),
    ],
    'energized and upbeat': [
        ('Drink water and turn on bright light or upbeat music', 'It gives the body a quick activation signal.'),
        ('Take three deep breaths while standing tall', 'It creates a physical shift without adding complexity.'),
        ('Do mobility, a brisk walk, or light cardio', 'It builds energy fast and prevents a sluggish start.'),
        ('Use a quick shower or face splash reset', 'It sharpens the transition from sleepy to ready.'),
        ('Add a short workout or protein-forward breakfast step', 'It makes the energy boost more durable.'),
        ('Do a fuller movement block before the day opens up', 'It uses the longer window for real momentum instead of scatter.'),
    ],
}

DURATION_MAP = {
    10: [2, 3, 5],
    20: [2, 3, 5, 10],
    30: [2, 3, 5, 8, 12],
    45: [2, 3, 10, 10, 8, 12],
}

LAYER_LABELS = ['Must-do', 'Must-do', 'Nice-to-have', 'Nice-to-have', 'Bonus', 'Bonus']


class MorningRitualPlanner:
    def __init__(self, inputs: Any):
        self.raw = _normalize_inputs(inputs)
        self.lower = self.raw.lower()
        self.time_budget = self._extract_time_budget()
        self.wake_time = self._extract_wake_time()
        self.anchor = self._detect_anchor()
        self.desired_feeling = self._detect_feeling()
        self.constraints = self._detect_constraints()
        self.sequence = self._build_sequence()
        self.prep_steps = self._night_before_prep()
        self.fallback = self._fallback_version()

    def _extract_time_budget(self) -> int:
        match = re.search(r'(\d{1,2})\s*(?:minutes|minute|mins|min)\b', self.lower)
        if match:
            return int(match.group(1))
        if any(word in self.lower for word in ['quick', 'tiny window', 'short', 'tight']):
            return 10
        if any(word in self.lower for word in ['half hour', '30 minute', '30-minute']):
            return 30
        if any(word in self.lower for word in ['long', 'full routine', '45 minute', '45-minute']):
            return 45
        return 20

    def _extract_wake_time(self) -> str:
        match = re.search(r'(?:wake(?: up)?(?: at| around| by)?|alarm(?: for)?|up by)\s*(\d{1,2}(?::\d{2})?\s*(?:am|pm)?)', self.lower)
        if match:
            return match.group(1).strip()
        return 'Not specified'

    def _detect_anchor(self) -> str:
        for label, keywords in ANCHOR_RULES:
            if any(keyword in self.lower for keyword in keywords):
                return label
        return 'get out of bed'

    def _detect_feeling(self) -> str:
        for label, keywords in FEELING_RULES.items():
            if any(keyword in self.lower for keyword in keywords):
                return label
        return 'calm and grounded'

    def _detect_constraints(self) -> List[str]:
        found = [message for message, keywords in CONSTRAINT_RULES if any(keyword in self.lower for keyword in keywords)]
        if self.time_budget <= 10:
            found.append('The routine has to fit a genuinely small morning window.')
        if not found:
            found.append('No major morning constraint was specified, so the routine stays simple and flexible.')
        return _dedupe(found)

    def _bucket(self) -> int:
        if self.time_budget <= 10:
            return 10
        if self.time_budget <= 20:
            return 20
        if self.time_budget <= 30:
            return 30
        return 45

    def _build_sequence(self) -> List[Tuple[str, str, int, str]]:
        template = RITUAL_TEMPLATES[self.desired_feeling]
        durations = DURATION_MAP[self._bucket()]
        sequence: List[Tuple[str, str, int, str]] = []
        for index, duration in enumerate(durations):
            activity, why = template[index]
            layer = LAYER_LABELS[index]
            sequence.append((layer, activity, duration, why))
        return sequence

    def _night_before_prep(self) -> List[str]:
        prep = [
            'Lay out the first object the ritual needs, such as clothes, notebook, water bottle, or mat.',
            'Decide what the first screen boundary is, so the morning does not begin inside notifications.',
        ]
        if self.anchor in ('make coffee', 'make tea'):
            prep.append('Set out the mug, kettle, and coffee or tea setup before bed.')
        elif self.anchor == 'brush teeth':
            prep.append('Place a filled water bottle or notebook near the sink so the next step is automatic.')
        elif self.anchor == 'after school drop-off':
            prep.append('Pack bags, clothes, and anything needed for the school handoff the night before.')
        else:
            prep.append('Choose the first two ritual steps in advance so there is no morning negotiation.')
        return prep

    def _fallback_version(self) -> str:
        if any('poor sleep' in item.lower() or 'energy may be limited' in item.lower() for item in self.constraints):
            return 'keep only water, three slow breaths, and the first must-do step, then skip every bonus item without guilt.'
        if self.time_budget <= 10:
            return 'keep only the anchor, one calming or energizing reset, and the first priority cue.'
        return 'compress the ritual into a 3 minute version: anchor, water, one short reset, and a single next-step cue.'

    def render(self) -> str:
        lines: List[str] = []
        lines.append('# Morning Ritual Plan')
        lines.append('')
        lines.append('## Goal')
        lines.append(f'- Desired morning feeling: {self.desired_feeling}')
        lines.append(f'- Available time: {self.time_budget} minutes')
        lines.append(f'- Wake-up anchor: {self.anchor}')
        lines.append(f'- Real wake time: {self.wake_time}')
        lines.append(f"- Real-world constraints: {'; '.join(self.constraints)}")
        lines.append('')
        lines.append('## Ritual Sequence')
        for index, (layer, activity, duration, why) in enumerate(self.sequence, 1):
            lines.append(f'{index}. [{layer}] {activity} - {duration} min - {why}')
        lines.append('')
        lines.append('## Night-Before Prep')
        for item in self.prep_steps:
            lines.append(f'- {item}')
        lines.append('')
        lines.append('## Fallback Version')
        lines.append(f'- If I woke late or slept poorly, I will: {self.fallback}')
        lines.append('')
        lines.append('## Weekly Review')
        lines.append('- What felt easy?')
        lines.append('- What created friction?')
        lines.append('- What should be shortened, moved, or removed?')
        return '\n'.join(lines)


def handle(inputs):
    _load_skill_meta('morning-ritual-planner')
    planner = MorningRitualPlanner(inputs)
    return planner.render()


if __name__ == '__main__':
    payload = sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read()
    print(handle(payload))
