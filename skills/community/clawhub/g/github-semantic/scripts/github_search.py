#!/usr/bin/env python3
"""
GitHub Semantic Search — search indexed GitHub data with natural language.
Usage:
  python github_search.py "memory search failing" --limit 10
  python github_search.py "CI broken" --repo openclaw/openclaw --type issue
  python github_search.py "PR review delays" --repo owner/repo --type PR
"""
import argparse
import json
import os
import subprocess
import sys
import urllib.request

os.environ.setdefault("OLLAMA_MODELS", r"D:\ChatAI\OpenClaw\.ollama\models")
os.environ.setdefault("PYTHONIOENCODING", "utf-8")

COLLECTION = "github_repos"
EMBED_MODEL = "nomic-embed-text:latest"
GH_EXE = r"C:\Program Files\GitHub CLI\gh.exe"

COLORS = {
    "issue": "\033[92m",
    "PR": "\033[94m",
    "repo": "\033[93m",
    "code": "\033[96m",
    "reset": "\033[0m"
}


def get_embedding(text: str) -> list:
    payload = {"model": EMBED_MODEL, "prompt": text}
    req = urllib.request.Request(
        "http://localhost:11434/api/embeddings",
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = json.loads(resp.read())
    return data["embedding"]


def search(qdrant_client, query: str, repo: str = None, type_filter: str = None, limit: int = 10):
    from qdrant_client.models import Filter, FieldCondition, MatchValue, SearchParams

    query_vec = get_embedding(query)
    search_filter = None
    must = []
    if repo:
        must.append(FieldCondition(key="repo", match=MatchValue(value=repo)))
    if type_filter:
        must.append(FieldCondition(key="type", match=MatchValue(value=type_filter)))
    if must:
        search_filter = Filter(must=must)

    results = qdrant_client.query_points(
        collection_name=COLLECTION,
        query=query_vec,
        query_filter=search_filter,
        limit=limit,
        with_payload=True,
    )
    return results.points


def gh(args: str) -> dict:
    result = subprocess.run(
        f'"{GH_EXE}" {args}',
        capture_output=True, encoding="utf-8", errors="replace"
    )
    if result.returncode != 0:
        return {}
    try:
        return json.loads(result.stdout or "{}")
    except:
        return {}


def format_result(item, score: float):
    p = item.payload
    color = COLORS.get(p["type"], COLORS["reset"])
    type_label = f"{color}{p['type'].upper()}{COLORS['reset']}"
    state_emoji = "🟢" if p.get("state") == "open" else "🔴"
    labels = ", ".join(p.get("labels", [])) or "none"
    score_pct = f"{score*100:.1f}%"

    lines = [
        f"{type_label} #{p['number']} {state_emoji}  [match {score_pct}]",
        f"  Title: {p.get('title', 'N/A')}",
        f"  Repo: {p.get('repo', 'N/A')} | Author: {p.get('author', 'N/A')}",
        f"  Labels: {labels}",
        f"  URL: {p.get('url', 'N/A')}",
        f"  Created: {p.get('created_at', 'N/A')} | Updated: {p.get('updated_at', 'N/A')}",
    ]
    body = p.get("body", "")
    if body:
        lines.append(f"  Body: {body[:200].strip()}...")
    return "\n".join(lines)


def get_ci_status(repo: str, limit: int = 5) -> str:
    try:
        result = subprocess.run(
            f'"{GH_EXE}" run list --repo {repo} --limit {limit} --json name,status,conclusion,createdAt,headBranch,url',
            capture_output=True, encoding="utf-8", errors="replace"
        )
        if result.returncode != 0:
            return ""
        runs = json.loads(result.stdout or "[]")
        if not runs:
            return "No CI runs found."
        lines = ["\n**Recent CI Runs:**"]
        for r in runs:
            icon = "✅" if r.get("conclusion") == "success" else "❌" if r.get("conclusion") == "failure" else "⏳"
            lines.append(f"  {icon} {r.get('name','workflow')} | {r.get('status','unknown')} | {r.get('conclusion','unknown')} | {r.get('headBranch','?')}")
        return "\n".join(lines)
    except:
        return ""


def main():
    parser = argparse.ArgumentParser(description="GitHub Semantic Search")
    parser.add_argument("query", help="Natural language search query")
    parser.add_argument("--repo", help="Filter by repo (owner/repo)")
    parser.add_argument("--type", choices=["issue", "PR", "repo", "code"], dest="type_filter")
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--ci", action="store_true")
    args = parser.parse_args()

    from qdrant_client import QdrantClient
    qc = QdrantClient("localhost", port=6333)

    print(f"\n🔍 Query: {args.query}")
    if args.repo:
        print(f"   Repo: {args.repo}")
    if args.type_filter:
        print(f"   Type: {args.type_filter}")

    if args.ci and args.repo:
        print(get_ci_status(args.repo, limit=5))

    try:
        results = search(qc, args.query, repo=args.repo, type_filter=args.type_filter, limit=args.limit)
    except Exception as e:
        print(f"Search error: {e}")
        return

    if not results:
        print("\n⚠ No results found.")
        return

    print(f"\n📋 Top {len(results)} results:\n")
    for i, r in enumerate(results, 1):
        print(f"[{i}] {format_result(r, r.score)}")
        print()


if __name__ == "__main__":
    main()
