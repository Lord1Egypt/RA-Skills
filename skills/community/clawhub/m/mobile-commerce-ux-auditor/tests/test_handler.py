#!/usr/bin/env python3
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from handler import MobileCommerceAuditor, handle


def test_mode_detection_deep():
    auditor = MobileCommerceAuditor('Please run a full audit of our mobile checkout')
    assert auditor.mode == 'deep'


def test_goal_detection_checkout():
    auditor = MobileCommerceAuditor('Our checkout conversion is dropping on mobile')
    assert auditor.goal == 'checkout'


def test_stage_detection():
    auditor = MobileCommerceAuditor('Review the homepage, PDP, cart, and checkout on mobile')
    assert 'Checkout' in auditor.stages
    assert 'Cart' in auditor.stages


def test_render_contains_sections():
    output = handle('Audit our mobile PDP and checkout for a fashion store')
    assert output.startswith('# Mobile Commerce UX Audit')
    assert '## Prioritized Findings' in output
    assert '## Experiment Backlog' in output


if __name__ == '__main__':
    for name, fn in list(globals().items()):
        if name.startswith('test_') and callable(fn):
            fn()
    print('All tests passed.')
