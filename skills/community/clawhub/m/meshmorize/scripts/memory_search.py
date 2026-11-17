#!/usr/bin/env python3
"""MeshMorize Local Memory Search — pure grep-based, no plugins needed"""
import os, sys, subprocess, json
from datetime import datetime, timedelta

MEMORY_DIR = os.path.expanduser("~/.openclaw/workspace/memory")
FRESH_DIR = os.path.join(MEMORY_DIR, "fresh")
TDAI_DIR = os.path.join(MEMORY_DIR, "tdai-archive")
MESH_FILE = os.path.join(MEMORY_DIR, "mesh.json")

def search_tdai_archive(query, max_results=5):
    """Search TDAI archive files"""
    results = []
    if not os.path.exists(TDAI_DIR):
        return results
    for f in sorted(os.listdir(TDAI_DIR)):
        if not f.endswith(".md"):
            continue
        fp = os.path.join(TDAI_DIR, f)
        with open(fp) as fh:
            for i, line in enumerate(fh, 1):
                if query.lower() in line.lower():
                    results.append((f, i, line.strip()[:200]))
                    if len(results) >= max_results:
                        return results
    return results


def search_daily_logs(query, max_results=5):
    """Search all daily log files for a query"""
    results = []
    for f in sorted(os.listdir(MEMORY_DIR)):
        if not f.endswith(".md") or not f[0].isdigit():
            continue
        fp = os.path.join(MEMORY_DIR, f)
        with open(fp) as fh:
            for i, line in enumerate(fh, 1):
                if query.lower() in line.lower():
                    results.append((f, i, line.strip()[:200]))
                    if len(results) >= max_results:
                        return results
    return results

def search_fresh(query):
    """Search the fresh layer first"""
    results = []
    for f in ["today.md", "yesterday.md", "2-days-ago.md", "3-days-ago.md", "4-days-ago.md"]:
        fp = os.path.join(FRESH_DIR, f)
        if not os.path.exists(fp):
            continue
        with open(fp) as fh:
            content = fh.read()
            if query.lower() in content.lower() or fuzzy_match(content, query):
                lines = [l.strip() for l in content.split('\n') if query.lower() in l.lower()]
                results.append((f, lines[:3]))
    return results

def read_today():
    """Read today's fresh context"""
    fp = os.path.join(FRESH_DIR, "today.md")
    if os.path.exists(fp):
        with open(fp) as fh:
            return fh.read()[:3000]
    return ""

def fuzzy_match(text, query):
    """Simple fuzzy matching for typos."""
    from difflib import SequenceMatcher
    if not text or not query:
        return False
    text = text.lower()
    query = query.lower()
    if query in text:
        return True
    return SequenceMatcher(None, text, query).ratio() > 0.6

def search_mesh_edges(query, mesh):
    """Search through mesh graph edges."""
    results = []
    edges = mesh.get('edges', [])
    for i, edge in enumerate(edges):
        src = edge.get('source', '')
        tgt = edge.get('target', '')
        rel = edge.get('relation', '')
        label = edge.get('label', '')
        text = f"{src} {tgt} {rel} {label}"
        if query.lower() in text.lower() or fuzzy_match(text, query):
            results.append(f"  Edge #{i}: {src} --{rel}--> {tgt} ({label})")
    return results

def search_mesh(query):
    """Search the mesh.json for matching nodes"""
    if not os.path.exists(MESH_FILE):
        return []
    with open(MESH_FILE) as f:
        mesh = json.load(f)
    nodes = mesh.get("nodes", mesh if isinstance(mesh, list) else [])
    if isinstance(mesh, dict) and "nodes" in mesh:
        nodes = mesh["nodes"]
    results = []
    for n in nodes:
        if isinstance(n, dict) and "id" in n:
            if query.lower() in n.get("id", "").lower() or query.lower() in n.get("note", "").lower():
                results.append(n)
    return results[:5]

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: memory_search <query>")
        print("       memory_search --today")
        sys.exit(1)
    
    if sys.argv[1] == "--today":
        print("=== FRESH LAYER (TODAY) ===")
        print(read_today() or "No today data")
        sys.exit(0)
    
    query = " ".join(sys.argv[1:])
    
    print(f"\n=== SEARCHING: {query} ===")
    
    fresh = search_fresh(query)
    if fresh:
        print(f"\n📂 FRESH LAYER ({len(fresh)} hits):")
        for f, lines in fresh:
            for l in lines:
                print(f"  📄 {f}: {l[:150]}")
    
    tdai = search_tdai_archive(query)
    if tdai:
        print(f"\n📦 TDAI ARCHIVE ({len(tdai)} hits):")
        for f, line, text in tdai:
            print(f"  📄 {f}:{line}: {text}")
    
    logs = search_daily_logs(query)
    if logs:
        print(f"\n📚 DAILY LOGS ({len(logs)} hits):")
        for f, line, text in logs:
            print(f"  📄 {f}:{line}: {text}")
    
    mesh = search_mesh(query)
    if mesh:
        print(f"\n🔗 MESH ({len(mesh)} hits):")
        for n in mesh:
            print(f"  🔗 {n['id']}: {n.get('note','')[:100]}")
    
    if not fresh and not logs and not mesh and not tdai:
        print("  No results found.")
