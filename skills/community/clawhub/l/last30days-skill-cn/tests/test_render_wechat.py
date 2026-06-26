"""测试 WechatItem 无 engagement 属性时 render_compact 不崩溃。"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from lib import schema, render


def test_render_compact_wechat_no_engagement():
    report = schema.create_report("test", "2026-01-01", "2026-01-31", "all")
    item = schema.WechatItem(
        id="WX1", title="测试文章", snippet="摘要",
        url="https://example.com", source_name="测试号",
        score=50, why_relevant="测试",
    )
    assert not hasattr(item, 'engagement')
    report.wechat = [item]
    output = render.render_compact(report)
    assert "WX1" in output
    assert "测试文章" in output


def test_render_compact_wechat_empty_list():
    report = schema.create_report("test", "2026-01-01", "2026-01-31", "all")
    report.wechat = []
    output = render.render_compact(report)
    assert isinstance(output, str)
