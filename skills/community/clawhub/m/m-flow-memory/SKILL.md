# M-Flow Memory Skill

## 描述
基于 M-Flow 的记忆系统，提供 Karpathy 风格的 4 阶段记忆管理工作流。

M-Flow 是一个集成了 Cone Graph、向量搜索 (LanceDB) 和图数据库 (Kuzu) 的记忆框架。

## 激活条件
- 用户请求记忆 distillation、memory search、记忆管理
- 需要 Karpathy LLM Knowledge Base 工作流

## 核心功能

### 1. 记忆添加 (add)
```python
from m_flow_memory import MFlowMemory

memory = MFlowMemory()
await memory.add("session content or knowledge point")
```

### 2. 记忆索引 (memorize)
```python
await memory.memorize()  # 索引所有未处理的内容
```

### 3. 记忆搜索 (search)
```python
# 全文搜索 (BM25)
results = await memory.search("query", mode="lexical")

# 向量搜索 (Cone Graph)
results = await memory.search("query", mode="episodic")

# 三元组搜索
results = await memory.search("query", mode="triplet")
```

## M-Flow 配置要求

### 必需环境变量
```
HF_HUB_OFFLINE=1
```

### .env 配置 (m_flow/.env)
```
LLM_PROVIDER="ollama"
LLM_MODEL="ollama/qwen2.5:14b-instruct-q8_0"
OLLAMA_BASE_URL="http://localhost:11434/v1"
LLM_ENDPOINT="http://localhost:11434/v1"
LLM_API_KEY="ollama"

EMBEDDING_PROVIDER="ollama"
EMBEDDING_MODEL="nomic-embed-text:latest"
EMBEDDING_ENDPOINT="http://localhost:11434/v1/embeddings"
EMBEDDING_DIMENSIONS=768

VECTOR_DB_PROVIDER=lancedb
DB_PROVIDER=sqlite
GRAPH_DATABASE_PROVIDER=kuzu
```

### LanceDB 版本
⚠️ **重要**: LanceDB 必须使用 **0.26.0**（0.27.1 有 bug）
```bash
uv pip install lancedb==0.26.0
```

## Karpathy 4 阶段工作流

### Phase 0: 审计与激活
- 清点现有资源
- 建立 KNOWLEDGE-STANDARDS.md
- 激活 knowledge-archive collection

### Phase 1: Query → Wiki 回流
- 用户发起查询
- 结果存入 wiki 层
- 格式规范: `source | content | tags | timestamp`

### Phase 2: Compile 层
- 使用 knowledge-distillation skill
- session → knowledge points
- wiki → structured knowledge

### Phase 3: Lint 层
- 每周健康检查
- 去重、合并、更新

### Phase 4: M-Flow 集成
- MCP server (需要 m_flow>=0.5.0)
- 多 Agent 共享

## 目录结构
```
m-flow-memory/
├── SKILL.md           # 本文件
├── scripts/
│   ├── __init__.py
│   ├── client.py      # M-Flow Python 客户端封装
│   ├── distill.py     # 记忆蒸馏
│   ├── query.py       # 记忆查询
│   └── config.py      # 配置
└── docs/
    └── README.md      # 详细文档
```

## 使用示例

### 添加记忆
```python
await memory.add("用户询问了 OpenClaw 的记忆系统架构")
```

### 搜索记忆
```python
# 混合搜索
results = await memory.search(
    "OpenClaw memory system",
    mode="episodic",
    top_k=10
)
```

### 记忆蒸馏
```python
# 从会话中提取知识要点
knowledge_points = await memory.distill(session_transcript)
```

## 已知限制
1. M-Flow REST API 需要认证（当前配置为开发模式）
2. Kuzu 图数据库在 Windows 上可能有文件锁定问题
3. LanceDB 0.27.1 有 bug，必须使用 0.26.0

## 依赖
- m-flow >= 0.3.1
- lancedb == 0.26.0
- ollama (本地运行)
- HF_HUB_OFFLINE=1
