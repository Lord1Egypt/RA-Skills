---
name: markdown-knowledge
description: 将本地 Markdown 知识库与 OpenClaw 集成，支持语义检索和上下文注入。仅在用户触发时检索（搜索知识库、查一下知识库等），不主动注入。
description_zh: 将本地 Markdown 知识库与 OpenClaw 集成，支持语义检索和上下文注入。仅在用户触发时检索，不主动注入。
author: aaronjager92
version: 1.1.2
license: MIT
homepage: 
tags:
    - markdown-knowledge
    - markdown
    - retrieval
    - productivity
defaults:
    knowledge_path: ~/Knowledge
    index_path: ~/.openclaw/skills/markdown-knowledge/index.json
    search_top_k: 3
    auto_refresh: false
triggers:
    - action: search
      description: 检索知识库相关内容
      patterns:
        - "搜索知识库"
        - "查一下知识库"
        - "知识库里"
        - "查知识库"
        - "知识库搜索"
        - "知识库查询"
    - action: rebuild
      description: 重建知识库索引
      patterns:
        - "刷新知识库"
        - "更新知识库"
        - "重建知识库"
        - "刷新知识库索引"
        - "更新知识库索引"
        - "重建知识库索引"
    - action: stats
      description: 查看知识库统计
      patterns:
        - "知识库统计"
        - "查看知识库"
        - "知识库状态"
---

# Markdown Knowledge Base

将您的本地 Markdown 知识库与 OpenClaw 集成，让 AI 助手能够基于您的专业知识回答问题。

## 核心原则

**触发式检索** - 仅在用户明确要求时检索知识库，不主动注入。

## 使用流程

### 1. 收到用户触发词 → 检索知识库

当用户说以下内容时，调用 search 动作：
- "搜索知识库"
- "查一下知识库"
- "知识库里..."

### 2. 搜到结果 → 注入上下文并回答

```python
# 调用示例
results = action_search("用户问题关键词")
```

### 3. 搜不到结果 → 明确告知

告诉用户"知识库中没有找到相关信息"，然后基于通用知识回答。

## 命令

| 命令 | 说明 |
|------|------|
| `python3 knowledge_base.py build` | 构建/更新索引 |
| `python3 knowledge_base.py search <词>` | 搜索知识库 |
| `python3 knowledge_base.py stats` | 查看统计 |
| `python3 knowledge_base.py init` | 初始化配置 |

## 安装

```bash
clawhub install markdown-knowledge
python3 ~/.openclaw/workspace/skills/markdown-knowledge/scripts/knowledge_base.py init
python3 ~/.openclaw/workspace/skills/markdown-knowledge/scripts/knowledge_base.py build
```

## 配置

编辑 `~/.openclaw/workspace/skills/markdown-knowledge/config.json`：

```json
{
    "knowledge_path": "~/Knowledge",
    "index_path": "~/.openclaw/workspace/skills/markdown-knowledge/index.json",
    "search_top_k": 3,
    "auto_refresh": false
}
```

## 隐私说明

- ✅ **触发式检索** - 仅用户明确要求时检索
- ❌ **无全局注入** - 不会主动注入知识库内容
- ❌ **无后台监听** - 不在后台自动运行

## 文件结构

```
markdown-knowledge/
├── SKILL.md
├── clawhub.json            # clawhub 元数据
├── scripts/
│   └── knowledge_base.py   # CLI 入口
├── src/
│   ├── __init__.py
│   ├── config.py           # 配置加载
│   ├── actions.py          # OpenClaw 动作
│   └── knowledge_core.py   # 核心检索逻辑
├── references/
│   └── README.md          # 详细文档
└── assets/
```
