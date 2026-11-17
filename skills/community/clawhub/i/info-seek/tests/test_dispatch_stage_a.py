#!/usr/bin/env python3
"""调度台阶段A（mod-v1.5.1，PATCH 零行为变化）专项守护。

覆盖 §6A.10 的：
  守护③ CN_SUBQ 四态 env（含旧布尔值兼容映射）
  守护④ always 旧全扇出行为锁定
以及阶段A配套：
  - 调用预算 env 解析（INFOSEEK_QUERY_BUDGET_VARIANTS 默认 2、下限 1、非法回落）
  - _resolve_subqueries 纯函数：off=仅整句；always/auto/stage=旧 decompose 全扇出
  - 旧布尔开关默认（空）等价 always
全离线、零网络（monkeypatch 掉 decompose，用桩计数）。
"""
import os
import sys
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))
sys.path.insert(0, str(Path(__file__).parent.parent / 'core'))

CN_KEYS = ('INFOSEEK_CN_SUBQ', 'INFOSEEK_QUERY_BUDGET_VARIANTS')
for _k in list(os.environ):
    if _k in CN_KEYS:
        os.environ.pop(_k, None)

P, F = [], []
def ok(n, c, x=''):
    (P if c else F).append(n); print(f"  {'PASS' if c else 'FAIL'} {n} {x}")

import infoseek_pipeline as p  # noqa: E402

print("═══ 守护③ CN_SUBQ 四态解析 ═══")
def _mode(val):
    if val is None:
        os.environ.pop('INFOSEEK_CN_SUBQ', None)
    else:
        os.environ['INFOSEEK_CN_SUBQ'] = val
    return p._cn_subq_mode()

ok("M1 未设置默认 → always（等价旧布尔开）", _mode(None) == 'always')
ok("M2 显式 always", _mode('always') == 'always')
ok("M3 显式 auto", _mode('auto') == 'auto')
ok("M4 显式 stage", _mode('stage') == 'stage')
ok("M5 显式 off", _mode('off') == 'off')
ok("M6 大小写/空白容错（' AUTO '）", _mode('  AUTO ') == 'auto')

print("═══ 守护③ 旧布尔兼容映射 ═══")
for v in ('0', 'false', 'False', 'no', 'off', 'OFF', ' 0 '):
    ok(f"M7 旧布尔关 '{v}' → off", _mode(v) == 'off')
for v in ('1', 'true', 'True', 'yes', 'on'):
    ok(f"M8 旧布尔开 '{v}' → always（非 stage）", _mode(v) == 'always')
ok("M9 非法值 → always 保守回退", _mode('weird') == 'always')

print("═══ 调用预算 env 解析 ═══")
def _bud(val):
    if val is None:
        os.environ.pop('INFOSEEK_QUERY_BUDGET_VARIANTS', None)
    else:
        os.environ['INFOSEEK_QUERY_BUDGET_VARIANTS'] = val
    return p._query_budget_variants()
ok("B1 默认预算=2", _bud(None) == 2)
ok("B2 显式 4", _bud('4') == 4)
ok("B3 0 被夹到下限 1", _bud('0') == 1)
ok("B4 负数夹到 1", _bud('-3') == 1)
ok("B5 浮点串取整 3", _bud('3.9') == 3)
ok("B6 非法回退默认 2", _bud('abc') == 2)
ok("B7 空白回退默认 2", _bud('   ') == 2)

print("═══ 守护④ always 旧全扇出 + _resolve_subqueries 等价性 ═══")
# 用桩替代 decompose：记录调用、回显，证明 always/auto/stage 都走旧全扇出路径
calls = {'n': 0}
def _fake_decompose(q):
    calls['n'] += 1
    return [q, q + ' 核心', q + ' 价格']
with mock.patch.object(p, '_decompose_longtail_cn', side_effect=_fake_decompose) as m_dec:
    calls['n'] = 0
    r_off = p._resolve_subqueries('原句', '扩展句', mode='off')
    ok("R1 off → 仅整句 [expanded]，零 decompose 调用",
       r_off == ['扩展句'] and calls['n'] == 0)
    calls['n'] = 0
    r_always = p._resolve_subqueries('原句', '扩展句', mode='always')
    ok("R2 always → decompose 全扇出（多子查询）",
       r_always == ['扩展句', '扩展句 核心', '扩展句 价格'] and calls['n'] == 1)
    calls['n'] = 0
    r_auto = p._resolve_subqueries('原句', '扩展句', mode='auto')
    ok("R3 阶段A auto 等价 always（走 decompose）",
       r_auto == r_always and calls['n'] == 1)
    calls['n'] = 0
    r_stage = p._resolve_subqueries('原句', '扩展句', mode='stage')
    ok("R4 阶段A stage 暂等价 always（阶梯留待阶段B）",
       r_stage == r_always and calls['n'] == 1)
    ok("R5 off 路径 decompose 从未被调（全程 0 次仅 R1）", m_dec.call_count == 3)

print("═══ 默认零行为变化：端到端 subs 产出与旧布尔实现对拍 ═══")
# 真实 decompose，不 mock：对拍「新 resolve(默认)」与「旧布尔逻辑」逐字节一致
long_q = '信阳板栗今年最新收购价格行情走势'   # CJK≥6 长尾
old_default = p._decompose_longtail_cn(long_q)   # 旧：默认 True
os.environ.pop('INFOSEEK_CN_SUBQ', None)
new_default = p._resolve_subqueries(long_q, long_q, mode=p._cn_subq_mode())
ok("E1 长尾 query 默认新路径 == 旧布尔开 decompose", new_default == old_default)
ok("E2 长尾拆解确实产出多子查询（全扇出前提成立）", len(new_default) >= 2)
short_q = '板栗'
old_short = p._decompose_longtail_cn(short_q)
new_short = p._resolve_subqueries(short_q, short_q, mode=p._cn_subq_mode())
ok("E3 短词 query 新旧一致（原样单条）", new_short == old_short == ['板栗'])
# 旧布尔关：_env_flag(CN_SUBQ,True)=False 时 subs=[query]；新 off 必须一致
os.environ['INFOSEEK_CN_SUBQ'] = '0'
new_off = p._resolve_subqueries(long_q, long_q, mode=p._cn_subq_mode())
ok("E4 旧布尔关(=0) == 仅整句", new_off == [long_q])

print("═══ Stage 脚手架常量存在（阶段B使用，阶段A不改执行路径）═══")
ok("S1 STAGE0/1/2 阶梯常量",
   (p.STAGE0, p.STAGE1, p.STAGE2) == (0, 1, 2))
ok("S2 晋升最小剩余时间=1.2s（守护②常量）", p._STAGE_MIN_REMAIN_S == 1.2)
ok("S3 四态集合齐备", set(p._CN_SUBQ_MODES) == {'off', 'always', 'auto', 'stage'})

print(f"\ntest_dispatch_stage_a: {len(P)} PASS / {len(F)} FAIL")
if F:
    print("未通过：" + ", ".join(F)); sys.exit(1)
print("ALL GREEN")
