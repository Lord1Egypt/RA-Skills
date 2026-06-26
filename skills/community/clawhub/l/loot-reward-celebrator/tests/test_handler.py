#!/usr/bin/env python3
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from handler import handle


def test_low_budget_health_friendly_reward_is_suggested():
    result = handle({
        'skill_name': 'loot-reward-celebrator',
        'input': {
            'completed_task': 'Finished 7 days of exercise',
            'effort': 'I showed up even when I was tired',
            'budget': '20',
            'values': 'health, budget-conscious',
        },
    })['result']
    assert 'Loot Table' in result
    assert 'low-cost' in result.lower()
    assert 'health backlash' in result.lower()


def test_next_unlock_condition_exists():
    result = handle({'skill_name': 'loot-reward-celebrator', 'input': 'Completed task: submitted the application\nBudget: medium'})['result']
    assert 'Next Unlock Condition' in result
    assert 'submitted the application' in result


def test_prompt_mode_returns_template():
    result = handle({'skill_name': 'loot-reward-celebrator', 'mode': 'prompt'})['result']
    assert 'earned loot' in result.lower()
    assert 'budget' in result.lower()


if __name__ == '__main__':
    for name, fn in list(globals().items()):
        if name.startswith('test_') and callable(fn):
            fn()
    print('All tests passed.')
