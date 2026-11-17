# Debugging Reference

Patterns for debugging Python code: post-mortem analysis, traceback introspection, exception summarization, profiling, and the `pdb` workflow. **Load this reference when the user wants to investigate a crash, find a bottleneck, or understand an exception.**

## Quick Decision Guide

| Situation | Use |
|-----------|-----|
| A script just crashed and you want to inspect the failing frame | `debug_utils.post_mortem()` |
| You caught an exception and want a structured summary | `debug_utils.summarize_exception(exc)` |
| You want a readable multi-line traceback (not full stdlib dump) | `debug_utils.format_exception(exc)` |
| Function is slow — find the bottleneck | `profiler.Profiler().profile_both(func, *args)` |
| Function eats memory — find allocations | `profiler.Profiler().profile_memory(func, *args)` |
| Regex hangs on certain inputs | `regex_debugger.RegexDebugger(pattern).stress_test()` |
| Need to mock filesystem/env/modules to reproduce a bug | `function_isolator.FunctionIsolator` |

## Post-Mortem Debugging

When a script raises an uncaught exception, `pdb.post_mortem(tb)` drops you into the pdb prompt at the failing frame, with all locals intact. This is the most powerful debugging tool — you can inspect any variable, run arbitrary expressions, walk up/down the call stack.

```python
import sys
SCRIPTS = '/home/z/my-project/skills/ipython-analyst/scripts'
if SCRIPTS not in sys.path: sys.path.insert(0, SCRIPTS)
from debug_utils import post_mortem, extract_traceback, summarize_exception, format_exception, breakpoint_helper
from function_isolator import FunctionIsolator
from profiler import Profiler, profile

try:
    result = risky_business()
except Exception as exc:
    # Drop into pdb at the failing frame
    post_mortem()  # uses sys.last_traceback by default
    # Or: post_mortem(exc.__traceback__)
```

Inside pdb, useful commands:
- `p expr` — print expression
- `pp expr` — pretty-print
- `l` — list source around current line
- `w` — full stack trace
- `u`/`d` — up/down the stack
- `a` — print all args of current function
- `!stmt` — execute a statement (e.g. `!x = 5` to mutate state)
- `q` — quit

For a non-interactive diagnostic (when you can't enter pdb because the model isn't interactive), use `summarize_exception`:

```python

try:
    risky_business()
except Exception as exc:
    summary = summarize_exception(exc)
    print(summary["type"], summary["message"])
    for frame in summary["frames"][:5]:
        print(f"  {frame['file']}:{frame['lineno']} in {frame['function']}")
        print(f"    {frame['source_line']}")
        for k, v in frame["locals"].items():
            print(f"    {k} = {v}")
```

## Traceback Introspection

`extract_traceback(exc)` returns a list of frame dicts. Each has `file`, `lineno`, `function`, `source_line`, and `locals`. Use to grep for patterns across many exceptions, or to filter out stdlib frames.

```python
frames = extract_traceback(exc)
# Show only user-code frames (not site-packages)
user_frames = [f for f in frames if "/home/z/my-project" in f["file"]]
for f in user_frames:
    print(f"{f['file']}:{f['lineno']} — {f['source_line']}")
```

## Exception Chaining

Python 3.5+ tracks two chains: `__cause__` (explicit `raise X from Y`) and `__context__` (implicit re-raise during except block). `summarize_exception` walks both and returns a `cause_chain` list. Useful when an exception is a wrapper around the real problem — the root cause is often 2-3 links down the chain.

```python
try:
    json.loads(bad_input)
except Exception as exc:
    summary = summarize_exception(exc)
    # cause_chain[0] is the outer exception, [-1] is the root cause
    print("Root cause:", summary["cause_chain"][-1])
```

## Python 3.11+ Exception Groups

If `risky_business()` raises an `ExceptionGroup` (from `TaskGroup` or `asyncio`), iterate `exc.exceptions` to handle each. Python 3.11 added fine-grained error locations in tracebacks — use `traceback.format_exception` to see them.

```python
try:
    async with asyncio.TaskGroup() as tg:
        tg.create_task(risky_a())
        tg.create_task(risky_b())
except ExceptionGroup as eg:
    for sub_exc in eg.exceptions:
        print(format_exception(sub_exc))
```

## Profiling

### When to profile
- A function takes >1s and you don't know why
- A function works on small inputs but hangs on larger ones
- Memory usage grows unexpectedly over time

### CPU + memory in one pass
```python

def my_heavy_function(df):
    return df.groupby('x').apply(lambda g: g['y'].rolling(100).mean().sum())

result = Profiler().profile_both(my_heavy_function, df)
print(f"Peak memory: {result['memory']['peak_mb']:.1f} MB")
print(f"Total calls: {result['cpu']['total_calls']}")
print(f"Total time:  {result['cpu']['total_time']:.3f}s")
print(result["cpu"]["stats"][:3000])  # top 20 by cumtime
for alloc in result["memory"]["top_allocations"][:5]:
    print(f"  {alloc['size_mb']:.2f}MB at {alloc['file']} ({alloc['count']} allocs)")
```

### Common patterns the profile reveals
- **One function dominates `tottime`** → it's CPU-bound; optimize the algorithm or use numpy vectorization.
- **Many small calls dominate `ncalls`** → likely a hot loop; consider batching or memoization.
- **Memory peaks early then plateaus** → bulk load; pre-allocate if you can.
- **Memory grows monotonically** → leak; check for accumulated caches or undereleased references.
- **`cumtime` of a function is high but `tottime` is low** → the cost is in a callee; dig deeper.

### Decorator for hot functions
```python
@profile(memory=True, cpu=True)
def my_hot_function(x):
    ...
```
On each call, prints `=== my_hot_function: 12.3MB peak, 1234 calls, 0.234s ===`.

### Line-by-line profiling
For pinpointing a single function's hot lines, `memory_profiler` and `line_profiler` give per-line cost. They're not in the standard library; install with `pip install memory_profiler line_profiler`. Then:

```python
# CPU line-by-line
%load_ext line_profiler
%lprun -f my_func my_func(args)

# Memory line-by-line
%load_ext memory_profiler
%mprun -f my_func my_func(args)
```

## Mocking Dependencies

When a function's bug only reproduces with specific env vars, files, or mocked modules, use `FunctionIsolator`:

```python

iso = FunctionIsolator()
iso.mock_env({"API_URL": "https://test.example.com", "DEBUG": "1"})
iso.mock_file("/etc/config.json", '{"timeout": 30}')
iso.mock_module("requests.get", return_value=MagicMock(status_code=200, json=lambda: {"ok": True}))

result = iso.run(my_function_that_uses_these)
print(result["result"], result["error"])
```

All mocks are reverted on exit. Useful for reproducing "works on my machine" bugs.

## Common Debugging Anti-Patterns

- **Bare `except:`** — swallows everything including `KeyboardInterrupt` and `SystemExit`. Use `except Exception:` at minimum.
- **`print`-debugging in a hot loop** — I/O is slow and skews timing. Use `logging.debug` or collect into a list and print at the end.
- **Mutating state in `except`** — if the handler raises, you've corrupted the state you were trying to debug. Snapshot first.
- **Profiling with `time.time()`** — wall clock includes GC, scheduling, I/O. Use `time.perf_counter()` for benchmarking, `cProfile` for breakdown.
- **`breakpoint()` in production code** — fine for debug, but don't commit. Use `if os.environ.get("DEBUG"): breakpoint()` instead.

## Workflow: Investigating a Mysterious Crash

1. Reproduce the crash in the ipython tool with a small input.
2. Wrap in `try/except` and call `summarize_exception(exc)` to get the structured summary.
3. Read the `cause_chain` to find the root cause (not just the wrapper).
4. Inspect `frames` — focus on user-code frames, skip stdlib.
5. For each suspect frame, check `locals` — was the input what you expected?
6. If the bug is data-dependent, save the failing input to `/home/z/my-project/download/` so you can replay. **⚠️ Treat the failing input as potentially sensitive**: it may contain credentials, PII, tokens, or proprietary data extracted from the user's environment. Redact or synthesize a minimal repro before saving — prefer an in-memory repro over disk whenever possible. If you must persist the real input, ask the user for explicit approval and use a clearly-named file so it's easy to find and delete after debugging.
7. Once you understand the cause, write a minimal test that reproduces it before fixing. Run `test_generator.TestCaseGenerator().stress_test(parser, cases)` to verify the fix handles edge cases.

## Sensitive Data in Debugging Output

Several helpers in this skill capture runtime state that may contain secrets:

- `extract_traceback(exc)` — includes frame `locals` by default; pass `include_locals=False` if the exception occurred in a context where credentials or PII may be in scope.
- `format_exception(exc)` — same: pass `show_locals=False` for user-facing output or when sharing transcripts.
- `summarize_exception(exc)` — calls `extract_traceback` with `include_locals=True` by default. If you intend to share the summary (e.g., in a bug report), strip or redact the `locals` field from each frame first, or post-process with a simple key-name allowlist (`{k: v for k, v in frame['locals'].items() if not any(s in k.lower() for s in ('pass', 'token', 'secret', 'key', 'auth', 'cookie'))}`).

The `locals` snapshot is genuinely useful for diagnosis — that's why it's opt-out rather than opt-in for interactive use. The trade-off is that anything visible in a frame's locals when the exception fired will be visible in the output. Use the opt-out flags whenever the output may cross a trust boundary (saved to disk, shared in a chat, attached to a ticket).
