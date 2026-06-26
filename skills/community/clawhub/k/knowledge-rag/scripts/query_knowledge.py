#!/usr/bin/env python3
"""
query_knowledge.py — 知识仓库搜索

用法：
  .venv/bin/python3 scripts/query_knowledge.py "你的问题"
  .venv/bin/python3 scripts/query_knowledge.py "你的问题" --source bilibili
  .venv/bin/python3 scripts/query_knowledge.py "你的问题" --top 10
  .venv/bin/python3 scripts/query_knowledge.py --stats
"""

import os, sys, json, sqlite3
import numpy as np
import requests

RAG_DIR = os.path.expanduser("~/workspace/knowledge/.rag_data")
OLLAMA_URL = "http://localhost:11434/api/embeddings"
EMBED_MODEL = "qwen3-embedding:0.6b"
TOP_K = 10
SCORE_THRESHOLD = 0.5

QUERY_EXPANSION = {
    "烹饪": ["烘焙", "红烧", "食谱", "做菜", "食材", "蛋糕", "面包", "炖", "炒", "煮", "煎", "炸", "烤", "五花肉", "厨房", "烤箱", "菜谱", "家常菜", "甜品", "煲汤"],
    "编程": ["代码", "开发", "程序员", "写代码", "脚本", "算法", "函数", "编程语言", "调试", "部署"],
    "旅行": ["旅游", "攻略", "景点", "机票", "酒店", "行程"],
    "健身": ["运动", "锻炼", "跑步", "健身房", "有氧", "力量训练", "减脂", "增肌"],
    "理财": ["投资", "股票", "基金", "理财", "存款", "保险", "财务"],
}

CONFIG_FILE = os.path.expanduser("~/workspace/knowledge/.knowledge-config.json")
MODEL_META_FILE = os.path.join(RAG_DIR, "model_meta.json")


class IndexNotFoundError(Exception):
    pass


class ModelMismatchError(Exception):
    pass


def _get_config():
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def get_embed_model():
    cfg = _get_config()
    return cfg.get("embed_model", EMBED_MODEL)


def save_model_meta(model_name, dim):
    os.makedirs(RAG_DIR, exist_ok=True)
    with open(MODEL_META_FILE, "w", encoding="utf-8") as f:
        json.dump({"model": model_name, "dim": dim}, f)


def load_index():
    db_path = os.path.join(RAG_DIR, "chunks.db")
    if not os.path.exists(db_path):
        raise IndexNotFoundError("索引不存在，请先运行 index_knowledge.py")

    current_model = get_embed_model()
    stored_model = None
    stored_dim = None

    if os.path.exists(MODEL_META_FILE):
        with open(MODEL_META_FILE, "r", encoding="utf-8") as f:
            meta = json.load(f)
        stored_model = meta.get("model")
        stored_dim = meta.get("dim")

    if stored_model is None or stored_dim is None:
        conn = sqlite3.connect(db_path)
        cursor = conn.execute("SELECT vector FROM chunks LIMIT 1")
        row = cursor.fetchone()
        if row:
            stored_dim = len(np.frombuffer(row[0], dtype=np.float32))
            stored_model = current_model
            save_model_meta(current_model, stored_dim)
        conn.close()

    if stored_model != current_model:
        raise ModelMismatchError(
            f"Embedding 模型不匹配！\n"
            f"  索引构建时使用: {stored_model} ({stored_dim}维)\n"
            f"  当前配置模型:   {current_model}\n"
            f"  请到「管理」页面点击「重新索引」来重建索引"
        )

    conn = sqlite3.connect(db_path)
    rows = conn.execute(
        "SELECT id, text, title, author, date, bvid, source_type, source_label, filename, chunk_index, hash, vector "
        "FROM chunks ORDER BY rowid"
    ).fetchall()
    conn.close()

    if not rows:
        raise IndexNotFoundError("索引为空")

    chunks = []
    vectors_list = []
    for r in rows:
        chunks.append({
            "id": r[0],
            "text": r[1],
            "title": r[2],
            "author": r[3],
            "date": r[4],
            "bvid": r[5],
            "source_type": r[6],
            "source_label": r[7],
            "filename": r[8],
            "chunk_index": r[9],
            "hash": r[10],
        })
        vectors_list.append(np.frombuffer(r[11], dtype=np.float32))

    vectors = np.array(vectors_list, dtype=np.float32)
    return chunks, vectors


def embed(text):
    resp = requests.post(OLLAMA_URL, json={
        "model": get_embed_model(), "prompt": text,
    }, timeout=30)
    resp.raise_for_status()
    return np.array(resp.json()["embedding"], dtype=np.float32)


def search(query, top_k=TOP_K, source=None, author=None):
    chunks, vectors = load_index()
    qvec = embed(query)

    dots = np.dot(vectors, qvec)
    norms = np.linalg.norm(vectors, axis=1) * np.linalg.norm(qvec)
    vec_scores = dots / np.clip(norms, 1e-10, None)

    query_lower = query.lower()
    query_words = [w for w in query_lower.split() if len(w) > 1]
    expanded_words = list(query_words)
    for word in query_words:
        if word in QUERY_EXPANSION:
            expanded_words.extend(QUERY_EXPANSION[word])

    hybrid_scores = np.zeros(len(chunks), dtype=np.float64)
    for i, chunk in enumerate(chunks):
        vs = float(vec_scores[i])
        bonus = 0.0
        if expanded_words:
            text_lower = chunk.get("text", "").lower()
            title_lower = chunk.get("title", "").lower()
            for word in expanded_words:
                if word in title_lower:
                    bonus += 0.25
                elif word in text_lower:
                    bonus += 0.15
        hybrid_scores[i] = vs + bonus

    indices = np.argsort(hybrid_scores)[::-1]
    results = []
    for idx in indices:
        chunk = chunks[idx]
        score = float(hybrid_scores[idx])
        if score < SCORE_THRESHOLD:
            break
        if source and chunk.get("source_label") != source:
            continue
        if author and author not in chunk.get("author", ""):
            continue
        results.append((score, chunk))
        if len(results) >= top_k:
            break

    return results


def show_stats():
    db_path = os.path.join(RAG_DIR, "chunks.db")
    if not os.path.exists(db_path):
        print("📊 知识仓库索引统计")
        print("   总段落数: 0")
        return
    conn = sqlite3.connect(db_path)
    cursor = conn.execute("SELECT source_label, COUNT(*) FROM chunks GROUP BY source_label")
    sources = dict(cursor.fetchall())
    total = sum(sources.values())
    conn.close()
    print(f"📊 知识仓库索引统计")
    print(f"   总段落数: {total}")
    for s, n in sorted(sources.items()):
        print(f"   {s}: {n} 段")


if __name__ == "__main__":
    args = sys.argv[1:]
    source = None
    top_k = TOP_K
    author = None
    show_stats_flag = False
    json_output = False
    query_parts = []
    i = 0
    while i < len(args):
        if args[i] == "--source" and i + 1 < len(args):
            source = args[i + 1]
            i += 2
        elif args[i] == "--top" and i + 1 < len(args):
            top_k = int(args[i + 1])
            i += 2
        elif args[i] == "--author" and i + 1 < len(args):
            author = args[i + 1]
            i += 2
        elif args[i] == "--stats":
            show_stats_flag = True
            i += 1
        elif args[i] == "--json":
            json_output = True
            i += 1
        else:
            query_parts.append(args[i])
            i += 1

    query = " ".join(query_parts) if query_parts else None

    if show_stats_flag:
        if json_output:
            db_path = os.path.join(RAG_DIR, "chunks.db")
            if os.path.exists(db_path):
                conn = sqlite3.connect(db_path)
                cursor = conn.execute("SELECT source_label, COUNT(*) FROM chunks GROUP BY source_label")
                sources = dict(cursor.fetchall())
                total = sum(sources.values())
                conn.close()
            else:
                sources = {}
                total = 0
            print(json.dumps({
                "total_chunks": total,
                "source_stats": sources,
            }, ensure_ascii=False))
        else:
            show_stats()
    elif not query:
        print("用法:")
        print("  .venv/bin/python3 scripts/query_knowledge.py '你的问题'")
        print("  .venv/bin/python3 scripts/query_knowledge.py '你的问题' --source bilibili")
        print("  .venv/bin/python3 scripts/query_knowledge.py '你的问题' --author 付鹏")
        print("  .venv/bin/python3 scripts/query_knowledge.py '你的问题' --top 10")
        print("  .venv/bin/python3 scripts/query_knowledge.py --stats")
        print("  .venv/bin/python3 scripts/query_knowledge.py --stats --json")
    else:
        results = search(query, top_k=top_k, source=source, author=author)
        if json_output:
            out = []
            for score, c in results:
                out.append({
                    "title": c.get("title", ""),
                    "author": c.get("author", ""),
                    "date": c.get("date", ""),
                    "bvid": c.get("bvid", ""),
                    "source_type": c.get("source_type", ""),
                    "source_label": c.get("source_label", ""),
                    "text": c["text"],
                    "score": round(float(score), 3),
                })
            print(json.dumps({"results": out}, ensure_ascii=False))
        elif not results:
            print("😴 没有找到相关结果")
        else:
            print(f"🔍 搜索: {query}\n")
            for i, (score, c) in enumerate(results):
                icon = {"bilibili": "📹", "note": "📚", "wechat": "📱", "other": "📄"}
                ico = icon.get(c.get("source_type", "other"), "📄")
                print(f"{'='*60}")
                print(f"  [{i+1}] 相似度: {score:.3f}")
                print(f"  {ico} {c.get('title','')}")
                print(f"  来源: {c.get('source_label','')}", end="")
                if c.get("author"): print(f"  👤 {c['author']}", end="")
                if c.get("date"): print(f"  📅 {c['date']}", end="")
                print()
                text = c["text"]
                if len(text) > 300: text = text[:300] + "..."
                print(f"\n  {text}\n")
            print(f"📊 共 {len(results)} 条结果")
