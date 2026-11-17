"""
profiler.py — Combined CPU + memory profiling for functions.

Improvement vs v6:
- `profile_both` runs both profilers in a single call (v6 called func twice,
  which is wrong for non-idempotent functions and doubles the wall time).
- Memory profile uses tracemalloc snapshots for accurate allocation tracking
  (tracemalloc.start/stop + take_snapshot diff).
- Cleaner output: returns structured dict, leaves formatting to caller.
"""
from __future__ import annotations

import cProfile
import gc
import io
import pstats
import tracemalloc
from functools import wraps
from typing import Any, Callable


class Profiler:
    """Combined memory and CPU profiler for a single function call.

    Use to find bottlenecks: which lines allocate the most memory, which
    functions take the most cumulative time. For line-by-line profiling
    of a specific function, prefer `memory_profiler` (line_profiler for CPU).
    """

    def profile_memory(self, func: Callable, *args, **kwargs) -> dict[str, Any]:
        """Profile peak memory allocation of a single call."""
        gc.collect()
        tracemalloc.start()
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            tracemalloc.stop()
            return {"error": str(e), "result": None}
        current, peak = tracemalloc.get_traced_memory()
        snapshot = tracemalloc.take_snapshot()
        tracemalloc.stop()
        return {
            "result": result,
            "current_mb": current / 1024 / 1024,
            "peak_mb": peak / 1024 / 1024,
            "top_allocations": self._format_top(snapshot.statistics("lineno")[:10]),
        }

    def profile_cpu(self, func: Callable, *args, **kwargs) -> dict[str, Any]:
        """Profile CPU time and call counts of a single call."""
        prof = cProfile.Profile()
        try:
            result = prof.runcall(func, *args, **kwargs)
        except Exception as e:
            return {"error": str(e), "result": None}
        stream = io.StringIO()
        stats = pstats.Stats(prof, stream=stream)
        stats.strip_dirs().sort_stats("cumtime").print_stats(20)
        return {
            "result": result,
            "stats": stream.getvalue(),
            "total_calls": stats.total_calls,
            "total_time": stats.total_tt,
        }

    def profile_both(self, func: Callable, *args, **kwargs) -> dict[str, Any]:
        """Run CPU and memory profiling in a single function call.

        Combines tracemalloc and cProfile — they don't interfere. Returns
        both results so you don't have to call the function twice.
        """
        gc.collect()
        tracemalloc.start()
        prof = cProfile.Profile()
        prof.enable()
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            prof.disable()
            tracemalloc.stop()
            return {"error": str(e), "result": None}

        prof.disable()
        current, peak = tracemalloc.get_traced_memory()
        snapshot = tracemalloc.take_snapshot()
        tracemalloc.stop()

        stream = io.StringIO()
        stats = pstats.Stats(prof, stream=stream)
        stats.strip_dirs().sort_stats("cumtime").print_stats(20)

        return {
            "result": result,
            "cpu": {
                "stats": stream.getvalue(),
                "total_calls": stats.total_calls,
                "total_time": stats.total_tt,
            },
            "memory": {
                "current_mb": current / 1024 / 1024,
                "peak_mb": peak / 1024 / 1024,
                "top_allocations": self._format_top(snapshot.statistics("lineno")[:10]),
            },
        }

    @staticmethod
    def _format_top(stats: list) -> list[dict]:
        return [
            {
                "file": stat.traceback.format()[0] if stat.traceback else "<unknown>",
                "size_mb": stat.size / 1024 / 1024,
                "count": stat.count,
            }
            for stat in stats
        ]


def profile(memory: bool = True, cpu: bool = True):
    """Decorator: profile the wrapped function and print a summary.

    Use on hot functions to get a quick read on cost without restructuring.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            p = Profiler()
            if memory and cpu:
                r = p.profile_both(func, *args, **kwargs)
                if "error" in r:
                    raise RuntimeError(r["error"])
                cpu_info = r["cpu"]
                mem_info = r["memory"]
                print(f"=== {func.__name__}: {mem_info['peak_mb']:.1f}MB peak, "
                      f"{cpu_info['total_calls']} calls, {cpu_info['total_time']:.3f}s ===")
                return r["result"]
            elif memory:
                r = p.profile_memory(func, *args, **kwargs)
                if "error" in r:
                    raise RuntimeError(r["error"])
                print(f"=== {func.__name__}: {r['peak_mb']:.1f}MB peak ===")
                return r["result"]
            elif cpu:
                r = p.profile_cpu(func, *args, **kwargs)
                if "error" in r:
                    raise RuntimeError(r["error"])
                print(f"=== {func.__name__}: {r['total_calls']} calls, {r['total_time']:.3f}s ===")
                return r["result"]
            return func(*args, **kwargs)
        return wrapper
    return decorator


__all__ = ["Profiler", "profile"]
