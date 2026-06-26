# Karpathy Query → Wiki 回流 Skill

## 描述
实现 Karpathy LLM Knowledge Base 的第一阶段：Query → Wiki回流。

当用户发起查询时：
1. 使用 M-Flow 搜索相关记忆
2. 将结果格式化为 wiki 条目
3. 存入 wiki 层供后续 Compile 使用

## 激活条件
- 用户发起知识查询
- 需要将查询结果回流到 wiki
- session → knowledge  pipeline

## 工作流

```
用户查询 → M-Flow搜索 → Wiki格式化 → 存入wiki层 → 供Compile使用
```

## Wiki 条目格式

```markdown
| source | content | tags | timestamp |
|--------|---------|------|-----------|
| session:xxx | 知识内容 | tag1,tag2 | 2026-04-05 |
```

## 使用方式

### Python API
```python
from karpathy_query_feedback import QueryFeedbackPipeline

pipeline = QueryFeedbackPipeline()
results = await pipeline.query("用户询问的问题")
wiki_entries = pipeline.format_as_wiki(results)
await pipeline.save_to_wiki(wiki_entries)
```

### 命令行
```bash
python scripts/query_and_save.py "查询内容" --format wiki --output ./wiki/
```

## 搜索模式
- `lexical`: BM25 全文搜索（快速、精确）
- `episodic`: 向量搜索（语义相似）
- `triplet`: 三元组搜索（关系推理）
- `hybrid`: 混合搜索（lexical + episodic）

## 配置
- 使用 M-Flow 作为底层记忆系统
- Wiki 存储路径: `knowledge/wiki/`
- 标签体系: 从配置或自动提取

## 依赖
- m-flow-memory skill (已安装)
- knowledge-distillation skill (用于标签提取)

## 文件结构
```
karpathy-query-feedback/
├── SKILL.md
├── scripts/
│   ├── __init__.py
│   ├── pipeline.py      # 核心管道
│   ├── formatter.py     # Wiki格式化
│   ├── search.py        # 搜索封装
│   └── query_and_save.py # CLI入口
└── docs/
    └── README.md
```
