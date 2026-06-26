# 文档搜索指南

本模块允许你在 OpenClaw中文社区文档和知识库中进行搜索，快速获取相关知识。

## 常用指令

### 1. 搜索文档
支持全文搜索，返回相关的文档片段和链接。

```bash
# 搜索关键词 "skill"
claw doc search "skill"

# 搜索关于 "authentication" 的内容
claw doc search "authentication"
```

### 2. 获取文档详情
根据搜索结果中的路径，读取完整的文档内容。

```bash
# 读取指定文档
claw doc read docs/forum/about.md
```

## 搜索范围
目前支持搜索以下内容：
*   官方文档 (Docs)
*   论坛帖子 (Forum Posts)
*   技能市场描述 (Skill Market)

## 提示
*   使用更具体的关键词可以获得更准确的结果。
*   搜索结果会包含相关度评分，建议优先阅读评分高的文档。
