# Memory Workflow

## 首次安装配置

> 以下规则需要添加到 `~/.openclaw/workspace/AGENTS.md`。如果规则已存在（见「已安装」标记），跳过此步骤。

**添加以下内容到 AGENTS.md 顶部（`## 每次消息时` 之前）：**

```markdown
<!-- [memory-workflow] 已安装 -->
## 每次消息时

自动搜索相关记忆（如果返回有结果则使用，无结果则忽略）：
Exec: python3 $HOME/.openclaw/workspace/skills/memory-workflow/memory_ops.py search --query "【用户发送的原始消息】" --llm-answer --limit 3

## /save 命令

当用户发送 /save 时，强制将当前 session 的完整对话存入记忆系统：
Exec: cat << 'EOF' | python3 $HOME/.openclaw/workspace/skills/memory-workflow/scripts/save_session.py
{"messages": [
  {"role": "user", "content": "【从当前对话上下文获取】"},
  {"role": "assistant", "content": "【从当前对话上下文获取】"}
]}
EOF
```

**检查是否已安装**：如果 AGENTS.md 中已有 `<!-- [memory-workflow] 已安装 -->` 标记，说明已配置，跳过。

---



你的记忆工作流助手。当用户提到"记忆"、"记得"、"之前说过"、"搜一下"、"去重"、"整理"等词时激活此 skill。

## 三层存储架构

| 层级 | 存储位置 | 依赖 | 说明 |
|------|----------|------|------|
| **文件** | `memory-workflow-data/memories/YYYY-MM-DD.md` | 无 | 永远可用 |
| **FTS5** | `memory-workflow-data/fts5_index.db` | SQLite 内置 | 全文搜索，零外部依赖 |
| **KG** | `memory-workflow-data/knowledge-graph/kg.db` | Ollama（可选） | 三元组知识图谱，规则降级 |
| **Milvus** | memory_workflow collection | 18779 端口（可选） | 向量检索，bge-m3 embedding |

**开箱即用**：即使没有任何外部服务，文件层 + FTS5 + KG(规则) 仍然正常工作。

## 核心文件

```
memory-workflow/
├── SKILL.md           # 本文件
├── memory_ops.py      # CLI 入口
├── README.md          # 使用说明
└── scripts/
    ├── config.py      # 配置（路径、服务地址）
    ├── store.py       # 三层存储写入
    ├── search.py      # FTS5 + Jaccard 搜索
    ├── fts5.py        # FTS5 全文索引
    ├── tools.py       # BaseTool 封装（6个工具）
    └── save_session.py # /save 命令处理器
```

## 工具接口

| 工具 | 说明 | 依赖 |
|------|------|------|
| `MemorySearch` | 语义搜索，FTS5 + 字符N-gram Jaccard 排序 | 无 |
| `MemoryStore` | 三层存储（文件 + KG + Milvus），自动去重 | Ollama(KG) / Milvus(可选) |
| `MemoryDedup` | Jaccard 去重（阈值 0.85） | 无 |
| `MemoryPrune` | 清理 N 天前记忆 | 无 |
| `MemoryConsolidate` | 合并相似记忆（Jaccard > 0.7） | 无 |
| `MemoryList` | 列出近期记忆文件 | 无 |

## 搜索算法

**字符级 N-gram Jaccard** — 解决中文分词问题：
- "发哥在测试" → `{'发哥','哥在','在测','测试'}`
- 中英混合无缝支持，无需外部分词服务

**搜索流程**：Jaccard 召回 → FTS5 BM25 重排 → 时间衰减 rerank

## 数据存储路径

- 记忆文件：`~/.openclaw/workspace/memory-workflow-data/memories/YYYY-MM-DD.md`
- FTS5 索引：`~/.openclaw/workspace/memory-workflow-data/fts5_index.db`
- KG 图谱：`~/.openclaw/workspace/memory-workflow-data/knowledge-graph/kg.db`
- 元数据：`~/.openclaw/workspace/memory-workflow-data/knowledge-graph/kg.db` 内

## 触发规则

| 模式 | 工具 |
|------|------|
| "记"、"存"、"记住"、"记一下" | `MemoryStore` |
| "搜"、"找"、"记得"、"之前说过" | `MemorySearch` |
| "去重"、"整理记忆" | `MemoryDedup` |
| "合并"、"整理一下" | `MemoryConsolidate` |
| "删除"、"清理旧" | `MemoryPrune` |
| "列出记忆文件"、"有哪些记忆" | `MemoryList` |

## CLI 用法

```bash
# 搜索
python memory_ops.py search --query "发哥 工作" --limit 3

# 存储
python memory_ops.py store --content "要记忆的内容" --tag work

# /save 存储 session
python scripts/save_session.py '{"messages": [...]}'

# 去重 / 整理
python memory_ops.py dedup
python memory_ops.py consolidate
python memory_ops.py prune --days 30

# 导出工具定义
python memory_ops.py register
```
