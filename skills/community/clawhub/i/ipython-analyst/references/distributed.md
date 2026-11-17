# Distributed Processing Reference

Parallel and chunked processing for large datasets. **Load this reference when the user has data too big to fit in memory, or a CPU-bound task that would benefit from parallelism.**

## When to Use What

| Situation | Use |
|-----------|-----|
| Large CSV, can't fit in memory | `process_large_csv(output_path=...)` streaming |
| CPU-bound task on small data | `parallel_map(func, items)` (multiprocessing) |
| I/O-bound task (HTTP, file reads) | `parallel_map(..., backend='threading')` |
| Lazy evaluation on huge data | `DaskProcessor` with `with` block |
| Pandas groupby on huge data | `DaskProcessor.parallel_apply` |
| Want a progress bar | pass `show_progress=True` to any of the above |

## Streaming Large CSV (No OOM)

```python
import sys
SCRIPTS = '/home/z/my-project/skills/ipython-analyst/scripts'
if SCRIPTS not in sys.path: sys.path.insert(0, SCRIPTS)
from distributed import DistributedProcessor, DaskProcessor, parallel_apply, process_large_csv

def process_chunk(chunk):
    # Compute per-chunk aggregation
    return chunk.groupby('product')['revenue'].sum().reset_index()

# Streams to disk — never accumulates in memory
result_path = '/home/z/my-project/download/per_product.csv'
process_large_csv(
    '/home/z/my-project/upload/huge_sales.csv',
    process_func=process_chunk,
    chunk_size=50_000,
    output_path=result_path,
    show_progress=True,
)

# Then load the (much smaller) aggregated result
import pandas as pd
final = pd.read_csv(result_path).groupby('product')['revenue'].sum().reset_index()
final.to_csv('/home/z/my-project/download/per_product_final.csv', index=False)
```

**Bug-fixed vs v6**: v6 pre-read the entire file once just to count rows for the progress bar — defeating the purpose of streaming. v7 estimates from file size, or counts chunks as they arrive.

## Parallel Map (CPU-bound)

```python

# Module-level function (must be picklable for multiprocessing)
def process_item(item):
    # CPU-heavy work
    return expensive_computation(item)

items = list(range(1000))
results = parallel_apply(process_item, items, n_workers=4, show_progress=True)
```

### Pickle requirement
Functions passed to multiprocessing must be picklable:
- ✅ Module-level `def`, lambdas at module scope
- ❌ Local closures, lambdas inside other functions
- ❌ Functions defined inside `__main__` block (in some setups)

If you must use a closure or lambda, use `backend='threading'` (no pickle, but GIL limits CPU speedup).

## Threading Backend (I/O-bound)

For network/disk-bound work, threads beat processes (no IPC overhead, GIL releases on I/O):

```python
dp = DistributedProcessor(n_workers=8, backend='threading')

import requests
def fetch(url):
    return requests.get(url).json()

urls = ['https://api.example.com/items/1', ...]
results = dp.parallel_map(fetch, urls, show_progress=True, desc='Fetching')
```

## Dask for Lazy Evaluation

Dask builds a task graph without executing it; `.compute()` triggers execution. Great for datasets that don't fit in memory but fit on disk.

```python

# Use as context manager — closes the cluster on exit (prevents zombies)
with DaskProcessor(n_workers=4) as dp:
    ddf = dp.read_csv('/home/z/my-project/upload/huge.csv')
    # Lazy operations — no execution yet
    filtered = ddf[ddf['amount'] > 100]
    grouped = filtered.groupby('category')['amount'].sum()
    # Trigger execution
    result = grouped.compute()
    print(result)
```

### Dask gotchas
- `ddf.apply(func, axis=1)` is slow — Dask can't vectorize across partitions. Prefer column-wise ops.
- `meta` parameter is required for `apply` — Dask needs to know the output schema to build the graph.
- `.compute()` materializes the whole result; for large outputs, write to disk: `ddf.to_csv('/output/*.csv')`.

## Parallel Groupby

For pandas DataFrames where the groupby itself is slow (many groups, expensive agg):

```python
dp = DistributedProcessor(n_workers=4)

def agg(group):
    # Per-group aggregation
    return pd.Series({
        'total': group['amount'].sum(),
        'count': len(group),
        'avg': group['amount'].mean(),
    })

result = dp.parallel_groupby(df, group_col='category', agg_func=agg, show_progress=True)
```

## When Parallelism Doesn't Help

- **Small data** (<1MB, <100ms serial) — overhead exceeds speedup. Just do it serially.
- **GIL-bound pure-Python loops** — multiprocessing helps, but threads don't. Consider numpy vectorization or Cython first.
- **Already-vectorized pandas/numpy** — these release the GIL internally, so threading helps; multiprocessing is wasteful.
- **I/O on a single disk** — parallel reads may saturate the disk and be slower than serial.

## Profiling Parallel Code

Always profile the serial version first. If `parallel_apply` is slower than serial, it's likely because:
1. The function is too small (overhead dominates) — batch items
2. Pickling is expensive (large args/returns) — pass indices, look up data in workers
3. The function releases the GIL anyway (use threading instead)

```python
# Compare serial vs parallel
import time
items = list(range(1000))

t0 = time.perf_counter()
serial = [process_item(i) for i in items]
t_serial = time.perf_counter() - t0

t0 = time.perf_counter()
parallel = parallel_apply(process_item, items, n_workers=4)
t_parallel = time.perf_counter() - t0

print(f"Serial:   {t_serial:.2f}s")
print(f"Parallel: {t_parallel:.2f}s  (speedup: {t_serial/t_parallel:.2f}x)")
```

## Common Pitfalls

### Zombie processes
v6 had this — Dask clients/cluster could leak. v7's `DaskProcessor` is a context manager that always closes:

```python
with DaskProcessor() as dp:
    ...
# cluster closed here, even on exception
```

If you must use it without `with`, call `dp.close()` explicitly in a `finally` block.

### Memory blow-up in `parallel_map`
Each worker gets a copy of the args (pickled). For large items, this multiplies memory:

```python
# BAD — each worker gets a copy of the 1GB array
results = parallel_apply(process, [huge_array] * 100, n_workers=8)

# GOOD — pass indices, look up in workers (or use shared memory)
def process_index(i):
    return process(huge_array[i])
results = parallel_apply(process_index, range(100), n_workers=8)
```

### Progress bar with multiprocessing
`tqdm` + `executor.map` works, but the bar may not update smoothly because workers can finish out of order. Use `total=` and `desc=` for clarity, and don't rely on exact progress — it's an estimate.
