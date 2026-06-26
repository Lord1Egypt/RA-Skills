#!/usr/bin/env python3
"""
MemPalace Search - Búsqueda semántica en el palacio
"""
import sys
import os
import json
import argparse

# Añadir mempalace al path
sys.path.insert(0, '/root/.openclaw/workspace/mempalace')

from mempalace.config import MempalaceConfig
from mempalace.searcher import search_memories


def main():
    parser = argparse.ArgumentParser(description='Search MemPalace memories')
    parser.add_argument('query', help='Search query')
    parser.add_argument('--limit', type=int, default=5, help='Max results (default: 5)')
    parser.add_argument('--wing', help='Filter by wing')
    parser.add_argument('--room', help='Filter by room')
    parser.add_argument('--palace-path', default=None, help='Custom palace path')
    
    args = parser.parse_args()
    
    palace_path = args.palace_path or os.path.expanduser('~/.mempalace/palace')
    
    try:
        results = search_memories(
            query=args.query,
            palace_path=palace_path,
            wing=args.wing,
            room=args.room,
            n_results=args.limit
        )
        print(json.dumps(results, indent=2, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"error": str(e)}, indent=2), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
