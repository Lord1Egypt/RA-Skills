"""Batch search pipeline with resume and rate limiting."""

import json
import csv
import inspect
import logging
import os
import time
from typing import Optional, List
from pathlib import Path
from datetime import datetime

from .config import Config, get_config
from .search import search, deep_research, model_council, step_by_step, SearchResult

MODE_FUNCTIONS = {
    "search": search,
    "deep_research": deep_research,
    "model_council": model_council,
    "step_by_step": step_by_step,
}


def _run_mode(fn, query: str, config: Config, verify: bool):
    """Call built-in or injected mode functions across old signatures."""
    try:
        signature = inspect.signature(fn)
        params = signature.parameters.values()
        supports_verify = (
            "verify" in signature.parameters
            or any(p.kind == inspect.Parameter.VAR_KEYWORD for p in params)
        )
    except (TypeError, ValueError):
        supports_verify = True
    if supports_verify:
        return fn(query, config=config, verify=verify)
    return fn(query, config=config)


logger = logging.getLogger(__name__)


def load_queries(source: str) -> List[dict]:
    """Load queries from file or inline string. Returns [{query, mode}]."""
    path = Path(source)
    if not path.exists():
        return [{"query": source, "mode": "search"}]

    suffix = path.suffix.lower()
    queries = []

    if suffix == ".json":
        with open(path) as f:
            data = json.load(f)
        for item in (data if isinstance(data, list) else [data]):
            if isinstance(item, str):
                queries.append({"query": item, "mode": "search"})
            elif isinstance(item, dict):
                queries.append({"query": item.get("query", ""), "mode": item.get("mode", "search")})
    elif suffix == ".csv":
        with open(path, newline="") as f:
            for row in csv.DictReader(f):
                q = row.get("query", row.get("q", ""))
                if q:
                    queries.append({"query": q, "mode": row.get("mode", "search")})
    elif suffix == ".txt":
        with open(path) as f:
            queries = [{"query": l.strip(), "mode": "search"} for l in f if l.strip()]

    return queries or [{"query": source, "mode": "search"}]


def run_batch(
    queries: List[dict],
    output_file: str = "batch_results.json",
    config: Optional[Config] = None,
    progress_file: Optional[str] = None,
    resume: bool = False,
    delay: Optional[float] = None,
    verify: bool = True,
) -> List[SearchResult]:
    """Run batch search with optional resume and rate limiting.

    Progress is always tracked in progress_file (if given): each query|||mode
    is appended only AFTER a successful search, so any batch — not just ones
    started with resume=True — can be resumed later. Failed searches are not
    marked done and are retried on resume. Output JSON is rewritten
    incrementally after every item so a mid-batch crash loses no completed work.
    """
    cfg = config or get_config()
    batch_delay = delay or cfg.batch_delay

    done_set = set()
    if progress_file and os.path.exists(progress_file):
        with open(progress_file) as f:
            done_set = {line.strip() for line in f if line.strip()}
        logger.debug("Resume: loaded %d completed keys from %s", len(done_set), progress_file)

    results = []
    total = len(queries)
    skipped = 0
    invalid = 0
    failed = 0
    logger.info(
        "Batch start: %d queries, output=%s, resume=%s, delay=%.1fs",
        total, output_file, resume, batch_delay,
    )

    def write_output():
        with open(output_file, "w") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

    for i, item in enumerate(queries):
        query = item.get("query", "")
        mode = item.get("mode", "search")

        if not query:
            invalid += 1
            logger.warning("[%d/%d] empty query, skipping", i + 1, total)
            continue

        if mode not in MODE_FUNCTIONS:
            invalid += 1
            logger.warning(
                "[%d/%d] unknown mode %r for query %r, skipping",
                i + 1, total, mode, query[:60],
            )
            continue

        key = f"{query}|||{mode}"
        if resume and key in done_set:
            skipped += 1
            logger.debug("[%d/%d] already done (resume), skipping: %s", i + 1, total, key)
            continue

        logger.info("[%d/%d] %s: %s", i + 1, total, mode, query[:80])

        ok = False
        try:
            result = _run_mode(MODE_FUNCTIONS[mode], query, cfg, verify)
            ok = True
        except Exception as e:
            failed += 1
            result = {"error": str(e), "query": query, "mode": mode}
            logger.error("[%d/%d] %s failed: %s", i + 1, total, mode, e)

        result["query"] = query
        result["searched_at"] = datetime.now().isoformat()
        logger.debug(
            "[%d/%d] %s: answer_len=%d sources=%d%s",
            i + 1, total, mode,
            len(result.get("answer") or ""),
            len(result.get("sources") or []),
            " (failed)" if not ok else "",
        )
        results.append(result)
        write_output()

        if ok and progress_file:
            with open(progress_file, "a") as f:
                f.write(key + "\n")

        if i < total - 1:
            time.sleep(batch_delay)

    # Ensure the output file exists even if every item was skipped/invalid.
    write_output()

    logger.info(
        "Batch done: %d searched, %d resumed-skipped, %d invalid/empty skipped, %d failed -> %s",
        len(results), skipped, invalid, failed, output_file,
    )
    return results
