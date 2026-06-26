#!/usr/bin/env python3
"""
轻量 RAG - 添加文档到知识库（BM25 存储，无需 embedding API）
用法: python3 store.py --content "文本内容" --title "标题"

数据存储到 ~/.openviking/light/data/bm25_store.json（无向量，纯文本）
"""
import argparse
import json
import os
import sys
import uuid
import time
from pathlib import Path

DATA_DIR = Path.home() / ".openviking/light/data"
DATA_FILE = DATA_DIR / "bm25_store.json"

def load_store():
    if DATA_FILE.exists():
        with open(DATA_FILE) as f:
            return json.load(f)
    return {"items": []}

def save_store(store):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(store, f, ensure_ascii=False, indent=2)

def main():
    parser = argparse.ArgumentParser(description="添加内容到知识库（BM25 检索）")
    parser.add_argument("--content", "-c", required=True, help="内容文本")
    parser.add_argument("--title", "-t", default=None, help="标题（可选）")
    parser.add_argument("--level", default="L2", help="知识层级 L0/L1/L2")
    args = parser.parse_args()

    content = args.content.strip()
    if not content:
        print("❌ 内容不能为空")
        sys.exit(1)

    title = args.title or content[:50]
    item_id = str(uuid.uuid4())[:8]

    item = {
        "id": item_id,
        "title": title,
        "content": content,
        "level": args.level,
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S")
    }

    store = load_store()
    store["items"].append(item)
    save_store(store)

    print(f"✅ 已添加: [{item_id}] {title}")
    print(f"   层级: {args.level} | 当前知识库共 {len(store['items'])} 条记录")

if __name__ == "__main__":
    main()
