#!/usr/bin/env python3
import sqlite3

conn = sqlite3.connect('search_cache.db')
cursor = conn.cursor()

# Check table structure
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables in database:", tables)

# Check search_cache table
cursor.execute("PRAGMA table_info(search_cache);")
columns = cursor.fetchall()
print("\nColumns in search_cache:")
for col in columns:
    print(f"  {col[1]} ({col[2]})")

# Count entries
cursor.execute("SELECT COUNT(*) FROM search_cache;")
count = cursor.fetchone()[0]
print(f"\nTotal entries: {count}")

# Show some entries
cursor.execute("SELECT query_text, method, created_at FROM search_cache ORDER BY created_at DESC LIMIT 5;")
rows = cursor.fetchall()
print("\nRecent entries:")
for row in rows:
    print(f"  Query: {row[0][:50]}... | Method: {row[1]} | Date: {row[2]}")

conn.close()