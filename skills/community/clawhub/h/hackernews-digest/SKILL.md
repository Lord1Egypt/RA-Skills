---
name: hackernews-digest
description: |
  获取 Hacker News 热门文章并生成每日摘要。对每篇文章进行总结、提炼核心要点、给出可实践建议、灵感启发，以及生成社交媒体分享文案（即刻 + 小红书 + Twitter/X）。
  触发场景：用户提到 "HN 摘要"、"Hacker News 日报"、"hackernews digest"、"今日 HN"、"HN 热门"、"技术日报" 等。即使用户只说 "看看今天 HN 有什么"，也应触发此技能。
---

# Hacker News 每日摘要技能

获取 Hacker News Top 10 热门文章，并行抓取原文内容，生成摘要、核心要点、可实践建议、灵感启发及社交媒体分享文案，汇总为一篇每日精选文档。

## 配置

| 配置方式 | 优先级 | 示例 |
|---------|--------|------|
| 命令行参数 `--base-dir` | 最高 | `/hackernews-digest --base-dir /tmp/hn` |
| 环境变量 `HN_DIGEST_BASE_DIR` | 中 | `export HN_DIGEST_BASE_DIR=...` |
| 默认值 | 最低 | `/Users/victor/Desktop/resource/daily-info/hacknews` |

路径规则（`{YYYYMMDD}` 为当天日期）：
- 临时目录：`{BASE_DIR}/{YYYYMMDD}/temp/`
- 最终文档：`{BASE_DIR}/{YYYYMMDD}/hackernews-daily-{YYYYMMDD}.md`

## 依赖

- **autocli**: 获取 Hacker News 热门文章列表
- **WebFetch**: 抓取文章原文内容

## 执行流程

### Step 1: 初始化

1. 按优先级确定 `BASE_DIR`（参数 > 环境变量 > 默认值）
2. 获取当天日期，计算 `TEMP_DIR` 和 `OUTPUT_DIR`
3. **检查并清理已存在文件**：
   - 检查 `{OUTPUT_DIR}/hackernews-daily-{YYYYMMDD}.md` 是否存在
   - 如果存在，先删除该文件及 `{TEMP_DIR}` 目录下的所有临时文件 和 `{OUTPUT_DIR}/hackernews-daily-{YYYYMMDD}.md`
4. `mkdir -p {TEMP_DIR}` 

### Step 2: 获取热门文章列表

```bash
autocli hackernews top --limit 10 --format json
```

### Step 3: 并行抓取与分析

为每篇文章创建一个并行 Agent，每个 Agent：

1. 使用 WebFetch 抓取原文内容
2. 按模板生成分析内容
3. 写入临时文件 `{TEMP_DIR}/{rank}-{sanitized_title}.md`

**Agent 输出模板：**

```markdown
## [序号]. [文章标题]

> 原文链接：[url]
> 得分：[score] | 评论数：[comments] | 作者：[author]

### 摘要
3-5 句话总结核心内容，准确、信息密度高。

### 核心要点
- （3-5 个关键要点）

### 可实践建议
2-3 条可立即付诸行动的具体建议。

### 灵感启发
思维模型、跨领域启发、值得深入探索的方向。1-2 段。

### 社交媒体分享文案

**即刻：**
口语化、有观点、适度 emoji、200 字以内，含 #HackerNews #技术日报

**小红书：**
标题党风格标题 + 正文，善用 emoji，300 字以内，带话题标签

**Twitter/X：**
使用简体中文, 简洁有力，280 字符以内，带 hashtag
```

### Step 4: 汇总生成最终文档

读取临时文件，按 rank 排序合并，写入 `{OUTPUT_DIR}/hackernews-daily-{YYYYMMDD}.md`：

```markdown
---
title: "Hacker News 每日精选 - {YYYY-MM-DD}"
date: {ISO 8601}
description: "今日 Hacker News Top 10 热门文章摘要与深度解读"
tags:
  - HackerNews
  - 技术日报
  - Daily Digest
categories:
  - 技术
---

# Hacker News 每日精选 - {YYYY-MM-DD}

> 本文精选今日 Hacker News 热门 Top 10 文章，为每篇文章提供摘要、核心要点、可实践建议、灵感启发及社交媒体分享文案。

---

{按 rank 顺序合并所有文章分析内容}

---

## 今日总结

（整体观察：共同趋势、值得关注的话题、给读者的建议。3-5 句话。）
```

## 注意事项

1. **并行化**：10 篇文章必须并行抓取分析
2. **容错**：URL 不可访问时, 使用 autocli 动态判断获取 URL 对应内容，如果还是不行使用 agent-browser 获取内容.
3. **语言**：中文撰写
4. **文案风格**：即刻轻松有态度、小红书吸睛有干货、Twitter 简洁专业
