#!/usr/bin/env python3
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from handler import MorningRitualPlanner, handle


def test_time_budget_detection():
    planner = MorningRitualPlanner('I only have 10 minutes before the school run.')
    assert planner.time_budget == 10


def test_anchor_detection():
    planner = MorningRitualPlanner('After I make coffee I want a calmer start to the day.')
    assert planner.anchor == 'make coffee'


def test_output_sections():
    output = handle('I want a focused 20 minute routine after I brush my teeth.')
    assert output.startswith('# Morning Ritual Plan')
    assert '## Fallback Version' in output
    assert '## Weekly Review' in output


if __name__ == '__main__':
    for name, fn in list(globals().items()):
        if name.startswith('test_') and callable(fn):
            fn()
    print('All tests passed.')
