#!/usr/bin/env python3
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from handler import PricingStrategyAdvisor, handle


def test_objective_detection_discount():
    advisor = PricingStrategyAdvisor('Our coupon cadence is out of control and markdowns are hurting margin.')
    assert advisor.objective == 'Discount Discipline'


def test_signal_detection_competitor_and_channel():
    advisor = PricingStrategyAdvisor('We face competitor pressure on Amazon and need better marketplace parity.')
    assert 'Competitor Pressure' in advisor.signals
    assert 'Channel Conflict' in advisor.signals


def test_dict_input_supported():
    output = handle({
        'objective': 'margin recovery',
        'prices': ['current price 129', 'target margin 62%'],
        'signals': ['cost increase', 'conversion sensitivity'],
        'notes': 'Need a recommendation before next quarter planning.',
    })
    assert '# Pricing Strategy Advisor Brief' in output
    assert '## Recommended Moves' in output


def test_render_contains_sections():
    output = handle('Design a better price ladder and bundle logic for our core product line.')
    assert output.startswith('# Pricing Strategy Advisor Brief')
    assert '## Test Design' in output
    assert '## Assumptions and Limits' in output


if __name__ == '__main__':
    for name, fn in list(globals().items()):
        if name.startswith('test_') and callable(fn):
            fn()
    print('All tests passed.')
