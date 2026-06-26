#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""验证向量化结果"""

from langchain_chroma import Chroma
import sys

print("=" * 60)
print("Verifying Vectorization Results")
print("=" * 60)

try:
    # Load vector store
    db = Chroma(
        persist_directory="chroma_db",
        collection_name="langchain"
    )
    
    # Get stats
    count = db._collection.count()
    print(f"\nVector Database Stats:")
    print(f"  Collection: langchain")
    print(f"  Total vectors: {count}")
    
    # Test search
    test_queries = ["瀑布", "TTS", "memory", "Aliyun"]
    
    for query in test_queries:
        print(f"\nSearch: '{query}'")
        results = db.similarity_search(query, k=2)
        print(f"  Found {len(results)} results")
        for i, doc in enumerate(results, 1):
            source = doc.metadata.get("source", "Unknown")
            print(f"    {i}. Source: {source}")
    
    print("\n" + "=" * 60)
    print("SUCCESS! Vectorization complete!")
    print("=" * 60)
    
except Exception as e:
    print(f"ERROR: {e}")
    sys.exit(1)
