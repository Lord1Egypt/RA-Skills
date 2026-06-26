#!/usr/bin/env python3
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from handler import InventoryHealthAuditor, handle


def test_objective_detection_stockout_prevention():
    auditor = InventoryHealthAuditor('Our hero SKU may stockout before 618 because lead time is 25 days and sales keep rising.')
    assert auditor.objective == 'Stockout prevention'


def test_signal_detection_sales_and_lead_time():
    auditor = InventoryHealthAuditor('Need an inventory review with sales velocity, supplier lead time, and current stock on hand.')
    assert 'Sales velocity' in auditor.signals
    assert 'Lead time / replenishment' in auditor.signals
    assert 'Inventory on hand' in auditor.signals


def test_render_contains_required_sections():
    output = handle('Check for aging inventory, overstock, and cash tied up in slow movers.')
    assert output.startswith('# Inventory Health Audit Report')
    assert '## Priority Queue' in output
    assert '## 30-Day Action Plan' in output


def test_dict_input_supported():
    output = handle({
        'inventory': 'hero sku 120 units, tail sku 900 units',
        'lead_time': '20 days',
        'campaign': '618 promotion',
    })
    assert '# Inventory Health Audit Report' in output
    assert '618 promotion' in output


if __name__ == '__main__':
    for name, fn in list(globals().items()):
        if name.startswith('test_') and callable(fn):
            fn()
    print('All tests passed.')
