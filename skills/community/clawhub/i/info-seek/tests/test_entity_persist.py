#!/usr/bin/env python3
"""
tests/test_entity_persist.py — 实体追踪器持久层回归（P1-1 G1 修复，v2.5.0）

覆盖：
- P1 record_hit / record_hits_batch 落盘，新实例读回
- P2 静态源零污染（静态词典不被运行时状态改写）
- P3 损坏状态文件容错（备份 .corrupt.bak + 空状态）
- P4 INFOSEEK_ENTITY_PERSIST=0 关闭（纯内存回退）
- P5 apply_decay 衰减落盘，跨实例持久
"""

import json
import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

DATA_DIR = tempfile.mkdtemp(prefix='infoseek_entpersist_')
os.environ['INFOSEEK_DATA_DIR'] = DATA_DIR
os.environ.pop('INFOSEEK_DB', None)
os.environ['INFOSEEK_ENTITY_PERSIST'] = '1'

from core.entity_tracker import EntityTracker  # noqa: E402
from core.entity_tracker import reset_tracker  # noqa: E402
from core import entities  # noqa: E402

STATE_FILE = os.path.join(DATA_DIR, 'entities_state.json')

_fails = []


def _check(name, cond, detail=''):
    if cond:
        print(f"  [PASS] {name}")
    else:
        _fails.append(name)
        print(f"  [FAIL] {name} {detail}")


def main():
    reset_tracker()

    # P1 记录 + 落盘 + 跨实例读回
    print("--- P1 记录/落盘/跨实例 ---")
    t1 = EntityTracker()
    _check('record_hit 已知实体', t1.record_hit('OpenAI') is True)
    _check('record_hit 未知实体拒绝', t1.record_hit('__NOPE_ENT__') is False)
    r = t1.record_hits_batch(['OpenAI', '__NOPE__', '比亚迪', 'NVIDIA'])
    _check('record_hits_batch 计数', r == {'total': 4, 'success': 3, 'unknown': 1}, str(r))
    _check('状态文件已生成', os.path.exists(STATE_FILE))
    data = json.loads(Path(STATE_FILE).read_text(encoding='utf-8'))
    _check('落盘 hit 计数', data['entities']['OpenAI']['hit_count_30d'] == 2,
           str(data['entities'].get('OpenAI')))
    t2 = EntityTracker()
    v = t2._find_entity('OpenAI')
    _check('跨实例读回', v and v['hit_count_30d'] == 2, str(v))
    hot = t2.get_hot_entities(top_n=5)
    _check('get_hot 反映状态', hot and hot[0]['name'] == 'OpenAI', str(hot[:1]))

    # P2 静态源零污染
    print("--- P2 静态源零污染 ---")
    static = [e for e in entities.get_all_entities() if e['name'] == 'OpenAI'][0]
    _check('静态 hit_count 未被改写', static['hit_count_30d'] == 0,
           str(static.get('hit_count_30d')))

    # P3 损坏容错
    print("--- P3 损坏容错 ---")
    Path(STATE_FILE).write_text('{corrupt!!!', encoding='utf-8')
    t3 = EntityTracker()
    _check('损坏 → 空状态', t3._state == {})
    _check('损坏备份生成', os.path.exists(STATE_FILE + '.corrupt.bak'))

    # P4 开关关闭
    print("--- P4 开关关闭 ---")
    os.remove(STATE_FILE)
    try:
        if os.path.exists(STATE_FILE + '.corrupt.bak'):
            os.remove(STATE_FILE + '.corrupt.bak')
    except OSError:
        pass
    os.environ['INFOSEEK_ENTITY_PERSIST'] = '0'
    t4 = EntityTracker()
    t4.record_hit('OpenAI')
    _check('关闭时不落盘', not os.path.exists(STATE_FILE))
    os.environ['INFOSEEK_ENTITY_PERSIST'] = '1'

    # P5 衰减持久
    print("--- P5 衰减持久 ---")
    t5 = EntityTracker()
    t5.record_hit('OpenAI')
    st = t5._state['OpenAI']
    st['hit_count_30d'] = 100
    st['last_seen_at'] = '2026-01-01'  # 故意置旧 → 触发衰减
    t5._mark_dirty()
    t5._save_state()
    d = t5.apply_decay()
    _check('衰减发生', d['decayed_count'] >= 1, str(d))
    t6 = EntityTracker()
    _check('衰减跨实例持久', t6._state['OpenAI']['hit_count_30d'] < 100,
           str(t6._state['OpenAI'].get('hit_count_30d')))

    print()
    if _fails:
        print(f"FAIL: {len(_fails)} 项失败 → {_fails}")
        sys.exit(1)
    print("ALL PASS (test_entity_persist) ✅")
    sys.exit(0)


if __name__ == '__main__':
    main()