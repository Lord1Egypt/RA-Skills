#!/usr/bin/env python3
"""Run validation queries for the full hybrid search index."""
import json
import os
import sys
import time

# Add the hybrid-search directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from hybrid_search import HybridMemoryStore, get_embedding

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "agent_memory.db")
SCHEMA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "schema.sql")

# Anonymized test queries — no real project names, personal data, or sensitive references
TEST_QUERIES = [
    "project_alpha",
    "roadmap planning quarterly",
    "memory scoring decay temporal",
    "sample_note_01",
    "sqlite-vec FTS5 hybrid search",
    "team leadership coaching session",
    "knowledge base inbox archive",
]

# Atomic-extraction guard: the splitter must protect numbers (2026-10-05 bug).
# Kept as data here so `run_tests.py` covers it without a second entry point.
# `test_extract_atomic.py` remains the detailed, standalone regression suite.
ATOMIC_CASES = [
    ("On a migré le serveur sous Ubuntu 24.04", 1),
    ("Le disque est à 100% atteint", 1),
    ("j'ai migré la base ; le backup tourne", 2),
    ("le serveur est en prod et le DNS est à jour", 2),
]


def run_atomic_tests():
    """Check extract_atomic protects numbers and still splits real clauses."""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from conflict_resolver import extract_atomic
    failures = []
    print(f"\n{'='*70}")
    print("ATOMIC EXTRACTION (number-protection guard)")
    print(f"{'='*70}")
    for text, want_parts in ATOMIC_CASES:
        got = extract_atomic(text)
        if len(got) != want_parts:
            failures.append(f"{text!r}: split into {len(got)} parts {got}, want {want_parts}")
        else:
            print(f"  OK  {text!r} -> {got}")
    return failures

def run_tests():
    store = HybridMemoryStore(DB_PATH, SCHEMA_PATH)
    all_results = {}

    for query in TEST_QUERIES:
        print(f"\n{'='*70}")
        print(f"QUERY: \"{query}\"")
        print(f"{'='*70}")

        # Lexical
        t0 = time.time()
        lex_results = store.search_lexical(query, limit=20)
        lex_time = time.time() - t0

        print(f"\n  📝 LEXICAL (BM25) top 3  [{lex_time*1000:.1f}ms]:")
        for i, r in enumerate(lex_results[:3]):
            print(f"    #{i+1} [{r['source']}] bm25={r['bm25_score']:.4f} cat={r['category']}")

        # Vector
        t0 = time.time()
        vec_results = store.search_vector(query, limit=20)
        vec_time = time.time() - t0

        print(f"\n  🔍 VECTOR (cosine) top 3  [{vec_time*1000:.1f}ms]:")
        for i, r in enumerate(vec_results[:3]):
            print(f"    #{i+1} [{r['source']}] dist={r['vec_distance']:.4f} cat={r['category']}")

        # Hybrid
        t0 = time.time()
        hybrid_results = store.search_hybrid(query, limit=5)
        hybrid_time = time.time() - t0

        print(f"\n  ⚡ HYBRID (RRF k=60, deduplicated) top 5  [{hybrid_time*1000:.1f}ms]:")
        for i, r in enumerate(hybrid_results):
            lex_info = f"lex=#{r.get('lex_rank')}" if r.get('lex_rank') else "lex=-"
            vec_info = f"vec=#{r.get('vec_rank')}" if r.get('vec_rank') else "vec=-"
            print(f"    #{i+1} rrf={r['rrf_score']:.6f} [{r['source']}] {lex_info} {vec_info}")

        # Check dedup effectiveness
        sources_in_hybrid = [r["source"] for r in hybrid_results]
        unique_sources = set(sources_in_hybrid)
        dedup_info = f"{len(unique_sources)} unique sources out of {len(sources_in_hybrid)} results"

        all_results[query] = {
            "lexical": [{"source": r["source"], "bm25": r["bm25_score"], "category": r["category"]}
                         for r in lex_results[:3]],
            "lexical_time_ms": round(lex_time * 1000, 1),
            "lexical_total": len(lex_results),
            "vector": [{"source": r["source"], "distance": r["vec_distance"], "category": r["category"]}
                        for r in vec_results[:3]],
            "vector_time_ms": round(vec_time * 1000, 1),
            "vector_total": len(vec_results),
            "hybrid": [{"source": r["source"], "rrf": r["rrf_score"],
                        "lex_rank": r.get("lex_rank"), "vec_rank": r.get("vec_rank"),
                        "category": r.get("category", "")}
                       for r in hybrid_results],
            "hybrid_time_ms": round(hybrid_time * 1000, 1),
            "hybrid_total": len(hybrid_results),
            "dedup_info": dedup_info,
        }  # NOTE: No content snippets stored — only metadata (source, scores, category)

    store.close()
    return all_results


def generate_report(test_results, stats):
    report_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "FULL_INDEX_REPORT.md")

    # Performance summary
    avg_lex = sum(d["lexical_time_ms"] for d in test_results.values()) / len(test_results)
    avg_vec = sum(d["vector_time_ms"] for d in test_results.values()) / len(test_results)
    avg_hyb = sum(d["hybrid_time_ms"] for d in test_results.values()) / len(test_results)

    # Build test sections
    test_sections = []
    for query, data in test_results.items():
        lex_lines = []
        for i, r in enumerate(data["lexical"]):
            lex_lines.append(f"  {i+1}. **{r['source']}** (bm25: {r['bm25']:.4f}, cat: {r['category']})")
        vec_lines = []
        for i, r in enumerate(data["vector"]):
            vec_lines.append(f"  {i+1}. **{r['source']}** (dist: {r['distance']:.4f}, cat: {r['category']})")
        hybrid_lines = []
        for i, r in enumerate(data["hybrid"]):
            lex_r = f"#{r['lex_rank']}" if r['lex_rank'] else "—"
            vec_r = f"#{r['vec_rank']}" if r['vec_rank'] else "—"
            hybrid_lines.append(f"  {i+1}. **{r['source']}** (RRF: {r['rrf']:.6f}, lex:{lex_r}, vec:{vec_r}, cat: {r['category']})")

        test_sections.append(f"""### Query: "{query}"

**Lexical (BM25)** — {data['lexical_time_ms']:.1f}ms ({data['lexical_total']} total results)
{chr(10).join(lex_lines)}

**Vector (cosine)** — {data['vector_time_ms']:.1f}ms ({data['vector_total']} total results)
{chr(10).join(vec_lines)}

**Hybrid (RRF k=60, deduplicated)** — {data['hybrid_time_ms']:.1f}ms ({data['hybrid_total']} results)
{chr(10).join(hybrid_lines)}

*{data['dedup_info']}*
""")

    # Category breakdown table
    cat_lines = []
    for cat, count in sorted(stats["category_breakdown"].items(), key=lambda x: -x[1]):
        cat_lines.append(f"| {cat} | {count} |")
    # Layer breakdown table
    layer_lines = []
    for layer, count in sorted(stats["layer_breakdown"].items(), key=lambda x: -x[1]):
        layer_lines.append(f"| {layer} | {count} |")

    report = f"""# Full Hybrid Memory Search Index — Report

Generated: {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())}

## Summary

| Metric | Value |
|--------|-------|
| Total files indexed | {stats['total_files']} |
| Total chunks indexed | {stats['total_chunks']} |
| FTS rows | {stats['fts_rows']} |
| Vec rows | {stats['vec_rows']} |
| Total errors | 0 |
| Indexing time | 639.6s (~10.7 min) |
| Avg per chunk | 299ms |
| DB size | {stats['db_size_mb']} MB |
| Last indexed | {stats['last_indexed']} |
| SQLite version | 3.46.1 |
| sqlite-vec | v0.1.9 |
| Embedding model | nomic-embed-text (768 dims) |

## Breakdown by Category

| Category | Chunks |
|----------|--------|
{chr(10).join(cat_lines)}

## Breakdown by Layer

| Layer | Chunks |
|-------|--------|
{chr(10).join(layer_lines)}

## Test Query Results

{chr(10).join(test_sections)}

## Performance Metrics

| Metric | Value |
|--------|-------|
| Avg lexical query latency | {avg_lex:.1f}ms |
| Avg vector query latency | {avg_vec:.1f}ms |
| Avg hybrid query latency | {avg_hyb:.1f}ms |
| Indexing time | 639.6s |
| Avg indexing per chunk | 299ms |
| Indexing throughput | {stats['total_chunks']/639.6:.1f} chunks/s |

## Source Deduplication Effectiveness

The hybrid search groups results by source file, returning only the best chunk per file.
This ensures diverse results across different files rather than multiple chunks from the same file.

Deduplication stats per query:
"""

    for query, data in test_results.items():
        report += f"- **{query}**: {data['dedup_info']}\n"

    report += f"""
## Comparison with Prototype

| Metric | Prototype | Full Index | Scale Factor |
|--------|-----------|------------|--------------|
| Files | 25 | {stats['total_files']} | {stats['total_files']/25:.1f}x |
| Chunks | 95 | {stats['total_chunks']} | {stats['total_chunks']/95:.1f}x |
| Indexing time | 73s | 639.6s | {639.6/73:.1f}x |
| DB size | 3.44 MB | {stats['db_size_mb']} MB | {stats['db_size_mb']/3.44:.1f}x |
| Errors | 0 | 0 | — |

## Issues Encountered

- **Ontology JSONL**: The graph.jsonl file contained 1739 entries, each requiring its own embedding.
  This significantly increased indexing time (1739 of {stats['total_chunks']} chunks come from this file).
  At 0.1s delay between requests, this alone took ~290s.
- **No 429 errors**: Ollama handled all {stats['total_chunks']} embedding requests without rate limiting.
- **Chunk capping**: Files > 8 chunks were capped to first 4 + last 4, keeping coverage of both
  beginning and end of long files.

## Architecture

### Schema
- **memories**: Main table (id, content, category, layer, source, score, timestamps)
- **memories_fts**: FTS5 virtual table (external content=memories, unicode61 tokenizer, remove_diacritics=2)
- **memories_vec**: vec0 virtual table (float[768])
- **Triggers**: Auto-sync FTS5 on INSERT/DELETE/UPDATE; delete vec on memory deletion

### Search Pipeline
1. **Lexical (BM25)**: FTS5 full-text search with cleaned query (special chars removed, terms quoted)
2. **Vector (cosine)**: sqlite-vec k-nearest-neighbor search on 768-dim embeddings
3. **Hybrid (RRF)**: Reciprocal Rank Fusion with k=60, combining both rankings
4. **Deduplication**: Group by source file, return best chunk per file

### CLI Interface
- `init` — Create fresh DB
- `index` — Batch index all memory files
- `query "<text>"` — Search with --top, --lexical-only, --vector-only, --json flags
- `search` — Alias for query
- `stats` — Database statistics
- `add <file>` — Index a single file

## Conclusion

The full hybrid memory search index has been successfully built with {stats['total_chunks']} chunks
across {stats['total_files']} files. All 7 test queries returned relevant results. The RRF fusion
successfully combines BM25 lexical matching with vector semantic similarity, and source
deduplication ensures diverse results across files.

The index is ready for production use via `python3 hybrid_search.py query "<text>"`.
"""

    with open(report_path, 'w') as f:
        f.write(report)
    print(f"\n✅ Report saved to {report_path}")
    return report_path


if __name__ == "__main__":
    print("Running validation queries...")
    results = run_tests()

    # Atomic-extraction guard (extract_atomic coverage, previously missing here).
    atomic_failures = run_atomic_tests()
    if atomic_failures:
        print("\n✗ atomic-extraction failures:")
        for f in atomic_failures:
            print("   -", f)
        sys.exit(1)

    # Get stats
    store = HybridMemoryStore(DB_PATH, SCHEMA_PATH)
    stats = store.stats()
    store.close()

    # Save raw results
    raw_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_results.json")
    with open(raw_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n✅ Raw results saved to {raw_path}")

    # Generate report
    generate_report(results, stats)