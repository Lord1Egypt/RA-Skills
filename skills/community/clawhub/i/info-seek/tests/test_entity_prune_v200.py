#!/usr/bin/env python3
"""test_entity_prune_v200.py — learned 层冷条目清理守护（v2.0.0 实体持久层收尾，ROADMAP P1#2）

覆盖：
- P1 冷 + 低置信 learned 实体被识别为候选；近期 / 高置信 / active 保护 / 日期损坏边界
- P2 dry_run 默认不改文件（安全）
- P3 dry_run=False 原子删除并跨读取生效
- P4 env INFOSEEK_LEARNED_PRUNE_APPLY=1 强制 apply
- P5 静态词典永不被清理触碰
- P6 FreshnessCron.run_full_scan 返回 learned_prune_candidates 统计字段
"""

import json
import os
import sys
import tempfile
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

DATA_DIR = tempfile.mkdtemp(prefix='infoseek_prune_')
os.environ['INFOSEEK_DATA_DIR'] = DATA_DIR
os.environ.pop('INFOSEEK_LEARNED_PRUNE_APPLY', None)

from core import entities  # noqa: E402

LEARNED = Path(DATA_DIR) / 'entities_learned.json'
_fails = []


def check(name, cond, detail=''):
    if cond:
        print(f"  [PASS] {name}")
    else:
        _fails.append(name)
        print(f"  [FAIL] {name} {detail}")


def _write_learned(items):
    LEARNED.write_text(json.dumps(items, ensure_ascii=False), encoding='utf-8')
    entities._LEARNED_CACHE = None
    entities._ALL_ENTITIES_CACHE = None


def main():
    old = (date.today() - timedelta(days=200)).isoformat()
    recent = (date.today() - timedelta(days=5)).isoformat()
    _write_learned([
        {'name': '老噪声公司', 'aliases': [], 'category': 'AUTO',
         'created_at': old, 'last_seen_at': old, 'source': 'learned', 'confidence': 0.1},
        {'name': '老而高价值', 'aliases': [], 'category': 'PERSON',
         'created_at': old, 'last_seen_at': old, 'source': 'learned', 'confidence': 0.9},
        {'name': '新近低置信', 'aliases': [], 'category': 'AUTO',
         'created_at': recent, 'last_seen_at': recent, 'source': 'learned', 'confidence': 0.1},
        {'name': '冷但活跃保护', 'aliases': [], 'category': 'AUTO',
         'created_at': old, 'last_seen_at': old, 'source': 'learned', 'confidence': 0.1},
        {'name': '损坏日期', 'aliases': [], 'category': 'AUTO',
         'created_at': '???', 'last_seen_at': '', 'source': 'learned', 'confidence': 0.1},
    ])

    # P1 候选识别
    print("--- P1 候选识别（dry_run）---")
    before = LEARNED.read_text(encoding='utf-8')
    r = entities.prune_learned_entities(
        max_age_days=180, min_confidence=0.3,
        active_names={'冷但活跃保护'}, dry_run=True)
    names = {c['name'] for c in r['candidates']}
    check('老+低置信 → 候选', '老噪声公司' in names, str(names))
    check('老+高置信仍算冷条目候选', '老而高价值' in names, str(names))
    check('日期损坏 → 超龄候选', '损坏日期' in names, str(names))
    check('新近低置信保留（未超龄）', '新近低置信' not in names, str(names))
    check('active_names 保护冷条目', '冷但活跃保护' not in names, str(names))

    # P2 dry_run 不落盘
    print("--- P2 dry_run 安全 ---")
    check('dry_run=True 不写文件', LEARNED.read_text(encoding='utf-8') == before)
    check('返回 dry_run 标志', r['dry_run'] is True and r['pruned'] == 0, str(r))
    check('remaining 反映原始数量', r['remaining'] == 5, str(r))

    # P3 真实 apply
    print("--- P3 apply 原子删除 ---")
    r3 = entities.prune_learned_entities(
        max_age_days=180, min_confidence=0.3,
        active_names={'冷但活跃保护'}, dry_run=False)
    check('apply 后 pruned=3', r3['pruned'] == 3, str(r3))
    check('apply 后 remaining=2', r3['remaining'] == 2, str(r3))
    check('apply applied=True', r3['applied'] is True, str(r3))
    on_disk = {e['name'] for e in json.loads(LEARNED.read_text(encoding='utf-8'))}
    check('磁盘只留保护/新近两项', on_disk == {'新近低置信', '冷但活跃保护'}, str(on_disk))
    entities._LEARNED_CACHE = None
    merged_names = {e['name'] for e in entities.get_learned_entities(force=True)}
    check('get_learned_entities 读回已清理结果', merged_names == on_disk, str(merged_names))

    # P4 env 强制 apply
    print("--- P4 env INFOSEEK_LEARNED_PRUNE_APPLY ---")
    _write_learned([
        {'name': '又一条老噪声', 'aliases': [], 'category': 'AUTO',
         'created_at': old, 'last_seen_at': old, 'source': 'learned', 'confidence': 0.1},
    ])
    os.environ['INFOSEEK_LEARNED_PRUNE_APPLY'] = '1'
    r4 = entities.prune_learned_entities(max_age_days=180, dry_run=True)
    check('env 强制 apply 生效（dry_run 被覆盖）', r4['applied'] is True and r4['pruned'] == 1,
          str(r4))
    os.environ.pop('INFOSEEK_LEARNED_PRUNE_APPLY', None)

    # P5 静态词典不受影响
    print("--- P5 静态词典零污染 ---")
    static_n = len(entities.ORG_ENTITIES + entities.PERSON_ENTITIES)
    check('静态 ORG/PERSON 条目仍在', static_n > 0 and
          any(e['name'] == 'OpenAI' for e in entities.get_all_entities()))

    # P6 cron 字段
    print("--- P6 FreshnessCron 统计字段 ---")
    sys.path.insert(0, str(Path(__file__).parent.parent / 'core'))
    import unittest.mock as mock
    import freshness_cron as fc
    with mock.patch('wikidata_sync.WikidataSync.verify_existence',
                    side_effect=RuntimeError('offline')):
        res = fc.FreshnessCron().run_full_scan()
    check('cron 返回 learned_prune_candidates 字段',
          'learned_prune_candidates' in res, str(sorted(res.keys())))
    check('cron 默认 dry_run（pruned=0）', res.get('learned_pruned') == 0,
          str(res.get('learned_pruned')))

    print()
    if _fails:
        print(f"FAIL: {len(_fails)} 项失败 → {_fails}")
        sys.exit(1)
    print("ALL PASS (test_entity_prune_v200) ✅")
    sys.exit(0)


if __name__ == '__main__':
    main()
