#!/usr/bin/env python3
"""test_engine_lifecycle_v101.py — 搜索引擎全生命周期管理测试（v1.0.1 评估升级 P0/P1/P2）

覆盖：
  EL1 错误分类（timeout/network/quota/forbidden/parse/unknown）
  EL2 配额耗尽 → 禁用 + get_active 过滤
  EL3 连续失败阈值 → 临时禁用
  EL4 成功清除失败计数
  EL5 reset 单/全
  EL6 持久化往返
  EL7 集成：search_web 经 _call_engine 包装，429 引擎被跳过并标记
"""

import os
import sys
import time
import tempfile
from pathlib import Path

INFOSEEK = Path(__file__).parent.parent
sys.path.insert(0, str(INFOSEEK / 'scripts'))
sys.path.insert(0, str(INFOSEEK / 'core'))

import engine_lifecycle as el

# 隔离数据目录
_tmp = tempfile.mkdtemp()
os.environ['INFOSEEK_DATA_DIR'] = _tmp
el.reset_instance()

passed, failed = [], []
def check(name, cond, detail=''):
    (passed if cond else failed).append(name)
    print(f"[{'PASS' if cond else 'FAIL'}] {name}" + (f" — {detail}" if detail else ""))


# ── EL1: 错误分类 ──
class _HTTPExc(Exception):
    def __init__(self, code, headers=None):
        self.code = code
        self.headers = headers or {}
check('EL1 429→quota', el.EngineLifecycle.classify(_HTTPExc(429)) == el.ERR_QUOTA)
check('EL1 403→forbidden', el.EngineLifecycle.classify(_HTTPExc(403)) == el.ERR_FORBIDDEN)
check('EL1 404→parse', el.EngineLifecycle.classify(_HTTPExc(404)) == el.ERR_PARSE)
check('EL1 TimeoutError→timeout', el.EngineLifecycle.classify(TimeoutError('timed out')) == el.ERR_TIMEOUT)
check('EL1 conn refused→network',
      el.EngineLifecycle.classify(Exception('urllib.error urlopen connection refused')) == el.ERR_NETWORK)
check('EL1 未知→unknown', el.EngineLifecycle.classify(Exception('weird')) == el.ERR_UNKNOWN)


# ── EL2: 配额耗尽 → 禁用 + 过滤 ──
lc = el.get_lifecycle()
lc.reset()
lc.record_failure('Exa', _HTTPExc(429))
check('EL2 配额后禁用', lc.is_disabled('Exa'))
active = [n for n, _ in lc.get_active([('Exa', None), ('Bing-RSS', None), ('Tavily', None)])]
check('EL2 get_active 过滤配额耗尽', active == ['Bing-RSS', 'Tavily'], f"{active}")


# ── EL3: 连续失败阈值 → 临时禁用 ──
lc2 = el.EngineLifecycle()
for _ in range(3):
    lc2.record_failure('Tavily', Exception('boom'))
check('EL3 3次失败禁用', lc2.is_disabled('Tavily'))
lc2.record_success('Tavily')
check('EL3 成功后解禁', not lc2.is_disabled('Tavily'))


# ── EL4: 成功清除失败计数（不清除配额标记）──
lc3 = el.EngineLifecycle()
lc3.record_failure('Exa', _HTTPExc(429))   # 配额耗尽
lc3.record_success('Exa')                   # 清除连续失败，但配额仍耗尽
st = lc3.status()['Exa']
check('EL4 成功清失败计数', st['fail_count'] == 0)
check('EL4 配额标记保留', st['quota_exhausted'] is True and lc3.is_disabled('Exa'))


# ── EL5: reset ──
lc.reset('Exa')
check('EL5 单引擎 reset', not lc.is_disabled('Exa') and 'Exa' not in lc.status())
lc.record_failure('Metaso', Exception('x'))
lc.reset()
check('EL5 全量 reset', lc.status() == {})


# ── EL6: 持久化往返 ──
lc.reset()
lc.record_failure('Zhipu', _HTTPExc(401))
p = Path(_tmp) / 'engine_state.json'
check('EL6 状态已落盘', p.exists())
lc2b = el.EngineLifecycle()
check('EL6 重载后保留', lc2b.status().get('Zhipu', {}).get('last_error') == el.ERR_FORBIDDEN)


# ── EL7: 集成 _call_engine 包装（429 引擎被标记并跳过）──
import infoseek_pipeline as pipe
el.reset_instance()
lc_i = el.get_lifecycle()
# EL7a: _call_engine 直接集成
def _exa_429(q, n):
    raise _HTTPExc(429)
r = pipe._call_engine('Exa', _exa_429, 'q', 5)
check('EL7a _call_engine 失败返回 []', r == [])
check('EL7a Exa 被标记配额禁用', lc_i.is_disabled('Exa'))

# EL7b: search_web（ai 模式，Exa 在层内）仍返回结果，Exa 被标记
os.environ['EXA_API_KEY'] = 'sk-test-x'
os.environ['INFOSEEK_SEARCH_PARALLEL'] = '1'
os.environ['INFOSEEK_SEARCH_ENGINE'] = 'ai'
el.reset_instance()
lc_i = el.get_lifecycle()
orig_bing = pipe._search_bing_rss
pipe._search_bing_rss = lambda q, n: [{"url": "https://x.com/1", "title": q, "snippet": "s"}]
got = pipe.search_web('测试查询', max_results=5)
pipe._search_bing_rss = orig_bing
check('EL7b search_web 仍返回结果', len(got) >= 1, f"got={len(got)}")
check('EL7b Exa 被标记配额禁用', lc_i.is_disabled('Exa'))
os.environ.pop('EXA_API_KEY', None)
os.environ['INFOSEEK_SEARCH_ENGINE'] = 'auto'


# ── P3: 新鲜度动态管理（配额重置/存活恢复/API漂移/对账CLI）──
class _HExc(Exception):
    def __init__(self, code, headers=None):
        self.code = code
        self.headers = headers or {}

now = time.time()

# P3.1 配额重置时刻推算（直接验证 _quota_reset_epoch 各模式）
rd = el._quota_reset_epoch(None, 'daily')
check('P3.1 daily 重置在未来1天内', now < rd <= now + 86400 + 60, f"rd={rd}")
rh = el._quota_reset_epoch(None, 'hourly')
check('P3.1 hourly 重置在未来1h内', now < rh <= now + 3600 + 60, f"rh={rh}")
rm = el._quota_reset_epoch(None, 'monthly')
check('P3.1 monthly 重置在下月1日(0-32天内)', now < rm <= now + 32*86400, f"rm={rm}")

# P3.1 配额到期自动清零（reconcile）
lc_p31 = el.EngineLifecycle()
lc_p31.reset()
el._QUOTA_RESET_MODE = 'daily'
lc_p31.record_failure('Bing', _HExc(429))
st = lc_p31.status()['Bing']
check('P3.1 配额耗尽已标记', st['quota_exhausted'] is True and lc_p31.is_disabled('Bing'))
lc_p31._engines['Bing']['quota_reset_at'] = int(now) - 10   # 模拟「重置时刻已过」（改真实状态）
lc_p31._persist()
changed = lc_p31.reconcile('Bing')
check('P3.1 reconcile 自动清零配额', changed and not lc_p31.status()['Bing']['quota_exhausted'])
check('P3.1 清零后不再禁用', not lc_p31.is_disabled('Bing'))

# P3.2 认证自动恢复（启用）vs 保持禁用（关闭）
el._AUTH_RECOVER_SECONDS = 3600
lc_p32 = el.EngineLifecycle()
lc_p32.reset()
lc_p32.record_failure('Tavily', _HExc(401))   # auth_broken (sticky 默认开)
check('P3.2 认证损坏禁用', lc_p32.is_disabled('Tavily'))
lc_p32._engines['Tavily']['last_failure'] = int(now) - 4000   # 冷却期满（改真实状态）
lc_p32._persist()
changed = lc_p32.reconcile('Tavily')
check('P3.2 冷却期满自动恢复', changed and not lc_p32.status()['Tavily']['auth_broken'])
check('P3.2 恢复后不再禁用', not lc_p32.is_disabled('Tavily'))

el._AUTH_RECOVER_SECONDS = 0                  # 关闭自动恢复（保持 sticky）
lc_p32b = el.EngineLifecycle()
lc_p32b.reset()
lc_p32b.record_failure('Metaso', _HExc(403))
lc_p32b._engines['Metaso']['last_failure'] = int(now) - 4000
lc_p32b._persist()
changed = lc_p32b.reconcile('Metaso')
check('P3.2 恢复关闭时保持禁用', not changed and lc_p32b.is_disabled('Metaso'))

# P3.3 API 漂移检测（默认关 → 不标记；开启 → 连续 N 次不一致标记）
_res_a = [{'url': 'u', 'title': 't', 'snippet': 's'}]
_res_b = [{'url': 'u', 'title': 't', 'content': 'c'}]   # 不同顶层 key → 不同签名
el._API_DRIFT = True
el._API_DRIFT_N = 3
lc_p33 = el.EngineLifecycle()
lc_p33.reset()
lc_p33.record_success('Exa', _res_a)          # 建基线
check('P3.3 基线签名已建', lc_p33.status()['Exa']['response_signature'] != '')
for _ in range(3):
    lc_p33.record_success('Exa', _res_b)
st = lc_p33.status()['Exa']
check('P3.3 漂移触发 api_changed', st['api_changed'] is True)
check('P3.3 漂移不导致禁用', not lc_p33.is_disabled('Exa'))

el._API_DRIFT = False
lc_p33b = el.EngineLifecycle()
lc_p33b.reset()
lc_p33b.record_success('Exa', _res_a)
for _ in range(5):
    lc_p33b.record_success('Exa', _res_b)
check('P3.3 关闭时不标记', lc_p33b.status()['Exa']['api_changed'] is False)

# P3.4 全量对账 + CLI 子命令
el._QUOTA_RESET_MODE = 'daily'
el._AUTH_RECOVER_SECONDS = 3600
lc_p34 = el.EngineLifecycle()
lc_p34.reset()
lc_p34.record_failure('A', _HExc(429))
lc_p34.record_failure('B', _HExc(401))
stA = lc_p34._engines['A']; stA['quota_reset_at'] = int(now) - 1; lc_p34._persist()
stB = lc_p34._engines['B']; stB['last_failure'] = int(now) - 4000; lc_p34._persist()
n = lc_p34.reconcile_all()
check('P3.4 reconcile_all 恢复 2 个', n == 2, f"n={n}")
check('P3.4 A 配额已清', not lc_p34.status()['A']['quota_exhausted'])
check('P3.4 B 认证已清', not lc_p34.status()['B']['auth_broken'])
el._QUOTA_RESET_MODE = 'monthly'
el._AUTH_RECOVER_SECONDS = 0

# CLI 子命令接线验证（engine-reconcile / engine-probe / engine-status 均可无异常运行）
try:
    import infoseek_keys_cli as _cli
    class _Args:
        engine = None
    _a = _Args()
    rc_rec = _cli.cmd_engine_reconcile(_a)
    rc_prb = _cli.cmd_engine_probe(_a)
    rc_st = _cli.cmd_engine_status(_a)
    check('P3.4 CLI reconcile 返回0', rc_rec == 0)
    check('P3.4 CLI probe 返回0', rc_prb == 0)
    check('P3.4 CLI status 返回0', rc_st == 0)
except Exception as _e:
    check('P3.4 CLI 子命令可加载', False, str(_e))


print(f"\n=== 引擎生命周期测试: {len(passed)} PASS / {len(failed)} FAIL ===")
if failed:
    print("FAILED:", failed)
    sys.exit(1)
print("ALL PASS")
