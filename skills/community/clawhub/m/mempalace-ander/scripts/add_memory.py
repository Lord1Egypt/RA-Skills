#!/usr/bin/env python3
"""
MemPalace Add Memory - Añadir memoria al palacio
"""
import sys
import os
import json
import argparse
import hashlib
from datetime import datetime

# Añadir mempalace al path
sys.path.insert(0, '/root/.openclaw/workspace/mempalace')

import chromadb
from mempalace.config import MempalaceConfig


def get_collection(palace_path, create=False):
    """Return the ChromaDB collection, or None on failure."""
    try:
        from mempalace.config import MempalaceConfig
        config = MempalaceConfig()
        collection_name = config.collection_name
        client = chromadb.PersistentClient(path=palace_path)
        if create:
            return client.get_or_create_collection(collection_name)
        return client.get_collection(collection_name)
    except Exception as e:
        return None


def check_duplicate(col, content, threshold=0.9):
    """Check if content already exists."""
    try:
        results = col.query(
            query_texts=[content],
            n_results=5,
            include=["metadatas", "documents", "distances"],
        )
        duplicates = []
        if results["ids"] and results["ids"][0]:
            for i, drawer_id in enumerate(results["ids"][0]):
                dist = results["distances"][0][i]
                similarity = round(1 - dist, 3)
                if similarity >= threshold:
                    meta = results["metadatas"][0][i]
                    doc = results["documents"][0][i]
                    duplicates.append({
                        "id": drawer_id,
                        "wing": meta.get("wing", "?"),
                        "room": meta.get("room", "?"),
                        "similarity": similarity,
                        "content": doc[:200] + "..." if len(doc) > 200 else doc,
                    })
        return {"is_duplicate": len(duplicates) > 0, "matches": duplicates}
    except Exception as e:
        return {"is_duplicate": False, "matches": [], "error": str(e)}


def main():
    parser = argparse.ArgumentParser(description='Add memory to MemPalace')
    parser.add_argument('--wing', required=True, help='Wing name (project)')
    parser.add_argument('--room', required=True, help='Room name (aspect)')
    parser.add_argument('--content', required=True, help='Content to store')
    parser.add_argument('--source-file', help='Source file path')
    parser.add_argument('--added-by', default='openclaw', help='Who is filing this')
    parser.add_argument('--palace-path', default=None, help='Custom palace path')
    
    args = parser.parse_args()
    
    palace_path = args.palace_path or os.path.expanduser('~/.mempalace/palace')
    
    col = get_collection(palace_path, create=True)
    if not col:
        print(json.dumps({"error": "Could not access palace", "path": palace_path}, indent=2), file=sys.stderr)
        sys.exit(1)
    
    # Check for duplicates
    dup = check_duplicate(col, args.content, threshold=0.9)
    if dup.get("is_duplicate"):
        print(json.dumps({
            "success": False,
            "reason": "duplicate",
            "matches": dup["matches"]
        }, indent=2, ensure_ascii=False))
        sys.exit(0)
    
    # Generate drawer ID
    drawer_id = f"drawer_{args.wing}_{args.room}_{hashlib.md5((args.content[:100] + datetime.now().isoformat()).encode()).hexdigest()[:16]}"
    
    try:
        col.add(
            ids=[drawer_id],
            documents=[args.content],
            metadatas=[{
                "wing": args.wing,
                "room": args.room,
                "source_file": args.source_file or "",
                "chunk_index": 0,
                "added_by": args.added_by,
                "filed_at": datetime.now().isoformat(),
            }]
        )
        print(json.dumps({
            "success": True,
            "drawer_id": drawer_id,
            "wing": args.wing,
            "room": args.room
        }, indent=2, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"success": False, "error": str(e)}, indent=2), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
