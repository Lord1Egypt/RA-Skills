#!/usr/bin/env python3
"""test_platform_adapter.py — 平台 Web 搜索适配器测试（P0 · 三路并发）

覆盖：
  N1-N6   schema 归一化（hits/results/data/web/items/裸 list/混排/去重/过滤）
  P1-P8   探测与注册（纯 CLI 零开销 / off / mock 通道 / health=False / 超时）
  C1-C4   接入契约（_ENGINE_WEIGHT 静态权重 / _default_layer 合并 /
           route_engines 放行 / INFOSEEK_CONCURRENT_ALL 开关）
  CLI1    python -m platform_adapter 无通道 → exit 0
"""

import os
import subprocess
import sys
import time
import types
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / 'scripts'))

import platform_adapter as pa
import engine_router as er
import infoseek_pipeline as P

_PASS = 0
_FAIL = 0


def check(label: str, cond: bool) -> None:
    global _PASS, _FAIL
    if cond:
        _PASS += 1
        print(f'  ✅ {label}')
    else:
        _FAIL += 1
        print(f'  ❌ {label}')


def _reset(env: dict | None = None) -> None:
    """重置进程内探测缓存 + 清理/设置 env。"""
    pa._ENGINE_PROBED = False
    pa._ENGINE_CACHE = None
    for k in (pa.MODE_ENV, pa.CHANNEL_ENV, pa.MCP_CHANNEL_ENV,
              pa.IMA_CHANNEL_ENV, pa.TIMEOUT_ENV, pa.WEIGHT_ENV,
              pa.THROTTLE_ENV):
        os.environ.pop(k, None)
    if env:
        os.environ.update(env)


def _fake_channel(name='WorkBuddy-WebSearch', health=True, sleep_s=0.0,
                  hits=None) -> types.ModuleType:
    """构造假平台通道模块（双通道共用。hits 缺省 → 3 条标准结果）。"""
    m = types.ModuleType('fakep_channel')
    m.name = name
    m.meta = {'name': name, 'provider': 'fake', 'cost': '$0'}
    if hits is None:
        hits = [{'url': f'https://fake.dev/{i}', 'title': f'T{i}',
                 'snippet': f'S{i}'} for i in range(3)]

    def search(query, max_results):
        if sleep_s:
            time.sleep(sleep_s)
        return {'ok': True, 'count': len(hits), 'provider': 'fake',
                'hits': hits[:max_results]}

    def _health():
        return health

    m.search = search
    m.health = _health
    return m


# ---------------------------------------------------------------------------
# N 组：schema 归一化
# ---------------------------------------------------------------------------

def test_n1_hits_ok_count() -> None:
    """N1 {ok,count,provider,hits} 标准形态 → 归一化列表。"""
    print('N1 标准 hits 形态')
    raw = {'ok': True, 'count': 2, 'provider': 'wb',
           'hits': [{'url': 'https://a.com', 'title': 'A', 'snippet': 'sa'},
                    {'url': 'https://b.com', 'title': 'B'}]}  # snippet 缺失
    out = pa._normalize(raw, 5)
    check('2 条归一化', len(out) == 2)
    check('字段完整', out[0] == {'url': 'https://a.com', 'title': 'A',
                                 'snippet': 'sa'})
    check('snippet 缺失补默认', out[1]['snippet'] == '')
    check('max_results 截断', len(pa._normalize(raw, 1)) == 1)


def test_n2_containers() -> None:
    """N2 results/data/web/items 容器形态（抗 schema 漂移）。"""
    print('N2 容器形态')
    for key in ('results', 'data', 'web', 'items'):
        raw = {key: [{'url': f'https://{key}.x/1', 'title': key}]}
        out = pa._normalize(raw, 3)
        check(f'{key} 容器解析', len(out) == 1 and out[0]['url'].startswith(
            f'https://{key}.x'))


def test_n3_mixed_dedup_filter() -> None:
    """N3 hits 混排（dict/str）+ 重复 url 去重 + 无 url 过滤。"""
    print('N3 混排/去重/过滤')
    raw = {'hits': [
        {'url': 'https://a.com', 'title': 'A'},
        'https://a.com',              # 重复 url（字符串形态）→ 去重
        {'title': '无url'},            # 无 url → 过滤
        {'link': 'https://c.com'},     # link 别名 → 归一
        'just-text',                   # 非 URL 文本 → 过滤
    ]}
    out = pa._normalize(raw, 9)
    check('去重后 2 条', len(out) == 2)
    check('link 别名识别', any(r['url'] == 'https://c.com' for r in out))
    check('纯文本丢弃', all(r['url'].startswith('http') for r in out))


def test_n4_defaults_truncate() -> None:
    """N4 缺失字段补默认 + 长度截断。"""
    print('N4 默认值/截断')
    out = pa._normalize(
        {'hits': [{'url': 'https://t.com',
                   'title': 'x' * 500, 'snippet': 'y' * 500}]}, 1)
    check('title 截断 200', len(out[0]['title']) == 200)
    check('snippet 截断 400', len(out[0]['snippet']) == 400)


def test_n5_bare_list_and_empty() -> None:
    """N5 裸 list 形态；None/空/未知 schema → []。"""
    print('N5 裸 list/空/未知')
    check('裸 list', len(pa._normalize(
        ['https://x.com', {'url': 'https://y.com', 'title': 'Y'}], 5)) == 2)
    check('None → []', pa._normalize(None, 5) == [])
    check('未知 schema dict → []', pa._normalize({'foo': 'bar'}, 5) == [])
    check('空 hits → []', pa._normalize({'hits': []}, 5) == [])


# ---------------------------------------------------------------------------
# P 组：探测与注册
# ---------------------------------------------------------------------------

def test_p1_pure_cli_noop() -> None:
    """P1 纯 CLI（通道未预装）→ 不注册 []，零网络开销。

    实测基建将 workbuddy_channel 物理写入 scripts/ 后，auto 探测可命中
    预装通道（设计意图）；本用例以 sys.modules[name]=None 标准阻断模拟
    "未预装"场景。
    """
    print('P1 纯 CLI 零开销（通道未预装）')
    _reset()
    sys.modules.pop('workbuddy_channel', None)
    sys.modules['workbuddy_channel'] = None  # 阻断 import：模拟未预装
    try:
        check('engines == []', pa.platform_engines() == [])
        check('engine == None', pa.platform_engine() is None)
    finally:
        sys.modules.pop('workbuddy_channel', None)  # 移除阻断，恢复预装态


def test_p2_off_mode() -> None:
    """P2 INFOSEEK_PLATFORM_WEBSEARCH=off → 显式关闭。"""
    print('P2 off 模式')
    _reset({pa.MODE_ENV: 'off'})
    check('off 不注册', pa.platform_engines() == [])


def test_p3_mock_channel_auto() -> None:
    """P3 auto 模式 + mock workbuddy_channel（sys.modules 注入）→ 注册 + 可调用。"""
    print('P3 auto + mock 通道')
    _reset()
    fake = _fake_channel()
    sys.modules['workbuddy_channel'] = fake
    engs = pa.platform_engines()
    check('注册 1 路', len(engs) == 1)
    check('引擎名正确', engs[0][0] == 'WorkBuddy-WebSearch')
    fn = engs[0][1]
    out = fn('量化交易', 2)
    check('fn 归一化结果', len(out) == 2 and out[0]['title'] == 'T0')
    check('结果已截断 max_results', len(out) <= 2)


def test_p4_health_false() -> None:
    """P4 health()=False → 不注册。"""
    print('P4 health=False')
    _reset()
    sys.modules['workbuddy_channel'] = _fake_channel(health=False)
    check('不注册', pa.platform_engines() == [])


def test_p5_health_exception() -> None:
    """P5 health() 抛异常 → 不注册（保底可用性）。"""
    print('P5 health 异常')
    _reset()
    fake = _fake_channel()
    fake.health = lambda: (_ for _ in ()).throw(RuntimeError('boom'))
    sys.modules['workbuddy_channel'] = fake
    check('不注册', pa.platform_engines() == [])


def test_p6_no_search_attr() -> None:
    """P6 通道无 search 可调用 → 不注册。"""
    print('P6 无 search')
    _reset()
    fake = _fake_channel()
    fake.search = None
    sys.modules['workbuddy_channel'] = fake
    check('不注册', pa.platform_engines() == [])


def test_p7_meta_name() -> None:
    """P7 meta.name 自定义引擎名生效（平台自定义注册名）。"""
    print('P7 meta 自定义名')
    _reset()
    sys.modules['workbuddy_channel'] = _fake_channel(name='My-Platform-Search')
    engs = pa.platform_engines()
    check('自定义名注册', len(engs) == 1 and engs[0][0] == 'My-Platform-Search')


def test_p8_hard_timeout() -> None:
    """P8 硬超时：慢通道 > timeout → fn 抛 TimeoutError（上层记 failure）。"""
    print('P8 硬超时')
    _reset({pa.TIMEOUT_ENV: '0.5'})
    sys.modules['workbuddy_channel'] = _fake_channel(sleep_s=3.0)
    fn = pa.platform_engines()[0][1]
    t0 = time.time()
    try:
        fn('slow', 3)
        check('超时抛异常', False)
    except TimeoutError:
        check('超时抛异常', True)
    check('超时 < 2s 返回', time.time() - t0 < 2.0)


# ---------------------------------------------------------------------------
# C 组：接入契约（pipeline / engine_router 侧）
# ---------------------------------------------------------------------------

def test_c1_static_weight() -> None:
    """C1 _ENGINE_WEIGHT 静态表绑定 0.9（_engine_weight_for 直接命中）。"""
    print('C1 静态权重 0.9')
    check('WorkBuddy-WebSearch == 0.9',
          P._ENGINE_WEIGHT.get('WorkBuddy-WebSearch') == 0.9)
    check('platform_weight() == 0.9', pa.platform_weight() == 0.9)
    _reset({pa.WEIGHT_ENV: '0.5'})
    check('env 覆盖 0.5', pa.platform_weight() == 0.5)


def test_c2_default_layer_merge() -> None:
    """C2 _default_layer() 无平台通道时正常返回（合并零开销，白名单放行）。"""
    print('C2 _default_layer 合并')
    _reset()
    sys.modules.pop('workbuddy_channel', None)
    sys.modules['workbuddy_channel'] = None  # 阻断 import：模拟未预装
    try:
        layer = P._default_layer()
        check('返回免费引擎列表', len(layer) >= 4)
        check('无 WorkBuddy（通道未预装 → 不合并）',
              not any(n == 'WorkBuddy-WebSearch' for n, _ in layer))
    finally:
        sys.modules.pop('workbuddy_channel', None)  # 移除阻断，恢复预装态


def test_c3_router_allow() -> None:
    """C3 route_engines 对 WorkBuddy-WebSearch 天然放行（非键控+未知名→True）。"""
    print('C3 route_engines 放行')
    for k in ('INFOSEEK_ENGINE_WHITELIST', 'INFOSEEK_ENGINE_PROBE'):
        os.environ.pop(k, None)
    engs = er.route_engines(
        [('DuckDuckGo-HTML', 1), ('WorkBuddy-WebSearch', 2)])
    check('WorkBuddy 放行', any(n == 'WorkBuddy-WebSearch' for n, _ in engs))


def test_c4_concurrent_all_flag() -> None:
    """C4 INFOSEEK_CONCURRENT_ALL 开关解析（默认关 → 付费保留池语义不变）。"""
    print('C4 CONCURRENT_ALL 开关')
    os.environ.pop('INFOSEEK_CONCURRENT_ALL', None)
    check('默认 False', P._env_flag('INFOSEEK_CONCURRENT_ALL', False) is False)
    os.environ['INFOSEEK_CONCURRENT_ALL'] = '1'
    check('=1 时 True', P._env_flag('INFOSEEK_CONCURRENT_ALL', False) is True)
    os.environ.pop('INFOSEEK_CONCURRENT_ALL', None)


def test_cli1() -> None:
    """CLI1 python -m platform_adapter：平台预装通道 → 注册成功 exit 0。"""
    print('CLI1 模块独立运行')
    r = subprocess.run([sys.executable, '-m', 'platform_adapter'],
                       capture_output=True, text=True, timeout=20,
                       cwd=str(ROOT / 'scripts'),
                       env={**os.environ, 'INFOSEEK_PLATFORM_WEBSEARCH': 'auto'})
    check('exit 0', r.returncode == 0)
    check('预装通道注册（WorkBuddy-WebSearch）',
          'WorkBuddy-WebSearch' in r.stdout)


def main() -> None:
    print('=== platform_adapter P0 测试 ===')
    for fn in sorted(
            [v for k, v in globals().items() if k.startswith('test_')],
            key=lambda f: f.__name__):
        try:
            fn()
        except Exception as e:
            print(f'  ❌ {fn.__name__} 异常: {e!r}')
            global _FAIL
            _FAIL += 1
    print(f'\nPASS={_PASS} FAIL={_FAIL}')
    sys.exit(1 if _FAIL else 0)


if __name__ == '__main__':
    main()