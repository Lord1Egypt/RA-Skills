#!/usr/bin/env python3
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from handler import HabitStackDesigner, handle


def test_target_habit_detection():
    designer = HabitStackDesigner('I want to meditate every day because I need a calmer start.')
    assert designer.target_habit == 'meditation'


def test_anchor_detection():
    designer = HabitStackDesigner('I want to read more after I brush my teeth each night.')
    assert designer.anchor == 'brush my teeth'


def test_output_sections():
    output = handle('I want to meditate after I brush my teeth because I need a calmer start.')
    assert output.startswith('# Habit Stack Design')
    assert 'After I brush my teeth, I will' in output
    assert '## Rescue Version' in output


if __name__ == '__main__':
    for name, fn in list(globals().items()):
        if name.startswith('test_') and callable(fn):
            fn()
    print('All tests passed.')
