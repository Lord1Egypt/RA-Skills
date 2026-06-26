# -*- coding: utf-8 -*-
"""删除记忆：按 ID 精确删除，或按语义搜索删除最匹配的一条。"""

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
    parser.add_argument("--id", default=None, help="按 ID 删除")
    parser.add_argument("--query", default=None, help="按语义搜索删除最匹配的一条")
    args = parser.parse_args()

    if not args.id and not args.query:
        print(json.dumps({"status": "error", "message": "必须提供 --id 或 --query"}, ensure_ascii=False))
        sys.exit(1)

    try:
        import chromadb

        client = chromadb.PersistentClient(path=DB_PATH)
        collection = client.get_or_create_collection(name=COLLECTION, metadata={"hnsw:space": "cosine"})

        if args.id:
            try:
                collection.delete(ids=[args.id])
                print(json.dumps({"status": "ok", "message": f"已删除 ID: {args.id}"}, ensure_ascii=False))
            except Exception as e:
                print(json.dumps({"status": "error", "message": f"删除失败: {e}"}, ensure_ascii=False))
                sys.exit(1)
        else:
            from sentence_transformers import SentenceTransformer

            if collection.count() == 0:
                print(json.dumps({"status": "error", "message": "记忆库为空，无法搜索删除"}, ensure_ascii=False))
                sys.exit(1)

            model = SentenceTransformer(MODEL_NAME)
            embedding = model.encode([args.query]).tolist()
            results = collection.query(query_embeddings=embedding, n_results=1)

            if not results["ids"][0]:
                print(json.dumps({"status": "error", "message": "未找到匹配记忆"}, ensure_ascii=False))
                sys.exit(1)

            target_id = results["ids"][0][0]
            target_text = results["documents"][0][0]
            collection.delete(ids=[target_id])
            print(json.dumps({
                "status": "ok",
                "message": f"已删除最匹配的记忆",
                "deleted_id": target_id,
                "deleted_text": target_text,
            }, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}, ensure_ascii=False))
        sys.exit(1)


if __name__ == "__main__":
    main()
