---
name: ollama-memory
description: |
  本地向量记忆系统 - 基于 Ollama + SQLite 的 AI 助手记忆方案。
  支持：Markdown 记录、向量搜索、本地嵌入、无 API 费用。
  特点：本地部署、语义搜索、隐私优先。
metadata:
  openclaw:
    emoji: 🧠
    requires:
      bins: ["python3", "sqlite3", "ollama"]
---

# 本地向量记忆系统

这是一个带本地向量搜索的 AI 助手记忆系统，基于 Markdown 文件 + SQLite 实现。

## 目录结构

```
~/.openclaw/workspace/
├── memory/
│   └── YYYY-MM-DD.md      # 每日记录
├── MEMORY.md               # 长期记忆（核心认知）
├── SOUL.md                 # AI 人格定义
├── USER.md                 # 用户信息
├── AGENTS.md               # 工作规范
└── scripts/memory-system/  # 记忆系统脚本
```

## 核心文件

### 1. memory/YYYY-MM-DD.md - 每日记录

每次会话记录当天发生的事：

```markdown
# 2026-03-09

## 会话 1
- 主题：xxx
- 关键决策：xxx
- 待办：xxx

## 会话 2
- ...
```

### 2. MEMORY.md - 长期记忆

核心认知和重要信息，包含：
- 核心工作原则
- 用户偏好
- 关键教训
- 禁止事项
- 习惯

## 向量搜索

使用本地 Ollama + `nomic-embed-text` 模型实现向量语义搜索。

### 安装 Ollama 和模型

```bash
# 安装 Ollama
brew install ollama

# 启动服务
ollama serve

# 下载 embedding 模型
ollama pull nomic-embed-text
```

### 搜索命令

```bash
# 使用 Python 脚本搜索（推荐）
python3 ~/.openclaw/workspace/scripts/memory-system/context-memory.py search "关键词"

# 简单搜索
python3 ~/.openclaw/workspace/scripts/memory-system/memory-py.py search "关键词"
```

## 会话启动流程

每次新会话开始时：

1. 读取 `SOUL.md` — AI 人格
2. 读取 `USER.md` — 用户信息
3. 读取 `memory/YYYY-MM-DD.md` (今天 + 昨天)
4. **主会话**：读取 `MEMORY.md`
5. 检查 `knowledge/` 目录

## 保存记忆

当用户说"记住..."：
- 更新 `memory/YYYY-MM-DD.md` 记录
- 重要内容同步到 `MEMORY.md`
- 可选：存入向量数据库

```bash
# 添加记忆（带重要性评分）
python3 ~/.openclaw/workspace/scripts/memory-system/context-memory.py add "内容" 8

# 添加标签
python3 ~/.openclaw/workspace/scripts/memory-system/memory-py.py add "内容" "标签1,标签2"
```

## 更新规则

### 必须更新的文件
1. **memory/YYYY-MM-DD.md** - 每次会话
2. **MEMORY.md** - 新教训/重要信息
3. **SOUL.md** - 人格变化
4. **USER.md** - 用户偏好变化

### 更新时机
- 任务完成时
- 重要发现或教训
- 用户偏好变化
- 新技能学习

## 安全规则

- ❌ **不暴露用户个人信息**
- ❌ 不在 skill 输出中包含真实姓名/账号/密码
- ❌ 不在公开场合提及用户隐私
- ✅ 需要时才读取 MEMORY.md
- ✅ 主会话才加载 MEMORY.md

## 配置示例

在 AGENTS.md 中添加：

```markdown
## Memory

### 每日记录 (memory/YYYY-MM-DD.md)
- 每次会话记录关键内容
- 格式：## 会话 X / ### 主题 / 决策 / 待办

### 长期记忆 (MEMORY.md)
- 核心原则和偏好
- 重要教训
- 禁止事项
- 仅主会话加载

### 向量搜索
- 模型：Ollama + nomic-embed-text
- 脚本：context-memory.py
```

## 优势

| 特点 | 说明 |
|------|------|
| 本地向量 | 无 API 费用，离线可用 |
| 语义搜索 | 理解相似含义，不只是关键词 |
| 可读 | Markdown 人工可直接编辑 |
| 便携 | 文件复制即迁移 |
| 安全 | 本地存储，不上传云端 |

## 依赖

- **Ollama**: 本地 LLM 运行时
- **nomic-embed-text**: 本地 embedding 模型 (274MB)
- **Python 3**: 运行脚本
- **SQLite**: 向量存储

## 快速开始

```bash
# 1. 安装 Ollama
brew install ollama

# 2. 启动并下载模型
ollama serve
ollama pull nomic-embed-text

# 3. 初始化数据库
python3 ~/.openclaw/workspace/scripts/memory-system/context-memory.py init

# 4. 添加记忆
python3 ~/.openclaw/workspace/scripts/memory-system/context-memory.py add "用户偏好使用 Gemini" 8

# 5. 搜索记忆
python3 ~/.openclaw/workspace/scripts/memory-system/context-memory.py search "模型偏好"
```
