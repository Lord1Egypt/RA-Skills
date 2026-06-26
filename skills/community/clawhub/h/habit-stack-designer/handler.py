#!/usr/bin/env python3
import json
import os
import re
import sys
from typing import Any, Dict, List, Tuple


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


HABIT_RULES: List[Tuple[str, List[str]]] = [
    ('meditation', ['meditate', 'meditation']),
    ('reading', ['read', 'reading', 'book']),
    ('stretching', ['stretch', 'mobility', 'yoga']),
    ('journaling', ['journal', 'write']),
    ('studying', ['study', 'revision', 'homework', 'practice problem']),
    ('hydration', ['drink water', 'hydration', 'water']),
    ('walking', ['walk', 'steps']),
    ('tidying', ['tidy', 'declutter', 'clean up']),
    ('flossing', ['floss']),
]

ANCHOR_RULES: List[Tuple[str, List[str], str]] = [
    ('brush my teeth', ['brush my teeth', 'toothbrush', 'brushing'], 'It already happens in a fixed place and rarely gets skipped.'),
    ('make coffee or tea', ['coffee', 'tea', 'kettle'], 'It is a repeatable ritual that naturally creates a transition point.'),
    ('sit at my desk', ['open my laptop', 'sit at my desk', 'desk'], 'It happens near the exact moment focus is needed.'),
    ('finish lunch', ['after lunch', 'lunch'], 'It is a clear daily event with a stable sequence.'),
    ('take a shower', ['shower'], 'It is anchored to a physical environment and hard to forget.'),
    ('finish dinner', ['after dinner', 'dinner'], 'It gives the habit a predictable evening landing spot.'),
    ('put my phone on the charger', ['charger', 'charge my phone', 'plug in my phone'], 'It creates a strong bedtime cue with a visible object.'),
]

TINY_HABITS = {
    'meditation': 'take 3 slow breaths with eyes closed',
    'reading': 'read one page',
    'stretching': 'do 60 seconds of stretching',
    'journaling': 'write one sentence',
    'studying': 'open the material and solve one small problem',
    'hydration': 'take 5 sips of water',
    'walking': 'walk for 2 minutes',
    'tidying': 'put away 3 items',
    'flossing': 'floss one tooth',
}

RESCUE_HABITS = {
    'meditation': 'take one slow breath and call it a win.',
    'reading': 'read one sentence and stop if needed.',
    'stretching': 'do one stretch for 10 seconds.',
    'journaling': 'write three words about the day.',
    'studying': 'open the book or file and look at one question.',
    'hydration': 'take one sip of water.',
    'walking': 'stand up and take ten steps.',
    'tidying': 'put away one item.',
    'flossing': 'floss one tooth.',
}

WHY_TEMPLATES = {
    'meditation': 'It helps you create a calmer start and better attention.',
    'reading': 'It helps you stay in contact with ideas instead of waiting for a perfect long block.',
    'stretching': 'It reduces stiffness and makes movement easier to begin.',
    'journaling': 'It helps you clear mental clutter and notice your own patterns.',
    'studying': 'It protects consistent learning over last-minute cramming.',
    'hydration': 'It supports energy and makes the habit almost frictionless.',
    'walking': 'It builds movement into ordinary life without needing a full workout.',
    'tidying': 'It lowers visual friction and keeps the space easier to use.',
    'flossing': 'It makes oral care automatic instead of optional.',
}


class HabitStackDesigner:
    def __init__(self, inputs: Any):
        self.raw = _normalize_inputs(inputs)
        self.lower = self.raw.lower()
        self.target_habit = self._extract_target_habit()
        self.why = self._extract_why()
        self.anchor, self.anchor_reason = self._extract_anchor()
        self.tiny_habit = TINY_HABITS[self.target_habit]
        self.stack_formula = f'After I {self.anchor}, I will {self.tiny_habit}.'
        self.friction_removal = self._friction_removal()
        self.reward = self._reward_loop()
        self.rescue_version = RESCUE_HABITS[self.target_habit]

    def _extract_target_habit(self) -> str:
        for label, keywords in HABIT_RULES:
            if any(keyword in self.lower for keyword in keywords):
                return label
        return 'journaling'

    def _extract_why(self) -> str:
        match = re.search(r'(?:because|so that)\s+(.+?)(?:[.?!]|$)', self.raw, flags=re.IGNORECASE)
        if match:
            return match.group(1).strip()
        return WHY_TEMPLATES[self.target_habit]

    def _extract_anchor(self) -> Tuple[str, str]:
        for label, keywords, reason in ANCHOR_RULES:
            if any(keyword in self.lower for keyword in keywords):
                if any(word in self.lower for word in ['shift', 'rotating', 'irregular']):
                    reason = reason + ' It is also place-based, which helps when the schedule changes.'
                return label, reason
        return 'brush my teeth', 'It already happens daily and gives the new habit a strong physical cue.'

    def _friction_removal(self) -> str:
        if self.target_habit == 'reading':
            return 'Keep the book where the anchor happens and stop choosing the next page in advance.'
        if self.target_habit == 'meditation':
            return 'Put a cushion, chair, or visual cue exactly where the anchor ends.'
        if self.target_habit == 'stretching':
            return 'Lay out a mat or choose one default stretch so there is no decision cost.'
        if self.target_habit == 'journaling':
            return 'Keep the notebook open with a pen ready at the anchor location.'
        return 'Prepare the smallest required tool before the anchor happens so the habit starts in one motion.'

    def _reward_loop(self) -> Dict[str, str]:
        return {
            'immediate': 'Mark one check, say "done," and enjoy the quick feeling of completion before moving on.',
            'weekly': 'Review the stack once at the end of the week and only scale it if it felt easy to repeat.',
        }

    def render(self) -> str:
        lines: List[str] = []
        lines.append('# Habit Stack Design')
        lines.append('')
        lines.append('## New Habit')
        lines.append(f'- Target habit: {self.target_habit}')
        lines.append(f'- Why it matters: {self.why}')
        lines.append('')
        lines.append('## Best Anchor')
        lines.append(f'- Existing routine: {self.anchor}')
        lines.append(f'- Why it is reliable: {self.anchor_reason}')
        lines.append('')
        lines.append('## Stack Formula')
        lines.append(f'- {self.stack_formula}')
        lines.append('')
        lines.append('## Friction Removal')
        lines.append(f'- {self.friction_removal}')
        lines.append('')
        lines.append('## Reward Loop')
        lines.append(f"- Immediate reward: {self.reward['immediate']}")
        lines.append(f"- Weekly review cue: {self.reward['weekly']}")
        lines.append('')
        lines.append('## Rescue Version')
        lines.append(f'- Minimum version for hard days: {self.rescue_version}')
        return '\n'.join(lines)


def handle(inputs):
    _load_skill_meta('habit-stack-designer')
    designer = HabitStackDesigner(inputs)
    return designer.render()


if __name__ == '__main__':
    payload = sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read()
    print(handle(payload))
