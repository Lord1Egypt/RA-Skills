#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Inspect Chroma DB"""

from langchain_chroma import Chroma

print("=" * 60)
print("Inspecting Chroma DB")
print("=" * 60)

# Load DB
db = Chroma(persist_directory="chroma_db", collection_name="openclaw_memory")

# Get stats
count = db._collection.count()
print(f"\nCollection: openclaw_memory")
print(f"Total vectors: {count}")

# Get sample documents
print("\nSample documents:")
results = db.get(include=["metadatas"], limit=5)

for i, (id, metadata) in enumerate(zip(results['ids'], results['metadatas']), 1):
    print(f"  {i}. ID: {id}")
    print(f"     Source: {metadata.get('source', 'N/A')}")
    print(f"     Type: {metadata.get('type', 'N/A')}")

print("\n" + "=" * 60)
