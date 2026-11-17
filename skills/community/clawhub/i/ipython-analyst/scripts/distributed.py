"""
distributed.py — Parallel/distributed processing for large datasets.

Bug fix vs v6:
- `process_large_file` no longer pre-reads the entire file just to count rows
  for the progress bar. That defeated the entire purpose of streaming. v7
  estimates total chunks from file size, or just counts chunks as they arrive
  if estimation isn't possible.
"""
from __future__ import annotations

import multiprocessing as mp
import os
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from functools import partial
from typing import Any, Callable, Iterable


class DistributedProcessor:
    """Parallel map / chunked file processing with optional progress bars.

    Defaults to multiprocessing for CPU-bound work, threading for I/O-bound
    (set backend='threading'). tqdm is used for progress if available.
    """

    def __init__(self, n_workers: int = -1, backend: str = "auto"):
        self.n_workers = mp.cpu_count() if n_workers == -1 else n_workers
        self.backend = backend if backend != "auto" else "multiprocessing"
        self._tqdm_available = self._check_tqdm()

    @staticmethod
    def _check_tqdm() -> bool:
        try:
            import tqdm  # noqa: F401
            return True
        except ImportError:
            return False

    def parallel_map(
        self,
        func: Callable,
        items: Iterable,
        show_progress: bool = False,
        desc: str = "Processing",
    ) -> list[Any]:
        """Apply `func` to each item in parallel. Returns list in input order."""
        items = list(items)
        n_workers = min(self.n_workers, len(items)) if items else 0

        if n_workers <= 1:
            # Serial fallback (still useful for debug or tiny inputs)
            if show_progress and self._tqdm_available:
                from tqdm import tqdm
                return [func(item) for item in tqdm(items, desc=desc)]
            return [func(item) for item in items]

        executor_cls = ThreadPoolExecutor if self.backend == "threading" else ProcessPoolExecutor
        with executor_cls(max_workers=n_workers) as executor:
            if show_progress and self._tqdm_available:
                from tqdm import tqdm
                return list(tqdm(executor.map(func, items), total=len(items), desc=desc))
            return list(executor.map(func, items))

    def process_large_file(
        self,
        file_path: str,
        process_chunk: Callable,
        chunk_size: int = 10000,
        output_path: str | None = None,
        show_progress: bool = False,
    ) -> Any:
        """Process a large CSV in chunks without loading it all into memory.

        If `output_path` is given, each chunk's result is appended to that
        file (CSV mode) — never accumulates in memory. Without `output_path`,
        results are collected and concatenated at the end (only viable if
        per-chunk results are small).

        Bug-fixed: no longer pre-reads the whole file just to count rows
        for the progress bar.
        """
        import pandas as pd

        # Estimate total chunks from file size, without reading the file.
        # Rough heuristic: average CSV row is ~80 bytes; chunk_size rows ≈ 8KB.
        # This is just for the progress bar — actual processing is exact.
        estimated_chunks = None
        if show_progress and self._tqdm_available:
            try:
                file_size = os.path.getsize(file_path)
                estimated_row_bytes = 80  # conservative average
                estimated_rows = max(1, file_size // estimated_row_bytes)
                estimated_chunks = max(1, estimated_rows // chunk_size)
            except OSError:
                pass

        results: list[Any] = []
        first_chunk = True
        chunk_iter = pd.read_csv(file_path, chunksize=chunk_size)

        if show_progress and self._tqdm_available:
            from tqdm import tqdm
            chunk_iter = tqdm(chunk_iter, total=estimated_chunks, desc="Processing chunks")

        for chunk in chunk_iter:
            result = process_chunk(chunk)

            if output_path and isinstance(result, pd.DataFrame):
                # Stream to disk — never accumulate
                result.to_csv(output_path, mode="a", header=first_chunk, index=False)
                first_chunk = False
                del result  # free immediately
            elif output_path and result is not None:
                # Non-DataFrame result with output_path — append as text
                with open(output_path, "a", encoding="utf-8") as f:
                    f.write(str(result) + "\n")
                first_chunk = False
                del result
            else:
                results.append(result)

        if output_path:
            return None

        # Concatenate in-memory results
        if results and isinstance(results[0], pd.DataFrame):
            return pd.concat(results, ignore_index=True)
        return results

    def parallel_groupby(
        self,
        df,
        group_col: str,
        agg_func: Callable,
        show_progress: bool = False,
    ) -> Any:
        """Parallel groupby: split df by group, apply agg_func to each, concat."""
        import pandas as pd

        groups = [group for _, group in df.groupby(group_col)]
        results = self.parallel_map(
            agg_func, groups, show_progress=show_progress, desc=f"Grouping by {group_col}"
        )
        return pd.concat(results, ignore_index=True)


class DaskProcessor:
    """Dask-based distributed processing for very large datasets.

    Use as a context manager to ensure cluster cleanup:

        with DaskProcessor() as dp:
            ddf = dp.read_csv("huge.csv")
            result = dp.parallel_apply(ddf, my_func)

    The __exit__ closes the cluster, preventing zombie processes.
    """

    def __init__(self, n_workers: int = -1):
        self.n_workers = mp.cpu_count() if n_workers == -1 else n_workers
        self._client = None
        self._cluster = None
        self._dask_available = self._check_dask()

    @staticmethod
    def _check_dask() -> bool:
        try:
            import dask  # noqa: F401
            return True
        except ImportError:
            return False

    def _get_client(self):
        if not self._dask_available:
            return None
        if self._client is None:
            try:
                from dask.distributed import Client, LocalCluster
                self._cluster = LocalCluster(n_workers=self.n_workers, threads_per_worker=1)
                self._client = Client(self._cluster)
            except Exception:
                self._client = None
        return self._client

    def close(self) -> None:
        """Clean up Dask client and cluster."""
        if self._client is not None:
            try:
                self._client.close()
            except Exception:
                pass
            self._client = None
        if self._cluster is not None:
            try:
                self._cluster.close()
            except Exception:
                pass
            self._cluster = None

    def __del__(self):
        self.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def read_csv(self, path: str, **kwargs):
        """Read CSV with Dask (lazy) if available, else pandas (eager)."""
        if self._dask_available:
            import dask.dataframe as dd
            return dd.read_csv(path, **kwargs)
        import pandas as pd
        return pd.read_csv(path, **kwargs)

    def parallel_apply(self, df, func: Callable, meta: Any = None, axis: int = 1) -> Any:
        """Apply `func` to df in parallel via Dask, falling back to pandas."""
        if self._dask_available:
            import dask.dataframe as dd
            if not isinstance(df, dd.DataFrame):
                df = dd.from_pandas(df, npartitions=self.n_workers)
            return df.apply(func, axis=axis, meta=meta).compute()
        return df.apply(func, axis=axis)


def parallel_apply(
    func: Callable,
    items: Iterable,
    n_workers: int = -1,
    show_progress: bool = False,
) -> list[Any]:
    """Quick parallel map. Convenience wrapper around DistributedProcessor."""
    return DistributedProcessor(n_workers).parallel_map(func, items, show_progress=show_progress)


def process_large_csv(
    file_path: str,
    process_func: Callable,
    chunk_size: int = 10000,
    output_path: str | None = None,
    show_progress: bool = False,
) -> Any:
    """Process large CSV without loading everything into memory."""
    return DistributedProcessor().process_large_file(
        file_path, process_func, chunk_size, output_path, show_progress
    )


__all__ = [
    "DistributedProcessor",
    "DaskProcessor",
    "parallel_apply",
    "process_large_csv",
]
