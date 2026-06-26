#!/usr/bin/env python3
"""Query the local RAG store with parent-child retrieval + cross-encoder reranker.

Search strategy:
1. Embed query → find top child chunks (cosine similarity)
2. Free embedding model, load reranker → rerank children
3. Resolve each top child → its parent chunk for full context
4. Return deduplicated parents ranked by best child score

Usage:
    query.py "your question" [--top-k 20] [--top-n 3] [--json]
"""

import argparse
import gc
import json
import os
import sys
import time
from datetime import datetime

import chromadb
from sentence_transformers import SentenceTransformer
from sentence_transformers import CrossEncoder

EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
RERANKER_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"
DB_DIR = os.path.expanduser("~/.local/share/local-rag/chromadb")
QUERY_LOG = os.path.expanduser("~/.local/share/local-rag/queries.log")
MAX_QUERY_LEN = 2000

# Singleton model cache — avoids reloading on repeated calls
_model_cache = {}


def get_embed_model():
    """Get or create cached embedding model."""
    if "embed" not in _model_cache:
        _model_cache["embed"] = SentenceTransformer(EMBED_MODEL)
    return _model_cache["embed"]


def log_query(question: str, n_results: int, elapsed: float, top_score: float | None):
    """Append query to log file for analytics."""
    os.makedirs(os.path.dirname(QUERY_LOG), exist_ok=True)
    entry = {
        "ts": datetime.now().isoformat(),
        "q": question[:80],  # Truncate for privacy
        "results": n_results,
        "elapsed_s": round(elapsed, 2),
        "top_score": top_score,
    }
    with open(QUERY_LOG, "a") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def query(question: str, top_k: int = 20, top_n: int = 3, timeout: int = 120, as_json: bool = False):
    """Search children → rerank → resolve parents."""
    # Sanitize input
    question = question[:MAX_QUERY_LEN].strip()
    if not question:
        return {"error": "Empty query"}

    t0 = time.time()

    # Step 1: Embed query (cached model)
    model = get_embed_model()
    q_embedding = model.encode([question], show_progress_bar=False).tolist()

    # Do NOT free model — keep cached for next query

    # Open DB
    client = chromadb.PersistentClient(path=DB_DIR)
    try:
        children_col = client.get_collection("children")
        parents_col = client.get_collection("parents")
    except Exception:
        return {"error": "No indexed data found. Run index.py first."}

    if children_col.count() == 0:
        return {"error": "Collection is empty. Run index.py to index your files."}

    # Vector search on children
    results = children_col.query(
        query_embeddings=q_embedding,
        n_results=min(top_k, children_col.count()),
        include=["documents", "metadatas", "distances"],
    )

    if not results["documents"][0]:
        return {"error": "No results found."}

    children = [
        {"text": doc, "meta": meta}
        for doc, meta in zip(results["documents"][0], results["metadatas"][0])
    ]

    # Step 2: Rerank with cross-encoder (cached for reuse)
    try:
        if "reranker" not in _model_cache:
            _model_cache["reranker"] = CrossEncoder(RERANKER_MODEL)
        reranker = _model_cache["reranker"]
        pairs = [[question, c["text"]] for c in children]
        scores = reranker.predict(pairs)

        for c, score in zip(children, scores):
            c["score"] = float(score)

        children.sort(key=lambda x: x["score"], reverse=True)
    except Exception as e:
        print(f"Warning: Reranker failed ({e}), using vector search order", file=sys.stderr)
        for c in children:
            c["score"] = 1.0

    # Step 3: Resolve parents (deduplicate by parent_idx per filepath)
    seen_parents = set()
    ranked_results = []

    for child in children:
        filepath = child["meta"]["filepath"]
        p_idx = child["meta"]["parent_idx"]
        parent_key = (filepath, p_idx)

        if parent_key in seen_parents:
            continue
        seen_parents.add(parent_key)

        parent_results = parents_col.get(
            where={"$and": [{"filepath": filepath}, {"parent_idx": p_idx}]},
            include=["documents"],
        )
        parent_text = parent_results["documents"][0] if parent_results["documents"] else child["text"]

        ranked_results.append({
            "score": round(child["score"], 4),
            "filepath": filepath,
            "parent_idx": p_idx,
            "parent_text": parent_text[:2000],
            "matching_child": child["text"][:500],
        })

        if len(ranked_results) >= top_n:
            break

    elapsed = time.time() - t0
    if elapsed > timeout:
        return {"error": f"Query timed out after {timeout}s"}

    top_score = ranked_results[0]["score"] if ranked_results else None
    log_query(question, len(ranked_results), elapsed, top_score)

    return {
        "question": question,
        "total_candidates": len(children),
        "results": ranked_results,
    }


def main():
    parser = argparse.ArgumentParser(description="Query local RAG with parent-child retrieval")
    parser.add_argument("question", help="Your question")
    parser.add_argument("--top-k", type=int, default=20, help="Initial child candidates")
    parser.add_argument("--top-n", type=int, default=3, help="Final parent results")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--timeout", type=int, default=120, help="Max seconds per query")
    args = parser.parse_args()

    result = query(args.question, args.top_k, args.top_n, args.timeout)

    if "error" in result:
        print(f"ERROR: {result['error']}", file=sys.stderr)
        sys.exit(1)

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"Question: {result['question']}")
        print(f"Candidates searched: {result['total_candidates']}\n")
        for i, r in enumerate(result["results"], 1):
            print(f"{'='*60}")
            print(f"Result {i} (score: {r['score']})")
            print(f"File: {r['filepath']} (parent chunk {r['parent_idx']})")
            print(f"\nMatched snippet:\n  {r['matching_child']}")
            print(f"\nFull context:\n{r['parent_text']}\n")


if __name__ == "__main__":
    main()
