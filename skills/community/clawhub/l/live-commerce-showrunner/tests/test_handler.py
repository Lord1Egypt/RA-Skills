#!/usr/bin/env python3
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from handler import LiveCommerceShowrunner, handle


def test_channel_detection_douyin_tiktok():
    show = LiveCommerceShowrunner('Plan a Douyin and TikTok Shop launch live for our new product.')
    assert 'Douyin Live' in show.channels
    assert 'TikTok Shop Live' in show.channels


def test_show_type_detection_promo():
    show = LiveCommerceShowrunner('We need a clearance livestream with discount bundles and markdown pressure.')
    assert show.show_type == 'Promo / Clearance Push'


def test_risk_detection_inventory_and_tech():
    show = LiveCommerceShowrunner('Traffic may be low, inventory is tight, and we are worried about audio lag in comments.')
    assert 'Traffic uncertainty' in show.risks
    assert 'Inventory pressure' in show.risks
    assert 'Technical / moderation load' in show.risks


def test_render_contains_sections():
    output = handle('Create a run of show for a 45-minute Douyin live with a host and moderator.')
    assert output.startswith('# Live Commerce Showrunner Brief')
    assert '## Run of Show' in output
    assert '## Host and Crew Checklist' in output
    assert '## Failure Modes and Backup Plan' in output


def test_dict_input_supported():
    output = handle({
        'channel': ['TikTok Shop', 'Douyin'],
        'objective': 'launch conversion',
        'products': ['serum', 'bundle'],
        'risks': ['inventory tight', 'tech rehearsal needed'],
    })
    assert '# Live Commerce Showrunner Brief' in output
    assert 'Launch Conversion' in output


if __name__ == '__main__':
    for name, fn in list(globals().items()):
        if name.startswith('test_') and callable(fn):
            fn()
    print('All tests passed.')
