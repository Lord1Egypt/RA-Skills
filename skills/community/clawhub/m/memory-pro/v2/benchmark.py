#!/usr/bin/env python3
import argparse
import json
import os
import time
import requests
from statistics import mean


def run_query(api_url, query, mode, top_k):
    payload = {"query": query, "top_k": top_k, "mode": mode}
    t0 = time.perf_counter()
    r = requests.post(api_url, json=payload, timeout=30)
    dt = (time.perf_counter() - t0) * 1000.0
    r.raise_for_status()
    data = r.json()
    return dt, data.get("results", [])


def duplicate_ratio(results):
    if not results:
        return 0.0
    sents = [x.get("sentence", "").strip() for x in results]
    uniq = len(set(sents))
    return 1.0 - (uniq / max(1, len(sents)))


def overlap_at_k(a, b, k=5):
    sa = [x.get("sentence", "").strip() for x in a[:k]]
    sb = [x.get("sentence", "").strip() for x in b[:k]]
    if not sa and not sb:
        return 1.0
    inter = len(set(sa) & set(sb))
    denom = max(1, min(len(sa), len(sb), k))
    return inter / denom


def main():
    ap = argparse.ArgumentParser(description="Memory Pro Phase-2 benchmark (vector vs hybrid)")
    ap.add_argument("--api", default="http://127.0.0.1:8001/search")
    ap.add_argument("--queries", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "eval_queries.json"))
    ap.add_argument("--top-k", type=int, default=5)
    ap.add_argument("--out", default="/tmp/memory_pro_benchmark.json")
    args = ap.parse_args()

    with open(args.queries, "r", encoding="utf-8") as f:
        queries = json.load(f)

    vec_lat, hyb_lat = [], []
    vec_dup, hyb_dup = [], []
    overlap = []
    details = []

    for q in queries:
        v_ms, v_res = run_query(args.api, q, "vector", args.top_k)
        h_ms, h_res = run_query(args.api, q, "hybrid", args.top_k)

        vec_lat.append(v_ms)
        hyb_lat.append(h_ms)
        vec_dup.append(duplicate_ratio(v_res))
        hyb_dup.append(duplicate_ratio(h_res))
        overlap.append(overlap_at_k(v_res, h_res, k=args.top_k))

        details.append({
            "query": q,
            "vector_latency_ms": round(v_ms, 2),
            "hybrid_latency_ms": round(h_ms, 2),
            "vector_top1": (v_res[0]["sentence"][:140] if v_res else ""),
            "hybrid_top1": (h_res[0]["sentence"][:140] if h_res else ""),
            "overlap_at_k": round(overlap[-1], 3),
        })

    summary = {
        "queries": len(queries),
        "avg_vector_latency_ms": round(mean(vec_lat), 2) if vec_lat else 0,
        "avg_hybrid_latency_ms": round(mean(hyb_lat), 2) if hyb_lat else 0,
        "latency_ratio_hybrid_over_vector": round((mean(hyb_lat) / mean(vec_lat)), 3) if vec_lat and mean(vec_lat) else None,
        "avg_vector_duplicate_ratio": round(mean(vec_dup), 3) if vec_dup else 0,
        "avg_hybrid_duplicate_ratio": round(mean(hyb_dup), 3) if hyb_dup else 0,
        "avg_overlap_at_k": round(mean(overlap), 3) if overlap else 0,
    }

    out = {"summary": summary, "details": details}
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print(f"Saved: {args.out}")


if __name__ == "__main__":
    main()
