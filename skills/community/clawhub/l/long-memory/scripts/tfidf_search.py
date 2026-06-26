#!/usr/bin/env python3
"""TF-IDF 语义搜索：超越关键词匹配的智能检索"""

import argparse
import json
import math
import re
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent))
from lib.filelock import safe_read

DEFAULT_MEMORY_DIR = Path.home() / ".openclaw" / "workspace" / "memory"
TFIDF_INDEX = ".tfidf_index.json"

# 中文停用词
STOPWORDS = set("""
的 了 在 是 我 有 和 就 不 人 都 一 一个 上 也 很 到 说 要 去 你 会 着 没有 看 好 
自己 这 他 她 它 们 那 里 来 对 过 可以 吗 吧 啊 呢 嗯 哦 哈 嘛 已 还 而 且 或 如果 
因为 所以 但是 虽然 这个 那个 什么 怎么 哪 为什么 多少 几 些 个 只 些 把 被 让 向 从 
给 比 等 更 最 之 中 与 及 其 关于 对于 通过 以 按照 为了 根据
""".split())

# 分词
def tokenize(text: str) -> list[str]:
    # 英文单词
    en_words = re.findall(r'[a-zA-Z]{2,}', text.lower())
    # 中文 2-4 字
    cjk_words = re.findall(r'[\u4e00-\u9fff]{2,4}', text)
    # 中文单字（补充）
    cjk_single = [c for c in text if '\u4e00' <= c <= '\u9fff']
    
    words = en_words + cjk_words + cjk_single
    return [w for w in words if w not in STOPWORDS and len(w) >= 1]


def compute_tf(tokens: list[str]) -> dict[str, float]:
    """计算词频"""
    total = len(tokens)
    if total == 0:
        return {}
    counts = Counter(tokens)
    return {word: count / total for word, count in counts.items()}


def build_tfidf_index(memory_dir: Path) -> dict:
    """构建 TF-IDF 索引"""
    conv_dir = memory_dir / "conversations"
    if not conv_dir.exists():
        return {"documents": {}, "idf": {}, "vocabulary": []}

    documents = {}
    all_doc_tokens = []

    for fp in sorted(conv_dir.glob("*.md")):
        content = fp.read_text(encoding="utf-8")
        tokens = tokenize(content)
        tf = compute_tf(tokens)
        documents[fp.stem] = {
            "tokens": tokens,
            "tf": tf,
            "topics": re.findall(r'###\s*话题[：:]\s*(.+)', content),
            "tags": list(set(t.strip() for tl in re.findall(r'\*\*标签[：:]\*\*\s*(.+)', content) for t in tl.split("，") if t.strip())),
            "size": fp.stat().st_size,
        }
        all_doc_tokens.append(set(tokens))

    # 计算 IDF
    num_docs = len(documents)
    all_terms = set()
    for doc_tokens in all_doc_tokens:
        all_terms.update(doc_tokens)

    idf = {}
    for term in all_terms:
        doc_count = sum(1 for tokens in all_doc_tokens if term in tokens)
        idf[term] = math.log((num_docs + 1) / (doc_count + 1)) + 1

    return {
        "documents": {k: {"tf": v["tf"], "topics": v["topics"], "tags": v["tags"], "size": v["size"]}
                     for k, v in documents.items()},
        "idf": idf,
        "vocabulary": sorted(all_terms),
        "num_docs": num_docs,
        "built": datetime.now().isoformat(),
    }


def cosine_similarity(vec_a: dict, vec_b: dict) -> float:
    """计算余弦相似度"""
    common_keys = set(vec_a.keys()) & set(vec_b.keys())
    if not common_keys:
        return 0.0

    dot = sum(vec_a[k] * vec_b[k] for k in common_keys)
    norm_a = math.sqrt(sum(v ** 2 for v in vec_a.values()))
    norm_b = math.sqrt(sum(v ** 2 for v in vec_b.values()))

    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def search_tfidf(memory_dir: Path, query: str, top_n: int = 10,
                 topic_filter: str | None = None, tag_filter: str | None = None,
                 days: int | None = None) -> list[dict]:

    # 加载或构建索引
    index_path = memory_dir / TFIDF_INDEX
    if index_path.exists():
        import json
        index = json.loads(index_path.read_text(encoding="utf-8"))
    else:
        index = build_tfidf_index(memory_dir)
        index_path.write_text(json.dumps(index, ensure_ascii=False), encoding="utf-8")

    # 构建查询向量
    query_tokens = tokenize(query)
    query_tf = compute_tf(query_tokens)
    query_vec = {term: query_tf.get(term, 0) * index["idf"].get(term, 1)
                 for term in set(query_tokens)}

    # 日期过滤
    cutoff = datetime.now() - timedelta(days=days) if days else None

    # 计算每个文档的相似度
    results = []
    for doc_id, doc_data in index["documents"].items():
        # 过滤
        if cutoff and doc_id < cutoff.strftime("%Y-%m-%d"):
            continue
        if topic_filter and not any(topic_filter.lower() in t.lower() for t in doc_data["topics"]):
            continue
        if tag_filter and not any(tag_filter.lower() in t.lower() for t in doc_data["tags"]):
            continue

        # 构建文档向量
        doc_vec = {term: tf * index["idf"].get(term, 1) for term, tf in doc_data["tf"].items()}

        sim = cosine_similarity(query_vec, doc_vec)
        if sim > 0.01:
            # 提取匹配的关键词
            matched = set(query_tokens) & set(doc_data["tf"].keys())
            results.append({
                "date": doc_id,
                "score": round(sim, 4),
                "matched_terms": sorted(matched),
                "topics": doc_data["topics"],
                "tags": doc_data["tags"],
            })

    results.sort(key=lambda x: -x["score"])
    return results[:top_n]


def print_results(results: list[dict]):
    if not results:
        print("📭 未找到相关记忆")
        return

    print(f"🔍 TF-IDF 语义搜索（{len(results)} 条结果）\n")
    for i, r in enumerate(results, 1):
        score_bar = "█" * int(r["score"] * 30)
        print(f"  [{i}] {r['date']}  {r['score']:.4f} |{score_bar}")
        if r["matched_terms"]:
            print(f"      匹配词: {', '.join(r['matched_terms'][:8])}")
        if r["topics"]:
            print(f"      话题: {', '.join(r['topics'][:3])}")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="TF-IDF 语义搜索")
    p.add_argument("query", help="搜索查询")
    p.add_argument("--memory-dir", default=None)
    p.add_argument("--top", type=int, default=10)
    p.add_argument("--topic", "-t", default=None)
    p.add_argument("--tag", default=None)
    p.add_argument("--days", type=int, default=None)
    p.add_argument("--rebuild", action="store_true", help="重建索引")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()

    md = args.memory_dir if args.memory_dir else DEFAULT_MEMORY_DIR
    md = Path(md)

    if args.rebuild:
        index = build_tfidf_index(md)
        import json
        (md / TFIDF_INDEX).write_text(json.dumps(index, ensure_ascii=False), encoding="utf-8")
        print(f"✅ 索引已重建（{index['num_docs']} 个文档，{len(index['vocabulary'])} 个词）")
        exit(0)

    results = search_tfidf(md, args.query, args.top, args.topic, args.tag, args.days)

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        print_results(results)
