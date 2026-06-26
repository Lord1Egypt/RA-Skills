#!/usr/bin/env python3
"""Context Manager - Search memory files and get recent context"""
import os
import json
from pathlib import Path

MEMORY_DIR = Path('memory')
SEARCH_DIRS = ['memory', 'skills']

def search_memory(keyword, limit=10):
    """Search memory files for keyword"""
    results = []
    for search_dir in SEARCH_DIRS:
        if not os.path.exists(search_dir):
            continue
        for root, dirs, files in os.walk(search_dir):
            for file in files:
                if file.endswith('.md') or file.endswith('.json'):
                    path = os.path.join(root, file)
                    try:
                        with open(path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            if keyword.lower() in content.lower():
                                results.append(path)
                    except:
                        pass
    return results[:limit]

def get_recent(count=5):
    """Get recent memory entries"""
    recent = []
    memory_dir = Path('memory')
    if memory_dir.exists():
        files = sorted(memory_dir.glob('*.md'), key=lambda p: p.stat().st_mtime, reverse=True)
        recent = [f.name for f in files[:count]]
    return recent

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        keyword = sys.argv[1]
        results = search_memory(keyword)
        print(f'Found {len(results)} results for "{keyword}"')
        for r in results:
            print(f'  - {r}')
    else:
        print('Recent memory:')
        for r in get_recent():
            print(f'  - {r}')
