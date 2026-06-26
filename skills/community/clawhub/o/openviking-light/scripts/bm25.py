#!/usr/bin/env python3
"""
轻量 RAG - BM25 全文检索 + LLM 生成回答
纯 Python 实现，无需外部 embedding API，不下载任何模型。

BM25 算法（Elasticsearch 核心）：对文档和查询进行中文分词，
计算词频和逆文档频率，返回相关性排序结果。

依赖：pip install rank-bm25 jiayan（或其他中文分词器，或用 jieba）
"""
import argparse
import json
import math
import os
import sys
import uuid
import time
from collections import Counter
from pathlib import Path

try:
    import jieba
except ImportError:
    print("正在安装 jieba 分词器...")
    os.system(f"{sys.executable} -m pip install jieba -q")
    import jieba

DATA_DIR = Path.home() / ".openviking/light/data"
DATA_FILE = DATA_DIR / "bm25_store.json"

# MiniMax LLM 配置
MINIMAX_API_HOST = os.environ.get("MINIMAX_API_HOST", "https://api.minimaxi.com")
MINIMAX_API_KEY = os.environ.get("MINIMAX_API_KEY", "")
CHAT_API = f"{MINIMAX_API_HOST}/v1/chat/completions"


# ─── BM25 实现 ────────────────────────────────────────────────────────────────

class BM25:
    """BM25 检索器"""

    def __init__(self, k1=1.5, b=0.75):
        self.k1 = k1
        self.b = b
        self.corpus = []
        self.tokenized_corpus = []
        self.avgdl = 0
        self.doc_freqs = {}      # token -> 文档数
        self.idf = {}            # token -> IDF
        self.doc_lens = []       # 每篇文档长度

    def index(self, documents):
        """建立 BM25 索引"""
        self.corpus = documents
        N = len(documents)
        self.doc_lens = []

        for doc in documents:
            tokens = list(jieba.cut(doc["content"]))
            self.tokenized_corpus.append(tokens)
            self.doc_lens.append(len(tokens))

        self.avgdl = sum(self.doc_lens) / max(N, 1)

        # 计算文档频率
        df = {}
        for tokens in self.tokenized_corpus:
            unique_tokens = set(tokens)
            for t in unique_tokens:
                df[t] = df.get(t, 0) + 1

        # 计算 IDF
        for t, df_t in df.items():
            self.idf[t] = math.log((N - df_t + 0.5) / (df_t + 0.5) + 1)

    def score(self, query, doc_idx):
        """计算单个文档对查询的 BM25 得分"""
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
        """返回 top_k 个最相关文档"""
        scores = []
        for i in range(len(self.corpus)):
            s = self.score(query, i)
            if s >= min_score:
                scores.append((s, i))
        scores.sort(key=lambda x: x[0], reverse=True)
        return [(s, self.corpus[i]) for s, i in scores[:top_k]]


# ─── 存储 ────────────────────────────────────────────────────────────────────

def load_store():
    if DATA_FILE.exists():
        with open(DATA_FILE) as f:
            return json.load(f)
    return {"items": []}

def save_store(store):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(store, f, ensure_ascii=False, indent=2)

def chat(prompt, model="MiniMax-M2.7"):
    """使用 MiniMax API 生成回答（OpenAI-compatible 格式）"""
    import urllib.request, urllib.error

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
        error_body = e.read().decode()
        raise RuntimeError(f"Chat error {e.code}: {error_body}")


# ─── 命令 ────────────────────────────────────────────────────────────────────

def cmd_add(args):
    content = args.content.strip()
    if not content:
        print("❌ 内容不能为空")
        sys.exit(1)
    title = args.title or content[:50]
    item = {
        "id": str(uuid.uuid4())[:8],
        "title": title,
        "content": content,
        "level": args.level,
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    store = load_store()
    store["items"].append(item)
    save_store(store)
    print(f"✅ 已添加: [{item['id']}] {title}")
    print(f"   层级: {args.level} | 当前共 {len(store['items'])} 条")

def cmd_search(args):
    store = load_store()
    items = store.get("items", [])
    if not items:
        print("📭 知识库为空，请先添加内容")
        print("   用法: python3 bm25.py add --content '你的内容'")
        sys.exit(0)

    bm25 = BM25()
    bm25.index(items)
    results = bm25.search(args.query, top_k=args.limit, min_score=args.threshold)

    if not results:
        print("❌ 未找到相关结果，尝试降低阈值（--threshold 0）")
        sys.exit(0)

    if args.json:
        print(json.dumps([{"id": i["id"], "title": i["title"], "content": i["content"],
                          "level": i["level"], "score": round(s, 4)} for s, i in results], ensure_ascii=False, indent=2))
    else:
        print(f"\n📊 找到 {len(results)} 条相关结果:\n")
        for s, item in results:
            bar = "█" * int(s / max(results[0][0], 0.01) * 10) + "░" * (10 - int(s / max(results[0][0], 0.01) * 10))
            print(f"  [{bar}] {s:.2f}")
            print(f"  📌 {item['title']} [{item['level']}] ({item['created_at']})")
            print(f"  📄 {item['content'][:150]}{'...' if len(item['content']) > 150 else ''}")
            print()

def cmd_ask(args):
    store = load_store()
    items = store.get("items", [])
    if not items:
        print("📭 知识库为空，请先添加内容")
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
            "results": [{"id": i["id"], "title": i["title"], "content": i["content"], "score": round(s, 4)} for s, i in results],
            "answer": None
        }, ensure_ascii=False, indent=2))
        return

    prompt = f"""你是一个助手，基于以下参考知识回答用户问题。

=== 参考知识 ===
{context}

=== 用户问题 ===
{args.query}

=== 回答要求 ===
1. 基于参考知识回答，不要编造
2. 如果参考知识不足以回答，坦诚说明
3. 回答要简洁、有条理，适当引用参考编号"""

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

def cmd_stats(args):
    store = load_store()
    items = store.get("items", [])
    print(f"📦 知识库统计:")
    print(f"   总条目: {len(items)}")
    if items:
        levels = Counter(i["level"] for i in items)
        print(f"   层级分布: {dict(levels)}")
        print(f"   最新: {items[-1]['title']} ({items[-1]['created_at']})")


# ─── 主入口 ──────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="轻量 RAG - BM25 检索 + LLM 回答")
    sub = parser.add_subparsers(dest="cmd")

    p = sub.add_parser("add", help="添加内容")
    p.add_argument("--content", "-c", required=True, help="内容")
    p.add_argument("--title", "-t", default=None, help="标题")
    p.add_argument("--level", default="L2", help="层级")

    p = sub.add_parser("search", help="搜索")
    p.add_argument("--query", "-q", required=True, help="查询")
    p.add_argument("--limit", "-l", type=int, default=5)
    p.add_argument("--threshold", type=float, default=0.0)
    p.add_argument("--json", action="store_true")

    p = sub.add_parser("ask", help="RAG 问答")
    p.add_argument("--query", "-q", required=True)
    p.add_argument("--limit", "-l", type=int, default=5)
    p.add_argument("--threshold", type=float, default=0.0)
    p.add_argument("--json", action="store_true")

    p = sub.add_parser("stats", help="统计")

    args = parser.parse_args()

    if args.cmd == "add":
        cmd_add(args)
    elif args.cmd == "search":
        cmd_search(args)
    elif args.cmd == "ask":
        cmd_ask(args)
    elif args.cmd == "stats":
        cmd_stats(args)
    else:
        parser.print_help()
