import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from handler import ScoutEngine, handle

def test_platform_detection():
    e = ScoutEngine('Skincare brand on Instagram with UGC goal')
    assert e.platform == 'instagram'
    print('✓ test_platform_detection passed')

def test_goal_detection():
    e = ScoutEngine('Pet accessory launch for affiliate campaign on TikTok')
    assert e.goal == 'affiliate'
    print('✓ test_goal_detection passed')

def test_tier_detection():
    e = ScoutEngine('Need micro creators 10k-80k on TikTok')
    assert e.tier == 'micro'
    print('✓ test_tier_detection passed')

def test_category_detection():
    e = ScoutEngine('敏感肌护肤品牌 美国市场')
    assert e.category == 'skincare'
    print('✓ test_category_detection passed')

def test_markdown_output():
    out = handle('Skincare brand on TikTok for UGC + conversion with micro creators')
    assert out.startswith('# Influencer Partnership Scout Brief')
    print('✓ test_markdown_output passed')

def test_contains_shortlist_and_outreach():
    out = handle('Pet brand awareness campaign on Instagram')
    assert '## Influencer Shortlist Framework' in out
    assert '## Outreach Recommendation' in out
    print('✓ test_contains_shortlist_and_outreach passed')

if __name__ == '__main__':
    for name, fn in list(globals().items()):
        if name.startswith('test_') and callable(fn):
            fn()
    print('All tests passed.')
