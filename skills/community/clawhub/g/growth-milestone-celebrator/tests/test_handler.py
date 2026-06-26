#!/usr/bin/env python3
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from handler import handle


def test_streak_context_detects_consistency_category():
    output = handle('I kept a 10-day walking streak even after a rough week')
    assert '# Growth Milestone Record' in output
    assert '- Category: Consistency' in output


def test_dict_input_preserves_milestone_and_evidence():
    output = handle({
        'milestone': 'Restarted my study habit after missing a week',
        'category': 'Recovery',
        'evidence': 'Studied 4 days this week instead of quitting'
    })
    assert 'Restarted my study habit after missing a week' in output
    assert 'Studied 4 days this week instead of quitting' in output
    assert '- Category: Recovery' in output


def test_output_contains_celebration_and_next_step():
    output = handle('I finally asked for help on a hard project instead of hiding it')
    assert '## Celebration' in output
    assert '- To build on this, I will:' in output


if __name__ == '__main__':
    for name, fn in list(globals().items()):
        if name.startswith('test_') and callable(fn):
            fn()
    print('All tests passed.')
