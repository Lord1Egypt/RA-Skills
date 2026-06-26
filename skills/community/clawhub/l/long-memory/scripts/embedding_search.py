#!/usr/bin/env python3
"""Embedding 向量搜索：真正的语义理解，不靠关键词匹配

使用 sentence-transformers 的 all-MiniLM-L6-v2 模型（免费、本地、80MB）
安装：pip install sentence-transformers
"""

import argparse
import json
import os
import re
from datetime import datetime, timedelta
from pathlib import Path

DEFAULT_MEMORY_DIR = Path.home() / ".openclaw" / "workspace" / "memory"
EMBEDDING_CACHE = ".embeddings.json"
MODEL_NAME = "all-MiniLM-L6-v2"

# 全局模型实例（懒加载）
_model = None
_vectorizer = None


def get_model():
    """懒加载 Embedding 模型"""
    global _model
    if _model is None:
        try:
            from sentence_transformers import SentenceTransformer
            print(f"📦 加载 Embedding 模型: {MODEL_NAME}（首次需下载，约80MB）")
            _model = SentenceTransformer(MODEL_NAME)
            print("✅ 模型加载完成")
        except ImportError:
            print("❌ 需要安装 sentence-transformers:")
            print("   pip install sentence-transformers")
            exit(1)
    return _model


def encode_texts(texts: list[str], batch_size: int = 32) -> list[list[float]]:
    """编码文本为向量"""
    model = get_model()
    embeddings = model.encode(texts, batch_size=batch_size, show_progress_bar=False,
                              normalize_embeddings=True)
    return [e.tolist() for e in embeddings]


def encode_query(text: str) -> list[float]:
    """编码查询"""
    model = get_model()
    embedding = model.encode(text, normalize_embeddings=True)
    return embedding.tolist()


def cosine_similarity(a: list[float], b: list[float]) -> float:
    """计算余弦相似度"""
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = sum(x ** 2 for x in a) ** 0.5
    norm_b = sum(x ** 2 for x in b) ** 0.5
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def build_embedding_index(memory_dir: Path) -> dict:
    """构建 Embedding 索引"""
    conv_dir = memory_dir / "conversations"
    if not conv_dir.exists():
        return {"documents": [], "model": MODEL_NAME}

    # 收集所有文档片段（按 session 分段）
    documents = []
    for fp in sorted(conv_dir.glob("*.md")):
        content = fp.read_text(encoding="utf-8")
        sections = re.split(r'(?=## \[)', content)
        for section in sections:
            if not section.strip() or len(section.strip()) < 20:
                continue
            time_match = re.search(r'\[(\d{2}:\d{2})\]', section)
            topic_match = re.search(r'###\s*话题[：:]\s*(.+)', section)
            tag_match = re.search(r'\*\*标签[：:]\*\*\s*(.+)', section)

            # 提取用户消息作为文档内容
            user_msgs = re.findall(r'\*\*用户[：:]\*\*\s*(.+)', section)
            doc_text = " ".join(user_msgs) if user_msgs else section.strip()[:500]

            documents.append({
                "date": fp.stem,
                "time": time_match.group(1) if time_match else "00:00",
                "topic": topic_match.group(1).strip() if topic_match else "",
                "tags": [t.strip() for t in tag_match.group(1).split("，") if t.strip()] if tag_match else [],
                "text": doc_text,
                "embedding": None,
            })

    if not documents:
        return {"documents": [], "model": MODEL_NAME}

    # 批量编码
    print(f"🔄 编码 {len(documents)} 个文档片段...")
    texts = [d["text"] for d in documents]
    embeddings = encode_texts(texts)

    for doc, emb in zip(documents, embeddings):
        doc["embedding"] = emb

    return {
        "documents": documents,
        "model": MODEL_NAME,
        "built": datetime.now().isoformat(),
        "count": len(documents),
    }


def save_index(index: dict, memory_dir: Path):
    """保存索引"""
    cache_path = memory_dir / EMBEDDING_CACHE
    # 不保存向量到 JSON（太大），单独存
    vectors = []
    for doc in index["documents"]:
        vectors.append(doc.pop("embedding", None))

    meta = {"documents": index["documents"], "model": index["model"],
            "built": index["built"], "count": index["count"]}

    # 向量单独存为二进制
    import struct
    vec_path = memory_dir / ".embeddings.bin"
    with open(vec_path, "wb") as f:
        for vec in vectors:
            packed = struct.pack(f'{len(vec)}f', *vec)
            f.write(packed)

    meta["vector_file"] = ".embeddings.bin"
    meta["vector_dims"] = len(vectors[0]) if vectors else 0
    cache_path.write_text(json.dumps(meta, ensure_ascii=False), encoding="utf-8")
    print(f"✅ 索引已保存（{len(vectors)} 向量，{cache_path.stat().st_size / 1024:.1f} KB）")


def load_index(memory_dir: Path) -> dict:
    """加载索引"""
    import struct
    cache_path = memory_dir / EMBEDDING_CACHE
    vec_path = memory_dir / ".embeddings.bin"

    if not cache_path.exists() or not vec_path.exists():
        return None

    meta = json.loads(cache_path.read_text(encoding="utf-8"))
    dims = meta.get("vector_dims", 384)

    with open(vec_path, "rb") as f:
        data = f.read()

    vec_size = dims * 4  # float32 = 4 bytes
    num_vecs = len(data) // vec_size
    vectors = []
    for i in range(num_vecs):
        offset = i * vec_size
        vec = list(struct.unpack(f'{dims}f', data[offset:offset + vec_size]))
        vectors.append(vec)

    for i, doc in enumerate(meta["documents"]):
        if i < len(vectors):
            doc["embedding"] = vectors[i]

    return meta


def search_embeddings(memory_dir: Path, query: str, top_n: int = 10,
                      topic: str = None, tag: str = None,
                      days: int = None) -> list[dict]:
    """向量语义搜索"""
    # 加载索引
    index = load_index(memory_dir)
    if index is None:
        print("🔄 首次使用，构建索引中...")
        index = build_embedding_index(memory_dir)
        save_index(index, memory_dir)
        # 重新加载
        index = load_index(memory_dir)

    # 编码查询
    query_vec = encode_query(query)

    # 计算相似度
    cutoff = datetime.now() - timedelta(days=days) if days else None

    results = []
    for doc in index["documents"]:
        # 过滤
        if cutoff and doc["date"] < cutoff.strftime("%Y-%m-%d"):
            continue
        if topic and topic.lower() not in doc.get("topic", "").lower():
            continue
        if tag and not any(tag.lower() in t.lower() for t in doc.get("tags", [])):
            continue

        if doc.get("embedding"):
            sim = cosine_similarity(query_vec, doc["embedding"])
            if sim > 0.1:
                results.append({
                    "date": doc["date"],
                    "time": doc["time"],
                    "topic": doc["topic"],
                    "tags": doc["tags"],
                    "score": round(sim, 4),
                    "text": doc["text"][:200],
                })

    results.sort(key=lambda x: -x["score"])
    return results[:top_n]


def print_results(results: list[dict]):
    if not results:
        print("📭 未找到语义相关的记忆")
        return

    print(f"🧠 语义搜索（{len(results)} 条结果）\n")
    for i, r in enumerate(results, 1):
        score_bar = "█" * int(r["score"] * 40)
        print(f"  [{i}] {r['date']} [{r['time']}] {r['score']:.4f} |{score_bar}")
        if r["topic"]:
            print(f"      话题: {r['topic']}")
        if r["tags"]:
            print(f"      标签: {', '.join(r['tags'])}")
        print(f"      内容: {r['text'][:80]}...")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Embedding 向量语义搜索")
    sub = p.add_subparsers(dest="command")

    search_cmd = sub.add_parser("search", help="语义搜索")
    search_cmd.add_argument("query", help="自然语言查询")
    search_cmd.add_argument("--memory-dir", default=None)
    search_cmd.add_argument("--top", type=int, default=10)
    search_cmd.add_argument("-t", "--topic", default=None)
    search_cmd.add_argument("--tag", default=None)
    search_cmd.add_argument("--days", type=int, default=None)

    build_cmd = sub.add_parser("build", help="构建索引")
    build_cmd.add_argument("--memory-dir", default=None)

    args = p.parse_args()
    md = args.memory_dir if args.memory_dir else DEFAULT_MEMORY_DIR
    md = Path(md)

    if args.command == "build":
        index = build_embedding_index(md)
        save_index(index, md)
    elif args.command == "search":
        results = search_embeddings(md, args.query, args.top, args.topic, args.tag, args.days)
        print_results(results)
    else:
        p.print_help()
