#!/usr/bin/env python3
"""
query_memory.py — Query the graph-rag memory system from the command line.

Usage:
    python3 query_memory.py "your question here"
    python3 query_memory.py "your question" --limit 10
    python3 query_memory.py "your question" --graph workspace --json

Output: Ranked list of relevant facts from the memory graph.
"""

import asyncio
import sys
import os
import json
import argparse

# Resolve memory-upgrade path relative to workspace root
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
WORKSPACE_ROOT = os.environ.get("OPENCLAW_WORKSPACE", "/home/node/.openclaw/workspace")
MEM_DIR = os.path.join(WORKSPACE_ROOT, "memory-upgrade")
sys.path.insert(0, MEM_DIR)

from setup_graphiti import init_graphiti
from read_path import query_memory
from router import DomainRouter
from config import OLLAMA_URL


async def main():
    parser = argparse.ArgumentParser(description="Query the graph-rag memory system")
    parser.add_argument("query", help="Natural language question")
    parser.add_argument("--limit", type=int, default=5, help="Max results (default: 5)")
    parser.add_argument("--graph", default="workspace", help="Graph name (default: workspace)")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--no-vector", action="store_true", help="BM25 only (no vector search)")
    args = parser.parse_args()

    graphiti = await init_graphiti(args.graph)
    router = DomainRouter(ollama_base_url=OLLAMA_URL)

    edges, routing = await query_memory(
        graphiti=graphiti,
        router=router,
        query=args.query,
        group_ids=[args.graph],
        limit=args.limit,
        use_vector=not args.no_vector,
    )

    await graphiti.close()

    if args.json:
        output = {
            "query": args.query,
            "routing": {
                "domain": routing.domain,
                "method": routing.method,
                "confidence": routing.confidence,
            },
            "results": [
                {
                    "fact": getattr(e, "fact", str(e)),
                    "uuid": getattr(e, "uuid", None),
                    "valid_at": str(getattr(e, "valid_at", "")),
                }
                for e in edges
            ],
        }
        print(json.dumps(output, indent=2))
    else:
        print(f"\n🔍 Query: {args.query}")
        print(f"📍 Routed to: {routing.domain} ({routing.method}, confidence={routing.confidence:.3f})")
        print(f"📊 Results: {len(edges)}\n")
        for i, edge in enumerate(edges, 1):
            fact = getattr(edge, "fact", str(edge))
            print(f"  {i}. {fact}")
        if not edges:
            print("  (no results)")


if __name__ == "__main__":
    asyncio.run(main())
