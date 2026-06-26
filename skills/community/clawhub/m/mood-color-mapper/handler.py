#!/usr/bin/env python3
import json
import os
import re
import sys
from typing import Any, Dict, List


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


COLOR_ORDER = ['blue', 'gray', 'grey', 'red', 'orange', 'yellow', 'green', 'purple', 'pink', 'black', 'white']

COLOR_EMOTIONS = {
    'blue': ['sad', 'tender', 'tired'],
    'gray': ['flat', 'numb', 'drained'],
    'grey': ['flat', 'numb', 'drained'],
    'red': ['angry', 'overloaded', 'activated'],
    'orange': ['frustrated', 'driven', 'restless'],
    'yellow': ['anxious', 'buzzing', 'alert'],
    'green': ['calm', 'steady', 'safe'],
    'purple': ['reflective', 'complex', 'sensitive'],
    'pink': ['soft', 'connected', 'comfort-seeking'],
    'black': ['heavy', 'shut down', 'overwhelmed'],
    'white': ['blank', 'spaced out', 'quiet'],
}

COLOR_NEEDS = {
    'blue': 'Rest, comfort, and a slower pace.',
    'gray': 'Gentle activation plus low-pressure care.',
    'grey': 'Gentle activation plus low-pressure care.',
    'red': 'Space, release, and a reduction in stimulation.',
    'orange': 'Movement, expression, and a clean boundary.',
    'yellow': 'Reassurance, grounding, and less mental noise.',
    'green': 'Protection of calm and steady routines.',
    'purple': 'Reflection, expression, and emotional room.',
    'pink': 'Warmth, softness, and relational safety.',
    'black': 'Containment, grounding, and support.',
    'white': 'Orientation, hydration, and a gentle return to the body.',
}

BODY_CUES = [
    ('tight chest or shallow breathing', ['chest', 'breath', 'breathing', 'tight']),
    ('heavy shoulders or body weight', ['heavy', 'slump', 'shoulder', 'tired', 'drained']),
    ('buzzing or restless energy', ['restless', 'buzzing', 'antsy', 'wired', 'jittery']),
    ('warmth, tension, or pressure', ['angry', 'heat', 'tense', 'pressure', 'frustrated']),
    ('softness or emotional tenderness', ['tender', 'tear', 'cry', 'soft', 'sad']),
    ('steady breathing and lower urgency', ['calm', 'steady', 'grounded', 'peaceful']),
]

INTENSITY_HIGH = ['very', 'intense', 'overwhelmed', 'panic', 'panicky', 'furious', 'extreme']
INTENSITY_LOW = ['slightly', 'a bit', 'soft', 'gentle', 'light', 'pale']

INFERRED_COLOR_RULES = [
    ('red', ['angry', 'rage', 'furious', 'overloaded']),
    ('yellow', ['anxious', 'nervous', 'restless', 'wired']),
    ('blue', ['sad', 'down', 'tearful', 'tired']),
    ('gray', ['numb', 'flat', 'drained', 'empty']),
    ('green', ['calm', 'steady', 'grounded', 'safe']),
    ('purple', ['mixed', 'complex', 'reflective']),
]


class MoodColorMapper:
    def __init__(self, inputs: Any):
        self.raw = _normalize_inputs(inputs)
        self.lower = self.raw.lower()
        self.primary_color, self.secondary_color = self._detect_palette()
        self.intensity = self._detect_intensity()
        self.body_note = self._body_note()
        self.emotion_words = self._emotion_words()
        self.likely_need = self._likely_need()
        self.next_step = self._next_step()

    def _explicit_colors(self) -> List[str]:
        found: List[str] = []
        for color in COLOR_ORDER:
            pattern = rf'\b{color}\b'
            if re.search(pattern, self.lower):
                normalized = 'gray' if color == 'grey' else color
                if normalized not in found:
                    found.append(normalized)
        return found

    def _detect_palette(self) -> List[str]:
        explicit = self._explicit_colors()
        if explicit:
            if len(explicit) == 1 and any(word in self.lower for word in ['mixed', 'and', 'but']) and explicit[0] not in ['gray', 'purple']:
                return [explicit[0], 'gray']
            return [explicit[0], explicit[1] if len(explicit) > 1 else '']
        inferred: List[str] = []
        for color, words in INFERRED_COLOR_RULES:
            if any(word in self.lower for word in words):
                inferred.append(color)
        if not inferred:
            inferred = ['blue'] if any(word in self.lower for word in ['low energy', 'quiet']) else ['green']
        if len(inferred) == 1 and any(word in self.lower for word in ['and', 'but', 'mixed']) and inferred[0] != 'gray':
            inferred.append('gray')
        unique: List[str] = []
        for color in inferred:
            if color not in unique:
                unique.append(color)
        return [unique[0], unique[1] if len(unique) > 1 else '']

    def _detect_intensity(self) -> str:
        if any(word in self.lower for word in INTENSITY_HIGH):
            return 'High'
        if any(word in self.lower for word in INTENSITY_LOW):
            return 'Low'
        if self.primary_color in ['red', 'black']:
            return 'High'
        return 'Medium'

    def _body_note(self) -> str:
        cues = [label for label, words in BODY_CUES if any(word in self.lower for word in words)]
        if cues:
            return '; '.join(cues[:2])
        defaults = {
            'blue': 'Energy feels lower and the body may want softness or rest.',
            'gray': 'The body may feel muted, low-drive, or hard to read clearly.',
            'red': 'The body may be carrying heat, pressure, or urgency.',
            'yellow': 'The body may feel buzzy, alert, or hard to settle.',
            'green': 'Breathing and body tension may be steadier than the mind expects.',
            'purple': 'The body may be holding more than one feeling at once.',
            'black': 'The body may need grounding and a sense of safety first.',
        }
        return defaults.get(self.primary_color, 'The body may be carrying a signal that needs gentle attention.')

    def _emotion_words(self) -> str:
        words: List[str] = []
        for color in [self.primary_color, self.secondary_color]:
            if color:
                for item in COLOR_EMOTIONS[color]:
                    if item not in words:
                        words.append(item)
        return ', '.join(words[:5])

    def _likely_need(self) -> str:
        primary_need = COLOR_NEEDS[self.primary_color]
        if self.secondary_color:
            secondary_need = COLOR_NEEDS[self.secondary_color]
            if secondary_need != primary_need:
                return f'{primary_need} Secondary need: {secondary_need}'
        return primary_need

    def _next_step(self) -> str:
        if self.primary_color in ['red', 'yellow', 'black'] or self.intensity == 'High':
            return 'Take 3 slow breaths, unclench your shoulders, and step away from extra stimulation for 5 minutes.'
        if self.primary_color in ['blue', 'gray']:
            return 'Choose one low-effort care move, like water, a blanket, a short walk, or a quiet note to yourself.'
        if self.primary_color == 'green':
            return 'Protect this steadier state for 5 more minutes before switching contexts.'
        return 'Write one sentence or draw one small color note about what this feeling is trying to say.'

    def render(self) -> str:
        lines: List[str] = []
        lines.append('# Mood Color Map')
        lines.append('')
        lines.append('## Current Palette')
        lines.append(f'- Primary color: {self.primary_color}')
        lines.append(f"- Secondary color, if any: {self.secondary_color or 'None'}")
        lines.append(f'- Intensity level: {self.intensity}')
        lines.append('')
        lines.append('## What the Body Is Saying')
        lines.append(f'- {self.body_note}')
        lines.append('')
        lines.append('## Possible Emotion Words')
        lines.append(f'- {self.emotion_words}')
        lines.append('')
        lines.append('## Likely Need')
        lines.append(f'- {self.likely_need}')
        lines.append('')
        lines.append('## Gentle Next Step')
        lines.append(f'- One action under 10 minutes: {self.next_step}')
        return '\n'.join(lines)


def handle(inputs):
    _load_skill_meta('mood-color-mapper')
    mapper = MoodColorMapper(inputs)
    return mapper.render()


if __name__ == '__main__':
    payload = sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read()
    print(handle(payload))
