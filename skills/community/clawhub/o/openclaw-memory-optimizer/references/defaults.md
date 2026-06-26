# OpenClaw Memory Search 默认参数详解

## OpenClaw 4.2 内置默认值（src/agents/memory-search.ts）

```typescript
DEFAULT_CHUNK_TOKENS = 400
DEFAULT_CHUNK_OVERLAP = 80
DEFAULT_WATCH_DEBOUNCE_MS = 1500
DEFAULT_SESSION_DELTA_BYTES = 1e5          // 100KB
DEFAULT_SESSION_DELTA_MESSAGES = 50
DEFAULT_MAX_RESULTS = 6
DEFAULT_MIN_SCORE = 0.35
DEFAULT_HYBRID_ENABLED = true
DEFAULT_HYBRID_VECTOR_WEIGHT = 0.7
DEFAULT_HYBRID_TEXT_WEIGHT = 0.3
DEFAULT_HYBRID_CANDIDATE_MULTIPLIER = 4
DEFAULT_MMR_ENABLED = false              // 默认关闭！
DEFAULT_MMR_LAMBDA = 0.7
DEFAULT_TEMPORAL_DECAY_ENABLED = false   // 默认关闭！
DEFAULT_TEMPORAL_DECAY_HALF_LIFE_DAYS = 30
DEFAULT_CACHE_ENABLED = true
```

## 参数含义与调优建议

### maxResults
- 控制每次搜索返回的记忆条数
- 6 条太少，容易漏掉相关记忆
- 建议 10-15，召回率提升明显

### minScore
- 向量相似度最低阈值（0-1）
- 0.35 太宽松，可能返回不相关内容
- 建议 0.20-0.30

### MMR（Maximal Marginal Relevance）
- 作用：避免返回高度相似的多条记忆，提升多样性
- `lambda` 参数：0=纯多样化，1=纯相关性
- 建议 `lambda=0.60-0.65`，平衡相关性与多样性

### Temporal Decay（时间衰减）
- 作用：越老的记忆权重越低，减少过时信息干扰
- `halfLifeDays`：记忆权重衰减到一半的天数
- 建议 `halfLifeDays=14`，更重视近期记忆

### sessionDeltaMessages
- 每多少条消息同步一次 session 记忆到向量库
- 50 太慢，长会话中早期关键上下文可能丢失
- 建议 10-15

### sessionDeltaBytes
- 每多少字节同步一次
- 100KB 过高，短对话可能永远达不到
- 建议 20-50KB

## 与 Claude Code 的对比

Claude Code 用的是 cosine similarity + 小模型 relevance scoring，没有向量库，但：
- 记忆新鲜度有明确提示（memoryFreshnessText）
- 每次压缩前先验证记忆有效性
- topic file 只读 frontmatter（前30行），不全文读

OpenClaw 有 LanceDB 向量库，架构更先进，但默认配置保守。
