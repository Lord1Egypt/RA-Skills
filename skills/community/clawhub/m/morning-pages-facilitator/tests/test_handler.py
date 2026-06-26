#!/usr/bin/env python3
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from handler import handle


def test_five_minute_freeze_context_sets_short_container():
    output = handle('I freeze on page one and only have 5 minutes before the kids wake up')
    assert '# Morning Pages Session' in output
    assert '- Time or page target: 5 minutes' in output
    assert 'What I do not want to write is' in output


def test_dict_input_preserves_page_target_and_focus():
    output = handle({
        'page_target': '3 pages',
        'focus': 'career anxiety'
    })
    assert '- Time or page target: 3 pages' in output
    assert 'career anxiety' in output


def test_output_contains_after_writing_closure():
    output = handle('I keep trying to make my morning pages sound polished')
    assert '## After Writing' in output
    assert '- One next action, if any:' in output


if __name__ == '__main__':
    for name, fn in list(globals().items()):
        if name.startswith('test_') and callable(fn):
            fn()
    print('All tests passed.')
