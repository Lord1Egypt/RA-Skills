# Knowledge Base Skill

**Version**: v1.2.0
**Repository**: https://github.com/ThomasLiu/knowledge-base-skill

---

## 触发条件

当用户提到以下关键词时触发：

- "加入知识库" / "存到 KB" / "存入知识库"
- "knowledge base" / "知识库" / "KB"
- "记得这个" / "保存上下文" / "记忆"
- "检索知识库" / "查一下 KB"

---

## 功能

### 1. Collect - 存储

```bash
kb store --title "标题" --content "内容" --source "manual"
```

### 2. Retrieve - 检索

```bash
kb search --query "关键词"
kb retrieve --topic-key "entry-key"
```

### 3. Recall - 对话前自动检索

在 `before_agent_start` hook 中自动调用，检索与当前对话相关的知识。

### 4. Capture - 对话后自动存储

在 `after_turn` hook 中自动调用，判断并存储重要内容。

---

## 使用方式

### 存储信息

```
用户: 把这个配置加入知识库
Agent: 使用 kb store 命令存储
```

### 检索信息

```
用户: 查一下知识库里关于 OpenClaw 的内容
Agent: 使用 kb search 查询并返回结果
```

---

## 脚本列表

| 脚本 | 功能 |
|------|------|
| `scripts/storage.sh` | 核心存储 API |
| `scripts/retriever.sh` | 检索 + recall/capture |
| `scripts/hooks.sh` | OpenClaw Hooks 集成 |
| `scripts/lifecycle.sh` | 生命周期管理 |

## 依赖

- bash
- sqlite3
- python3

---

## 配置

### 默认模式（安装即用）

Skill 安装后默认使用**自身目录**存储，无需任何配置：

```
~/.openclaw/workspace/skills/kb-mini/data/knowledge.db
```

### 共享 KB 模式（多 Agent 共用）

多个 Agent 共用同一个知识库：

```bash
# 在调用 skill 前设置
export KNOWLEDGE_SHARED_NAME="coding-kb"
# 实际路径: ~/.openclaw/shared/knowledge-bases/coding-kb/knowledge.db
```

### 显式路径模式

指定任意路径作为 KB：

```bash
export KNOWLEDGE_DB="/path/to/your/knowledge.db"
```

### 环境变量优先级

| 优先级 | 变量 | 说明 |
|--------|------|------|
| 1 | `KNOWLEDGE_DB` | 显式指定路径 |
| 2 | `KNOWLEDGE_SHARED_NAME` | 共享 KB 名称 |
| 3 | Skill 内部目录 | 默认，安装即用 |

---

## 目录结构

```
kb-mini/
├── data/
│   └── knowledge.db      # 默认 KB 路径
├── scripts/
│   ├── storage.sh        # 存储 API
│   ├── retriever.sh      # 检索 API
│   ├── hooks.sh          # Hooks 集成
│   └── lifecycle.sh      # 生命周期
└── SKILL.md
```
