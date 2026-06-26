---
name: qmd-memory
description: |
  QMD 本地记忆向量检索系统 - 使用 BM25 全文检索替代全量上下文注入，大幅减少 token 消耗。
  支持记忆索引构建、检索、添加功能。
allowed-tools:
  - Bash(qmd-*)
  - Bash(node qmd-*)
license: MIT
metadata:
  {"author":"OpenClaw","version":"1.0.0"}
---

## QMD Memory Skill

### 概述

QMD (Quick Memory Database) 是一个**纯本地**的记忆检索系统，使用 BM25 全文检索算法，无需下载向量模型，无需外部 API。

**优势：**
- 🚀 速度快 - 毫秒级检索
- 💾 纯本地 - 无需网络、无需 API
- 📉 省 token - 只注入相关记忆 (top-k)，而非全量
- 🔒 隐私安全 - 所有数据在本地

### 命令

| 命令 | 说明 | 示例 |
|------|------|------|
| `qmd-index` | 构建/重建记忆索引 | `cd ~/workspace/qmd && node qmd-index.js` |
| `qmd-search <查询> [limit]` | 检索记忆 | `node qmd-search.js "代币创建" 5` |
| `qmd-add <内容>` | 添加记忆并重建索引 | `node qmd-add.js "用户喜欢喝咖啡"` |

### 工作流程

```
用户提问
    ↓
memory_search (调用 qmd-search)
    ↓
BM25 检索 top-k 相关记忆
    ↓
只注入相关片段到上下文 (而非全部 MEMORY.md)
    ↓
LLM 回答
```

### 集成到 OpenClaw

在 OpenClaw 的 `memory_search` 工具中，可以调用此 skill 进行检索：

```bash
cd /Users/ben/.openclaw/workspace/qmd && node qmd-search.js "<查询文本>" 5
```

返回 JSON 格式结果，解析后注入上下文。

### 文件结构

```
/Users/ben/.openclaw/workspace/
├── MEMORY.md              # 长期记忆 ( curated )
├── memory/
│   └── YYYY-MM-DD.md      # 每日记忆 ( raw logs )
├── qmd/
│   ├── qmd-index.js       # 索引构建脚本
│   ├── qmd-search.js      # 检索脚本
│   ├── qmd-add.js         # 添加记忆脚本
│   └── package.json
└── qmd-index/
    └── bm25-index.json    # BM25 索引文件
```

### 性能对比

| 方案 | Token 消耗 | 响应速度 | 网络依赖 |
|------|-----------|---------|---------|
| 原方案 (全量注入) | 100% | 快 | 无 |
| QMD (top-5 检索) | ~20% | 快 | 无 |

**节省约 80% token 消耗！**

### 使用示例

**1. 构建索引**
```bash
cd /Users/ben/.openclaw/workspace/qmd
node qmd-index.js
```

**2. 检索记忆**
```bash
node qmd-search.js "用户偏好" 3
```

**3. 添加新记忆**
```bash
node qmd-add.js "用户说下周要去上海出差"
```

### 注意事项

- 索引文件 `bm25-index.json` 是纯文本 JSON，可版本控制
- 每次添加记忆后会自动重建索引
- 支持中文和英文混合检索
- 建议定期清理过期的每日记忆文件
