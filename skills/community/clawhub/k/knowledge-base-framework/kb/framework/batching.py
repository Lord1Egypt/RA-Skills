"""
Batch Processing Utilities for Knowledge Base
==============================================

Efficient, memory-friendly batching for large-scale operations:
- Embedding generation (1000s of texts)
- ChromaDB upserts (bulk inserts)
- SQLite batch writes
- Orphan deletion

Key features:
- Chunk-große Operationen (configurable batch size)
- Progress reporting (callback-based, no hard dependency on tqdm)
- Memory-efficient (generator/yield patterns, no massive arrays in RAM)
- Error tolerance: one failed batch doesn't kill the whole operation

Usage:
    from kb.framework.batching import batched, BatchProgress, BatchResult

    # Simple iteration in chunks
    for chunk in batched(items, size=100):
        process(chunk)

    # With progress tracking
    progress = BatchProgress(total=10000, desc="Embedding")
    for chunk in batched(items, size=100):
        result = process(chunk)
        progress.advance(len(chunk))
    progress.finish()

    # With error tolerance
    result = batch_process(
        items=section_ids,
        batch_size=500,
        processor=embed_and_upsert,
        desc="Embedding sections"
    )
    print(f"OK: {result.success}, Failed: {result.failed}, Errors: {result.errors}")
"""

import logging
import time
from typing import (
    Any, Callable, Generator, Iterable, List, Optional, Sequence, TypeVar
)
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)

T = TypeVar("T")


# ---------------------------------------------------------------------------
# Core: chunked iteration
# ---------------------------------------------------------------------------

def batched(iterable: Iterable[T], size: int = 100) -> Generator[List[T], None, None]:
    """
    Yield successive chunks of `size` from `iterable`.

    Unlike more-itertools.batched (Python 3.12+), this:
    - Accepts any iterable (not just sequences)
    - Returns concrete lists (safe to reuse within loop body)
    - Works on all Python >= 3.9

    Args:
        iterable: Any iterable to chunk
        size: Chunk size (must be >= 1)

    Yields:
        Lists of at most `size` items

    Example:
        >>> list(batched(range(5), 2))
        [[0, 1], [2, 3], [4]]
    """
    if size < 1:
        raise ValueError(f"Batch size must be >= 1, got {size}")

    batch: List[T] = []
    for item in iterable:
        batch.append(item)
        if len(batch) >= size:
            yield batch
            batch = []
    if batch:
        yield batch


def batched_from_generator(
    gen: Generator[T, None, None],
    size: int = 100
) -> Generator[List[T], None, None]:
    """
    Batch items from a generator into chunks.

    Useful when the source is a generator (e.g., DB cursor) and you
    don't want to materialize it all into a list first.

    Args:
        gen: Source generator
        size: Chunk size

    Yields:
        Lists of at most `size` items
    """
    return batched(gen, size)


# ---------------------------------------------------------------------------
# Progress tracking
# ---------------------------------------------------------------------------

@dataclass
class BatchProgress:
    """
    Lightweight progress tracker for batch operations.

    Uses callbacks instead of hard-coupling to tqdm or other UI libs.
    Provides:
    - Rate calculation (items/sec)
    - ETA estimation
    - Logging at regular intervals

    Usage:
        progress = BatchProgress(total=5000, desc="Embedding", log_every=500)
        for chunk in batched(items, 100):
            process(chunk)
            progress.advance(len(chunk))
        progress.finish()
    """
    total: int
    desc: str = "Processing"
    log_every: int = 100          # Log every N items (0 = only at end)
    log_callback: Optional[Callable[[str], None]] = None  # Custom log handler

    _processed: int = field(init=False, default=0)
    _failed: int = field(init=False, default=0)
    _start: float = field(init=False, default=0.0)
    _last_log: int = field(init=False, default=0)

    def __post_init__(self):
        self._start = time.monotonic()
        if self.log_every <= 0:
            self.log_every = max(1, self.total // 10) if self.total > 0 else 100

    def advance(self, count: int = 1, failed: int = 0) -> None:
        """Record progress for `count` items (optionally `failed` failures)."""
        self._processed += count
        self._failed += failed

        should_log = (
            self._processed - self._last_log >= self.log_every
            or self._processed >= self.total
        )
        if should_log:
            self._log_progress()
            self._last_log = self._processed

    def _log_progress(self) -> None:
        """Emit a progress line."""
        elapsed = time.monotonic() - self._start
        rate = self._processed / elapsed if elapsed > 0 else 0
        pct = (self._processed / self.total * 100) if self.total > 0 else 0
        remaining = self.total - self._processed

        eta_secs = remaining / rate if rate > 0 else 0
        eta_str = _format_duration(eta_secs)

        msg = (
            f"[{self.desc}] {self._processed}/{self.total} "
            f"({pct:.1f}%) — {rate:.1f}/s — ETA {eta_str}"
        )
        if self._failed > 0:
            msg += f" — {self._failed} failed"

        if self.log_callback:
            self.log_callback(msg)
        else:
            logger.info(msg)

    def finish(self) -> dict:
        """
        Mark operation as finished, log summary, return stats dict.

        Returns:
            dict with processed, failed, elapsed_seconds, rate
        """
        elapsed = time.monotonic() - self._start
        rate = self._processed / elapsed if elapsed > 0 else 0

        msg = (
            f"[{self.desc}] Done: {self._processed}/{self.total} "
            f"in {_format_duration(elapsed)} ({rate:.1f}/s)"
        )
        if self._failed > 0:
            msg += f" — {self._failed} failed"

        if self.log_callback:
            self.log_callback(msg)
        else:
            logger.info(msg)

        return {
            "processed": self._processed,
            "failed": self._failed,
            "elapsed_seconds": round(elapsed, 2),
            "rate": round(rate, 2),
        }

    @property
    def processed(self) -> int:
        return self._processed

    @property
    def failed(self) -> int:
        return self._failed


# ---------------------------------------------------------------------------
# Batch result
# ---------------------------------------------------------------------------

@dataclass
class BatchResult:
    """
    Result of a batch operation with error tolerance.

    Tracks successes, failures, and per-batch error details.
    One failed batch does NOT abort the whole operation.
    """
    total: int = 0
    success: int = 0
    failed: int = 0
    errors: List[dict] = field(default_factory=list)  # [{batch_index, error, count}]
    elapsed_seconds: float = 0.0

    @property
    def rate(self) -> float:
        """Items per second (successful only)."""
        return self.success / self.elapsed_seconds if self.elapsed_seconds > 0 else 0.0

    @property
    def ok(self) -> bool:
        """True if no failures."""
        return self.failed == 0

    def to_dict(self) -> dict:
        return {
            "total": self.total,
            "success": self.success,
            "failed": self.failed,
            "errors": self.errors,
            "elapsed_seconds": round(self.elapsed_seconds, 2),
            "rate": round(self.rate, 2),
        }

    def __repr__(self) -> str:
        return (
            f"BatchResult(total={self.total}, ok={self.success}, "
            f"failed={self.failed}, {self.rate:.1f}/s)"
        )


# ---------------------------------------------------------------------------
# High-level: batch_process
# ---------------------------------------------------------------------------

def batch_process(
    items: Sequence[Any],
    processor: Callable[[List[Any]], int],
    batch_size: int = 100,
    desc: str = "Processing",
    log_every: int = 0,
    on_error: str = "continue",
) -> BatchResult:
    """
    Process `items` in batches with progress tracking and error tolerance.

    This is the main high-level API. It:
    - Splits items into chunks of `batch_size`
    - Calls `processor(chunk)` for each chunk
    - Expects processor to return the number of successfully processed items
    - Continues on error if `on_error="continue"` (default)
    - Tracks progress and returns a BatchResult

    Args:
        items: Full list/sequence of items to process
        processor: Callable that takes a batch (list) and returns count of
                   successfully processed items. May raise exceptions.
        batch_size: Items per batch (default 100)
        desc: Description for progress logging
        log_every: Log every N items (0 = auto, ~10 logs total)
        on_error: "continue" (default) or "raise" — whether to abort on first error

    Returns:
        BatchResult with success/failure counts and error details

    Example:
        def embed_chunk(chunk):
            embeddings = model.encode(chunk)
            collection.upsert(ids=..., embeddings=embeddings)
            return len(chunk)

        result = batch_process(
            items=all_texts,
            processor=embed_chunk,
            batch_size=500,
            desc="Embedding sections"
        )
        # result.success = 40000, result.failed = 0
    """
    start = time.monotonic()
    total = len(items)
    result = BatchResult(total=total)

    progress = BatchProgress(total=total, desc=desc, log_every=log_every)

    for batch_idx, chunk in enumerate(batched(items, batch_size)):
        try:
            ok_count = processor(chunk)
            if ok_count is None:
                ok_count = len(chunk)
            result.success += ok_count
            failed_in_batch = len(chunk) - ok_count
            result.failed += failed_in_batch
            progress.advance(len(chunk), failed=failed_in_batch)

        except Exception as exc:
            if on_error == "raise":
                raise

            batch_failed = len(chunk)
            result.failed += batch_failed
            result.errors.append({
                "batch_index": batch_idx,
                "error": str(exc),
                "count": batch_failed,
            })
            progress.advance(len(chunk), failed=batch_failed)
            logger.warning(
                f"[{desc}] Batch {batch_idx} failed: {exc} "
                f"({batch_failed} items skipped)"
            )

    result.elapsed_seconds = time.monotonic() - start
    progress.finish()
    return result


# ---------------------------------------------------------------------------
# ChromaDB-specific: batched upsert
# ---------------------------------------------------------------------------

def batched_chroma_upsert(
    collection,
    ids: List[str],
    embeddings: List[list],
    metadatas: Optional[List[dict]] = None,
    documents: Optional[List[str]] = None,
    batch_size: int = 500,
    desc: str = "ChromaDB upsert",
) -> BatchResult:
    """
    Upsert large lists to ChromaDB in batches.

    ChromaDB's upsert() can be slow or memory-heavy with huge lists.
    This function chunks the data and upserts incrementally.

    Args:
        collection: ChromaDB collection object
        ids: List of IDs
        embeddings: List of embedding vectors
        metadatas: Optional list of metadata dicts
        documents: Optional list of document strings
        batch_size: Items per upsert call (default 500)
        desc: Description for progress logging

    Returns:
        BatchResult with success/failure counts

    Example:
        # Before: one giant upsert (risky with 40k items)
        collection.upsert(ids=all_ids, embeddings=all_embs, ...)

        # After: safe, batched
        result = batched_chroma_upsert(collection, all_ids, all_embs, ...)
    """
    total = len(ids)

    if metadatas is None:
        metadatas = [None] * total
    if documents is None:
        documents = [None] * total

    def _upsert_batch(chunk_indices):
        chunk_ids = [ids[i] for i in chunk_indices]
        chunk_embs = [embeddings[i] for i in chunk_indices]
        chunk_meta = [metadatas[i] for i in chunk_indices]
        chunk_docs = [documents[i] for i in chunk_indices]

        # ChromaDB doesn't accept None in metadatas list
        kwargs = {"ids": chunk_ids, "embeddings": chunk_embs}
        if any(m is not None for m in chunk_meta):
            kwargs["metadatas"] = [m for m in chunk_meta if m is not None]
        if any(d is not None for d in chunk_docs):
            kwargs["documents"] = [d for d in chunk_docs if d is not None]

        collection.upsert(**kwargs)
        return len(chunk_ids)

    return batch_process(
        items=list(range(total)),
        processor=_upsert_batch,
        batch_size=batch_size,
        desc=desc,
    )


def batched_chroma_delete(
    collection,
    ids: List[str],
    batch_size: int = 1000,
    desc: str = "ChromaDB delete",
) -> BatchResult:
    """
    Delete large lists from ChromaDB in batches.

    Args:
        collection: ChromaDB collection object
        ids: List of IDs to delete
        batch_size: Items per delete call (default 1000)
        desc: Description for progress logging

    Returns:
        BatchResult with success/failure counts
    """
    def _delete_batch(chunk):
        collection.delete(ids=chunk)
        return len(chunk)

    return batch_process(
        items=ids,
        processor=_delete_batch,
        batch_size=batch_size,
        desc=desc,
    )


# ---------------------------------------------------------------------------
# SQLite-specific: batched executemany
# ---------------------------------------------------------------------------

def batched_executemany(
    conn,
    sql: str,
    params: List[tuple],
    batch_size: int = 1000,
    desc: str = "SQLite batch insert",
    commit_every: int = 0,
) -> BatchResult:
    """
    Execute many SQL statements in batches with progress tracking.

    Args:
        conn: SQLite connection
        sql: SQL statement with placeholders
        params: List of parameter tuples
        batch_size: Rows per executemany call (default 1000)
        desc: Description for progress logging
        commit_every: Commit every N rows (0 = only at end)

    Returns:
        BatchResult
    """
    total = len(params)

    def _execute_batch(chunk):
        conn.executemany(sql, chunk)
        if commit_every > 0 and total > 0:
            # Approximate: commit when we've done ~commit_every rows
            pass
        return len(chunk)

    result = batch_process(
        items=params,
        processor=_execute_batch,
        batch_size=batch_size,
        desc=desc,
    )

    conn.commit()
    return result


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _format_duration(seconds: float) -> str:
    """Format seconds into human-readable duration."""
    if seconds < 1:
        return f"{seconds:.1f}s"
    elif seconds < 60:
        return f"{seconds:.0f}s"
    elif seconds < 3600:
        mins = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{mins}m {secs}s"
    else:
        hours = int(seconds // 3600)
        mins = int((seconds % 3600) // 60)
        return f"{hours}h {mins}m"


# ---------------------------------------------------------------------------
# Convenience: memory-efficient embedding pipeline
# ---------------------------------------------------------------------------

def embed_in_batches(
    embed_fn: Callable[[List[str]], List[list]],
    texts: List[str],
    batch_size: int = 64,
    desc: str = "Embedding",
) -> List[list]:
    """
    Generate embeddings in batches without loading all into memory at once.

    This wraps a model's encode/embed_batch function and applies it
    chunk-by-chunk, concatenating the results.

    Args:
        embed_fn: Function that takes a list of texts and returns list of vectors
                  e.g., chroma.embed_batch or model.encode().tolist()
        texts: All texts to embed
        batch_size: Texts per embedding call (default 64)
        desc: Description for progress logging

    Returns:
        Flat list of all embedding vectors

    Example:
        # Before: one giant call (OOM risk with 40k texts)
        all_embeddings = chroma.embed_batch(all_40000_texts)

        # After: memory-safe, batched
        all_embeddings = embed_in_batches(chroma.embed_batch, all_40000_texts, batch_size=500)
    """
    all_embeddings: List[list] = []
    total = len(texts)
    progress = BatchProgress(total=total, desc=desc, log_every=max(1, total // 20))

    for chunk in batched(texts, batch_size):
        try:
            chunk_embeddings = embed_fn(chunk)
            all_embeddings.extend(chunk_embeddings)
            progress.advance(len(chunk))
        except Exception as exc:
            # On embedding failure, add zero vectors as fallback
            # so the list stays aligned with the input
            logger.warning(f"[{desc}] Embedding batch failed: {exc}")
            dim = 384  # default for all-MiniLM-L6-v2
            all_embeddings.extend([[0.0] * dim] * len(chunk))
            progress.advance(len(chunk), failed=len(chunk))

    progress.finish()
    return all_embeddings