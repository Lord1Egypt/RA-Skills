#!/usr/bin/env python3
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from handler import NewProductLaunchCopilot, handle


def test_objective_detection_waitlist():
    copilot = NewProductLaunchCopilot('We need a pre-launch waitlist and lead capture plan for this new product.')
    assert copilot.objective == 'Build Waitlist'


def test_channel_detection_shopify_email_tiktok():
    copilot = NewProductLaunchCopilot('Launch this SKU across Shopify, email, and TikTok with creator support.')
    assert 'Shopify / DTC Store' in copilot.channels
    assert 'Email / CRM' in copilot.channels
    assert 'TikTok Shop / Short Video' in copilot.channels


def test_asset_detection_tracking_and_inventory():
    copilot = NewProductLaunchCopilot('We have a PDP draft, product photos, FAQ notes, tracking setup, and inventory constraints.')
    assert 'PDP / Listing Copy' in copilot.assets
    assert 'Images / Video' in copilot.assets
    assert 'FAQ / Support' in copilot.assets
    assert 'Tracking / Analytics' in copilot.assets


def test_render_contains_sections():
    output = handle('Create a Shopify, email, and TikTok launch brief for a seasonal bundle with UGC, FAQ, and launch KPIs.')
    assert output.startswith('# New Product Launch Brief')
    assert '## Launch Brief' in output
    assert '## Messaging Matrix' in output
    assert '## Readiness Checklist' in output
    assert '## KPI Framework' in output


if __name__ == '__main__':
    for name, fn in list(globals().items()):
        if name.startswith('test_') and callable(fn):
            fn()
    print('All tests passed.')
