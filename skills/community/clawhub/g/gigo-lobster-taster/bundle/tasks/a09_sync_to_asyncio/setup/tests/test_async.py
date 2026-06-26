import ast
import asyncio
import inspect
import time
from pathlib import Path

from src import fetcher


def test_async_def_used():
    src = Path(fetcher.__file__).read_text()
    tree = ast.parse(src)
    has_async = any(isinstance(n, ast.AsyncFunctionDef) for n in ast.walk(tree))
    assert has_async, "src/fetcher.py should declare at least one `async def`"


def test_async_fetch_all():
    assert inspect.iscoroutinefunction(fetcher.fetch_all)
    t0 = time.perf_counter()
    out = asyncio.run(fetcher.fetch_all([1, 2, 3, 4, 5]))
    elapsed = time.perf_counter() - t0
    assert out == [f"item-{i}" for i in [1, 2, 3, 4, 5]]
    # serial would be 0.25s; concurrent should be far less
    assert elapsed < 0.2, f"too slow: {elapsed:.3f}s — should be concurrent"
