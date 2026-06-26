# -*- coding: utf-8 -*-
"""存储一条记忆到本地向量数据库。"""

import os
import certifi
os.environ.setdefault("HF_ENDPOINT", "https://hf-mirror.com")
os.environ.setdefault("REQUESTS_CA_BUNDLE", certifi.where())
os.environ.setdefault("SSL_CERT_FILE", certifi.where())

import argparse
import json
import sys
import uuid
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, '..', 'data')
COLLECTION = "openclaw_memory"
MODEL_NAME = "BAAI/bge-small-zh-v1.5"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", required=True, help="记忆内容")
    parser.add_argument("--category", default="other", choices=["fact", "preference", "decision", "entity", "other"])
    parser.add_argument("--importance", type=float, default=0.7)
    args = parser.parse_args()

    try:
        import chromadb
        from sentence_transformers import SentenceTransformer

        os.makedirs(DB_PATH, exist_ok=True)

        model = SentenceTransformer(MODEL_NAME)
        client = chromadb.PersistentClient(path=DB_PATH)
        collection = client.get_or_create_collection(name=COLLECTION, metadata={"hnsw:space": "cosine"})

        embedding = model.encode([args.text]).tolist()
        mem_id = uuid.uuid4().hex[:12]
        now = datetime.now().isoformat()

        collection.add(
            ids=[mem_id],
            embeddings=embedding,
            documents=[args.text],
            metadatas=[{"category": args.category, "importance": args.importance, "created_at": now}],
        )

        print(json.dumps({"status": "ok", "id": mem_id, "message": "已存储"}, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}, ensure_ascii=False))
        sys.exit(1)


if __name__ == "__main__":
    main()
