#!/usr/bin/env python3
"""test_freshness_cron_v101.py — FreshnessCron 功能验证（1.2.X-2 · v1.2.x）

审计发现并修复：
  FC1  sync run_full_scan 不再对实体静态列表做"看起来落盘"的 last_verified_at 无效更新
       （实体库无持久层，v1.2.x 起验证结果以统计字段返回）
  FC2  async 版删除死代码 _wikidata_verify（引用不存在的 _stale_result，从未被 await）

冒烟覆盖：
  FC3  run_full_scan 离线（wikidata 异常）不抛异常，返回结构化统计
  FC4  run_full_scan wikidata 可用路径（mock verify_existence True/False）统计正确
  FC5  run_incremental_decay 返回 decay stats
  FC6  run_full_scan_async 可运行且离线降级不崩
  FC7  alias/profile/claim 模块异常不阻断主流程（降级优雅）
"""

import asyncio
import os
import sys
import tempfile
import unittest.mock as mock
from pathlib import Path

INFOSEEK = Path(__file__).parent.parent
sys.path.insert(0, str(INFOSEEK / 'scripts'))
sys.path.insert(0, str(INFOSEEK / 'core'))

import freshness_cron as fc

passed, failed = [], []
def check(name, cond, detail=''):
    (passed if cond else failed).append(name)
    print(f"[{'PASS' if cond else 'FAIL'}] {name}" + (f" — {detail}" if detail else ""))


# ── FC3: run_full_scan 离线不崩 + 结构化统计 ──
cron = fc.FreshnessCron()
with mock.patch('wikidata_sync.WikidataSync.verify_existence',
                side_effect=RuntimeError('offline-mock')):
    try:
        res = cron.run_full_scan()
        ok = isinstance(res, dict)
        check('FC3 full-scan 离线不抛异常且返回 dict', ok, f"keys={len(res)}")
        for k in ('decayed_count', 'total_reduction', 'stale_count', 'wikidata_verified',
                  'wikidata_marked_stale', 'wikidata_available', 'alias_active',
                  'alias_stale_cleaned', 'profile_scanned', 'claim_decay', 'scan_time'):
            check(f'FC3 字段存在: {k}', isinstance(res.get(k), (int, bool, dict, str)), f"={res.get(k)!r}")
        check('FC3 离线 wikidata_available=False', res.get('wikidata_available') is False)
    except Exception as e:
        check('FC3 full-scan 离线不抛异常', False, f"{type(e).__name__}: {e}")

# ── FC4: wikidata 可用路径统计（构造 stale 实体，确保走验证分支） ──
_STALE = [{'name': 'OpenAI'}, {'name': '腾讯'}, {'name': 'Meta'}]
with mock.patch('entity_tracker.EntityTracker.get_stale_entities', return_value=_STALE), \
     mock.patch('wikidata_sync.WikidataSync.verify_existence',
                side_effect=lambda name: name.startswith('OpenAI')):
    try:
        res4 = cron.run_full_scan()
        check('FC4 wikidata 可用时 available=True', res4.get('wikidata_available') is True)
        check('FC4 verified=1 (OpenAI)', res4.get('wikidata_verified') == 1,
              f"={res4.get('wikidata_verified')}")
        check('FC4 marked_stale=2', res4.get('wikidata_marked_stale') == 2,
              f"={res4.get('wikidata_marked_stale')}")
    except Exception as e:
        check('FC4 wikidata 可用路径不崩', False, f"{type(e).__name__}: {e}")

# ── FC5: run_incremental_decay ──
try:
    decay = cron.run_incremental_decay()
    check('FC5 decay 返回 dict', isinstance(decay, dict),
          f"keys={list(decay.keys())[:4]}")
except Exception as e:
    check('FC5 decay 不抛异常', False, f"{type(e).__name__}: {e}")

# ── FC6: async 路径离线降级不崩（构造 stale，验证 wikidata 异常降级） ──
with mock.patch('entity_tracker.EntityTracker.get_stale_entities', return_value=_STALE), \
     mock.patch('wikidata_sync.WikidataSync.verify_existence_async',
                side_effect=RuntimeError('offline-mock')):
    try:
        res6 = asyncio.run(cron.run_full_scan_async())
        check('FC6 async full-scan 离线不崩且返回 dict', isinstance(res6, dict),
              f"keys={len(res6)}")
        check('FC6 async 字段 scan_time=async', 'async' in str(res6.get('scan_time', '')))
        check('FC6 async wikidata 异常降级 available=False',
              res6.get('wikidata_available') is False)
    except Exception as e:
        check('FC6 async 离线不抛异常', False, f"{type(e).__name__}: {e}")

# ── FC7: alias/profile/claim 模块异常不阻断 ──
with mock.patch('wikidata_sync.WikidataSync.verify_existence',
                side_effect=RuntimeError('offline-mock')), \
     mock.patch.dict('sys.modules', {
         'entity_aliases': None, 'entity_profile': None, 'claim_store': None,
     }):
    try:
        res7 = cron.run_full_scan()
        check('FC7 子模块缺失仍返回统计', isinstance(res7, dict))
        check('FC7 alias 缺模块降级为 0', res7.get('alias_stale') == 0)
        check('FC7 profile 缺模块降级为 0', res7.get('profile_scanned') == 0)
    except Exception as e:
        check('FC7 子模块缺失不阻断', False, f"{type(e).__name__}: {e}")


print(f"\n=== FreshnessCron 冒烟: {len(passed)} PASS / {len(failed)} FAIL ===")
sys.exit(1 if failed else 0)
