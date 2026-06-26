#!/usr/bin/env python3
"""
python-perf-test.py — Python 性能优化模式验证脚本
验证 performance-mastery skill 中 Python 部分的各项优化建议

用法: python3 python-perf-test.py
"""
import sys
import time
import timeit
import cProfile
import pstats
import io
import tracemalloc
from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

passed = 0
failed = 0

def test(name, condition, detail=""):
    global passed, failed
    if condition:
        passed += 1
        print(f"  PASS  {name}" + (f"  ({detail})" if detail else ""))
    else:
        failed += 1
        print(f"  FAIL  {name}" + (f"  ({detail})" if detail else ""))

print("=" * 60)
print("Python Performance Optimization — Validation Tests")
print("=" * 60)

# --- Test 1: List comprehension vs loop ---
N = 1_000_000
data = list(range(N))
t1 = timeit.timeit(lambda: [x * 2 for x in data], number=5)
def loop_ver():
    r = []
    for x in data:
        r.append(x * 2)
    return r
t2 = timeit.timeit(loop_ver, number=5)
test("List comprehension faster than loop", t1 < t2, f"{t2/t1:.2f}x")

# --- Test 2: Generator memory (peak comparison) ---
# 测量列表推导式的峰值内存
tracemalloc.start()
_ = sum([x for x in range(N)])
_, list_peak = tracemalloc.get_traced_memory()
tracemalloc.stop()

# 测量生成器表达式的峰值内存
tracemalloc.start()
_ = sum(x for x in range(N))
_, gen_peak = tracemalloc.get_traced_memory()
tracemalloc.stop()

test("Generator uses less memory", gen_peak < list_peak,
     f"list peak={list_peak/1024:.0f}KB, gen peak={gen_peak/1024:.0f}KB, "
     f"saved {(list_peak-gen_peak)/1024:.0f}KB ({(1-gen_peak/list_peak)*100:.0f}%)")

# --- Test 3: set lookup vs list ---
sdata = list(range(100_000))
sset = set(sdata)
targets = list(range(0, 100_000, 7))
t_list = timeit.timeit(lambda: [x in sdata for x in targets], number=3)
t_set = timeit.timeit(lambda: [x in sset for x in targets], number=3)
test("set lookup faster than list", t_set < t_list, f"{t_list/t_set:.0f}x")

# --- Test 4: join vs += ---
pieces = [str(i) for i in range(10_000)]
t_join = timeit.timeit(lambda: ''.join(pieces), number=500)
def concat_plus():
    r = ''
    for p in pieces:
        r += p
    return r
t_plus = timeit.timeit(concat_plus, number=500)
test("join faster than +=", t_join < t_plus, f"{t_plus/t_join:.1f}x")

# --- Test 5: lru_cache ---
@lru_cache(maxsize=256)
def fib(n):
    if n < 2: return n
    return fib(n-1) + fib(n-2)
fib.cache_clear()
t_cached = timeit.timeit(lambda: fib(30), number=1)
test("lru_cache works", fib(30) == 832040, f"fib(30)={fib(30)}")

# --- Test 6: cProfile ---
profiler = cProfile.Profile()
profiler.enable()
sum(range(100_000))
profiler.disable()
s = io.StringIO()
pstats.Stats(profiler, stream=s).print_stats(3)
test("cProfile works", 'ncalls' in s.getvalue())

# --- Test 7: tracemalloc ---
tracemalloc.start()
_ = [bytearray(1024) for _ in range(100)]
snap = tracemalloc.take_snapshot()
stats = snap.statistics('lineno')
tracemalloc.stop()
test("tracemalloc detects allocations", len(stats) > 0, f"{len(stats)} alloc points")

# --- Test 8: timeit ---
result = timeit.timeit('sum(range(100))', number=10000)
test("timeit works", result > 0, f"{result:.4f}s for 10000 iters")

# --- Test 9: ThreadPoolExecutor ---
def io_sim(n):
    time.sleep(0.02)
    return n
items = list(range(20))
t_seq = timeit.timeit(lambda: [io_sim(n) for n in items], number=1)
def run_tp():
    with ThreadPoolExecutor(max_workers=10) as ex:
        list(ex.map(io_sim, items))
t_tp = timeit.timeit(run_tp, number=1)
test("ThreadPoolExecutor speeds up I/O", t_tp < t_seq, f"{t_seq/t_tp:.1f}x")

# --- Summary ---
print("\n" + "=" * 60)
total = passed + failed
print(f"Results: {passed}/{total} passed, {failed} failed")
if failed == 0:
    print("All tests passed!")
else:
    print(f"WARNING: {failed} test(s) failed")
    sys.exit(1)
