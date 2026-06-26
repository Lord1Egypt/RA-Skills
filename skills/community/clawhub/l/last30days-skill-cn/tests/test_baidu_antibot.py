"""测试百度反爬检测与 Bing 兜底路径。"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from unittest.mock import patch
from lib import baidu


ANTIBOT_HTML = '<html><title>百度安全验证</title><script src="https://wappass.baidu.com/static/verify"></script></html>'
NORMAL_HTML = '''<html><div class="result c-container new-pmd" id="1">
<h3 class="t"><a href="https://example.com/1" target="_blank">测试标题</a></h3>
<span class="content-right_8Zs40">测试摘要内容</span>
</div></html>'''


def test_antibot_detection():
    assert baidu._is_antibot_page(ANTIBOT_HTML) is True
    assert baidu._is_antibot_page(NORMAL_HTML) is False
    assert baidu._is_antibot_page("") is True
    assert baidu._is_antibot_page("x" * 100) is False


def test_public_search_antibot_returns_empty():
    with patch.object(baidu, '_fetch', return_value=ANTIBOT_HTML):
        result = baidu._search_via_public("test", 10)
        assert result == []


def test_scrapecreators_removed_from_xiaohongshu():
    from lib import xiaohongshu
    assert not hasattr(xiaohongshu, '_search_via_scrapecreators')
