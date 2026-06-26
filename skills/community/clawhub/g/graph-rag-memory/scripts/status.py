#!/usr/bin/env python3
"""
status.py — Check graph-rag memory system status.

Usage:
    python3 status.py
    python3 status.py --graph workspace
    python3 status.py --json
"""

import sys
import os
import json
import argparse

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
WORKSPACE_ROOT = os.environ.get("OPENCLAW_WORKSPACE", "/home/node/.openclaw/workspace")
MEM_DIR = os.path.join(WORKSPACE_ROOT, "memory-upgrade")
sys.path.insert(0, MEM_DIR)

import httpx
import falkordb
from config import (
    OLLAMA_URL, AMD_OLLAMA_URL, FALKORDB_HOST, FALKORDB_PORT,
    LLM_MODEL, EMBED_GENERAL
)


def check_service(name, url, timeout=5):
    try:
        resp = httpx.get(url, timeout=timeout)
        return True, resp.status_code
    except Exception as e:
        return False, str(e)[:60]


def check_ollama_models(base_url):
    try:
        resp = httpx.get(f"{base_url}/api/tags", timeout=10)
        data = resp.json()
        return [m["name"] for m in data.get("models", [])]
    except:
        return []


def check_falkordb(graph_name="workspace"):
    try:
        r = falkordb.FalkorDB(host=FALKORDB_HOST, port=FALKORDB_PORT)
        graphs = r.list_graphs()
        if graph_name in graphs:
            g = r.select_graph(graph_name)
            n = g.query("MATCH (n) RETURN count(n)").result_set[0][0]
            e = g.query("MATCH ()-[r:RELATES_TO]->() RETURN count(r)").result_set[0][0]
            emb = g.query("MATCH ()-[r:RELATES_TO]->() WHERE r.fact_embedding IS NOT NULL RETURN count(r)").result_set[0][0]
            return True, {"graphs": graphs, "nodes": n, "edges": e, "edges_with_embedding": emb}
        return True, {"graphs": graphs, "nodes": 0, "edges": 0, "edges_with_embedding": 0}
    except Exception as ex:
        return False, str(ex)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--graph", default="workspace")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    status = {}

    # Check NVIDIA Ollama
    ok, detail = check_service("NVIDIA Ollama", f"{OLLAMA_URL}/api/tags")
    models = check_ollama_models(OLLAMA_URL) if ok else []
    embed_ok = EMBED_GENERAL in [m.split(":")[0] for m in models] or \
               any(EMBED_GENERAL in m for m in models)
    status["nvidia_ollama"] = {
        "ok": ok, "url": OLLAMA_URL, "models": models,
        "embed_model_loaded": embed_ok,
    }

    # Check AMD Ollama (if different)
    if AMD_OLLAMA_URL != OLLAMA_URL:
        ok2, _ = check_service("AMD Ollama", f"{AMD_OLLAMA_URL}/api/tags")
        models2 = check_ollama_models(AMD_OLLAMA_URL) if ok2 else []
        llm_ok = any(LLM_MODEL.split(":")[0] in m for m in models2)
        status["amd_ollama"] = {
            "ok": ok2, "url": AMD_OLLAMA_URL, "models": models2,
            "llm_model_loaded": llm_ok,
        }

    # Check FalkorDB
    ok3, db_detail = check_falkordb(args.graph)
    status["falkordb"] = {"ok": ok3, "detail": db_detail}

    # Check centroids
    centroids_path = os.path.join(MEM_DIR, "checkpoints", "centroids.json")
    if os.path.exists(centroids_path):
        with open(centroids_path) as f:
            centroids = json.load(f)
        status["centroids"] = {"domains": list(centroids.keys())}
    else:
        status["centroids"] = {"domains": [], "warning": "Not bootstrapped yet"}

    if args.json:
        print(json.dumps(status, indent=2))
        return

    # Human-readable output
    print("=== Graph-RAG Memory Status ===\n")

    nv = status["nvidia_ollama"]
    icon = "✅" if nv["ok"] else "❌"
    emb = "✅" if nv.get("embed_model_loaded") else "⚠️"
    print(f"{icon} NVIDIA Ollama ({nv['url']})")
    print(f"   Models: {', '.join(nv['models']) or 'none'}")
    print(f"   {emb} {EMBED_GENERAL} (required for embeddings)")

    if "amd_ollama" in status:
        amd = status["amd_ollama"]
        icon2 = "✅" if amd["ok"] else "❌"
        llm = "✅" if amd.get("llm_model_loaded") else "⚠️"
        print(f"\n{icon2} AMD Ollama ({amd['url']})")
        print(f"   Models: {', '.join(amd['models']) or 'none'}")
        print(f"   {llm} {LLM_MODEL} (required for write path)")

    fdb = status["falkordb"]
    icon3 = "✅" if fdb["ok"] else "❌"
    print(f"\n{icon3} FalkorDB ({FALKORDB_HOST}:{FALKORDB_PORT})")
    if fdb["ok"] and isinstance(fdb["detail"], dict):
        d = fdb["detail"]
        print(f"   Graphs: {', '.join(d.get('graphs', []))}")
        print(f"   '{args.graph}' graph: {d['nodes']} nodes, {d['edges']} edges")
        print(f"   Embeddings stored: {d['edges_with_embedding']}/{d['edges']}")
    else:
        print(f"   Error: {fdb['detail']}")

    ctr = status["centroids"]
    icon4 = "✅" if ctr["domains"] else "⚠️"
    print(f"\n{icon4} Centroid Router")
    if ctr["domains"]:
        print(f"   Domains: {', '.join(ctr['domains'])}")
    else:
        print(f"   Not bootstrapped — run phase3_ingest.py first")

    print()
    all_ok = (nv["ok"] and nv.get("embed_model_loaded") and fdb["ok"] and ctr["domains"])
    if all_ok:
        print("✅ System ready")
    else:
        print("⚠️  System partially ready — check items above")


if __name__ == "__main__":
    main()
