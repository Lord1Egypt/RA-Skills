#!/usr/bin/env python3
"""test_learned_prune_cron_r1a.py — R1-a/D-1 learned prune cron 安全收口守护

覆盖（Phase-R1）：
- cron 第 7 步向 prune_learned_entities 传入真实 active_names（非空集合，近期命中实体受保护）
- cron learned_prune 统计透出 applied 字段（dry_run 默认 False）
不设置 INFOSEEK_LEARNED_PRUNE_APPLY，仅验证 dry_run 路径接线（无落盘副作用）。
"""
import json
import os
import sys
import tempfile
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / 'core'))

DATA_DIR = tempfile.mkdtemp(prefix='infoseek_cron_r1a_')
os.environ['INFOSEEK_DATA_DIR'] = DATA_DIR
os.environ.pop('INFOSEEK_LEARNED_PRUNE_APPLY', None)

import entities as entities_mod  # noqa: E402
import freshness_cron as fc  # noqa: E402

_fails = []


def check(name, cond, detail=''):
    if cond:
        print(f'  [PASS] {name}')
    else:
        _fails.append(name)
        print(f'  [FAIL] {name} {detail}')


def main():
    old = (date.today() - timedelta(days=200)).isoformat()
    recent = (date.today() - timedelta(days=5)).isoformat()
    LEARNED = Path(DATA_DIR) / 'entities_learned.json'
    LEARNED.write_text(json.dumps([
        {'name': '活跃A', 'aliases': [], 'category': 'ORG',
         'created_at': old, 'last_seen_at': recent, 'source': 'learned', 'confidence': 0.9},
        {'name': '活跃B', 'aliases': [], 'category': 'ORG',
         'created_at': old, 'last_seen_at': recent, 'source': 'learned', 'confidence': 0.9},
        {'name': '活跃C', 'aliases': [], 'category': 'ORG',
         'created_at': old, 'last_seen_at': recent, 'source': 'learned', 'confidence': 0.9},
    ], ensure_ascii=False), encoding='utf-8')
    entities_mod._LEARNED_CACHE = None

    captured = {}

    def fake_prune(max_age_days=180, min_confidence=0.3, active_names=None, dry_run=True):
        captured['active_names'] = active_names
        captured['dry_run'] = dry_run
        return {'candidates': [{'name': 'x', 'age_days': 200, 'confidence': 0.1,
                                'reason': 'cold'}],
                'pruned': 0, 'remaining': 3, 'dry_run': True, 'applied': False}

    # run_full_scan 内部 `from entities import prune_learned_entities` 在调用时绑定，
    # 替换 entities 模块属性即可生效（无需触碰 cron 命名空间）。
    entities_mod.prune_learned_entities = fake_prune

    print('--- R1-a cron 第 7 步 learned prune 接线 ---')
    res = fc.FreshnessCron().run_full_scan()

    check('cron 向 prune 传入真实 active_names（集合非空）',
          isinstance(captured.get('active_names'), set)
          and len(captured.get('active_names', set())) > 0,
          str(captured.get('active_names')))
    check('cron 默认 dry_run（不真实落盘）',
          captured.get('dry_run') is True and res.get('learned_pruned') == 0, str(res))
    check('cron learned_prune 统计透出 applied 字段',
          'learned_prune_applied' in res and res.get('learned_prune_applied') is False,
          str({k: v for k, v in res.items() if 'prune' in k}))
    check('cron 透出 learned_prune_candidates',
          res.get('learned_prune_candidates') == 1,
          str(res.get('learned_prune_candidates')))

    print()
    if _fails:
        print(f'FAIL: {len(_fails)} 项失败 → {_fails}')
        sys.exit(1)
    print('ALL PASS (test_learned_prune_cron_r1a) ✅')
    sys.exit(0)


if __name__ == '__main__':
    main()
