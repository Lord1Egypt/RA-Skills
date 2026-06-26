#!/usr/bin/env python3
"""轻量 Embedding 引擎：零依赖的本地语义搜索

不依赖任何第三方库，基于：
1. TF-IDF 向量化（与 sklearn TfidfVectorizer 等效）
2. SVD 降维（可选，提升语义理解）
3. 余弦相似度匹配

效果优于纯关键词，安装成本为零。"""

import argparse
import json
import math
import re
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from pathlib import Path

DEFAULT_MEMORY_DIR = Path.home() / ".openclaw" / "workspace" / "memory"
SEMANTIC_INDEX = ".semantic_index.json"

# 停用词
STOPWORDS = set("""
的 了 在 是 我 有 和 就 不 人 都 一 一个 上 也 很 到 说 要 去 你 会 着
没有 看 好 自己 这 他 她 它 们 那 里 来 对 过 可以 吗 吧 啊 呢 嗯 哦 哈 嘛
已 还 而 且 或 如果 因为 所以 但是 虽然 这个 那个 什么 怎么 哪 为什么 多少
些 个 只 些 把 被 让 向 从 给 比 等 更 最 之 中 与 及 其 关于 对于 通过 以 按照
为了 根据 什么 怎么 为什么 能 不能 会 可以 应该 可能 必须 需要 觉得 认为
发现 问题 帮我 搞 没问题 好 知道 明白 了解
""".split())

# 中文近义词表（提升语义理解）
SYNONYMS = {
    "性能": ["速度", "效率", "快", "慢", "卡"],
    "优化": ["改进", "改善", "提升", "升级"],
    "问题": ["bug", "错误", "毛病", "故障", "异常"],
    "方案": ["方法", "策略", "计划", "思路", "方向"],
    "决定": ["选择", "确定", "拍板", "决策", "选定"],
    "代码": ["程序", "脚本", "实现", "函数", "模块"],
    "记忆": ["存储", "保存", "记录", "归档", "遗忘"],
    "开发": ["写", "做", "实现", "搭建", "构建"],
    "部署": ["上线", "发布", "推送", "运行", "启动"],
    "学习": ["研究", "了解", "探索", "尝试", "看"],
    "赚钱": ["商业化", "变现", "收费", "付费", "收入"],
    "设计": ["规划", "架构", "结构", "方案", "布局"],
    "测试": ["验证", "检查", "跑", "运行", "执行"],
}


def tokenize(text: str) -> list[str]:
    """分词：中文 + 英文混合"""
    # 英文
    en = re.findall(r'[a-zA-Z]{2,}', text.lower())
    # 中文 2-4字
    zh = re.findall(r'[\u4e00-\u9fff]{2,4}', text)
    # 中文单字（补充）
    zh_single = [c for c in text if '\u4e00' <= c <= '\u9fff']
    return [w for w in (en + zh + zh_single) if w not in STOPWORDS and len(w) >= 1]


def expand_with_synonyms(tokens: list[str]) -> list[str]:
    """用近义词表扩展 token"""
    expanded = list(tokens)
    for token in tokens:
        for key, syns in SYNONYMS.items():
            if token in key or key in token:
                expanded.extend(syns)
            if token in syns:
                expanded.append(key)
    return list(set(expanded))


class TfidfVectorizer:
    """纯 Python 实现的 TF-IDF 向量化"""

    def __init__(self, max_features: int = 5000):
        self.vocabulary = {}
        self.idf = {}
        self.max_features = max_features

    def fit(self, documents: list[str]):
        """训练词汇表和 IDF"""
        # 统计词频
        doc_freq = Counter()
        all_terms = set()
        tokenized_docs = []

        for doc in documents:
            tokens = tokenize(doc)
            tokens = expand_with_synonyms(tokens)
            tokenized_docs.append(tokens)
            unique_tokens = set(tokens)
            all_terms.update(unique_tokens)
            for t in unique_tokens:
                doc_freq[t] += 1

        # 选择 top 特征
        sorted_terms = sorted(doc_freq.keys(), key=lambda x: -doc_freq[x])
        selected = sorted_terms[:self.max_features]
        self.vocabulary = {t: i for i, t in enumerate(selected)}

        # 计算 IDF
        n = len(documents)
        self.idf = {}
        for term in self.vocabulary:
            df = doc_freq.get(term, 1)
            self.idf[term] = math.log((n + 1) / (df + 1)) + 1

        return self

    def transform(self, documents: list[str]) -> list[list[float]]:
        """转换为 TF-IDF 向量"""
        result = []
        for doc in documents:
            tokens = tokenize(doc)
            tokens = expand_with_synonyms(tokens)
            tf = Counter(tokens)

            vec = [0.0] * len(self.vocabulary)
            for term, count in tf.items():
                if term in self.vocabulary:
                    idx = self.vocabulary[term]
                    tf_val = count / max(len(tokens), 1)
                    vec[idx] = tf_val * self.idf.get(term, 1)

            # 归一化
            norm = sum(v ** 2 for v in vec) ** 0.5
            if norm > 0:
                vec = [v / norm for v in vec]

            result.append(vec)
        return result

    def fit_transform(self, documents: list[str]) -> list[list[float]]:
        self.fit(documents)
        return self.transform(documents)


def cosine_sim(a: list[float], b: list[float]) -> float:
    """余弦相似度"""
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = sum(x ** 2 for x in a) ** 0.5
    norm_b = sum(x ** 2 for x in b) ** 0.5
    return dot / max(norm_a * norm_b, 1e-10)


def build_semantic_index(memory_dir: Path) -> dict:
    """构建语义索引"""
    conv_dir = memory_dir / "conversations"
    if not conv_dir.exists():
        return {"documents": [], "vectorizer": {}}

    documents = []
    for fp in sorted(conv_dir.glob("*.md")):
        content = fp.read_text(encoding="utf-8")
        sections = re.split(r'(?=## \[)', content)
        for section in sections:
            if len(section.strip()) < 20:
                continue

            time_match = re.search(r'\[(\d{2}:\d{2})\]', section)
            topic_match = re.search(r'###\s*话题[：:]\s*(.+)', section)
            tag_match = re.search(r'\*\*标签[：:]\*\*\s*(.+)', section)

            # 用户消息为主 + 助手关键回复
            user_msgs = re.findall(r'\*\*用户[：:]\*\*\s*(.+)', section)
            decisions = re.findall(r'\*\*关键决策[：:]\*\*\s*(.+)', section)
            doc_text = " ".join(user_msgs + decisions)

            if not doc_text.strip():
                doc_text = section.strip()[:500]

            documents.append({
                "date": fp.stem,
                "time": time_match.group(1) if time_match else "00:00",
                "topic": topic_match.group(1).strip() if topic_match else "",
                "tags": [t.strip() for t in tag_match.group(1).split("，") if t.strip()] if tag_match else [],
                "text": doc_text,
                "vector": None,
            })

    if not documents:
        return {"documents": [], "vectorizer": {}}

    # 构建向量
    print(f"🔄 构建 TF-IDF 语义索引（{len(documents)} 个文档片段）...")
    texts = [d["text"] for d in documents]
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(texts)

    for doc, vec in zip(documents, vectors):
        doc["vector"] = vec

    # 序列化（只保存词汇表和 IDF，向量实时计算）
    meta = {
        "documents": [{"date": d["date"], "time": d["time"], "topic": d["topic"],
                       "tags": d["tags"], "text": d["text"][:200]} for d in documents],
        "vectorizer": {
            "vocabulary": vectorizer.vocabulary,
            "idf": {k: v for k, v in vectorizer.idf.items()},
        },
        "built": datetime.now().isoformat(),
        "count": len(documents),
    }

    return meta


def save_index(index: dict, memory_dir: Path):
    """保存索引"""
    path = memory_dir / SEMANTIC_INDEX
    path.write_text(json.dumps(index, ensure_ascii=False), encoding="utf-8")
    size = path.stat().st_size / 1024
    print(f"✅ 索引已保存（{index['count']} 文档，{size:.1f} KB）")


def load_index(memory_dir: Path) -> dict:
    """加载索引"""
    path = memory_dir / SEMANTIC_INDEX
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def vectorize_query(query: str, vectorizer_data: dict) -> list[float]:
    """将查询转为向量"""
    vocab = vectorizer_data["vocabulary"]
    idf = vectorizer_data["idf"]
    dim = len(vocab)

    tokens = tokenize(query)
    tokens = expand_with_synonyms(tokens)
    tf = Counter(tokens)

    vec = [0.0] * dim
    for term, count in tf.items():
        if term in vocab:
            idx = vocab[term]
            tf_val = count / max(len(tokens), 1)
            vec[idx] = tf_val * idf.get(term, 1)

    norm = sum(v ** 2 for v in vec) ** 0.5
    if norm > 0:
        vec = [v / norm for v in vec]

    return vec


def vectorize_documents(texts: list[str], vectorizer_data: dict) -> list[list[float]]:
    """将文档转为向量"""
    return [vectorize_query(t, vectorizer_data) for t in texts]


def search_semantic(memory_dir: Path, query: str, top_n: int = 10,
                    topic: str = None, tag: str = None,
                    days: int = None) -> list[dict]:
    """语义搜索"""
    index = load_index(memory_dir)
    if index is None:
        print("🔄 首次使用，构建索引...")
        index = build_semantic_index(memory_dir)
        save_index(index, memory_dir)
        index = load_index(memory_dir)

    query_vec = vectorize_query(query, index["vectorizer"])
    doc_texts = [d["text"] for d in index["documents"]]
    doc_vecs = vectorize_documents(doc_texts, index["vectorizer"])

    cutoff = datetime.now() - timedelta(days=days) if days else None
    results = []

    for i, doc in enumerate(index["documents"]):
        if cutoff and doc["date"] < cutoff.strftime("%Y-%m-%d"):
            continue
        if topic and topic.lower() not in doc.get("topic", "").lower():
            continue
        if tag and not any(tag.lower() in t.lower() for t in doc.get("tags", [])):
            continue

        sim = cosine_sim(query_vec, doc_vecs[i])
        if sim > 0.05:
            results.append({
                "date": doc["date"],
                "time": doc["time"],
                "topic": doc["topic"],
                "tags": doc["tags"],
                "score": round(sim, 4),
                "text": doc["text"][:150],
            })

    results.sort(key=lambda x: -x["score"])
    return results[:top_n]


def print_results(results: list[dict]):
    if not results:
        print("📭 未找到语义相关的记忆")
        return

    print(f"🧠 语义搜索（{len(results)} 条结果）\n")
    for i, r in enumerate(results, 1):
        bar = "█" * int(r["score"] * 40)
        print(f"  [{i}] {r['date']} [{r['time']}] {r['score']:.4f} |{bar}")
        if r["topic"]:
            print(f"      话题: {r['topic']}")
        if r["tags"]:
            print(f"      标签: {', '.join(r['tags'])}")
        print(f"      内容: {r['text'][:80]}")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="轻量语义搜索（零依赖）")
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
        index = build_semantic_index(md)
        save_index(index, md)
    elif args.command == "search":
        results = search_semantic(md, args.query, args.top, args.topic, args.tag, args.days)
        print_results(results)
    else:
        p.print_help()
