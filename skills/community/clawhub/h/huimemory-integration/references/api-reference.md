# HuiMemory API 参考

## 核心类

### Retriever

主要的检索接口。

#### 初始化

```python
from huimemory import Retriever
from huimemory.embedding import BGEEmbedding

# 使用配置文件
retriever = Retriever(
    embedding=BGEEmbedding(model_path="models/bge-small-zh-v1.5"),
    config_path="configs/config.yaml"
)

# 使用默认配置
retriever = Retriever(
    embedding=BGEEmbedding(model_path="models/bge-small-zh-v1.5")
)
```

#### search()

检索历史对话。

```python
results = retriever.search(
    query="AI 意识",              # 搜索关键词
    top_k=5,                      # 返回结果数量
    filter_expr="timestamp >= '2026-04-06'",  # 时间过滤
    context_window=2,             # 上下文窗口（±N 轮）
    enable_progressive_scan=True  # 启用分段扫描
)
```

**参数**：

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `query` | `str` | 必填 | 搜索关键词或问题 |
| `top_k` | `int` | `5` | 返回结果数量 |
| `filter_expr` | `str \| None` | `None` | 时间过滤表达式 |
| `context_window` | `int` | `0` | 上下文窗口大小 |
| `enable_progressive_scan` | `bool` | `False` | 是否启用分段扫描 |

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

#### search_with_progress()

分段扫描版本。

```python
results = retriever.search_with_progress(
    query="项目讨论",
    on_round=lambda week, results: print(f"扫描 {week}，找到 {len(results)} 条"),
    max_weeks=16
)
```

**参数**：

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `query` | `str` | 必填 | 搜索关键词 |
| `on_round` | `Callable[[str, List[SearchResult]], None] \| None` | `None` | 每轮回调 |
| `max_weeks` | `int` | `16` | 最大扫描周数 |
| `top_k` | `int` | `5` | 每周返回结果数量 |

**返回**：`ScanResult`

```python
ScanResult(
    results=[...],
    scan_info={
        "weeks_scanned": 3,
        "total_candidates": 12,
        "reached_limit": False
    }
)
```

#### get_turn()

根据 metadata 精确检索。

```python
results = retriever.get_turn(
    session_file="2026-W15/2026-04-13/chat_xxx.md",
    turn_index=5,
    context_window=2
)
```

**参数**：

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `session_file` | `str` | 必填 | 对话文件路径 |
| `turn_index` | `int` | `-1` | 轮次索引（0-based） |
| `turn_label` | `int` | `-1` | 轮次标签（1-based，优先级更高） |
| `context_window` | `int` | `0` | 上下文窗口大小 |

**返回**：`List[SearchResult]`

#### format_search_result()

格式化单个检索结果。

```python
formatted = retriever.format_search_result(results[0])
```

**输出格式**：

```
[id:a3f2c7 | prev: k7f2a1 | next: d2n7p3 | 相似度: 0.778]
📁 2026-W15/2026-04-13/chat_xxx.md | 话题: 本地模型部署 | 2026-04-13 Mon 10:00:07

<user timestamp="...">...</user>
<assistant timestamp="...">...</assistant>
```

#### format_search_results()

格式化多个检索结果。

```python
formatted = retriever.format_search_results(results)
```

**输出格式**：

```
[id:a3f2c7 | prev: k7f2a1 | next: d2n7p3 | 相似度: 0.778]
📁 2026-W15/2026-04-13/chat_xxx.md | 话题: 本地模型部署 | 2026-04-13 Mon 10:00:07

<user timestamp="...">...</user>
<assistant timestamp="...">...</assistant>

---

[id:k7f2a1 | prev: d2n7p3 | next: a3f2c7 | 相似度: 0.723]
📁 2026-W15/2026-04-13/chat_xxx.md | 话题: 项目架构 | 2026-04-13 Mon 10:01:20

<user timestamp="...">...</user>
<assistant timestamp="...">...</assistant>
```

---

### Archiver

归档管理器。

#### 初始化

```python
from huimemory import Archiver

archiver = Archiver(config_path="configs/config.yaml")
```

#### archive_month()

归档一个月的对话。

```python
archiver.archive_month(
    year=2026,
    month=4,
    sessions_dir="memory/sessions"
)
```

**输出**：`memory/sessions/2026-W15/2026-04.tar.zst`

#### extract_month()

解压归档。

```python
archiver.extract_month(
    year=2026,
    month=4,
    output_dir="memory/sessions"
)
```

#### cleanup_expired_cache()

清理过期缓存。

```python
archiver.cleanup_expired_cache()
```

---

### TopicManager

话题管理器。

#### 初始化

```python
from huimemory import TopicManager

topic_manager = TopicManager()
```

#### extract_topic()

从对话中提取话题。

```python
topic = topic_manager.extract_topic(
    user_msg="我想了解一下本地模型部署",
    assistant_msg="好的，我来介绍一下..."
)
```

**返回**：`"本地模型部署"`

---

## 工具类

### TurnChunker

轮次切分器。

```python
from huimemory.chunker import TurnChunker

chunker = TurnChunker()
chunks = chunker.chunk_file("memory/sessions/2026-W15/2026-04-13/chat_xxx.md")
```

**输出**：`List[Chunk]`

```python
[
    Chunk(
        id="turn_text",
        metadata={
            "turn_id": "a3f2c7",
            "turn_index": 0,
            "timestamp": "2026-04-13T10:00:07",
            "weekday": "Mon",
            "session_file": "2026-W15/2026-04-13/chat_xxx.md",
            "topic": "本地模型部署",
            "text_type": "conversation",
            "text": "<user timestamp=\"...\">...</user>\n<assistant timestamp=\"...\">...</assistant>"
        }
    )
]
```

---

### TimeResolver

时间解析器。

```python
from huimemory.utils.time_resolver import TimeResolver

resolver = TimeResolver()
result = resolver.parse("上周三下午")
```

**输出**：

```python
{
    "start": "2026-04-09T12:00:00",
    "end": "2026-04-09T18:00:00",
    "is_fuzzy": False
}
```

---

### ProgressiveScanner

分段扫描器。

```python
from huimemory.core.progressive_scanner import ProgressiveScanner

scanner = ProgressiveScanner(
    retriever=retriever,
    max_weeks=16
)

result = scanner.scan(
    query="项目讨论",
    on_round=lambda week, results: print(f"扫描 {week}，找到 {len(results)} 条")
)
```

**返回**：`ScanResult`

```python
ScanResult(
    results=[...],
    scan_info={
        "weeks_scanned": 3,
        "total_candidates": 12,
        "reached_limit": False
    }
)
```

---

## Embedding 类

### BGEEmbedding

BGE 模型 embedding。

```python
from huimemory.embedding import BGEEmbedding

embedding = BGEEmbedding(
    model_path="models/bge-small-zh-v1.5",
    device="cpu"
)

vectors = embedding.encode(["文本1", "文本2"])
```

**参数**：

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `model_path` | `str` | 必填 | 模型路径 |
| `device` | `str` | `"cpu"` | 设备（`"cpu"` 或 `"cuda"`） |
| `batch_size` | `int` | `32` | 批处理大小 |

**返回**：`List[List[float]]`（向量列表）

---

### BGEMockEmbedding

Mock embedding（用于测试）。

```python
from huimemory.embedding import BGEMockEmbedding

embedding = BGEMockEmbedding()
vectors = embedding.encode(["文本1", "文本2"])
```

**返回**：固定维度的随机向量（384 维）

---

## 数据类型

### SearchResult

检索结果。

```python
@dataclass
class SearchResult:
    id: str          # 原文内容
    score: float     # 相似度分数
    metadata: dict   # 元数据
```

### Chunk

文本块。

```python
@dataclass
class Chunk:
    id: str          # 固定值 "turn_text"
    metadata: dict   # 元数据（含 text 字段）
```

### ScanResult

扫描结果。

```python
@dataclass
class ScanResult:
    results: List[SearchResult]  # 检索结果
    scan_info: dict              # 扫描信息
```

---

## 配置文件

### config.yaml

```yaml
embedding:
  model_path: "models/bge-small-zh-v1.5"
  device: "cpu"
  batch_size: 32

storage:
  db_path: "data/huimemory.db"
  cache_dir: ".cache"
  cache_ttl_hours: 72

archive:
  base_dir: "memory/sessions"
  compression: "zstd"
  level: 3

retriever:
  default_top_k: 5
  enable_progressive_scan: true
  max_scan_weeks: 16
```

---

## 错误处理

### 常见错误

#### 1. 模型文件不存在

```python
FileNotFoundError: [Errno 2] No such file or directory: 'models/bge-small-zh-v1.5'
```

**解决**：下载模型

```bash
git clone https://gitcode.com/hf_mirrors/BAAI/bge-small-zh-v1.5.git models/bge-small-zh-v1.5
```

#### 2. 向量维度不匹配

```python
ValueError: Vector dimension mismatch: expected 384, got 1024
```

**解决**：检查模型配置，确保 `model_path` 指向正确的模型

#### 3. 时间格式错误

```python
ValueError: Invalid timestamp format: '2026-04-13 10:00:07'
```

**解决**：使用 ISO 8601 格式：`'2026-04-13T10:00:07'`

---

**完整 API 文档**：https://gitee.com/HuiMengAI/hui-memory
