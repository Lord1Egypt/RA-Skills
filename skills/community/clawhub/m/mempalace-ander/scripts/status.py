#!/usr/bin/env python3
"""
MemPalace Status - Estado del palacio
"""
import sys
import os
import json
import argparse

# Añadir mempalace al path
sys.path.insert(0, '/root/.openclaw/workspace/mempalace')

import chromadb
from mempalace.config import MempalaceConfig


def main():
    parser = argparse.ArgumentParser(description='Get MemPalace status')
    parser.add_argument('--palace-path', default=None, help='Custom palace path')
    
    args = parser.parse_args()
    
    palace_path = args.palace_path or os.path.expanduser('~/.mempalace/palace')
    
    # Load config to get collection name
    config = MempalaceConfig()
    collection_name = config.collection_name
    
    try:
        client = chromadb.PersistentClient(path=palace_path)
        col = client.get_collection(collection_name)
    except Exception as e:
        print(json.dumps({
            "error": "No palace found",
            "path": palace_path,
            "hint": "Run: mempalace init <dir> && mempalace mine <dir>"
        }, indent=2), file=sys.stderr)
        sys.exit(1)
    
    try:
        count = col.count()
        wings = {}
        rooms = {}
        
        try:
            all_meta = col.get(include=["metadatas"], limit=10000)["metadatas"]
            for m in all_meta:
                w = m.get("wing", "unknown")
                r = m.get("room", "unknown")
                wings[w] = wings.get(w, 0) + 1
                rooms[r] = rooms.get(r, 0) + 1
        except Exception:
            pass
        
        result = {
            "total_drawers": count,
            "wings": wings,
            "rooms": rooms,
            "palace_path": palace_path,
        }
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"error": str(e)}, indent=2), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
