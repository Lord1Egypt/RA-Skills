---
name: novel-outliner
description: >
  从小说大纲自动拆解逐章prompt。支持纯文本、JSON、Markdown格式大纲，
  一键生成每章写作指令。
  用法：用户给出大纲文件并要求"拆解大纲"/"生成每章prompt"/"把大纲转成写作指令"。
NOT for: 写作、扩写——只负责从大纲生成prompt
---

# Novel Outliner — 大纲拆解

## 用法

```bash
python3 scripts/parse_outline.py --outline <大纲文件> --output <输出目录>
```

## 支持格式

- **纯文本**：按"第X章"分隔
- **JSON**：`{"chapters": {"1": {"title": "...", "plot": "..."}}}`
- **Markdown**：`# 第X章` 格式

## 输出

- 每章一个 prompt 文件（`.txt`），可直接配合小说生成工具使用
- 汇总文件 `chapters.json`，包含所有章节信息

## 约束

每个 prompt 自动注入硬性约束：纯中文、零AI标记词、字数12000+、忠于大纲。
