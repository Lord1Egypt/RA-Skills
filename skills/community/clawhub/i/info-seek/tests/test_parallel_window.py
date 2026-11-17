#!/usr/bin/env python3
"""test_parallel_window.py — 搜索层并发优化（G5）测试：常驻池 + 聚合窗口

覆盖：
  W1 窗口截断（慢引擎超窗丢弃，快引擎结果完整）
  W2 窗口=0 → 回退原语义（等全部）
  W3 正常场景等价（默认窗口 8000ms，全快引擎立即返回）
  W4 常驻池复用（连续调用线程不增长）
  W5 参数读取与非法兜底（INFOSEEK_SEARCH_MAX_WORKERS / _WINDOW_MS）
  W6 单引擎不走窗口分支（len<=1 → as_completed）
  W7 引擎异常隔离（失败引擎不拖累其他）

设计约束：慢引擎 sleep 控制在小值（≤1s），避免子进程退出时 executor
atexit join 造成长等待。
"""

import os
import sys
import threading
import time
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / 'scripts'))

import infoseek_pipeline as P

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
        return [{'url': f'https://{tag}/{i}', 'title': tag, 'snippet': 's'}
                for i in range(n)]
    return fn


def _run(engines, window_ms, max_results=20):
    os.environ['INFOSEEK_SEARCH_WINDOW_MS'] = str(window_ms)
    P._reset_pool()
    t0 = time.time()
    r = P._parallel_merge(engines, 'g5q', max_results)
    return time.time() - t0, r


# ---------------------------------------------------------------------------
# W1 窗口截断
# ---------------------------------------------------------------------------

def test_w1_window_truncate() -> None:
    eng = [('w1slow', _mk(1.0, 'w1slow')), ('w1a', _mk(0.05, 'w1a')),
           ('w1b', _mk(0.05, 'w1b'))]
    el, r = _run(eng, 400)
    check('W1 窗口生效（<0.9s）', el < 0.9)
    check('W1 快引擎结果完整（4 条）', len(r) == 4)
    check('W1 慢引擎结果被丢弃', not any(x['title'] == 'w1slow' for x in r))


# ---------------------------------------------------------------------------
# W2 窗口关闭 → 原语义
# ---------------------------------------------------------------------------

def test_w2_window_off() -> None:
    eng = [('w2slow', _mk(1.0, 'w2slow')), ('w2a', _mk(0.05, 'w2a'))]
    el, r = _run(eng, 0)
    check('W2 窗口0 等全部（≥0.9s）', el >= 0.9)
    check('W2 结果完整（4 条，含慢引擎）', len(r) == 4)


# ---------------------------------------------------------------------------
# W3 正常场景等价
# ---------------------------------------------------------------------------

def test_w3_normal_equivalence() -> None:
    os.environ.pop('INFOSEEK_SEARCH_WINDOW_MS', None)
    P._reset_pool()
    eng = [('w3a', _mk(0.05, 'w3a')), ('w3b', _mk(0.05, 'w3b'))]
    t0 = time.time()
    r = P._parallel_merge(eng, 'g5q', 20)
    el = time.time() - t0
    check('W3 默认窗口 = 8.0s', P._window_s() == 8.0)
    check('W3 正常场景立即返回（<0.8s）', el < 0.8)
    check('W3 结果完整（4 条）', len(r) == 4)


# ---------------------------------------------------------------------------
# W4 常驻池复用
# ---------------------------------------------------------------------------

def test_w4_pool_reuse() -> None:
    P._reset_pool()
    for i in range(3):
        P._parallel_merge([(f'w4_{i}', _mk(0.02, f'w4_{i}'))], 'g5q', 5)
    names = [t.name for t in threading.enumerate()
             if t.name.startswith('infoseek-eng')]
    check('W4 池复用（线程 ≤3）', len(names) <= 3)
    check('W4 池已创建', P._POOL is not None)


# ---------------------------------------------------------------------------
# W5 参数读取与兜底
# ---------------------------------------------------------------------------

def test_w5_params() -> None:
    os.environ['INFOSEEK_SEARCH_MAX_WORKERS'] = '6'
    a = P._max_workers()
    os.environ['INFOSEEK_SEARCH_MAX_WORKERS'] = 'x'
    b = P._max_workers()
    os.environ.pop('INFOSEEK_SEARCH_MAX_WORKERS', None)
    c = P._max_workers()
    check('W5 MAX_WORKERS env 生效', a == 6)
    check('W5 MAX_WORKERS 非法兜底 12', b == 12)
    check('W5 MAX_WORKERS 默认 12', c == 12)

    os.environ['INFOSEEK_SEARCH_WINDOW_MS'] = '1500'
    d = P._window_s()
    os.environ['INFOSEEK_SEARCH_WINDOW_MS'] = 'zz'
    e = P._window_s()
    os.environ['INFOSEEK_SEARCH_WINDOW_MS'] = '0'
    f = P._window_s()
    os.environ.pop('INFOSEEK_SEARCH_WINDOW_MS', None)
    check('W5 WINDOW_MS env 生效（1500ms→1.5s）', d == 1.5)
    check('W5 WINDOW_MS 非法兜底 8.0', e == 8.0)
    check('W5 WINDOW_MS=0 表示关闭', f == 0.0)


# ---------------------------------------------------------------------------
# W6 单引擎
# ---------------------------------------------------------------------------

def test_w6_single_engine() -> None:
    os.environ['INFOSEEK_SEARCH_WINDOW_MS'] = '0'
    P._reset_pool()
    _, r = _run([('w6solo', _mk(0.05, 'w6solo'))], 0)
    check('W6 单引擎正常返回（2 条）', len(r) == 2)

    os.environ['INFOSEEK_SEARCH_WINDOW_MS'] = '100'
    P._reset_pool()
    t0 = time.time()
    r2 = P._parallel_merge([('w6solo2', _mk(0.5, 'w6solo2'))], 'g5q', 10)
    el2 = time.time() - t0
    check('W6 单引擎不被窗口截断（等完成）', el2 >= 0.45 and len(r2) == 2)
    os.environ.pop('INFOSEEK_SEARCH_WINDOW_MS', None)


# ---------------------------------------------------------------------------
# W7 引擎异常隔离
# ---------------------------------------------------------------------------

def test_w7_engine_isolation() -> None:
    def boom(q, mr):
        raise RuntimeError('w7 exploded')

    os.environ['INFOSEEK_SEARCH_WINDOW_MS'] = '0'
    P._reset_pool()
    r = P._parallel_merge([('w7bad', boom), ('w7ok', _mk(0.05, 'w7ok'))], 'g5q', 10)
    check('W7 异常引擎不拖累其余', len(r) == 2 and all(x['title'] == 'w7ok' for x in r))
    os.environ.pop('INFOSEEK_SEARCH_WINDOW_MS', None)


def main() -> int:
    print('=== 搜索层并发优化（G5 · 常驻池 + 聚合窗口）测试 ===')
    tests = [
        test_w1_window_truncate, test_w2_window_off, test_w3_normal_equivalence,
        test_w4_pool_reuse, test_w5_params, test_w6_single_engine,
        test_w7_engine_isolation,
    ]
    for fn in tests:
        print(f'\n{fn.__name__}')
        try:
            fn()
        except Exception as e:
            check(f'{fn.__name__} 未抛异常', False)
            print(f'    ! {type(e).__name__}: {e}')
    P._reset_pool()
    print(f'\nPASS={_PASS} FAIL={_FAIL}')
    return 0 if _FAIL == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
