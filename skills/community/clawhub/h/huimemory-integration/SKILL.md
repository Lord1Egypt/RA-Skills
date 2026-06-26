---
name: huimemory-integration
version: 1.0.0
description: |
  HuiMemory 本地语义记忆系统集成指南。帮助用户快速集成对话记忆、语义检索、时间过滤功能到 AI 应用中。
  
  触发场景：记忆系统、对话检索、语义搜索、HuiMemory、本地记忆、turn anchor、对话管理、长期记忆、上下文窗口、分段扫描、时间解析、BGE embedding、向量检索、对话轮次、记忆召回。
  
  当用户提到"记忆系统"、"对话检索"、"语义搜索"、"本地记忆"、"turn anchor"等关键词，或询问如何实现对话记忆管理、长期记忆、上下文扩展时，主动使用此 skill。
---

# HuiMemory 集成指南

HuiMemory 是一个"延长单窗口对话"的本地语义记忆系统，核心设计哲学：**检索系统 = 搜索引擎，不负责语义理解和答案生成**。

## 集成模式

HuiMemory 采用 **"默认增强、可选接管"** 的集成模式，与 Mem0、Zep 等主流记忆库保持一致：

### 增强模式（默认）
- **无侵入外挂**：宿主应用保留自己的对话存储和短期记忆管理
- **只做增强**：HuiMemory 负责存储历史对话、检索相关内容、返回结果
- **不碰内部逻辑**：完全不影响宿主原有的记忆系统
- **适用场景**：已有记忆系统的应用，想增加长期记忆能力

```
宿主应用                    HuiMemory
┌─────────────┐            ┌─────────────┐
│ 短期对话存储 │            │ 长期记忆存储 │
│ 上下文管理   │  ← 调用 →  │ 语义检索     │
│ 业务逻辑     │            │ 时间过滤     │
└─────────────┘            └─────────────┘
```

### 接管模式（可选）
- **完整记忆内核**：宿主不再维护对话存储，所有记忆读写都交给 HuiMemory
- **需要主动配合**：宿主需要调用 HuiMemory 的 API 进行所有记忆操作
- **适用场景**：新应用、需要完整记忆方案的应用

```
宿主应用                    HuiMemory
┌─────────────┐            ┌─────────────┐
│ 业务逻辑     │  ← 全部 →  │ 短期+长期记忆 │
│             │            │ 上下文管理   │
│             │            │ 语义检索     │
└─────────────┘            └─────────────┘
```

**默认情况下，HuiMemory 作为增强模式的外挂技能使用，不会接管或破坏宿主原有的记忆系统。**

## 核心特性

- ✅ **三层架构**：LLM 提炼 → 检索系统（关键词+时间）→ LLM 回答
- ✅ **轮次锚点系统**：`[id:xxx | prev: yyy | next: zzz]` 双向链表导航
- ✅ **时间解析**：自然语言时间 → 分段扫描（周步长）
- ✅ **轻量模型**：默认使用 `bge-base-zh-v1.5`（768 维，~430MB）

## 快速开始

### 1. 安装依赖

```bash
# 克隆项目
git clone https://gitee.com/HuiMengAI/hui-memory.git
cd hui-memory

# 安装依赖
pip install -r requirements.txt

# 安装 embedding 依赖（轻量模型）
pip install -r requirements-embedding.txt
```

### 2. 下载模型

```bash
# 下载轻量中文模型（推荐，平衡性能和体积）
git clone https://gitcode.com/hf_mirrors/BAAI/bge-base-zh-v1.5.git models/bge-base-zh-v1.5

# 或使用极致轻量版（嵌入式设备）
# git clone https://gitcode.com/hf_mirrors/BAAI/bge-small-zh-v1.5.git models/bge-small-zh-v1.5

# 或使用 BGE-M3（重模型，性能最好）
# git clone https://gitcode.com/hf_mirrors/BAAI/bge-m3.git models/bge-m3
```

### 3. 配置文件

创建 `configs/config.yaml`：

```yaml
embedding:
  model_path: "models/bge-base-zh-v1.5"  # 轻量模型（推荐）
  dimension: 768                          # base=768, small=384, m3=1024
  # model_path: "models/bge-small-zh-v1.5"  # 极致轻量版
  # model_path: "models/bge-m3"             # 重模型（可选）
  device: "cpu"                            # 或 "cuda"
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

### 4. 基本用法

```python
from huimemory import Retriever, Archiver, TopicManager
from huimemory.embedding import BGEMockEmbedding  # 或 BGEEmbedding

# 初始化
embedding = BGEMockEmbedding()  # 或 BGEEmbedding(model_path="models/bge-base-zh-v1.5")
retriever = Retriever(embedding=embedding, config_path="configs/config.yaml")

# 索引对话
from huimemory.chunker import TurnChunker

chunker = TurnChunker()
chunks = chunker.chunk_file("memory/sessions/2026-W15/2026-04-13/chat_xxx.md")
retriever.store.add(chunks)

# 检索
results = retriever.search(
    query="用户问过什么关于 AI 意识的问题？",
    top_k=5,
    enable_progressive_scan=True
)

# 格式化输出
for r in results:
    print(retriever.format_search_result(r))
    print("---")
```

## LLM 集成

### System Prompt 模板

```markdown
你是一个拥有长期记忆的 AI 助手。你可以通过 `recall_memory` 工具检索历史对话。

## 记忆检索规则

1. **关键词检索**：当用户提到具体内容时，使用关键词搜索
   - 用户："我之前问过什么关于 AI 意识的问题？"
   - 调用：`recall_memory(query="AI 意识", top_k=5)`

2. **时间过滤**：当用户提到时间范围时，使用时间过滤
   - 用户："上周我们讨论了什么？"
   - 调用：`recall_memory(query="", filter_expr="timestamp >= '2026-04-06' AND timestamp <= '2026-04-13'")`

3. **分段扫描**：当时间模糊时，系统会自动分段扫描
   - 用户："前段时间我们聊过什么项目？"
   - 系统自动：从最近一周开始，逐步向前扫描

4. **轮次导航**：当需要查看上下文时，使用 `recall_by_id`
   - 检索结果：`[id:a3f2c7 | prev: k7f2a1 | next: d2n7p3]`
   - 调用：`recall_by_id(turn_id="k7f2a1")` 查看上一轮

## 输出格式

检索结果格式：
```
[id:a3f2c7 | prev: k7f2a1 | next: d2n7p3 | 相似度: 0.778]
📁 2026-W11/2026-03-05/chat_xxx.md | 话题: 本地模型部署 | 2026-03-05 Mon 10:00:07

<user timestamp="...">...</user>
<assistant timestamp="...">...</assistant>
```

使用 `prev`/`next` 值调用 `recall_by_id` 查看相邻轮次。
```

### Tool Schema

```json
{
  "tools": [
    {
      "name": "recall_memory",
      "description": "检索历史对话记忆。支持关键词搜索、时间过滤、分段扫描。",
      "parameters": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string",
            "description": "搜索关键词或问题"
          },
          "filter_expr": {
            "type": "string",
            "description": "时间过滤表达式，如 \"timestamp >= '2026-04-06'\""
          },
          "top_k": {
            "type": "integer",
            "description": "返回结果数量，默认 5",
            "default": 5
          }
        },
        "required": ["query"]
      }
    },
    {
      "name": "recall_by_id",
      "description": "根据轮次 ID 检索特定对话。用于导航到相邻轮次。",
      "parameters": {
        "type": "object",
        "properties": {
          "turn_id": {
            "type": "string",
            "description": "轮次 ID，如 'a3f2c7'"
          }
        },
        "required": ["turn_id"]
      }
    }
  ]
}
```

## 架构设计

### 三层架构

```
┌─────────────────────────────────────────────────────────────┐
│                      LLM 层（理解+回答）                      │
│  - 意图理解：关键词提取、时间范围推断                          │
│  - 答案组织：基于检索结果生成回答                              │
│  - 追问决策：是否需要更多上下文                                │
└─────────────────────────────────────────────────────────────┘
                              ↓ 调用工具
┌─────────────────────────────────────────────────────────────┐
│                   检索系统层（搜索引擎）                       │
│  - 关键词检索：向量相似度搜索                                  │
│  - 时间过滤：metadata 范围查询                                 │
│  - 分段扫描：周步长渐进式扫描                                  │
│  - 轮次导航：prev/next 指针                                   │
└─────────────────────────────────────────────────────────────┘
                              ↓ 读取文件
┌─────────────────────────────────────────────────────────────┐
│                      存储层（数据持久化）                      │
│  - 向量存储：SQLite + Faiss                                   │
│  - 元数据索引：timestamp, turn_index, topic, session_file    │
│  - 归档管理：月包压缩（.tar.zst）                              │
└─────────────────────────────────────────────────────────────┘
```

### 核心原则

1. **检索系统 = 搜索引擎**：只负责"捞"候选，不做判断
2. **LLM = 决策者**：负责判断、追问、组织答案
3. **向量模型无上下文**：不做"哪个是对的"判断

## 高级功能

### 1. 分段扫描（Progressive Scan）

当时间模糊时，系统自动从近到远扫描：

```python
results = retriever.search_with_progress(
    query="项目讨论",
    on_round=lambda week, results: print(f"扫描 {week}，找到 {len(results)} 条"),
    max_weeks=16
)
```

### 2. 上下文窗口扩展

检索到结果后，自动扩展相邻轮次：

```python
results = retriever.search(
    query="AI 意识",
    context_window=2  # 包含 ±2 轮
)
```

### 3. 时间解析

支持自然语言时间：

```python
from huimemory.utils.time_resolver import TimeResolver

resolver = TimeResolver()
result = resolver.parse("上周三下午")
# {"start": "2026-04-09T12:00:00", "end": "2026-04-09T18:00:00"}
```

## 常见问题

### Q1: 为什么不用 BGE-M3？

**模型对比**：
- **BGE-M3**：1024 维，2G+ 模型，性能最好（C-MTEB ~65）
- **bge-base-zh-v1.5**：768 维，~430MB，性能优秀（C-MTEB ~63.1）
- **bge-small-zh-v1.5**：384 维，~100MB，性能合格（C-MTEB ~57.8）

**推荐**：
- 默认使用 `bge-base-zh-v1.5`：平衡性能和体积，适合大多数应用
- 极致轻量场景用 `bge-small-zh-v1.5`：嵌入式设备、移动端
- 追求极致性能用 `BGE-M3`：服务器部署、专业应用

### Q2: 如何处理模糊时间？

系统采用**分段扫描**策略：
1. 规则引擎解析精确时间（"上周三"）
2. 模糊时间触发分段扫描（"前段时间"）
3. 从最近一周开始，逐步向前扫描
4. 每周最多返回 5 个候选，交给 LLM 判断

### Q3: 如何扩展上下文？

使用 `context_window` 参数：

```python
results = retriever.search(
    query="项目架构",
    context_window=3  # 包含 ±3 轮
)
```

结果会标记 `_context_role`：`hit`（命中）、`neighbor`（邻居）

## 参考文档

- `references/architecture.md` - 详细架构设计
- `references/api-reference.md` - 完整 API 文档
- `references/llm-integration.md` - LLM 集成深度指南

## 示例项目

- `examples/quickstart.py` - 快速入门示例
- `examples/llm_integration_demo.py` - LLM 集成完整示例

---

**核心设计哲学**：检索系统只负责"捞"，LLM 负责"判断"。保持简单，避免过度设计。
