# Memory Indexer 🧠

> 短期记忆关键词索引工具，为 AI Agent 提供长期记忆能力

**版本**: v2.0.0 | [English](./README_EN.md) | 中文

## 简介

Memory Indexer 帮助 AI Agent 持久化记忆：

- 自动提取记忆中的关键词
- 建立关键词 → 记忆文件的快速索引
- 支持多关键词精确搜索（AND/OR 模式）
- 自动发现关联记忆
- 按时间线展示记忆
- 标记和查看重要记忆
- 增量同步外部记忆目录
- 会话备份与精简（避免 session memory 无限膨胀）

## 为什么需要它？

AI Agent 每次会话结束后会丢失上下文。传统方案只能保存原始文本，检索困难。

Memory Indexer 通过关键词索引，让记忆可搜索、可关联、可追溯。

## 功能特性

1. 自动关键词提取：使用 jieba 中文分词
2. 多模式搜索：OR（任一匹配）/ AND（全部匹配）
3. 关联发现：自动发现经常一起出现的记忆
4. 时间线视图：按时间顺序展示记忆
5. 主动提醒：根据当前关键词提示相关旧记忆
6. 重要记忆标记：手动标记优先保留
7. 增量同步：只索引新增或修改的文件
8. 失效清理：自动清理已删除记忆的索引
9. **三级级联搜索**：关键词 → 向量语义 → 原文，自动降级
10. **向量语义搜索**：基于 HuggingFace bge-base-zh-v1.5 模型
11. **会话备份与精简**：备份用户消息到索引，精简 session 文件到 ~10KB
12. **Memory 文件精简**：备份 memory/*.md 到索引，精简大文件到 ~10KB
13. **新对话自动搜索**：Hook 机制，新会话开始时自动检索相关记忆
14. **压缩风险检测**：检测 memory 目录大小，评估压缩风险
15. **使用统计**：查看 memory 文件数量、大小、关键词统计
16. **快照备份**：压缩前自动/手动创建快照，支持恢复

## 安装

### 方式一：运行安装脚本（推荐）

```bash
git clone https://github.com/smallmj/memory-indexer.git
cd memory-indexer
chmod +x install.sh
./install.sh
```

安装脚本会自动：
- 检查并安装依赖（jieba）
- 创建到 OpenClaw skills 目录的软链接
- 配置 AGENTS.md、MEMORY.md、HEARTBEAT.md

### 方式二：手动安装

```bash
git clone https://github.com/smallmj/memory-indexer.git
cd memory-indexer
pip install -r requirements.txt
ln -sf "$(pwd)" ~/.openclaw/workspace/skills/memory-indexer
python3 memory-indexer.py status
```

### 自动配置说明

运行 `install.sh` 会自动完成以下配置：

| 文件 | 配置内容 | 作用 |
|------|---------|------|
| `AGENTS.md` | 检索记忆的规则 | 新会话时自动搜索相关记忆 |
| `MEMORY.md` | 强制规则：保存/新会话时调用 indexer | 自动建立索引、自动检索 |
| `HEARTBEAT.md` | 定期同步 + 会话备份 | 自动备份和精简 session memory |

**手动配置（不运行 install.sh）：**

如果你不想运行安装脚本，需要手动在 OpenClaw workspace 中添加以下配置：

1. **AGENTS.md** - 启动流程检索记忆 + 主动搜索规则
   ```markdown
   ## 记忆系统（强制规则）

   ### 搜索顺序（必须遵守）
   1. **memory-indexer** - 三级级联搜索（**最先**）
   2. **memory_search** - 原始记忆文件搜索
   3. **直接读文件** - 仅当前会话内容

   ### 主动搜索规则（Agent 智能判断）
   Agent 根据问题内容主动判断是否搜索：
   - 用户提到"之前"、"记得"、"有没有"
   - 用户问"找找"、"为什么"、"原因"
   - 讨论特定项目/任务时
   - 不盲目搜索，避免浪费 token

2. **MEMORY.md** - 强制规则：保存/新会话时调用 indexer
3. **HEARTBEAT.md** - 定期同步 + 会话备份

## 快速开始

```bash
# 添加记忆
python memory-indexer.py add "今天学习了 Python"

# 搜索（OR 模式）
python memory-indexer.py search "Python"

# 搜索（AND 模式）
python memory-indexer.py search "Python 编程" --and

# 列出所有记忆
python memory-indexer.py list

# 记忆摘要
python memory-indexer.py summary
```

### 向量语义搜索（需要安装依赖）

```bash
# 安装向量模型依赖
pip install sentence-transformers

# 测试向量生成
python embedding.py test

# 查看向量索引状态
python embedding.py status

# 批量生成历史记忆的向量
python embedding.py reindex

# 三级级联搜索（默认）
python memory-indexer.py search "今天天气"

# 只用关键词搜索
python memory-indexer.py search "天气" --keyword

# 只用向量搜索
python memory-indexer.py search "天气" --semantic

# 只用原文搜索
python memory-indexer.py search "天气" --raw

# add 命令同时生成向量
python memory-indexer.py add "今天天气很好" --embed
```

**向量模型配置（可选）：**
- 默认使用 HuggingFace `BAAI/bge-base-zh-v1.5`（768维）
- 可通过环境变量配置：
  - `EMBEDDING_PROVIDER=huggingface` (默认)
  - `EMBEDDING_PROVIDER=ollama`
  - `EMBEDDING_PROVIDER=minimax`
  - `HF_MODEL_NAME=BAAI/bge-base-zh-v1.5`

## 与 OpenClaw 集成

```bash
cd ~/.openclaw/workspace
uv pip install jieba
uv run python skills/memory-indexer/memory-indexer.py add "记忆内容"

# 会话备份与精简（每次 heartbeat 自动运行）
uv run python skills/memory-indexer/session_backup.py

# Memory 文件精简（每次 heartbeat 自动运行）
uv run python skills/memory-indexer/memory_compact.py

# 压缩风险检测（新增）
uv run python skills/memory-indexer/memory_detect.py

# 使用统计（新增）
uv run python skills/memory-indexer/memory_stats.py

# 快照管理（新增）
uv run python skills/memory-indexer/memory_snapshot.py create   # 创建快照
uv run python skills/memory-indexer/memory_snapshot.py list    # 列出快照
uv run python skills/memory-indexer/memory_snapshot.py restore <name>  # 恢复快照
```

### Hook: 新对话自动搜索记忆

从 v2.0.0 开始，提供 OpenClaw Hook `memory-indexer-on-new`，在新对话开始时自动搜索相关记忆。

**安装 Hook：**

```bash
# 复制 Hook 目录到 OpenClaw
cp -r hooks/memory-indexer-on-new ~/.openclaw/hooks/

# 重启 Gateway 使其生效
openclaw gateway restart
```

**工作原理：**
- Hook 监听 `/new` 命令（可在 AGENTS.md 中配置自动触发）
- 自动调用 memory-indexer 搜索与用户相关的记忆
- 搜索关键词：用户名称、偏好、项目、任务等

**文件位置：** `~/.openclaw/hooks/memory-indexer-on-new/`

| 文件 | 说明 |
|------|------|
| `handler.ts` | Hook 执行逻辑 |
| `HOOK.md` | Hook 元数据配置 |

## 命令参考

| 命令 | 功能 | 示例 |
|------|------|------|
| `add` | 添加记忆 | `add "今天学习了 Python"` |
| `search` | 搜索记忆 | `search "Python"` |
| `search --and` | AND 搜索 | `search "Python AI" --and` |
| `list` | 列出所有记忆 | `list` |
| `sync` | 同步外部目录 | `sync` |
| `cleanup` | 清理失效索引 | `cleanup` |
| `related` | 关联发现 | `related` |
| `timeline` | 时间线视图 | `timeline` |
| `recall` | 主动提醒 | `recall "Python"` |
| `summary` | 记忆摘要 | `summary` |
| `star` | 标记重要 | `star 20260312.md` |
| `stars` | 查看重要记忆 | `stars` |
| `status` | 查看状态 | `status` |

## 配置

数据目录：`~/.memory-indexer/`

```
~/.memory-indexer/
├── index.json          # 关键词索引
├── sync-state.json    # 同步状态
└── stars.json         # 重要记忆标记
```

备份目录：`~/.openclaw/workspace/memory-index/session-backups/`

可通过修改代码中的 `WORKSPACE` 变量自定义存储路径。

## 更新

```bash
cd memory-indexer
chmod +x update.sh
./update.sh
```

更新脚本会自动拉取代码、备份数据、检查依赖、重新同步索引。

---

技术栈：Python 3.8+、jieba、argparse、json

贡献：欢迎提交 Issue 和 Pull Request！
1. Fork 本仓库
2. 创建特性分支 (git checkout -b feature/xxx)
3. 提交更改 (git commit -m 'Add xxx')
4. 推送分支 (git push origin feature/xxx)
5. 创建 Pull Request

开源许可证：MIT

作者：@smallmj | hexiealan007@gmail.com

---

如果这个项目对你有帮助，请 ⭐ Star 支持！
