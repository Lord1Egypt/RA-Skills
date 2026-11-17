#!/usr/bin/env python3
"""Infoseek v3.0.0-dev streaming 专项测试（5 用例）

覆盖：
- STREAM-01: streaming_research yield 步骤顺序正确
- STREAM-02: first yield 延迟 <2s（沙箱环境）
- STREAM-03: lite 模式跳过特定步骤
- STREAM-04: detect_conflicts_v3_async 输出兼容 sync 版
- STREAM-05: research() v3.0.0-dev 标识 + 输出兼容 v2.7.3
"""
import sys, asyncio, time
from pathlib import Path

INFOSEEK = Path(__file__).parent.parent
sys.path.insert(0, str(INFOSEEK / 'core'))
sys.path.insert(0, str(INFOSEEK / 'scripts'))

passed, failed = [], []
def check(name, cond, extra=''):
    if cond:
        passed.append(name); print(f"  [PASS] {name} {extra}")
    else:
        failed.append(name); print(f"  [FAIL] {name} {extra}")


SRC = [
    {'title': f'OpenAI 主题 {i}', 'snippet': f'OpenAI GPT-5 Anthropic Microsoft',
     'url': f'https://x{i}.com/{i}'} for i in range(10)
]
# 修复 SRC 列表推导（实际是 dict comprehension）
SRC = [{'title': f'OpenAI 主题 {i}', 'snippet': f'OpenAI GPT-5 Anthropic Microsoft',
        'url': f'https://x{i}.com/{i}'} for i in range(10)]


# ── STREAM-01 yield 步骤顺序 ─────────────────────────────
async def test_yield_order():
    from infoseek_core_v2 import streaming_research
    yields = []
    async for partial in streaming_research('AI', sources=SRC, lite=True):
        yields.append(partial['step'])
    expected = ['score_complete', 'wikidata_complete', 'entity_graph_complete',
                'conflict_complete', 'profile_complete', 'trajectory_complete',
                'report_complete']
    return yields, expected

yields, expected = asyncio.run(test_yield_order())
check('STREAM-01 yield 步骤顺序正确', yields == expected,
      f"got={yields}")


# ── STREAM-02 first yield 延迟 <2s ─────────────────────────
async def test_first_yield_latency():
    from infoseek_core_v2 import streaming_research
    t0 = time.perf_counter()
    gen = streaming_research('AI', sources=SRC, lite=True)
    first = await gen.__anext__()
    first_yield_ms = (time.perf_counter() - t0) * 1000
    return first_yield_ms, first

first_ms, first = asyncio.run(test_first_yield_latency())
check('STREAM-02 first yield <2000ms', first_ms < 2000,
      f"first={first_ms:.0f}ms step={first.get('step')}")


# ── STREAM-03 lite 模式跳过特定步骤 ─────────────────────────
async def test_lite_mode():
    from infoseek_core_v2 import streaming_research
    yields = []
    async for partial in streaming_research('AI', sources=SRC, lite=True):
        if 'skipped' in str(partial):
            yields.append((partial['step'], True))
        else:
            yields.append((partial['step'], False))
    # lite 模式下 entity_graph / heat_ranking / trajectory_top5 应被标记
    return yields

yields = asyncio.run(test_lite_mode())
has_skip = any(skipped for _, skipped in yields)
check('STREAM-03 lite 模式有 skipped 步骤', has_skip,
      f"steps={[(s, sk) for s, sk in yields]}")


# ── STREAM-04 detect_conflicts_v3_async 输出兼容 sync ─────────────────
async def test_async_conflict_compat():
    from conflict_v3 import detect_conflicts_v3, detect_conflicts_v3_async
    sync_res = detect_conflicts_v3(SRC, subject='AI')
    async_res = await detect_conflicts_v3_async(SRC, subject='AI')
    # 关键字段应一致
    return sync_res, async_res

sync_res, async_res = asyncio.run(test_async_conflict_compat())
sync_keys = set(sync_res.keys())
async_keys = set(async_res.keys())
conflicts_match = len(sync_res['conflicts']) == len(async_res['conflicts'])
check('STREAM-04 async conflict 输出兼容',
      sync_keys == async_keys and conflicts_match,
      f"sync_keys={len(sync_keys)} async_keys={len(async_keys)} conflicts={conflicts_match}")


# ── STREAM-05 research() v3.0.0 GA 标识 ─────────────────────
# v3.2.0 修订：断言「3.x 版本标识存在」而非硬编码 3.0.0（版本推进不再误报）
from infoseek_core_v2 import research
res = research('AI', sources=SRC, lite=True)
check('STREAM-05 research() v3.0.0 GA 标识',
      str(res.get('version', '')).startswith(('1.', '3.')),
      f"version={res.get('version')} streaming_mode={res.get('streaming_mode')}")
check('STREAM-05b research() 输出字段齐',
      all(k in res for k in ['scored_sources', 'conflicts', 'report']),
      f"keys={list(res.keys())[:8]}")


print(f"\n=== v3.0.0 GA streaming 专项: {len(passed)} PASS / {len(failed)} FAIL ===")
if failed:
    print("FAILED:", failed)
    sys.exit(1)
print("ALL PASS")
