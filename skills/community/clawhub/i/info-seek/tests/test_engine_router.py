#!/usr/bin/env python3
"""test_engine_router.py — 引擎路由测试（策略② · engine_router v1.0.0）

覆盖：
  R1  键控引擎无 key 直接剔除（零网络开销）
  R2  白名单过滤：env INFOSEEK_ENGINE_WHITELIST 精确控制（名单外一律剔除）
  R3  白名单为空 = 全部放行（免费引擎保留）
  R4  白名单 env 优先级高于配置文件
  R5  CLI 输出含关键路由信息（白名单/探测状态）
"""

import os
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / 'scripts'))

import engine_router as er

# 清理可能干扰的环境变量
for k in ('INFOSEEK_ENGINE_WHITELIST', 'INFOSEEK_ENGINE_PROBE',
          'INFOSEEK_PROBE_TIMEOUT', 'INFOSEEK_PROBE_TTL', 'INFOSEEK_ROUTE_CACHE'):
    os.environ.pop(k, None)

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


def test_r1_keyed_without_key() -> None:
    """R1 键控引擎无 key 剔除：exa/tavily 等未配 key → 直接剔除，免费引擎保留。"""
    print('R1 键控引擎无 key 剔除')
    for k in ('EXA_API_KEY', 'TAVILY_API_KEY', 'ZHIPU_API_KEY'):
        os.environ.pop(k, None)
    engs = [('Exa', 1), ('Tavily', 2), ('Wikipedia', 3), ('DuckDuckGo-HTML', 4)]
    out = er.route_engines(engs)
    names = [n for n, _ in out]
    check('exa 被剔除', 'Exa' not in names)
    check('tavily 被剔除', 'Tavily' not in names)
    check('wikipedia 保留', 'Wikipedia' in names)
    check('duckduckgo 保留', 'DuckDuckGo-HTML' in names)


def test_r2_whitelist_env() -> None:
    """R2 env 白名单精确控制：名单外一律剔除。"""
    print('R2 env 白名单过滤')
    os.environ['INFOSEEK_ENGINE_WHITELIST'] = 'wikipedia'
    engs = [('Wikipedia', 1), ('Bing-RSS', 2), ('DuckDuckGo-HTML', 3)]
    out = er.route_engines(engs)
    names = [n for n, _ in out]
    check('wikipedia 通过', 'Wikipedia' in names)
    check('bing-rss 剔除', 'Bing-RSS' not in names)
    check('duckduckgo 剔除', 'DuckDuckGo-HTML' not in names)
    os.environ.pop('INFOSEEK_ENGINE_WHITELIST', None)


def test_r3_whitelist_empty_passthrough() -> None:
    """R3 白名单为空 = 全部放行：无 env 且配置里 whitelist=[]。"""
    print('R3 空白名单全部放行')
    engs = [('Wikipedia', 1), ('DuckDuckGo-HTML', 2)]
    out = er.route_engines(engs)
    check('全部保留', len(out) == 2)


def test_r4_env_overrides_config() -> None:
    """R4 env 优先级：即便写死配置文件，env 白名单也生效。"""
    print('R4 env 优先于配置')
    # 直接写临时配置回读会走 _load_config；这里验证 env 覆盖
    os.environ['INFOSEEK_ENGINE_WHITELIST'] = 'jina-ai'
    engs = [('Wikipedia', 1), ('Jina-AI', 2)]
    out = er.route_engines(engs)
    names = [n for n, _ in out]
    check('jina-ai 通过', 'Jina-AI' in names)
    check('wikipedia 被 env 剔除', 'Wikipedia' not in names)
    os.environ.pop('INFOSEEK_ENGINE_WHITELIST', None)


def test_r5_engine_whitelist_returns_set() -> None:
    """R5 engine_whitelist() 返回小写集合。"""
    print('R5 engine_whitelist() 返回小写集合')
    os.environ['INFOSEEK_ENGINE_WHITELIST'] = 'Exa, TAVILY , wikipedia'
    wl = er.engine_whitelist()
    check('小写归一', wl == {'exa', 'tavily', 'wikipedia'})
    check('类型为 set', isinstance(wl, set))
    os.environ.pop('INFOSEEK_ENGINE_WHITELIST', None)


def test_r6_cli_output() -> None:
    """R6 CLI 输出包含关键路由信息。"""
    print('R6 CLI 输出')
    import io
    import contextlib
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = er.cli()
    text = buf.getvalue()
    check('退出码 0', rc == 0)
    check('含白名单行', '白名单' in text)
    check('含探测状态行', '探测' in text)


if __name__ == '__main__':
    test_r1_keyed_without_key()
    test_r2_whitelist_env()
    test_r3_whitelist_empty_passthrough()
    test_r4_env_overrides_config()
    test_r5_engine_whitelist_returns_set()
    test_r6_cli_output()
    print(f'\nengine_router 测试: {_PASS} 通过 / {_FAIL} 失败')
    sys.exit(1 if _FAIL else 0)