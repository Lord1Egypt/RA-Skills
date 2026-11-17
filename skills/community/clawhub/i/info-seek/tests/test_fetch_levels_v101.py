#!/usr/bin/env python3
"""test_fetch_levels_v101.py — 抓取层 L3/L4 测试（1.2.X-3 · v1.2.x）

覆盖：
  FL1 _classify_media 扩展名分类（image/video/audio/None）
  FL2 _classify_media Content-Type 优先
  FL3 _probe_media 媒体 → 结构化 chunk；非媒体 → None；网络失败降级
  FL4 _get_host_credential 命中/缺失
  FL5 tool_fetch_content extraction_level=4 → multimodal chunk
  FL6 tool_fetch_content extraction_level=3 无凭证 → 降级 L1/L2（非 L3）
  FL7 tool_fetch_content extraction_level=3 有凭证 → L3 且凭证不泄漏
  FL8 req_level 钳制（99→4，'abc'→1）
"""

import os
import sys
import unittest.mock as mock
from pathlib import Path

INFOSEEK = Path(__file__).parent.parent
sys.path.insert(0, str(INFOSEEK / 'scripts'))
sys.path.insert(0, str(INFOSEEK / 'core'))
sys.path.insert(0, str(INFOSEEK))

import mcp_tools_search as mts

passed, failed = [], []
def check(name, cond, detail=''):
    (passed if cond else failed).append(name)
    print(f"[{'PASS' if cond else 'FAIL'}] {name}" + (f" — {detail}" if detail else ""))


# ── FL1/FL2: _classify_media ──
check('FL1 image 扩展名', mts._classify_media('https://a.com/x.jpg?w=100') == 'image')
check('FL1 video 扩展名', mts._classify_media('https://a.com/v.mp4') == 'video')
check('FL1 audio 扩展名', mts._classify_media('https://a.com/s.mp3') == 'audio')
check('FL1 非媒体 None', mts._classify_media('https://a.com/page.html') is None)
check('FL2 Content-Type 优先',
      mts._classify_media('https://a.com/stream', 'video/mp4; charset=utf-8') == 'video')
check('FL2 未知 Content-Type 回退扩展名',
      mts._classify_media('https://a.com/photo.png', 'application/octet-stream') == 'image')


# ── FL3: _probe_media ──
with mock.patch('urllib.request.urlopen', side_effect=OSError('offline-mock')):
    p = mts._probe_media('https://a.com/clip.mp3')
    check('FL3 媒体返回结构化 chunk', isinstance(p, dict) and p.get('media_type') == 'audio')
    check('FL3 chunk 含 metadata/transcript 字段',
          'metadata' in p and 'transcript' in p and 'transcript_available' in p)
    check('FL3 网络失败 format 由扩展名推断', p['metadata']['format'] == 'mp3',
          f"={p['metadata']['format']}")
    check('FL3 非媒体 None', mts._probe_media('https://a.com/news.html') is None)


# ── FL4: _get_host_credential ──
with mock.patch('core.key_manager.get_key',
                side_effect=lambda p: 'sk-abc' if p == 'paywall.news' else ''):
    c = mts._get_host_credential('paywall.news')
    check('FL4 精确 host 命中', c == 'sk-abc', f"={c!r}")
    c2 = mts._get_host_credential('other.com')
    check('FL4 无凭证 → 空串', c2 == '', f"={c2!r}")
with mock.patch('core.key_manager.get_key', side_effect=RuntimeError('km broken')):
    c3 = mts._get_host_credential('x.com')
    check('FL4 KeyManager 异常 → 空串', c3 == '')


# ── FL5: extraction_level=4 → multimodal chunk ──
_FAKE_MEDIA = {'media_type': 'video', 'metadata': {'format': 'mp4'}, 'transcript': None,
               'transcript_available': False}
with mock.patch('urllib.request.urlopen', side_effect=OSError('offline-mock')), \
     mock.patch.object(mts, '_fetch_render_with_playwright', return_value=''), \
     mock.patch.object(mts, '_probe_media', return_value=_FAKE_MEDIA):
    r5 = mts.tool_fetch_content({'url': 'https://a.com/clip.mp4', 'extraction_level': 4})
    check('FL5 extraction_level=4', r5.get('extraction_level') == 4, f"={r5.get('extraction_level')}")
    check('FL5 multimodal=True', r5.get('multimodal') is True)
    check('FL5 media 字段注入', r5.get('media') == _FAKE_MEDIA)
    check('FL5 兼容字段保留', 'chain_tracking_v3' in r5 and 'content' in r5)


# ── FL6: extraction_level=3 无凭证 → 降级（非 L3） ──
with mock.patch('urllib.request.urlopen', side_effect=OSError('offline-mock')), \
     mock.patch.object(mts, '_fetch_render_with_playwright', return_value=''), \
     mock.patch.object(mts, '_get_host_credential', return_value=''):
    r6 = mts.tool_fetch_content({'url': 'https://paywall.news/a.html', 'extraction_level': 3})
    check('FL6 无凭证不置 L3', r6.get('extraction_level') != 3, f"={r6.get('extraction_level')}")
    check('FL6 降级返回结构完整', 'url' in r6 and 'fetch_error' in r6)


# ── FL7: extraction_level=3 有凭证 → L3，且凭证不泄漏 ──
_HTML = '<html><head><title>Paywall Page</title></head><body><h1>Title</h1><p>正文内容' + ('很长' * 100) + '</p></body></html>'
with mock.patch('urllib.request.urlopen', side_effect=OSError('offline-mock')), \
     mock.patch.object(mts, '_fetch_render_with_playwright', return_value=''), \
     mock.patch.object(mts, '_get_host_credential', return_value='Cookie: session=supersecret'), \
     mock.patch.object(mts, '_fetch_with_credential', return_value=_HTML):
    r7 = mts.tool_fetch_content({'url': 'https://paywall.news/a.html', 'extraction_level': 3})
    check('FL7 有凭证置 L3', r7.get('extraction_level') == 3, f"={r7.get('extraction_level')}")
    check('FL7 正文来自凭证抓取', len(r7.get('content', '')) > 100)
    check('FL7 凭证不泄漏到返回', 'supersecret' not in str(r7), '凭证已脱敏')


# ── FL8: req_level 钳制（返回 extraction_level 是实际执行级别，故用媒体 URL 验证） ──
def _clamp_ok(mod, raw, expect_media):
    with mock.patch('urllib.request.urlopen', side_effect=OSError('offline-mock')), \
         mock.patch.object(mod, '_fetch_render_with_playwright', return_value=''), \
         mock.patch.object(mod, '_probe_media', return_value=_FAKE_MEDIA):
        r = mod.tool_fetch_content({'url': 'https://a.com/clip.mp4', 'extraction_level': raw})
        if expect_media:
            return r.get('extraction_level') == 4 and r.get('multimodal') is True, \
                f"level={r.get('extraction_level')} multimodal={r.get('multimodal')}"
        return r.get('extraction_level') != 3, f"level={r.get('extraction_level')}"

# 请求 5/99 → 钳制到 4 → 媒体命中 → 实际 4（multimodal）
for raw in (5, 99):
    cond, detail = _clamp_ok(mts, raw, True)
    check(f'FL8 钳制 {raw} → 4（媒体实际 4）', cond, detail)
# 非法值 → 1：非媒体页面实际级别保持 1（无 L3/L4 触发）
with mock.patch('urllib.request.urlopen', side_effect=OSError('offline-mock')), \
     mock.patch.object(mts, '_fetch_render_with_playwright', return_value=''):
    for raw in ('abc', -3):
        r = mts.tool_fetch_content({'url': 'https://a.com/p.html', 'extraction_level': raw})
        check(f'FL8 非法值 {raw!r} → 实际 1', r.get('extraction_level') == 1,
              f"={r.get('extraction_level')}")


print(f"\n=== 抓取层 L3/L4 测试: {len(passed)} PASS / {len(failed)} FAIL ===")
sys.exit(1 if failed else 0)
