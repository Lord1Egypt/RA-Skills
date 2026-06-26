---
name: knowledge-mapper
description: "Notes knowledge mapper. Input Markdown/TXT notes or a topic folder; extract entities, similar ideas, relationships, and map views, then output searchable JSON/graph summaries and follow-up questions. Privacy boundary: local-first analysis unless the user explicitly chooses otherwise."
---
- 📄 **文档解析**: 支持 Markdown、TXT 格式
- 🔍 **实体识别**: 基于规则和关键词的实体提取
- 🔗 **关系发现**: 基于共现的实体关系提取
- 📊 **知识可视化**: 文本、JSON、GraphViz DOT 格式导出
- 🔎 **知识查询**: 搜索实体和文档

## 安装

```bash
# 添加到 PATH
ln -s ~/.openclaw/workspace/skills/knowledge-mapper/knowledge-graph ~/.local/bin/knowledge-graph
```

## 使用

### 添加文档

```bash
# 添加 Markdown 文档
knowledge-graph add ~/documents/article.md

# 添加文本文件
knowledge-graph add ~/notes/ideas.txt
```

### 查看文档列表

```bash
knowledge-graph documents
```

### 查看实体

```bash
# 列出所有实体（默认50个）
knowledge-graph entities

# 列出更多实体
knowledge-graph entities --limit 100

# 按类型过滤
knowledge-graph entities --type TECH
```

### 实体类型

- `PERSON` - 人物
- `ORG` - 组织/公司
- `TECH` - 技术/编程语言
- `CONCEPT` - 概念/术语
- `TERM` - 高频词/术语
- `UNKNOWN` - 未分类

### 查看关系

```bash
# 列出所有关系（默认30个）
knowledge-graph relations

# 列出更多关系
knowledge-graph relations --limit 50
```

### 导出知识图谱

```bash
# 文本格式（默认）
knowledge-graph export

# JSON 格式
knowledge-graph export --format json

# GraphViz DOT 格式（可用于绘图）
knowledge-graph export --format dot > graph.dot
dot -Tpng graph.dot -o graph.png
```

### 搜索知识库

```bash
# 搜索关键词
knowledge-graph search "人工智能"

# 搜索实体
knowledge-graph search "Python"
```

### 查看统计

```bash
knowledge-graph stats
```

## 示例工作流程

```bash
# 1. 添加文档到知识库
knowledge-graph add ~/docs/project-notes.md
knowledge-graph add ~/docs/research-paper.md
knowledge-graph add ~/docs/tech-stack.md

# 2. 查看提取的实体
knowledge-graph entities --limit 20

# 3. 查看发现的关系
knowledge-graph relations

# 4. 导出为可视化格式
knowledge-graph export --format dot > my-knowledge.dot

# 5. 生成图片（需要安装 GraphViz）
dot -Tpng my-knowledge.dot -o my-knowledge.png
```

## 数据存储

数据存储在 `~/.openclaw/data/knowledge-graph/`:
- `knowledge_graph.db` - SQLite 数据库

## 技术栈

- Python 3.8+
- SQLite
- argparse
- 正则表达式（实体提取）

## 扩展计划

- [ ] 支持更多文档格式（PDF、Word）
- [ ] 集成 NLP 模型进行更精确的实体识别
- [ ] 支持关系推理和补全
- [ ] 交互式知识图谱可视化
- [ ] 实体链接和消歧
