# RAG 检索管线实现手册

> 本篇是 `rag-retrieval` 子技能的深层 playbook，聚焦**如何从零搭一条生产级检索管线**。
> 如果你的语料本身是一个 LLM Wiki（raw/wiki 双层 Markdown），应先读
> `retrieval-and-synthesis-playbook.md` 的"检索阶梯"判断能否用索引 + 全文检索解决——
> 简单检索优先，只有评测证明召回不足才上向量。两篇不重复：那篇讲"Wiki 何时升级语义检索"，
> 这篇讲"独立 RAG 后端怎么实现"。

## 1. 决策树：这条语料要不要 RAG

```text
语料 < 数百页 且 术语稳定 且 需精确字段匹配？
  ├─ 是 → 索引 + rg/全文（见 wiki retrieval playbook），不要上向量
  └─ 否 ↓
已有 ≥30–50 条代表性评测问题，可比较 Recall@K？
  ├─ 否 → 先攒评测集；没有评测就上 RAG 等于盲飞
  └─ 是 ↓
混合检索显著优于全文检索（用 eval 证明，不是看 Demo）？
  ├─ 否 → 继续用全文 + 同义词/字段索引
  └─ 是 → 进入下面的管线实现
```

**黄金法则**：向量数据库不是 Wiki 成熟度徽章。上 RAG 的成本（切块、Embedding 更新、
权限过滤、索引漂移治理）只有在召回收益被 eval 量化后才值得付。

## 2. 分块：边界决定能检索到什么

固定大小硬切会切断句子/段落语义，是最常见也最隐蔽的坑。

```python
# 按结构边界分块（推荐）：在 H2/H3/段落边界切，保留 10–20% 重叠
CHUNK_CONFIG = {
    "target_tokens": 500,      # 约 400–600 token / 块
    "max_tokens": 800,         # 硬上限
    "overlap_tokens": 75,      # 约 15% 重叠，保证边界上下文连续
    "boundary_markers": ["\n## ", "\n### ", "\n\n", ". "],  # 优先级从高到低
}

def chunk_by_sentences(text, chunk_size=512, overlap=75):
    sentences = text.split(". ")
    chunks, current, cur_len = [], [], 0
    for sent in sentences:
        if cur_len + len(sent) > chunk_size and current:
            chunks.append(". ".join(current) + ".")
            tail = current[-2:] if len(current) > 2 else current
            current, cur_len = tail, sum(len(s) for s in tail)
        else:
            current.append(sent)
            cur_len += len(sent)
    if current:
        chunks.append(". ".join(current))
    return chunks
```

**规则**：
- 块大小 256–1024 token（512 甜点）；重叠 10–20%。
- 每块必须带元数据：`title` / `source` / `section` / `updated`，检索与引用都靠它。
- 长文档不分块是错误——上下文会在 Embedding 里被稀释。

## 3. Embedding：查询与文档必须同模型

```python
# 文档入库与线上查询用同一个模型与同一个预处理
from openai import OpenAI
client = OpenAI()

def embed(texts, model="text-embedding-3-small"):
    # 批量 + 缓存：重复文本不重复调用，控制吞吐（约 120 rps 上限）
    return client.embeddings.create(model=model, input=texts).data

# 评测/小库可换 Voyage：voyage-3.5 质量更高，注意维度与向量库匹配
```

**模型选择**：`text-embedding-3-small`（便宜、够用）/ `voyage-3.5`（质量更高）。
**红线**：查询侧与文档侧必须用同一模型，否则余弦相似度无意义。

## 4. 混合检索：词法 + 语义，RRF 融合

只用向量会漏精确术语（如错误码、API 名），只用 BM25 会漏语义复述。两者用
Reciprocal Rank Fusion 融合，k=60 是经验稳健值、无需调参。

```python
def reciprocal_rank_fusion(semantic, keyword, k: int = 60):
    """semantic/keyword 各是 [(id, score)] 排名列表，返回融合后排名。"""
    scores = {}
    for rank, (doc_id, _) in enumerate(semantic):
        scores[doc_id] = scores.get(doc_id, 0) + 1 / (k + rank + 1)
    for rank, (doc_id, _) in enumerate(keyword):
        scores[doc_id] = scores.get(doc_id, 0) + 1 / (k + rank + 1)
    return sorted(scores, key=lambda x: scores[x], reverse=True)

# 多概念查询：先分解，各子查询分别检索，再用 multi-list RRF 融合
def multi_rrf(result_lists, k: int = 60):
    from collections import defaultdict
    s = defaultdict(float)
    for rl in result_lists:
        for rank, (doc_id, _) in enumerate(rl, 1):
            s[doc_id] += 1.0 / (k + rank)
    return sorted(s, key=lambda x: s[x], reverse=True)
```

**关键规则**：
- 召回倍数停 3×：取 top-30 融出 top-10 已覆盖绝大多数收益，再翻倍数收益边际递减。
- 元数据 boosting **在 RRF 之后**做：section-title 1.5×、path 1.15×、code-block 1.2×；
  前置会破坏排名融合。
- 权限过滤在检索前执行，绝不召回私有片段后再遮盖。

## 5. 重排：候选多取，精读少留

交叉编码器把 query+doc 一起编码，精度高但慢。先广召回、再窄重排。

```python
from sentence_transformers import CrossEncoder

reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L6-v2")  # ~50ms，免费

def rerank(query, docs, top_k=10, take=50):
    candidates = docs[:take]
    pairs = [(query, d["content"][:400]) for d in candidates]  # 截断提速
    scores = reranker.predict(pairs)
    ranked = sorted(zip(candidates, scores), key=lambda x: x[1], reverse=True)
    return [{**d, "score": float(s)} for d, s in ranked[:top_k]]
```

**模型梯度**：`ms-marco-MiniLM-L6-v2`（~50ms，免费）< `BAAI/bge-reranker-large`（~100ms）<
`cohere rerank-v4`（~200ms，付费，质量最佳）。默认 MiniLM 起步。

## 6. 评测：用数据定门槛，不靠感觉

上线前必须有黄金问题集与发版门槛；否则"线上漏召回"无人知晓。

```python
def recall_at_k(retrieved, relevant, k):
    return len(set(retrieved[:k]) & set(relevant)) / len(relevant)

def mrr(retrieved_lists, relevant_sets):
    total = 0.0
    for retrieved, relevant in zip(retrieved_lists, relevant_sets):
        for i, rid in enumerate(retrieved, 1):
            if rid in relevant:
                total += 1 / i
                break
    return total / len(retrieved_lists)
```

**发版门槛（示例，按语料重测）**：P@10 ≥ 0.70、R@10 ≥ 0.85、MRR ≥ 0.65。
**延迟预算**：端到端 p95 < 500ms；分阶段断言：向量 < 100ms、关键词 < 50ms、混合 < 150ms。
**测 p95 而非均值**——长尾才是用户体感。

## 7. 生成装配：引用可溯源

```python
context = "\n\n".join(
    f"[{i+1}] {doc['content']}\nSource: {doc['metadata']['source']}"
    for i, doc in enumerate(top_docs)
)
system = "用提供的上下文作答，带 [1][2] 编号引用；上下文没有就明确说没有该信息。"
```

系统提示必须强制"仅用上下文作答"，返回 sources 供透明审计。

## 8. 完成检查表

- [ ] 已用决策树确认"该语料确实需要 RAG"（有 eval 证据，而非技术偏好）
- [ ] 分块在结构边界切，带 title/source/section 元数据，重叠 10–20%
- [ ] 查询与文档用同一 Embedding 模型，嵌入已批处理 + 缓存
- [ ] 混合检索用 RRF（k=60）融合，召回 3×k，元数据 boosting 在融合之后
- [ ] 重排取候选 50 → 10，交叉编码器截断 200–400 字符
- [ ] 有黄金问题集，Recall@K / MRR / 引用正确率达发版门槛
- [ ] 延迟 p95 < 500ms，分阶段有断言
- [ ] 生成装配带 `[1]` 引用，系统提示强制仅用上下文作答
- [ ] 权限过滤在检索前执行
- [ ] 无"Demo 好看、线上漏召回"的盲区（评测覆盖召回、引用、弃答）

## 相关子技能（L3）

本手册的「RAG 检索管线」方法论由以下子技能在搭建或调优检索时调用：

- [rag-retrieval](../skills/rag-retrieval/SKILL.md) — 分块、Embedding、混合检索、重排、生成装配引用时，先读本手册 §1–§8。
