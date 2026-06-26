# 检索 Pipeline 详解

## 1. 整体流程

```
用户查询
    ↓
┌─────────────────────────────────────────────┐
│            1. Query 解析                     │
│  - 分词                                      │
│  - 实体提取                                  │
│  - 同义词扩展（可选）                          │
└─────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────┐
│         2. 多策略并行搜索                     │
│  - FTS5 关键词搜索                            │
│  - 标签匹配搜索                              │
│  - 来源偏好搜索                              │
└─────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────┐
│         3. RRF 融合                          │
│  - 多策略结果排名融合                         │
│  - 计算综合得分                              │
└─────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────┐
│         4. 时间衰减加权                        │
│  - 越新的内容权重越高                          │
└─────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────┐
│         5. 分层加载                          │
│  - L0/L1/L2 按需加载                          │
└─────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────┐
│         6. 输出 Top-K                        │
└─────────────────────────────────────────────┘
```

## 2. Query 解析

### 2.1 分词

```bash
# 使用 FTS5 的分词器
query = "openclaw hooks 配置"
tokens = fts5_tokenize(query)
# → ["openclaw", "hooks", "配置"]
```

### 2.2 布尔搜索支持

```sql
-- AND: openclaw AND hooks
-- OR:  openclaw OR hooks  
-- NOT: openclaw NOT hooks
```

### 2.3 短语搜索

```sql
-- 匹配完整短语 "openclaw hooks"
SELECT * FROM knowledge_entries WHERE content MATCH '"openclaw hooks"';
```

## 3. 多策略搜索

### 3.1 FTS5 关键词搜索

```sql
-- 基础搜索，带权重
SELECT id, topic_key, title, content,
       bm25(knowledge_entries, 10.0, 1.0) as score
FROM knowledge_entries
WHERE knowledge_entries MATCH ?
ORDER BY score
LIMIT 100;
```

**权重配置**：
- `bm25(knowledge_entries, 10.0, 1.0)` = 标题权重 10.0，内容权重 1.0

### 3.2 标签匹配搜索

```sql
-- 查询 tags 包含关键词的记录
SELECT * FROM entries 
WHERE json_each(tags) IN (SELECT value FROM json_each(?));
```

### 3.3 来源偏好搜索

```sql
-- 优先返回同一来源的记录
SELECT *, 
       CASE WHEN source = ? THEN 1.2 ELSE 1.0 END as source_boost
FROM entries
WHERE content MATCH ?
ORDER BY source_boost DESC;
```

## 4. RRF 融合

### 4.1 公式

```
RRF_score(d) = Σ 1 / (k + rank_i(d))

其中：
- d 是文档
- k 是常数（通常 60）
- rank_i(d) 是策略 i 中文档 d 的排名
```

### 4.2 实现

```python
def rrf_fuse(results_by_strategy, k=60):
    scores = defaultdict(float)
    
    for strategy, results in results_by_strategy.items():
        for rank, doc in enumerate(results):
            doc_id = doc['id']
            scores[doc_id] += 1.0 / (k + rank)
    
    # 排序返回
    sorted_docs = sorted(scores.items(), key=lambda x: -x[1])
    return sorted_docs
```

### 4.3 k 值影响

| k 值 | 效果 |
|------|------|
| k=0 | 只看排名，不平滑 |
| k=60 | 标准值，平衡好 |
| k=120 | 重视多样性 |

## 5. 时间衰减

### 5.1 指数衰减

```
decay(d) = e^(-λ * days_ago)

其中：
- λ 是衰减因子（通常 0.1）
- days_ago 是距离今天的天数
```

### 5.2 衰减曲线

| days_ago | λ=0.1 时的权重 |
|----------|----------------|
| 0 | 1.00 |
| 7 | 0.50 |
| 14 | 0.25 |
| 30 | 0.05 |
| 90 | 0.0001 |

### 5.3 实现

```python
import math

def time_decay(created_at, lambda_param=0.1):
    days_ago = (datetime.now() - created_at).days
    return math.exp(-lambda_param * days_ago)

# 最终得分
final_score = rrf_score * time_decay(created_at)
```

## 6. 分层加载

### 6.1 L0 - 摘要层

```sql
SELECT 
  id,
  topic_key,
  title,
  substr(content, 1, 200) as summary,
  source,
  updated_at
FROM entries
WHERE ...
-- < 200 tokens
```

### 6.2 L1 - 概览层

```sql
SELECT 
  id,
  topic_key,
  title,
  content as overview,
  json_extract(metadata, '$.key_points') as key_points,
  source,
  updated_at
FROM entries
WHERE ...
-- < 1000 tokens
```

### 6.3 L2 - 详情层

```sql
SELECT 
  *,
  content
FROM entries
WHERE ...
-- 完整内容
```

## 7. MMR 多样性重排（可选）

### 7.1 公式

```
MMR = argmax [ λ * Similarity(doc, query) - (1-λ) * max Similarity(doc, already_selected) ]
```

### 7.2 用途

避免返回结果过于相似，提高多样性。

## 8. 完整流程实现

```python
def retrieve(query, limit=5, level=1, time_decay_lambda=0.1):
    # 1. Query 解析
    tokens = tokenize(query)
    
    # 2. 多策略搜索
    fts_results = fts5_search(tokens, limit=100)
    tag_results = tag_search(tokens, limit=100)
    source_results = source_search(tokens, limit=100)
    
    # 3. RRF 融合
    fused = rrf_fuse({
        'fts': fts_results,
        'tag': tag_results,
        'source': source_results
    })
    
    # 4. 时间衰减
    for doc in fused:
        doc['final_score'] = doc['score'] * time_decay(doc['created_at'])
    
    # 5. 分层加载
    loaded = load_levels(fused, level=level)
    
    # 6. Top-K
    return loaded[:limit]
```

## 9. 性能优化

### 9.1 索引优化

```sql
-- FTS 索引
CREATE VIRTUAL TABLE knowledge_entries USING fts5(...);

-- 普通索引
CREATE INDEX idx_entries_source ON entries(source);
CREATE INDEX idx_entries_created_at ON entries(created_at);
```

### 9.2 缓存策略

- 热数据（FTS 索引）常驻内存
- 查询结果缓存 5 分钟

### 9.3 限制

```sql
-- 最大返回 100 条
LIMIT 100

-- 超时 1 秒
PRAGMA query_only = 1;
PRAGMA busy_timeout = 1000;
```

## 10. 评估指标

| 指标 | 说明 |
|------|------|
| MRR@K | 平均倒数排名 |
| NDCG@K | 归一化折扣收益 |
| Recall@K | 召回率 |
| Query Time | 查询耗时 |
