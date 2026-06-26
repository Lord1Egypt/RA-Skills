#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import statistics
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from literag_runtime import preferred_python

SEARCH_SCRIPT = SCRIPT_DIR / "search_library.py"


def run_search(*, library: str, query: str, mode: str, limit: int) -> tuple[float, dict[str, Any]]:
    cmd = [
        preferred_python(),
        str(SEARCH_SCRIPT),
        library,
        query,
        "--mode",
        mode,
        "--limit",
        str(limit),
        "--format",
        "json",
        "--group-by",
        "path",
        "--merge-adjacent",
        "--no-text",
    ]
    started = time.perf_counter()
    proc = subprocess.run(cmd, capture_output=True, text=True)
    elapsed_ms = (time.perf_counter() - started) * 1000.0
    if proc.returncode != 0:
        detail = (proc.stderr or proc.stdout or "").strip()
        raise RuntimeError(f"search failed for mode={mode} query={query!r}: {detail}")
    try:
        payload = json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"invalid JSON from search for mode={mode} query={query!r}: {exc}") from exc
    return elapsed_ms, payload


def load_queries(args: argparse.Namespace) -> list[str]:
    queries: list[str] = []
    for query in args.query or []:
        stripped = query.strip()
        if stripped:
            queries.append(stripped)
    if args.queries_file:
        path = Path(args.queries_file).expanduser().resolve()
        if path.suffix.lower() == ".json":
            raw = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(raw, list):
                raise SystemExit("queries JSON must be an array of strings")
            for item in raw:
                if not isinstance(item, str):
                    raise SystemExit("queries JSON must contain only strings")
                stripped = item.strip()
                if stripped:
                    queries.append(stripped)
        else:
            for line in path.read_text(encoding="utf-8").splitlines():
                stripped = line.strip()
                if stripped and not stripped.startswith("#"):
                    queries.append(stripped)
    deduped: list[str] = []
    seen: set[str] = set()
    for query in queries:
        if query in seen:
            continue
        seen.add(query)
        deduped.append(query)
    if not deduped:
        raise SystemExit("provide at least one --query or --queries-file")
    return deduped


def summarize_run(query: str, mode: str, elapsed_ms: float, payload: dict[str, Any]) -> dict[str, Any]:
    results = payload.get("results") or []
    top = results[0] if results else None
    top_range = (top.get("ranges") or [None])[0] if top else None
    return {
        "query": query,
        "mode": mode,
        "elapsed_ms": round(elapsed_ms, 3),
        "result_count": len(results),
        "warning": payload.get("warning"),
        "top": None if not top else {
            "path": top.get("source_rel_path") or top.get("path"),
            "score": top.get("score"),
            "heading": top.get("heading"),
            "range": None if not top_range else {
                "start_chunk_index": top_range.get("start_chunk_index"),
                "end_chunk_index": top_range.get("end_chunk_index"),
                "score": top_range.get("score"),
            },
        },
    }


def build_summary(library: str, modes: list[str], queries: list[str], runs: list[dict[str, Any]]) -> dict[str, Any]:
    per_mode: dict[str, dict[str, Any]] = {}
    for mode in modes:
        mode_runs = [run for run in runs if run["mode"] == mode]
        elapsed_values = [float(run["elapsed_ms"]) for run in mode_runs]
        hit_counts = [int(run["result_count"]) for run in mode_runs]
        per_mode[mode] = {
            "runs": len(mode_runs),
            "avg_elapsed_ms": round(statistics.fmean(elapsed_values), 3) if elapsed_values else None,
            "median_elapsed_ms": round(statistics.median(elapsed_values), 3) if elapsed_values else None,
            "min_elapsed_ms": round(min(elapsed_values), 3) if elapsed_values else None,
            "max_elapsed_ms": round(max(elapsed_values), 3) if elapsed_values else None,
            "avg_result_count": round(statistics.fmean(hit_counts), 3) if hit_counts else None,
            "zero_hit_queries": sum(1 for run in mode_runs if int(run["result_count"]) == 0),
        }
    return {
        "schema": "literag.benchmark.v1",
        "library": library,
        "query_count": len(queries),
        "modes": modes,
        "summary": per_mode,
        "runs": runs,
    }


def render_text(payload: dict[str, Any]) -> None:
    print(f"LiteRAG benchmark: {payload['library']}")
    print(f"queries: {payload['query_count']} | modes: {', '.join(payload['modes'])}")
    print()
    for mode in payload["modes"]:
        stats = payload["summary"][mode]
        print(
            f"[{mode}] avg={stats['avg_elapsed_ms']}ms median={stats['median_elapsed_ms']}ms "
            f"min={stats['min_elapsed_ms']}ms max={stats['max_elapsed_ms']}ms "
            f"avg_hits={stats['avg_result_count']} zero_hits={stats['zero_hit_queries']}"
        )
    print()
    for run in payload["runs"]:
        top = run.get("top")
        top_desc = "no hits"
        if top:
            heading = top.get("heading") or "(no heading)"
            top_desc = f"{top.get('path')} | {heading} | score={top.get('score')}"
        print(f"- [{run['mode']}] {run['query']} -> {run['elapsed_ms']}ms | hits={run['result_count']} | {top_desc}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Benchmark LiteRAG search latency and hit shape")
    parser.add_argument("library")
    parser.add_argument("--query", action="append", default=[], help="Repeatable query text")
    parser.add_argument("--queries-file", default=None, help="Path to .txt or .json query list")
    parser.add_argument("--mode", dest="modes", action="append", choices=["hybrid", "fts", "vector"], help="Repeatable mode; defaults to hybrid,fts,vector")
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--warmup", action="store_true", help="Warm each mode once before timed runs")
    parser.add_argument("--repeat", type=int, default=1, help="Timed runs per query+mode")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    args = parser.parse_args()

    queries = load_queries(args)
    modes = args.modes or ["hybrid", "fts", "vector"]
    repeat = max(1, args.repeat)

    if args.warmup:
        for mode in modes:
            for query in queries:
                run_search(library=args.library, query=query, mode=mode, limit=args.limit)

    runs: list[dict[str, Any]] = []
    for query in queries:
        for mode in modes:
            for _ in range(repeat):
                elapsed_ms, payload = run_search(library=args.library, query=query, mode=mode, limit=args.limit)
                runs.append(summarize_run(query, mode, elapsed_ms, payload))

    result = build_summary(args.library, modes, queries, runs)
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        render_text(result)


if __name__ == "__main__":
    main()
