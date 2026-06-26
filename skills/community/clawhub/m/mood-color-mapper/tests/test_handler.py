#!/usr/bin/env python3
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from handler import MoodColorMapper, handle


def test_explicit_primary_color_detection():
    mapper = MoodColorMapper('I feel dark blue today and a little gray underneath it.')
    assert mapper.primary_color == 'blue'
    assert mapper.secondary_color == 'gray'


def test_need_statement_exists():
    mapper = MoodColorMapper('I feel anxious and wired, like bright yellow all over.')
    assert 'grounding' in mapper.likely_need.lower() or 'reassurance' in mapper.likely_need.lower()


def test_output_sections():
    output = handle('My mood feels red and tense after a hard day.')
    assert output.startswith('# Mood Color Map')
    assert '## What the Body Is Saying' in output
    assert '## Likely Need' in output
    assert 'One action under 10 minutes' in output


if __name__ == '__main__':
    for name, fn in list(globals().items()):
        if name.startswith('test_') and callable(fn):
            fn()
    print('All tests passed.')
