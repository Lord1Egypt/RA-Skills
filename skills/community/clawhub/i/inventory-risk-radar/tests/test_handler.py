#!/usr/bin/env python3
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from handler import InventoryRiskRadar, handle


def test_review_mode_detection_prepromo():
    radar = InventoryRiskRadar('Run a pre-promo risk review before our holiday campaign.')
    assert radar.review_mode == 'Pre-Promo Risk Review'


def test_risk_detection_stockout_and_inbound():
    radar = InventoryRiskRadar('Our hero SKU has low stock, only a few days of cover, and the inbound PO may be delayed.')
    assert 'Stockout Risk' in radar.risk_types
    assert 'Inbound Delay Risk' in radar.risk_types


def test_signal_detection_inventory_velocity_supplier():
    radar = InventoryRiskRadar('Check on-hand stock, sales velocity, supplier lead time, and cash tied up in excess inventory.')
    assert 'On-hand / Available Stock' in radar.signals
    assert 'Sales Velocity' in radar.signals
    assert 'Lead Time / Supplier Reliability' in radar.signals
    assert 'Margin / Cash Pressure' in radar.signals


def test_render_contains_sections():
    output = handle('Create an inventory watchlist for stockout, overstock, aging, and promo-readiness risk ahead of our campaign.')
    assert output.startswith('# Inventory Risk Radar')
    assert '## Inventory Risk Dashboard' in output
    assert '## SKU Action Watchlist' in output
    assert '## Action Ladder' in output


if __name__ == '__main__':
    for name, fn in list(globals().items()):
        if name.startswith('test_') and callable(fn):
            fn()
    print('All tests passed.')
