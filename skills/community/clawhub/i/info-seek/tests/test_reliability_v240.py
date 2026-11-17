#!/usr/bin/env python3
"""Infoseek v2.4.0 L3 可靠性测试（10 用例）

覆盖：文件损坏/权限/超时/步骤失败的容错
"""
import sys, os, json, tempfile
from pathlib import Path
from unittest import mock

INFOSEEK = Path(__file__).parent.parent
sys.path.insert(0, str(INFOSEEK / 'core'))
sys.path.insert(0, str(INFOSEEK / 'scripts'))

passed, failed = [], []
def check(name, cond, extra=''):
    if cond:
        passed.append(name); print(f"  [PASS] {name} {extra}")
    else:
        failed.append(name); print(f"  [FAIL] {name} {extra}")


# L3-01 claim_store 文件损坏（坏 JSON）
from claim_store import ClaimStore
tf = tempfile.mktemp(suffix='.json')
with open(tf, 'w') as f:
    f.write('{[invalid json garbage')
cs = ClaimStore(path=tf)
try:
    data = cs.load()
    check('L3-01 坏 JSON 不抛', data == {}, f"data={data}")
except Exception as e:
    check('L3-01 坏 JSON 不抛', False, f"raised {type(e).__name__}")
os.remove(tf)

# L3-02 claim_store 文件不存在
tf2 = tempfile.mktemp(suffix='.json')
cs2 = ClaimStore(path=tf2)
try:
    data = cs2.load()
    check('L3-02 文件不存在返回空', data == {}, f"data={data}")
except Exception as e:
    check('L3-02 文件不存在返回空', False, f"raised {type(e).__name__}")
# 写到不存在路径再 save
cs2.add_claim('X', {'source': 'a', 'text': 'b', 'timestamp': '2026-08-01'})
try:
    cs2.save()
    check('L3-02 save 创建文件', os.path.exists(tf2))
except Exception as e:
    check('L3-02 save 创建文件', False, f"raised {type(e).__name__}: {e}")
os.remove(tf2)

# L3-03 entity_trajectory 损坏 profile JSON
tf3 = tempfile.mktemp(suffix='.json')
with open(tf3, 'w') as f:
    f.write('{"SomeEntity": {truncated garbage')
import entity_profile
with mock.patch.object(entity_profile, 'CORE_DIR', Path(tf3).parent):
    with mock.patch.object(entity_profile.EntityProfile, 'PROFILE_FILE', tf3):
        from entity_trajectory import trace_entity
        try:
            r = trace_entity('SomeEntity', days_back=90)
            check('L3-03 损坏 profile 不崩',
                  'timeline' in r, f"keys={list(r.keys())[:5]}")
        except Exception as e:
            check('L3-03 损坏 profile 不崩', False, f"raised {type(e).__name__}: {e}")

# L3-04 entity_heat tracker.load 失败
import entity_tracker
with mock.patch.object(entity_tracker.EntityTracker, '_find_entity',
                       side_effect=RuntimeError('mock')):
    from entity_heat import predict_heat
    try:
        r = predict_heat('OpenAI', days_ahead=7)
        check('L3-04 heat tracker 失败不崩',
              isinstance(r, dict) and r.get('recommendation') == 'cold',
              f"rec={r.get('recommendation')} err_source={r.get('error_source')}")
    except Exception as e:
        check('L3-04 heat tracker 失败不崩', False, f"raised {type(e).__name__}: {e}")

# L3-05 contradiction_scorer 模板抛异常（mock re）
import contradiction_scorer as cs_mod
orig_finditer = cs_mod.re.finditer
def _boom(*a, **kw):
    raise RuntimeError('mock re error')
with mock.patch.object(cs_mod.re, 'finditer', side_effect=_boom):
    from contradiction_scorer import score_contradiction
    try:
        r = score_contradiction({'text': 'X 不发布'}, {'text': 'X 发布'})
        check('L3-05 模板异常不崩',
              isinstance(r, dict) and 'score' in r,
              f"score={r.get('score')} reasons={r.get('reasons')}")
    except Exception as e:
        check('L3-05 模板异常不崩', False, f"raised {type(e).__name__}: {e}")

# L3-06 research() 步骤9 detect_conflicts_v3 抛错
from infoseek_core_v2 import research
SRC = [{'title': 'A', 'snippet': 'OpenAI 开源', 'url': 'https://a.com/1'}]
# 改用 mock.patch 模块属性（research 内部是局部 import conflict_v3）
with mock.patch('conflict_v3.detect_conflicts_v3', side_effect=RuntimeError('mock')):
    try:
        r6 = research('AI', sources=SRC)
        check('L3-06 research 步骤9 失败不崩',
              isinstance(r6, dict) and 'conflict_v3' in r6,
              f"keys={list(r6.keys())[:5]}")
    except Exception as e:
        check('L3-06 research 步骤9 失败不崩', False, f"raised {type(e).__name__}: {e}")

# L3-07 research() 步骤10 entity_profile 抛错
import entity_profile as ep_mod
with mock.patch.object(ep_mod.EntityProfile, 'update_profiles',
                       side_effect=RuntimeError('mock')):
    try:
        r7 = research('AI', sources=SRC)
        check('L3-07 research 步骤10 失败不崩',
              isinstance(r7, dict),
              f"profiles={r7.get('entity_profiles')}")
    except Exception as e:
        check('L3-07 research 步骤10 失败不崩', False, f"raised {type(e).__name__}: {e}")

# L3-08 research() 步骤10.1 heat_ranking 抛错
# v2.4.1 PATCH 后 infoseek_core_v2 内部 import get_heat_ranking，需要 patch 在正确命名空间
import sys as _sys
# 提前 import 让模块名出现在 sys.modules
import entity_heat as _eh_mod_pre
_sys.modules['infoseek_core_v2.entity_heat'] = _eh_mod_pre
with mock.patch.object(_eh_mod_pre, 'get_heat_ranking', side_effect=RuntimeError('mock')):
    try:
        r8 = research('AI', sources=SRC)
        check('L3-08 research 步骤10.1 失败不崩',
              isinstance(r8, dict),
              f"heat={r8.get('heat_ranking')}")
    except Exception as e:
        check('L3-08 research 步骤10.1 失败不崩', False, f"raised {type(e).__name__}: {e}")

# L3-09 freshness_cron wikidata 超时（mock 30s 延迟）
from freshness_cron import FreshnessCron
import wikidata_sync as ws_mod

def _slow_verify(*a, **kw):
    import time as _t
    _t.sleep(0.1)  # 0.1s 模拟（避免真 30s 拖时间）
    return True

with mock.patch.object(ws_mod.WikidataSync, 'verify_existence', side_effect=_slow_verify):
    import time as _t
    t0 = _t.time()
    try:
        cron = FreshnessCron()
        cron_res = cron.run_full_scan()
        elapsed = (_t.time() - t0) * 1000
        check('L3-09 cron wikidata 失败不卡死',
              elapsed < 5000 and isinstance(cron_res, dict),
              f"elapsed={elapsed:.1f}ms")
    except Exception as e:
        check('L3-09 cron wikidata 失败不卡死', False, f"raised {type(e).__name__}: {e}")

# L3-10 concurrent claim_store add 不丢数据（单进程多线程）
from claim_store import ClaimStore
import threading
tf10 = tempfile.mktemp(suffix='.json')
cs10 = ClaimStore(path=tf10); cs10.clear()
def worker(i):
    cs10.add_claim('Co', {'source': f'http://x/{i}', 'text': f't{i}',
                            'timestamp': '2026-08-01'})
threads = [threading.Thread(target=worker, args=(i,)) for i in range(50)]
for t in threads: t.start()
for t in threads: t.join()
cs10.save()
cs10r = ClaimStore(path=tf10)
n = len(cs10r.get_claims('Co'))
check('L3-10 多线程 add', n == 50, f"count={n}")
os.remove(tf10)


print(f"\n=== L3 可靠性: {len(passed)} PASS / {len(failed)} FAIL ===")
if failed:
    print("FAILED:", failed); sys.exit(1)
print("ALL PASS")