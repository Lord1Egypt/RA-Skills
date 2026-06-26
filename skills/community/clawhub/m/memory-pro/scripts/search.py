#!/usr/bin/env python3
"""
Memory Search - Search indexed memories
"""

import json
import os
import sys
from pathlib import Path


def _env_path(name: str, fallback: str) -> Path:
    value = os.getenv(name, fallback)
    return Path(os.path.expandvars(value)).expanduser()


INDEX_FILE = _env_path(
    "MEMORY_PRO_LEGACY_INDEX_PATH",
    os.path.join(os.getenv("OPENCLAW_WORKSPACE", ""), "skills", "memory-pro", "data", "INDEX.json"),
)


def save_index(index):
    INDEX_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        json.dump(index, f, ensure_ascii=False, indent=2)

def search(query):
    """Search for keyword in index"""
    # Create empty index if not exists
    if not INDEX_FILE.exists():
        print("ℹ️ Index not found. Creating empty index...")
        save_index({})
        print("❌ No results found (empty index)")
        return
    
    try:
        with open(INDEX_FILE, 'r', encoding='utf-8') as f:
            index = json.load(f)
    except json.JSONDecodeError:
        print("⚠️ Index file corrupted. Resetting...")
        save_index({})
        print("❌ No results found (reset index)")
        return
    
    query_lower = query.lower()
    results = []
    
    # Search for exact and partial matches
    for keyword, contexts in index.items():
        if query_lower in keyword.lower():
            results.extend(contexts)
    
    if not results:
        print(f"❌ No results found for: {query}")
        return
    
    print(f"🔍 Search results for: {query}")
    print(f"📊 Found {len(results)} mentions\n")
    
    # Group by date and deduplicate
    seen = set()
    for result in sorted(results, key=lambda x: x['date'], reverse=True):
        key = (result['date'], result['context'])
        if key not in seen:
            seen.add(key)
            print(f"📅 {result['date']} ({result['file']})")
            print(f"   {result['context']}")
            print()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python search.py <keyword>")
        sys.exit(1)
    
    query = ' '.join(sys.argv[1:])
    search(query)
