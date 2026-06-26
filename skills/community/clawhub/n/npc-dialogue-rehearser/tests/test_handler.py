#!/usr/bin/env python3
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from handler import handle


def test_authority_branch_is_selected_for_teacher_case():
    result = handle({
        'skill_name': 'npc-dialogue-rehearser',
        'input': {
            'scenario': 'I need to ask for a two-day extension on an essay.',
            'counterpart': 'teacher',
            'goal': 'request a two-day extension',
            'worry': 'They may think I am making excuses.',
            'tone': 'respectful and direct',
        },
    })['result']
    assert 'Authority NPC' in result
    assert 'Opening Line' in result
    assert 'request a two-day extension' in result


def test_safety_note_appears_for_high_risk_language():
    result = handle({
        'skill_name': 'npc-dialogue-rehearser',
        'input': {
            'scenario': 'I need wording for an abusive partner who has become threatening.',
            'counterpart': 'partner',
            'goal': 'state a boundary',
        },
    })['result']
    assert 'Safety Note' in result


def test_prompt_mode_returns_template():
    result = handle({'skill_name': 'npc-dialogue-rehearser', 'mode': 'prompt'})['result']
    assert 'conversation' in result.lower()
    assert 'three short response branches' in result


if __name__ == '__main__':
    for name, fn in list(globals().items()):
        if name.startswith('test_') and callable(fn):
            fn()
    print('All tests passed.')
