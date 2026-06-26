#!/usr/bin/env python3
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from handler import PromotionCalendarPlanner, handle


def test_window_detection_q4():
    planner = PromotionCalendarPlanner('Build our Q4 promotion calendar around 11.11 and Black Friday.')
    assert planner.window == 'Q4'
    assert '11.11' in planner.anchors or 'Black Friday' in planner.anchors


def test_goal_detection_inventory_digestion():
    planner = PromotionCalendarPlanner('Create a quarterly promo plan to clear aged inventory and improve sell-through.')
    assert planner.goal == 'Inventory digestion'


def test_render_contains_sections():
    output = handle('Plan a quarterly promotion calendar for revenue growth with 618 as the main anchor.')
    assert output.startswith('# Promotion Calendar Plan')
    assert '## Calendar Recommendations' in output
    assert '## Team Preparation Checklist' in output
    assert '## Conflict Watchlist' in output


def test_dict_input_supported():
    output = handle({
        'window': 'annual',
        'goal': 'margin and member retention',
        'anchors': ['Lunar New Year', '618', '11.11'],
    })
    assert '# Promotion Calendar Plan' in output
    assert 'Lunar New Year' in output


if __name__ == '__main__':
    for name, fn in list(globals().items()):
        if name.startswith('test_') and callable(fn):
            fn()
    print('All tests passed.')
