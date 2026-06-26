# HuiMemory 架构设计

## 核心设计哲学

**检索系统 = 搜索引擎，不负责语义理解和答案生成**

HuiMemory 的定位非常明确：它是一个高效的"捞数据"工具，而不是一个智能问答系统。所有的语义理解、意图推断、答案组织都交给 LLM 完成。

## 三层架构

```
┌─────────────────────────────────────────────────────────────┐
│                      LLM 层（理解+回答）                      │
│  - 意图理解：关键词提取、时间范围推断                          │
│  - 答案组织：基于检索结果生成回答                              │
│  - 追问决策：是否需要更多上下文                                │
│  - 工具调用：recall_memory / recall_by_id                    │
└─────────────────────────────────────────────────────────────┘
                              ↓ 工具调用
┌─────────────────────────────────────────────────────────────┐
│                   检索系统层（搜索引擎）                       │
│  - 关键词检索：向量相似度搜索（BGE embedding）                 │
│  - 时间过滤：metadata 范围查询（>=, <=, >, <, !=）            │
│  - 分段扫描：周步长渐进式扫描（max_weeks=16）                  │
│  - 轮次导航：prev/next 指针系统                               │
│  - 上下文窗口：自动扩展相邻轮次                                │
└─────────────────────────────────────────────────────────────┘
                              ↓ 文件读取
┌─────────────────────────────────────────────────────────────┐
│                      存储层（数据持久化）                      │
│  - 向量存储：SQLite + Faiss（本地部署）                        │
│  - 元数据索引：timestamp, turn_index, topic, session_file    │
│  - 归档管理：月包压缩（.tar.zst，72h 缓存）                    │
│  - 对话格式：Markdown + turn_id 标记                          │
└─────────────────────────────────────────────────────────────┘
```

## 核心组件

### 1. TurnChunker（轮次切分器）

**职责**：将对话文件切分为独立的轮次块

**输入**：Markdown 格式的对话文件

```markdown
[id:a3f2c7]
<user timestamp="2026-04-13T10:00:07">用户消息</user>
<assistant timestamp="2026-04-13T10:00:15">助手回复</assistant>

[id:k7f2a1]
<user timestamp="2026-04-13T10:01:20">下一个问题</user>
<assistant timestamp="2026-04-13T10:01:30">下一个回答</assistant>
```

**输出**：Chunk 列表，每个 Chunk 包含：

```python
{
    "id": "turn_text",  # 固定值（向量存储限制）
    "metadata": {
        "turn_id": "a3f2c7",
        "turn_index": 0,
        "timestamp": "2026-04-13T10:00:07",
        "weekday": "Mon",
        "session_file": "2026-W15/2026-04-13/chat_xxx.md",
        "topic": "本地模型部署",
        "text_type": "conversation",
        "text": "<user timestamp=\"...\">用户消息</user>\n<assistant timestamp=\"...\">助手回复</assistant>"
    }
}
```

### 2. Retriever（检索器）

**职责**：提供多种检索策略

**核心方法**：

#### `search(query, top_k, filter_expr, context_window, enable_progressive_scan)`

- **query**：搜索关键词
- **top_k**：返回结果数量（默认 5）
- **filter_expr**：时间过滤表达式（如 `"timestamp >= '2026-04-06'"`）
- **context_window**：上下文窗口大小（0 = 不扩展）
- **enable_progressive_scan**：是否启用分段扫描

**返回**：`List[SearchResult]`

```python
[
    SearchResult(
        id="<user timestamp=\"...\">...</user>\n<assistant timestamp=\"...\">...</assistant>",
        score=0.778,
        metadata={
            "turn_id": "a3f2c7",
            "turn_index": 0,
            "timestamp": "2026-04-13T10:00:07",
            "weekday": "Mon",
            "session_file": "2026-W15/2026-04-13/chat_xxx.md",
            "topic": "本地模型部署"
        }
    )
]
```

#### `search_with_progress(query, on_round, max_weeks)`

分段扫描版本，支持回调：

```python
results = retriever.search_with_progress(
    query="项目讨论",
    on_round=lambda week, results: print(f"扫描 {week}，找到 {len(results)} 条"),
    max_weeks=16
)
```

#### `get_turn(session_file, turn_index, context_window)`

根据 metadata 精确检索：

```python
results = retriever.get_turn(
    session_file="2026-W15/2026-04-13/chat_xxx.md",
    turn_index=5,
    context_window=2
)
```

### 3. TimeResolver（时间解析器）

**职责**：解析自然语言时间

**支持的时间格式**：

- **精确时间**："2026-04-13"、"上周三"、"昨天下午"
- **相对时间**："最近一周"、"上个月"、"前三天"
- **模糊时间**："前段时间"、"之前"

**输出**：

```python
{
    "start": "2026-04-09T12:00:00",
    "end": "2026-04-09T18:00:00",
    "is_fuzzy": False  # 是否模糊时间
}
```

### 4. ProgressiveScanner（分段扫描器）

**职责**：渐进式扫描历史对话

**扫描策略**：
- 从最近一周开始
- 每周最多返回 5 个候选
- 最多扫描 16 周（约 4 个月）
- 支持 `on_round` 回调

**核心原则**：
- Scanner 只负责"捞"候选，不做判断
- 判断交给上层 LLM

## 数据流

### 1. 索引流程

```
对话文件 → TurnChunker → Chunk 列表 → BGE Embedding → 向量 + Metadata → SQLite + Faiss
```

### 2. 检索流程

```
用户查询 → LLM 提炼关键词 → TimeResolver 解析时间
    ↓
Retriever.search(query, filter_expr)
    ↓
向量相似度搜索 + Metadata 过滤
    ↓
扩展上下文窗口（可选）
    ↓
格式化输出 → LLM 回答
```

### 3. 分段扫描流程

```
模糊时间查询 → TimeResolver 返回 is_fuzzy=True
    ↓
ProgressiveScanner 启动
    ↓
Week 1: 检索 → 返回候选 → LLM 判断
    ↓ (未命中)
Week 2: 检索 → 返回候选 → LLM 判断
    ↓ (未命中)
Week 3: 检索 → 返回候选 → LLM 判断
    ↓ (命中)
返回结果
```

## 性能指标

### 检索性能

- **向量检索**：~5-10ms（Faiss）
- **Metadata 过滤**：~1-2ms（SQLite）
- **分段扫描**：~50-100ms/周
- **上下文窗口扩展**：~5ms

### 存储效率

- **向量维度**：384（bge-small-zh-v1.5）或 1024（BGE-M3）
- **Metadata 大小**：~500 bytes/轮次
- **归档压缩率**：~70%（.tar.zst）
- **缓存 TTL**：72 小时

## 设计决策

### 为什么不用 Late Chunking？

**Late Chunking**：先对整个文档做 embedding，再切分

**问题**：
- 增加复杂度
- 破坏"检索系统 = 搜索引擎"的简单原则
- 对话场景下收益有限

**结论**：放弃，保持简单

### 为什么用周步长扫描？

**原因**：
- 与存储粒度对齐（每周文件夹）
- 平衡效率和覆盖度
- 符合用户认知习惯

### 为什么用双向链表而不是顺序编号？

**双向链表**：`[id:xxx | prev: yyy | next: zzz]`

**优势**：
- 插入/删除不影响其他节点
- 无需重新编号
- 天然支持双向导航

## 扩展点

### 1. 自定义 Embedding

```python
from huimemory.embedding import BaseEmbedding

class MyEmbedding(BaseEmbedding):
    def encode(self, texts: List[str]) -> List[List[float]]:
        # 自定义实现
        return vectors
```

### 2. 自定义 Chunker

```python
from huimemory.chunker import BaseChunker

class MyChunker(BaseChunker):
    def chunk_file(self, file_path: str) -> List[Chunk]:
        # 自定义切分逻辑
        return chunks
```

### 3. 自定义存储

```python
from huimemory.storage import BaseStore

class MyStore(BaseStore):
    def add(self, chunks: List[Chunk]) -> None:
        # 自定义存储逻辑
        pass
    
    def search(self, vector: List[float], top_k: int) -> List[SearchResult]:
        # 自定义检索逻辑
        return results
```

---

**核心原则**：简单、高效、职责清晰。检索系统只做一件事：高效地"捞"数据。
