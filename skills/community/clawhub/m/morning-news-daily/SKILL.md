---
name: morning-news-daily
slug: morning-news-daily
description: >
  Daily morning news digest covering tech & finance.
  Collects latest news from global sources, curates top 20 items with one-line summaries + original links.
  Weekend news auto-merges into Monday delivery.
version: 1.3.0
metadata:
  openclaw:
    requires:
      bins:
        - curl
    emoji: "📰"
    homepage: https://clawhub.ai/BusTes01/morning-news-daily
    models:
      - gpt-4
      - deepseek-v4-flash
      - gemini-2.0-flash
      - claude-4-opus
---

# 📰 Morning Tech & Finance Digest

Automatically collects the latest tech and finance news from domestic and international sources, curating 20 concise items daily. Each item includes a one-line summary plus original link. Weekend news is cached and merged into Monday's delivery.

## Usage

User says: "morning news today"

The agent performs the following workflow:

### Step 1: News Collection

Use `web_search` to gather today's coverage from:
- **Tech**: TechCrunch, The Verge, ArsTechnica
- **Finance**: Bloomberg, Reuters, CNBC
- **AI**: ArsTechnica AI, VentureBeat AI

### Step 2: Curation & Ranking

Select top 20 items with priority:
1. Breaking / major events
2. Tech breakthroughs / product launches
3. Major capital market movements
4. Policy & regulation changes
5. Industry trend analysis

### Step 3: Format Output

Each item format:
```
📌 [Category] One-line summary
🔗 Original link
```

Category tags: 🚀 AI | 💹 Finance | 📱 Tech | 🏭 Industry | 🌐 Global

### Step 4: Weekend Merge Rule

- **Mon-Fri**: Normal daily delivery
- **Sat-Sun**: No delivery; news cached
- **Monday morning**: Deliver a "📦 Weekend + Monday Merged Edition" (~25-30 items)

## Output Example

```
📰 Morning Tech & Finance Digest · 2026-05-19 Tue

🚀 AI
• OpenAI released GPT-5 with 300% reasoning improvement
  🔗 https://example.com/gpt5
• Google Gemini 3.1 Pro launches with native video understanding
  🔗 https://example.com/gemini

💹 Finance
• Fed holds rates steady; market expects September cut
  🔗 https://example.com/fed
• NVIDIA market cap exceeds $4 trillion
  🔗 https://example.com/nvidia

📱 Tech
• Apple Vision Pro 2 delayed to 2027
  🔗 https://example.com/vision-pro
• Tesla Optimus robot starts trial run in factories
  🔗 https://example.com/optimus
```

## Custom Options

```
"Today's news, focus on AI and semiconductors"
"Finance section only"
"Filter Tencent-related news"
```

## Behavior Guidelines

1. **Objective & neutral** — Present facts without commentary
2. **High information density** — Every item worth reading
3. **Traceable sources** — Every item must have original link
4. **Priority on timeliness** — Prefer today's content
5. **No duplicates** — Same event appears only once

---

# 📰 晨间科技财经速递

每日自动收集国内外科技与财经领域的最新资讯，整理成20条精炼推送。每条包含一句话提要加原文链接。周末新闻自动缓存，周一合并推送。

## 使用方法

用户只需说："今天的早间新闻"

Agent 自动执行以下流程：

### 第一步：搜集新闻

使用 `web_search` 搜索当日最新资讯，覆盖以下来源：
- **科技**：TechCrunch、The Verge、ArsTechnica
- **财经**：Bloomberg、Reuters、CNBC
- **AI/大模型**：ArsTechnica AI、VentureBeat AI

### 第二步：筛选排序

精选20条，排序优先级：
1. 重大突发事件
2. 科技突破/产品发布
3. 资本市场重大变动
4. 政策法规变化
5. 行业趋势分析

### 第三步：格式化输出

每条格式：
```
📌 [分类] 一句话提要
🔗 原文链接
```

分类标签：🚀 AI｜💹 财经｜📱 科技｜🏭 行业｜🌐 国际

### 第四步：周末合并规则

- **周一至周五**：正常推送
- **周六/周日**：不推送，缓存
- **周一早上**：推送「📦 周末+周一融合版」（约25-30条）

## 输出示例

```
📰 晨间科技财经速递 · 2026年5月19日 周二

🚀 AI
• OpenAI发布GPT-5，推理能力提升300%
  🔗 https://example.com/gpt5
• Google Gemini 3.1 Pro上线，支持原生视频理解
  🔗 https://example.com/gemini

💹 财经
• 美联储维持利率不变，市场预期9月降息
  🔗 https://example.com/fed
• 英伟达市值突破4万亿美元
  🔗 https://example.com/nvidia

📱 科技
• 苹果Vision Pro 2代延期至2027年
  🔗 https://example.com/vision-pro
• 特斯拉Optimus机器人开始在工厂试运行
  🔗 https://example.com/optimus
```

## 自定义选项

```
"今日新闻，重点看AI和半导体"
"只看财经板块"
"筛选和腾讯相关的新闻"
```

## 行为准则

1. **客观中立** — 只陈述事实，不夹带观点
2. **高信息密度** — 每条都值得读
3. **来源可追溯** — 每条必须有原文链接
4. **时效优先** — 优先当日内容
5. **无重复** — 同一事件只出现一次
