#!/usr/bin/env python3
"""
Quick Recall — Uses lazy_recall (FAISS + embeddings) for full semantic search.

Usage:
    python3 quick_recall.py "what did David say about autonomy"
    python3 quick_recall.py "NIMA architecture" --top 5
    python3 quick_recall.py "Melissa" --compact

Uses:
    - Pre-computed embedding index (15K vectors)
    - FAISS for O(log N) search
    - Full graph.sqlite (18K memories)
"""

import sys
import os
import time

# Add nima-core to path
sys.path.insert(0, os.path.expanduser("~/.openclaw/workspace/nima-core/openclaw_hooks/nima-recall-live"))

def quick_recall(query: str, top_k: int = 3, compact: bool = False):
    """Run lazy_recall with full embedding search."""
    start = time.time()
    
    try:
        from lazy_recall import lazy_recall
        
        result = lazy_recall(query, max_results=top_k)
        elapsed = time.time() - start
        
        memories = result.get('memories', [])
        
        if not memories:
            print(f"🧠 NIMA: No relevant memories ({elapsed:.1f}s)")
            return
        
        print(f"🧠 NIMA ({elapsed:.1f}s):")
        
        if compact:
            for mem in memories[:top_k]:
                content = mem.get('content', '')
                text = content[:200] + "..." if len(content) > 200 else content
                print(f"  ⭐ {text}")
        else:
            print(f"\n**Query:** {query}")
            print(f"**Results:** {len(memories)} found\n")
            for i, mem in enumerate(memories[:top_k], 1):
                content = mem.get('content', '')
                text = content[:300] + "..." if len(content) > 300 else content
                print(f"{i}. {text}\n")
                        
    except Exception as e:
        print(f"🧠 NIMA Error: {e}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Quick NIMA recall with embeddings")
    parser.add_argument("query", help="What to search for")
    parser.add_argument("--top", type=int, default=3, help="Number of results (default: 3)")
    parser.add_argument("--compact", action="store_true", help="Compact output format")
    
    args = parser.parse_args()
    quick_recall(args.query, top_k=args.top, compact=args.compact)
