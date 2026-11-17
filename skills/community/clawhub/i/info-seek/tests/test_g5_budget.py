#!/usr/bin/env python3
"""test_g5_budget.py — 搜索层 G5 P1/P2 测试（v1.6.1）
提前收敛 + 保留池入预算 + 层间共享总预算 + 超窗计数降级。

覆盖：
  R1 提前收敛（EARLY_FACTOR）：快引擎结果 ≥ max_results×1.5 提前返回，不等慢引擎
  R1b 提前收敛关闭（EARLY_FACTOR=0）：等全部
  R2 保留池兜底纳入预算：主并行不足 → 保留引擎并行兜底于剩余预算（无 0.8s 串行）
  R3 预算耗尽跳过兜底：remaining ≤ 0.05 → 不兜底快速返回
  R4 层间共享总预算（search_web 端到端）：AI 层空 → 默认层用剩余预算，总耗时 ≤ 预算
  R4b 共享预算关闭（SHARED_BUDGET=0）：各层各耗窗口（dealine=None，原语义）
  R5 超窗计数降级：连续 N 次超窗 → 临时 mute（后续调用不拉起）
  R6 mute 冷却复活：静默期到期后引擎恢复参与
  R7 参数读取与回退（EARLY_FACTOR / SHARED_BUDGET / TOTAL_BUDGET_MS / OVERRUN_*）
  R8 deadline 直接传递：_parallel_merge(deadline=now+0.2) 越过本层窗口生效

设计约束：慢引擎 sleep ≤1s；每个用例独立引擎名；用例间 reset 超窗状态与池。
"""

import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / 'scripts'))

import infoseek_pipeline as P

# 预热：jieba 词典首次构建 ~0.5s（一次性进程内成本），不应计入 R4「共享预算 ≤0.9s」
# 这类稳态时序断言。2026-09-14：jieba 安装后 R4 因该初始化超窗，故在此显式预热。
try:
    P._filter_relevant([{'url': 'https://warmup', 'title': '预热文本', 'snippet': ''}],
                       '预热主题 词元')
except Exception:
    pass

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


def _mk(sleep_s: float, tag: str, n: int = 2):
    """构造假引擎：sleep 后返回 n 条带 tag 的结果。"""
    def fn(q, mr):
        time.sleep(sleep_s)
        return [{'url': f'https://{tag}/{i}', 'title': f'{tag} {q}', 'snippet': 's'}
                for i in range(n)]
    return fn


def _mk_calls(sleep_s: float, tag: str, calls: dict, n: int = 2):
    """带调用计数器的假引擎（用于验证是否被拉起）。"""
    def fn(q, mr):
        calls['n'] = calls.get('n', 0) + 1
        time.sleep(sleep_s)
        return [{'url': f'https://{tag}/{i}', 'title': f'{tag} {q}', 'snippet': 's'}
                for i in range(n)]
    return fn


def _prep(window_ms='500'):
    os.environ['INFOSEEK_SEARCH_WINDOW_MS'] = window_ms
    os.environ['INFOSEEK_SEARCH_EARLY_FACTOR'] = '1.5'
    os.environ['INFOSEEK_SEARCH_SHARED_BUDGET'] = '1'
    P._reset_overrun_state()
    P._reset_pool()


def _clean():
    for k in ('INFOSEEK_SEARCH_WINDOW_MS', 'INFOSEEK_SEARCH_EARLY_FACTOR',
              'INFOSEEK_SEARCH_SHARED_BUDGET', 'INFOSEEK_SEARCH_TOTAL_BUDGET_MS',
              'INFOSEEK_SEARCH_OVERRUN_LIMIT', 'INFOSEEK_SEARCH_OVERRUN_MUTE_S',
              'INFOSEEK_SEARCH_ENGINE', 'INFOSEEK_SEARCH_PARALLEL',
              'INFOSEEK_RECALL_EXPAND', 'INFOSEEK_SEARCH_RESERVED',
              'INFOSEEK_RESERVE_QUOTA'):
        os.environ.pop(k, None)
    P._reset_overrun_state()
    P._reset_pool()


# ---------------------------------------------------------------------------
# R1 提前收敛 / R1b 关闭
# ---------------------------------------------------------------------------

def test_r1_early_converge() -> None:
    _prep('2000')
    # 快引擎 A/B 各 10 条 → 去重 20 ≥ 10×1.5=15，应提前返回；C 1.5s 慢引擎被取消
    eng = [('r1A', _mk(0.05, 'r1A', n=10)), ('r1B', _mk(0.05, 'r1B', n=10)),
           ('r1C', _mk(1.5, 'r1C', n=10))]
    t0 = time.time()
    r = P._parallel_merge(eng, 'r1q', 10)
    el = time.time() - t0
    check('R1 提前返回（<0.6s，不等 1.5s 慢引擎）', el < 0.6)
    check('R1 结果含 A/B（≥10 条截断）', len(r) == 10)
    check('R1 慢引擎 C 被丢弃', not any(x['title'] == 'r1C' for x in r))

    # R1b EARLY_FACTOR=0 → 关闭提前收敛，等全部
    os.environ['INFOSEEK_SEARCH_EARLY_FACTOR'] = '0'
    P._reset_overrun_state()
    P._reset_pool()
    t0 = time.time()
    r2 = P._parallel_merge(eng, 'r1q', 10)
    el2 = time.time() - t0
    check('R1b EARLY_FACTOR=0 等全部（≥1.4s）', el2 >= 1.4)
    check('R1b 结果含 C（30 条截断 10）', any('r1C' in x['title'] for x in r2))


# ---------------------------------------------------------------------------
# R2 保留池兜底纳入预算（无 sleep(0.8) 串行）
# ---------------------------------------------------------------------------

def test_r2_reserve_in_budget() -> None:
    _prep('500')  # 0.5s 预算
    # 主引擎 2 条（< min_expected=3）→ 触发保留兜底
    main = [('r2main', _mk(0.05, 'r2main', n=2))]
    reserve = [('r2res', _mk(0.05, 'r2res', n=2))]
    t0 = time.time()
    r = P._parallel_merge_with_reserve(main, 'r2q', 10, reserve)
    el = time.time() - t0
    check('R2 兜底补充生效（4 条）', len(r) == 4)
    check('R2 无 0.8s 串行（<0.4s）', el < 0.4)
    check('R2 主+保留结果齐全', all(t.split()[0] in {'r2main', 'r2res'} for t in [x['title'] for x in r]) and len({x['title'].split()[0] for x in r}) == 2)


# ---------------------------------------------------------------------------
# R3 预算耗尽跳过兜底
# ---------------------------------------------------------------------------

def test_r3_budget_exhausted() -> None:
    _prep('2000')  # 本层窗口 2s
    P._reset_overrun_state()
    # 主引擎慢（0.3s）超 tight deadline（+0.05s）→ 结果空、预算耗尽 → 不兜底
    main = [('r3a', _mk(0.3, 'r3a')), ('r3b', _mk(0.3, 'r3b'))]
    reserve = [('r3res', _mk(0.02, 'r3res'))]
    t0 = time.time()
    r = P._parallel_merge_with_reserve(main, 'r3q', 10, reserve,
                                       deadline=time.monotonic() + 0.05)
    el = time.time() - t0
    check('R3 预算耗尽跳过兜底（结果空）', len(r) == 0)
    check('R3 快速返回（<0.35s）', el < 0.35)


# ---------------------------------------------------------------------------
# R4 层间共享总预算（search_web 端到端）
# ---------------------------------------------------------------------------

def _patch_engines(ai_fn, def_fn):
    _orig = {}
    for attr in ('_ai_engines', '_has_ai_key', '_free_engines',
                 '_default_layer', '_quota_engines_with_key'):
        _orig[attr] = getattr(P, attr)
    P._ai_engines = lambda: [('ai0', ai_fn)]
    P._has_ai_key = lambda: True
    P._free_engines = lambda: []
    P._default_layer = lambda query=None: [('def0', def_fn)]
    P._quota_engines_with_key = lambda: []
    return _orig


def test_r4_shared_budget() -> None:
    _prep('800')
    os.environ['INFOSEEK_SEARCH_ENGINE'] = 'ai'
    os.environ['INFOSEEK_SEARCH_TOTAL_BUDGET_MS'] = '800'
    os.environ['INFOSEEK_RECALL_EXPAND'] = '0'
    # AI 引擎 0.5s 返回空 → 回退默认层（剩余预算 0.3s > 0.8 阈值 → 跳过限速）
    ai_fn = _mk_calls(0.5, 'ai0', {}, n=0)
    def_fn = _mk(0.05, 'def0')
    _orig = _patch_engines(ai_fn, def_fn)
    try:
        t0 = time.time()
        r = P.search_web('r4q', 10)
        el = time.time() - t0
    finally:
        for attr, v in _orig.items():
            setattr(P, attr, v)
    check('R4 AI 层空回退默认层成功（2 条）', len(r) == 2)
    check('R4 共享预算生效（总耗时 ≤0.9s）', el < 0.9)
    check('R4 结果来自默认层', any('def0' in x['title'] for x in r))


def test_r4b_shared_budget_off() -> None:
    _prep('800')
    os.environ['INFOSEEK_SEARCH_ENGINE'] = 'ai'
    os.environ['INFOSEEK_SEARCH_SHARED_BUDGET'] = '0'
    os.environ['INFOSEEK_RECALL_EXPAND'] = '0'
    ai_fn = _mk(0.5, 'ai0', n=0)
    def_fn = _mk(0.05, 'def0')
    _orig = _patch_engines(ai_fn, def_fn)
    try:
        check('R4b SHARED_BUDGET=0 → deadline=None',
              P._search_deadline() is None)
        t0 = time.time()
        r = P.search_web('r4bq', 10)
        el = time.time() - t0
    finally:
        for attr, v in _orig.items():
            setattr(P, attr, v)
    check('R4b 原语义各层各耗窗口（≥1.7s：0.8+0.5+0.8）', el >= 1.7)
    check('R4b 结果 2 条', len(r) == 2)


# ---------------------------------------------------------------------------
# R5 超窗计数降级（连续超窗 → mute）
# ---------------------------------------------------------------------------

def test_r5_overrun_mute() -> None:
    _prep('300')
    os.environ['INFOSEEK_SEARCH_OVERRUN_LIMIT'] = '2'
    os.environ['INFOSEEK_SEARCH_OVERRUN_MUTE_S'] = '60'
    calls = {}
    slow = _mk_calls(0.6, 'slowR5', calls)
    fast = _mk(0.03, 'fastR5')
    eng = [('slowR5', slow), ('fastR5', fast)]

    # 第 1 次：slowR5 超窗（count=1，未 mute）
    r1 = P._parallel_merge(eng, 'r5q', 10)
    check('R5 第1次：结果 2 条（fast）', len(r1) == 2 and not any(
        x['title'].startswith('slowR5') for x in r1))

    # 第 2 次：超窗 count=2 → mute slowR5
    r2 = P._parallel_merge(eng, 'r5q', 10)
    check('R5 第2次：触发 mute（引擎被静默）', P._is_muted('slowR5'))
    check('R5 第2次：结果 2 条', len(r2) == 2)

    # 第 3 次：slowR5 被 _filter_muted 剔除，不再拉起
    n_before = calls.get('n', 0)
    r3 = P._parallel_merge(eng, 'r5q', 10)
    check('R5 第3次：slowR5 不再被调用', calls.get('n', 0) == n_before)
    check('R5 第3次：fast 结果完整（2 条）', len(r3) == 2)
    check('R5 共调用 slowR5 2 次', calls.get('n', 0) == 2)


# ---------------------------------------------------------------------------
# R6 mute 冷却复活
# ---------------------------------------------------------------------------

def test_r6_revive() -> None:
    _prep()
    P._muted_until['reviveX'] = time.monotonic() + 5.0
    P._muted_until['reviveY'] = time.monotonic() - 1.0
    check('R6 静默期引擎被剔除', P._is_muted('reviveX')
          and not any(n == 'reviveX' for n, _ in P._filter_muted(
              [('reviveX', lambda q, m: []), ('ok', lambda q, m: [])])))
    check('R6 冷却到期复活', not P._is_muted('reviveY')
          and any(n == 'reviveY' for n, _ in P._filter_muted(
              [('reviveY', lambda q, m: [])])))


# ---------------------------------------------------------------------------
# R7 参数读取与回退
# ---------------------------------------------------------------------------

def test_r7_params() -> None:
    _prep('800')
    # EARLY_FACTOR
    os.environ['INFOSEEK_SEARCH_EARLY_FACTOR'] = '2.0'
    a = P._early_factor()
    os.environ['INFOSEEK_SEARCH_EARLY_FACTOR'] = 'x'
    b = P._early_factor()
    os.environ['INFOSEEK_SEARCH_EARLY_FACTOR'] = '0'
    c = P._early_factor()
    os.environ.pop('INFOSEEK_SEARCH_EARLY_FACTOR', None)
    d = P._early_factor()
    check('R7 EARLY_FACTOR env 生效', a == 2.0)
    check('R7 EARLY_FACTOR 非法兜底 1.5', b == 1.5)
    check('R7 EARLY_FACTOR=0 关闭', c == 0.0)
    check('R7 EARLY_FACTOR 默认 1.5', d == 1.5)

    # SHARED_BUDGET
    os.environ['INFOSEEK_SEARCH_SHARED_BUDGET'] = '1'
    e = P._shared_budget()
    os.environ['INFOSEEK_SEARCH_SHARED_BUDGET'] = '0'
    f = P._shared_budget()
    os.environ.pop('INFOSEEK_SEARCH_SHARED_BUDGET', None)
    g = P._shared_budget()
    check('R7 SHARED_BUDGET=1 开', e is True)
    check('R7 SHARED_BUDGET=0 关', f is False)
    check('R7 SHARED_BUDGET 默认开', g is True)

    # TOTAL_BUDGET_MS
    os.environ['INFOSEEK_SEARCH_TOTAL_BUDGET_MS'] = '1200'
    h = P._total_budget_s()
    os.environ.pop('INFOSEEK_SEARCH_TOTAL_BUDGET_MS', None)
    i = P._total_budget_s()
    check('R7 TOTAL_BUDGET_MS env 生效（1.2s）', h == 1.2)
    check('R7 TOTAL_BUDGET_MS 默认 = WINDOW（0.8s）', i == 0.8)

    # OVERRUN_*
    os.environ['INFOSEEK_SEARCH_OVERRUN_LIMIT'] = '3'
    j = P._overrun_limit()
    os.environ['INFOSEEK_SEARCH_OVERRUN_LIMIT'] = 'x'
    k = P._overrun_limit()
    os.environ['INFOSEEK_SEARCH_OVERRUN_LIMIT'] = '0'
    l = P._overrun_limit()
    os.environ.pop('INFOSEEK_SEARCH_OVERRUN_LIMIT', None)
    m = P._overrun_limit()
    check('R7 OVERRUN_LIMIT env 生效', j == 3)
    check('R7 OVERRUN_LIMIT 非法兜底 2', k == 2)
    check('R7 OVERRUN_LIMIT=0 关闭降级', l == 0)
    check('R7 OVERRUN_LIMIT 默认 2', m == 2)

    os.environ['INFOSEEK_SEARCH_OVERRUN_MUTE_S'] = '10'
    n = P._overrun_mute_s()
    os.environ['INFOSEEK_SEARCH_OVERRUN_MUTE_S'] = 'x'
    o = P._overrun_mute_s()
    os.environ.pop('INFOSEEK_SEARCH_OVERRUN_MUTE_S', None)
    p = P._overrun_mute_s()
    check('R7 OVERRUN_MUTE_S env 生效', n == 10.0)
    check('R7 OVERRUN_MUTE_S 非法兜底 60', o == 60.0)
    check('R7 OVERRUN_MUTE_S 默认 60', p == 60.0)

    # _search_deadline：共享开 → ≈now+total；关 → None
    os.environ['INFOSEEK_SEARCH_TOTAL_BUDGET_MS'] = '600'
    os.environ['INFOSEEK_SEARCH_SHARED_BUDGET'] = '1'
    dl = P._search_deadline()
    check('R7 deadline ≈ now+0.6s', dl is not None and 0.4 < dl - time.monotonic() <= 0.7)
    os.environ['INFOSEEK_SEARCH_SHARED_BUDGET'] = '0'
    check('R7 SHARED_BUDGET=0 → deadline None', P._search_deadline() is None)


# ---------------------------------------------------------------------------
# R8 deadline 直接传递
# ---------------------------------------------------------------------------

def test_r8_deadline_passthrough() -> None:
    _prep('2000')  # 本层窗口 2s，但外部 deadline 更紧
    P._reset_overrun_state()
    eng = [('r8fast', _mk(0.03, 'r8fast')), ('r8slow', _mk(0.5, 'r8slow'))]
    t0 = time.time()
    r = P._parallel_merge(eng, 'r8q', 10, deadline=time.monotonic() + 0.2)
    el = time.time() - t0
    check('R8 deadline 生效（<0.35s）', el < 0.35)
    check('R8 快引擎结果完整（2 条）', len(r) == 2)
    check('R8 慢引擎被截断', not any(x['title'].startswith('r8slow') for x in r))
    check('R8 超窗已计数', P._overrun_count.get('r8slow', 0) == 1)


# ---------------------------------------------------------------------------
def main() -> int:
    print('=== 搜索层 G5 P1/P2（预算+收敛+降级）测试 ===')
    for fn in (test_r1_early_converge, test_r2_reserve_in_budget,
               test_r3_budget_exhausted, test_r4_shared_budget,
               test_r4b_shared_budget_off, test_r5_overrun_mute,
               test_r6_revive, test_r7_params, test_r8_deadline_passthrough):
        print(f'\n{fn.__name__}')
        try:
            fn()
        except Exception as e:
            check(f'{fn.__name__} 异常', False)
            print(f'         ERR: {type(e).__name__}: {e}')
    _clean()
    print(f'\nPASS={_PASS} FAIL={_FAIL}')
    return 1 if _FAIL else 0


if __name__ == '__main__':
    sys.exit(main())