#!/usr/bin/env python3
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from handler import handle


def test_string_input_generates_goal_breakdown():
    output = handle('I want to launch a small course by next month')
    assert '# Goal Breakdown' in output
    assert '## Milestone Ladder' in output
    assert '## Next Actions' in output


def test_dict_input_preserves_goal_details():
    output = handle({
        'goal': 'Finish a writing portfolio',
        'why': 'Apply for new roles with stronger samples',
        'deadline': 'in 6 weeks'
    })
    assert 'Finish a writing portfolio' in output
    assert 'Apply for new roles with stronger samples' in output
    assert 'in 6 weeks' in output


def test_output_contains_action_slots_and_dependencies():
    output = handle('Learn Python for data analysis this quarter')
    assert '- Action 1:' in output
    assert '- Action 2:' in output
    assert '## Dependencies and Risks' in output


if __name__ == '__main__':
    for name, fn in list(globals().items()):
        if name.startswith('test_') and callable(fn):
            fn()
    print('All tests passed.')
