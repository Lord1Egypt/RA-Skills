import chromadb
from chromadb.config import Settings
import sys

# 设置 UTF-8 编码
sys.stdout.reconfigure(encoding='utf-8')

try:
    client = chromadb.PersistentClient(path="C:\\Users\\Xiabi\\.openclaw\\workspace\\chroma_db")
    collections = client.list_collections()
    print(f"[OK] ChromaDB connection successful!")
    print(f"Found {len(collections)} collection(s):")
    for col in collections:
        print(f"  - {col.name}")
except Exception as e:
    print(f"[ERROR] ChromaDB connection failed: {e}")
    import traceback
    traceback.print_exc()
