---
name: local-memory
description: 本地向量记忆工具，替代内置 memory 工具。使用 ChromaDB + BGE-small-zh 实现完全离线的语义记忆存储和检索。使用场景：(1) 存储重要信息到长期记忆，(2) 语义搜索历史记忆，(3) 删除特定记忆。触发词：记住、记忆、recall、memory、forget。
---

# Local Memory

本地向量记忆工具，使用 ChromaDB + BGE-small-zh-v1.5 实现完全离线的语义记忆存储和检索。

## 首次使用

运行安装脚本（约需 5-10 分钟下载模型和依赖）：

```bash
python scripts/setup.py
```

## 数据存储位置

skill 目录下的 `data/` 子目录（自动创建）。

## 脚本用法

所有脚本位于 `scripts/` 目录，输出均为 JSON 格式。

### 存储记忆

```bash
python scripts/memory_store.py --text "要记住的内容" [--category fact|preference|decision|entity|other] [--importance 0.7]
```

- `--text`（必填）：记忆内容
- `--category`（可选，默认 other）：分类
- `--importance`（可选，默认 0.7）：重要性 0-1

### 搜索记忆

```bash
python scripts/memory_recall.py --query "搜索关键词" [--limit 5]
```

- `--query`（必填）：语义搜索词
- `--limit`（可选，默认 5）：返回条数

### 删除记忆

```bash
python scripts/memory_forget.py --id "记忆ID"
python scripts/memory_forget.py --query "搜索关键词"
```

- `--id`：按 ID 精确删除
- `--query`：删除语义最匹配的一条
