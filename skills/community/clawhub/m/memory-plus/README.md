# Memory Workflow

你的记忆工作流助手。零外部依赖开箱即用。

## 快速开始

```bash
# 搜索记忆
python memory_ops.py search --query "发哥 项目"

# 存储记忆
python memory_ops.py store --content "发哥在思特奇工作" --tag work

# /save 存储 session
python scripts/save_session.py '{"messages": [...]}'

# 去重 / 清理
python memory_ops.py dedup
python memory_ops.py prune --days 30
```

## 三层存储

| 层 | 说明 |
|----|------|
| 文件 | `memory-workflow-data/memories/*.md` |
| FTS5 | SQLite 全文索引，零依赖 |
| KG | 三元组知识图谱（Ollama LLM 提取，规则降级） |
| Milvus | 向量检索（可选，需要 18779 embedding 服务） |

## 工具（可注册到 Agent）

- `MemorySearch` — 语义搜索
- `MemoryStore` — 存储记忆
- `MemoryDedup` — 去重
- `MemoryPrune` — 清理旧记忆
- `MemoryConsolidate` — 合并相似记忆
- `MemoryList` — 列出记忆文件
