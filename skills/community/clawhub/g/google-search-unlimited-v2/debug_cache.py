#!/usr/bin/env python3
import hashlib
import sqlite3
import json

def get_cache_key(query: str, method: str = "auto") -> str:
    """Generate cache key from query and method"""
    key = f"{query}:{method}"
    return hashlib.sha256(key.encode()).hexdigest()

# Test the hash
query = "test cache corrigé"
method = "auto"
hash1 = get_cache_key(query, method)
print(f"Hash for '{query}' with method '{method}': {hash1}")

method = "oxylabs_mock"
hash2 = get_cache_key(query, method)
print(f"Hash for '{query}' with method '{method}': {hash2}")

# Check what's in the database
conn = sqlite3.connect('search_cache.db')
cursor = conn.cursor()

# Look for our query
cursor.execute("SELECT query_hash, query_text, method FROM search_cache WHERE query_text LIKE ?", 
               (f"%{query}%",))
rows = cursor.fetchall()

print(f"\nFound {len(rows)} entries for query containing '{query}':")
for row in rows:
    print(f"  Hash: {row[0][:16]}... | Query: {row[1][:30]}... | Method: {row[2]}")

conn.close()