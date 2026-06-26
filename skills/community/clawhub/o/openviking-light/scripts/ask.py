#!/usr/bin/env python3
"""
轻量 RAG - 检索 + 生成回答（BM25 检索 + MiniMax LLM）
用法: python3 ask.py --query "问题" --limit 5

BM25 检索（纯本地，无需 API），LLM 调用 MiniMax（M2.7）
"""
import argparse
import json
import math
import os
import sys
import urllib.request
import urllib.error
from collections import Counter
from pathlib import Path

try:
    import jieba
except ImportError:
    print("正在安装 jieba 分词器...")
    os.system(f"{sys.executable} -m pip install jieba -q")
    import jieba

DATA_FILE = Path.home() / ".openviking/light/data/bm25_store.json"

# MiniMax LLM 配置
MINIMAX_API_HOST = os.environ.get("MINIMAX_API_HOST", "https://api.minimaxi.com")
MINIMAX_API_KEY  = os.environ.get("MINIMAX_API_KEY", "")
CHAT_API = f"{MINIMAX_API_HOST}/v1/chat/completions"


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


# ─── MiniMax LLM ──────────────────────────────────────────────────────────────

def chat(prompt, model="MiniMax-M2.7"):
    if not MINIMAX_API_KEY:
        raise Exception("需要设置 MINIMAX_API_KEY 环境变量")

    body = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 2048,
        "temperature": 0.3
    }).encode("utf-8")
    req = urllib.request.Request(
        CHAT_API, data=body,
        headers={
            "Authorization": f"Bearer {MINIMAX_API_KEY}",
            "Content-Type": "application/json"
        },
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            result = json.loads(resp.read())
            if "choices" not in result:
                raise RuntimeError(f"Chat failed: {result}")
            return result["choices"][0]["message"]["content"]
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"Chat error {e.code}: {e.read().decode()}")


# ─── 主逻辑 ───────────────────────────────────────────────────────────────────

def load_store():
    if DATA_FILE.exists():
        with open(DATA_FILE) as f:
            return json.load(f)
    return {"items": []}

def main():
    parser = argparse.ArgumentParser(description="RAG 问答（BM25 + MiniMax）")
    parser.add_argument("--query", "-q", required=True, help="查询内容")
    parser.add_argument("--limit", "-l", type=int, default=5, help="参考条数")
    parser.add_argument("--threshold", type=float, default=0.0, help="最低相关度")
    parser.add_argument("--json", action="store_true", help="JSON输出")
    args = parser.parse_args()

    store = load_store()
    items = store.get("items", [])

    if not items:
        print("📭 知识库为空，请先添加内容: python3 bm25.py add --content '内容'")
        sys.exit(0)

    print(f"🔍 正在检索相关知识...", flush=True)
    bm25 = BM25()
    bm25.index(items)
    results = bm25.search(args.query, top_k=args.limit, min_score=args.threshold)

    if not results:
        print("❌ 未找到相关结果")
        sys.exit(0)

    # 构建上下文
    context_parts = []
    for s, item in results:
        context_parts.append(f"[参考 {len(context_parts)+1}] (相关度 {s:.2f})\n{item['content']}")
    context = "\n\n".join(context_parts)

    if args.json:
        print(json.dumps({
            "query": args.query,
            "results": [{"title": i["title"], "content": i["content"], "score": round(s, 4)} for s, i in results],
            "answer": None
        }, ensure_ascii=False, indent=2))
        return

    # 构造 prompt
    prompt = f"""你是一个助手，基于以下参考知识回答用户问题。

=== 参考知识 ===
{context}

=== 用户问题 ===
{args.query}

=== 回答要求 ===
1. 基于参考知识回答，不要编造
2. 如果参考知识不足以回答，坦诚说明
3. 回答要简洁、有条理，适当引用参考编号

回答："""

    print(f"🤖 正在生成回答...\n")
    try:
        answer = chat(prompt)
        print(answer)
    except Exception as e:
        print(f"❌ 生成失败: {e}")
        print("\n--- 检索到的参考内容 ---")
        for s, item in results:
            print(f"\n📄 [{item['title']}] (相关度 {s:.2f})")
            print(item["content"][:300])

if __name__ == "__main__":
    main()
