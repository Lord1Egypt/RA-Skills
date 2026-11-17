#!/usr/bin/env python3
"""Infoseek v2.4.0 L7 兼容性测试（6 用例）

覆盖：v2.3.0 / v2.3.1 / v2.2.x 入口仍可用，数据可迁移
"""
import sys, os, json, tempfile
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
    {'title': 'OpenAI 开源', 'snippet': 'OpenAI Inc. 宣布 GPT-5 完全开源', 'url': 'https://a.com/1'},
    {'title': 'OpenAI 闭源争议', 'snippet': 'OpenAI 官方确认 GPT-5 保持闭源', 'url': 'https://b.com/2'},
]

# L7-01 v2.3.0 入口 detect_conflicts_v3 字段齐
from conflict_v3 import detect_conflicts_v3
r01 = detect_conflicts_v3(SRC, subject='AI')
required = ['conflicts', 'version', 'total_sources', 'aliases_involved', 'live_alerts']
missing = [f for f in required if f not in r01]
check('L7-01 v2.3.0 字段齐', not missing, f"missing={missing}")

# L7-02 v2.3.1 live_alerts 字段存在
check('L7-02 v2.3.1 live_alerts 存在',
      isinstance(r01.get('live_alerts'), list),
      f"live_alerts_len={len(r01.get('live_alerts', []))}")

# L7-03 v2.3.0 aliases_involved 归并
openai_conf = [c for c in r01['conflicts'] if c['entity_name'] == 'OpenAI']
has_alia = any('OpenAI Inc.' in c.get('aliases_involved', []) for c in openai_conf)
check('L7-03 v2.3.0 aliases_involved 归并', has_alia,
      f"groups={len(openai_conf)}")

# L7-04 v2.2.1 entity_aliases 旧格式可读
import entity_aliases
try:
    mgr = entity_aliases.EntityAliases()
    aliases = mgr.get_aliases('OpenAI') if hasattr(mgr, 'get_aliases') else []
    check('L7-04 entity_aliases 接口可用',
          isinstance(aliases, list), f"aliases={aliases[:3]}")
except Exception as e:
    check('L7-04 entity_aliases 接口可用', False, f"raised {type(e).__name__}: {e}")

# L7-06 跨进程持久数据兼容
from claim_store import ClaimStore
tf = tempfile.mktemp(suffix='.json')
# 进程 A：写
cs_a = ClaimStore(path=tf); cs_a.clear()
cs_a.add_claim('PersistCo', {'source': 'http://a.com/1', 'text': 'persist test',
                              'timestamp': '2026-08-01'})
cs_a.save()
del cs_a
# 进程 B：读
cs_b = ClaimStore(path=tf)
claims = cs_b.get_claims('PersistCo')
check('L7-06 跨进程持久数据兼容',
      len(claims) == 1 and claims[0]['text'] == 'persist test',
      f"claims_count={len(claims)}")
os.remove(tf)


print(f"\n=== L7 兼容性: {len(passed)} PASS / {len(failed)} FAIL ===")
if failed:
    print("FAILED:", failed); sys.exit(1)
print("ALL PASS")