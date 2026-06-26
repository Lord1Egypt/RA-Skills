# -*- coding: utf-8 -*-
"""语义搜索召回记忆。"""

import os
import certifi
os.environ.setdefault("HF_ENDPOINT", "https://hf-mirror.com")
os.environ.setdefault("REQUESTS_CA_BUNDLE", certifi.where())
os.environ.setdefault("SSL_CERT_FILE", certifi.where())

import argparse
import json
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, '..', 'data')
COLLECTION = "openclaw_memory"
MODEL_NAME = "BAAI/bge-small-zh-v1.5"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", required=True, help="搜索关键词")
    parser.add_argument("--limit", type=int, default=5)
    args = parser.parse_args()

    try:
        import chromadb
        from sentence_transformers import SentenceTransformer

        model = SentenceTransformer(MODEL_NAME)
        client = chromadb.PersistentClient(path=DB_PATH)
        collection = client.get_or_create_collection(name=COLLECTION, metadata={"hnsw:space": "cosine"})

        if collection.count() == 0:
            print(json.dumps({"status": "ok", "results": []}, ensure_ascii=False))
            return

        embedding = model.encode([args.query]).tolist()
        results = collection.query(query_embeddings=embedding, n_results=min(args.limit, collection.count()))

        items = []
        for i in range(len(results["ids"][0])):
            meta = results["metadatas"][0][i]
            items.append({
                "id": results["ids"][0][i],
                "text": results["documents"][0][i],
                "category": meta.get("category", "other"),
                "importance": meta.get("importance", 0.7),
                "created_at": meta.get("created_at", ""),
                "distance": round(results["distances"][0][i], 4),
            })

        print(json.dumps({"status": "ok", "results": items}, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}, ensure_ascii=False))
        sys.exit(1)


if __name__ == "__main__":
    main()
