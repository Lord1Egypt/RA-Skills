#!/usr/bin/env python3
"""
轻量 RAG - 全文搜索（BM25 检索，纯本地，无需任何外部 API）
用法: python3 search.py --query "查询内容" --limit 5
"""
import argparse
import json
import math
import os
import sys
from collections import Counter
from pathlib import Path

try:
    import jieba
except ImportError:
    print("正在安装 jieba 分词器...")
    os.system(f"{sys.executable} -m pip install jieba -q")
    import jieba

DATA_FILE = Path.home() / ".openviking/light/data/bm25_store.json"


# ─── BM25 检索器 ──────────────────────────────────────────────────────────────

class BM25:
    def __init__(self, k1=1.5, b=0.75):
        self.k1 = k1
        self.b = b
        self.corpus = []
        self.tokenized_corpus = []
        self.avgdl = 0
        self.idf = {}
        self.doc_lens = []

    def index(self, documents):
        self.corpus = documents
        N = len(documents)
        self.doc_lens = []
        for doc in documents:
            tokens = list(jieba.cut(doc["content"]))
            self.tokenized_corpus.append(tokens)
            self.doc_lens.append(len(tokens))
        self.avgdl = sum(self.doc_lens) / max(N, 1)
        df = {}
        for tokens in self.tokenized_corpus:
            for t in set(tokens):
                df[t] = df.get(t, 0) + 1
        for t, df_t in df.items():
            self.idf[t] = math.log((N - df_t + 0.5) / (df_t + 0.5) + 1)

    def score(self, query, doc_idx):
        tokens = list(jieba.cut(query))
        doc_tokens = self.tokenized_corpus[doc_idx]
        doc_len = self.doc_lens[doc_idx]
        tf_doc = Counter(doc_tokens)
        score = 0.0
        for token in tokens:
            if token not in self.idf:
                continue
            tf_q = tokens.count(token)
            idf = self.idf[token]
            tf_doc_t = tf_doc.get(token, 0)
            numerator = idf * tf_q * (self.k1 + 1) * tf_doc_t
            denominator = tf_q * (self.k1 * (1 - self.b + self.b * doc_len / self.avgdl)) + tf_doc_t
            score += numerator / max(denominator, 1e-10)
        return score

    def search(self, query, top_k=5, min_score=0.0):
        scores = []
        for i in range(len(self.corpus)):
            s = self.score(query, i)
            if s >= min_score:
                scores.append((s, i))
        scores.sort(key=lambda x: x[0], reverse=True)
        return [(s, self.corpus[i]) for s, i in scores[:top_k]]


# ─── 主逻辑 ───────────────────────────────────────────────────────────────────

def load_store():
    if DATA_FILE.exists():
        with open(DATA_FILE) as f:
            return json.load(f)
    return {"items": []}

def main():
    parser = argparse.ArgumentParser(description="BM25 全文搜索（纯本地，无需 API）")
    parser.add_argument("--query", "-q", required=True, help="查询内容")
    parser.add_argument("--limit", "-l", type=int, default=5, help="返回数量")
    parser.add_argument("--threshold", "-t", type=float, default=0.0, help="最低相关度阈值")
    parser.add_argument("--json", action="store_true", help="JSON输出")
    args = parser.parse_args()

    store = load_store()
    items = store.get("items", [])

    if not items:
        print("📭 知识库为空，请先添加内容")
        print("   用法: python3 bm25.py add --content '你的内容'")
        sys.exit(0)

    print(f"🔍 正在搜索: {args.query}")
    bm25 = BM25()
    bm25.index(items)
    results = bm25.search(args.query, top_k=args.limit, min_score=args.threshold)

    if not results:
        print("❌ 未找到相关结果，尝试降低阈值（--threshold 0）")
        sys.exit(0)

    if args.json:
        output = [{
            "id": item["id"],
            "title": item["title"],
            "content": item["content"],
            "level": item["level"],
            "score": round(s, 4),
            "created_at": item["created_at"]
        } for s, item in results]
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        print(f"\n📊 找到 {len(results)} 条相关结果:\n")
        for s, item in results:
            bar = "█" * int(s / max(results[0][0], 0.01) * 10) + "░" * (10 - int(s / max(results[0][0], 0.01) * 10))
            print(f"  [{bar}] {s:.2f}")
            print(f"  📌 {item['title']} [{item['level']}] ({item['created_at']})")
            print(f"  📄 {item['content'][:150]}{'...' if len(item['content']) > 150 else ''}")
            print()

if __name__ == "__main__":
    main()
