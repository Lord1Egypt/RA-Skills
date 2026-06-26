#!/usr/bin/env python3
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from handler import PaymentRouteOptimizer, handle


def test_objective_detection_approval():
    optimizer = PaymentRouteOptimizer('Need better authorization rate in Brazil card payments')
    assert optimizer.objective == 'Approval-first'


def test_mode_detection_failover():
    optimizer = PaymentRouteOptimizer('Create a failover plan before peak season for our PSP stack')
    assert optimizer.mode == 'Failover Planning'


def test_market_and_method_detection():
    optimizer = PaymentRouteOptimizer('Review card and PIX routing in Brazil and Europe')
    assert 'Brazil' in optimizer.markets
    assert 'EU' in optimizer.markets
    assert 'Card' in optimizer.methods
    assert 'Local Method' in optimizer.methods


def test_render_contains_key_sections():
    output = handle('We need a balanced routing matrix with retry guidance and rollout guardrails')
    assert output.startswith('# Payment Routing Optimization Brief')
    assert '## Suggested Route Matrix' in output
    assert '## Retry and Failover Policy' in output
    assert '## Rollout Plan' in output


if __name__ == '__main__':
    for name, fn in list(globals().items()):
        if name.startswith('test_') and callable(fn):
            fn()
    print('All tests passed.')
