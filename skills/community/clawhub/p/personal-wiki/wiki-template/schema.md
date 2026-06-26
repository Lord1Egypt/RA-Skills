# Wiki Schema

> 这是 Claude 处理和组织知识的规则文件。Claude 在执行 Ingest / Query / Lint 时遵循此文件，并可随着使用不断更新此规则。

## 来源说明

本 Wiki 从三个来源 Ingest 内容：
- **印象笔记**：通过 Evernote API 读取，按 `guid` + `updated` 追踪
- **IMA 笔记**：通过 IMA OpenAPI 读取，按 `doc_id` + `modify_time` 追踪
- **本地文件**：`~/wiki/raw/` 目录下的 PDF、PPT、Word、Markdown 等，按文件名 + mtime 追踪

## 分类规则

- **不预设固定分类**，根据内容自动聚类
- 每次 Ingest 新内容时，判断归入现有分类还是创建新分类
- 分类粒度：太宽泛（如"工作"）没有意义，太细碎（如"2026年3月某会议"）也无价值，目标是"主题级别"
- 随 Wiki 增长，定期在 Lint 时合并过于细碎的分类

## Page 格式

每个 `pages/[主题名].md` 文件的结构：

```markdown
---
category: [分类名]
tags: [标签1, 标签2]
sources:
  - type: evernote | ima_note | local_file
    id: [guid / doc_id / 文件名]
    title: [原始标题]
last_updated: YYYY-MM-DD
---

# [主题名]

## 核心摘要
（3-5 句话，概括这个主题的核心要点）

## 详细内容
（要点、关键概念、重要数据、背景信息）

## 关联主题
- [[相关主题1]]
- [[相关主题2]]

## 来源记录
- [原始标题](来源类型) — YYYY-MM-DD
```

## Ingest 规则

1. 读取原始内容全文
2. 提取：核心主题、关键概念、重要观点、人物/产品/技术名词
3. 判断：内容应归入哪个现有 page？还是需要新建 page？
4. 更新 1-5 个相关 pages（更新 `详细内容` 和 `关联主题`）
5. 更新 `index.md`（如有新 page 或新分类）
6. 更新 `log.md`（记录已处理的来源 ID）

**重复内容处理**：同一主题从不同来源出现时，合并到同一 page，在"来源记录"里列出所有来源。

## Query 规则

1. 搜索 `pages/` 目录中相关内容
2. 综合多个 page 的信息回答
3. 有价值的回答（如综合分析）可通过 File Back 存为新 page

## Lint 规则（定期执行）

检查以下问题：
- 孤立 page（没有任何 `关联主题` 指向它）
- 内容矛盾（同一主题在不同 page 中有不一致的描述）
- 过时内容（来源中有更新版本但 page 未更新）
- 细碎分类（可以合并的 page）
- 缺失关联（两个 page 明显相关但没有互相链接）
