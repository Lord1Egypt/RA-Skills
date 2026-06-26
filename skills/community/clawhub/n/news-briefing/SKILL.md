---
name: news-briefing
description: >
  Real-time AI news briefing for any topic. Say "给我看大谷翔平的新闻" or "AI今天有什么大新闻",
  and your agent instantly searches the web, summarizes the top stories in Chinese,
  and delivers a rich Feishu card with AI-powered deep insights — all collapsed cleanly
  for mobile reading.
  
  Trigger phrases: "看下XXX新闻", "查一下XXX最新动态", "XXX有什么新闻", "帮我追踪XXX", 
  "briefing on XXX", "给我XXX的情报"
version: 2.0.0
author: derekhsu529
tags: [news, briefing, ai-insights, feishu, realtime, chinese]
---

# 📰 News Briefing

> **让 AI Agent 成为你的私人情报官**  
> 任意话题 → 联网实时搜索 → 中文摘要 → AI深度洞察 → 飞书卡片，一句话触发。

## 为什么选 News Briefing？

| 普通新闻 App | News Briefing |
|------------|--------------|
| 固定频道，被动推送 | **任意话题**，主动触发 |
| 只有标题/摘要 | **AI深度洞察**：背景、逻辑、影响、信号 |
| 英文/日文混杂 | **全程中文**输出 |
| 需要打开 App | **飞书卡片**直达，不换 App |
| 每天定时推送 | **随时触发**，也支持定时 |

## 快速开始

### 对话触发（最简单）

直接对你的 Agent 说：
```
看下大谷翔平的新闻
AI今天有什么大新闻
两会最新动态
帮我查一下特斯拉近期消息
```

Agent 自动调用 News Briefing，发卡片到你的飞书。

### 命令行调用

```bash
# 单主题
node {baseDir}/scripts/news-digest.mjs \
  --topics "全球AI科技动态" \
  --categories "AI" \
  --title "🧠 AI情报简报" \
  --target-user ou_xxx

# 多主题合并（每日日报）
node {baseDir}/scripts/news-digest.mjs \
  --topics "全球AI科技,时政要闻" \
  --counts "5,5" \
  --categories "AI,GEO" \
  --title "📰 每日情报简报" \
  --target-user ou_xxx
```

## 卡片效果

每条新闻：
```
🧠 标题（25字以内，中文）
摘要一句话说清（50-60字，手机2-3行）

[📄 查看原文]
💡 查看AI洞察 ▼
  📌 背景：为何发生
  🔍 深层逻辑：核心驱动力  
  💥 影响：行业/市场影响
  👁 关注点：值得追踪的信号
```

## 参数说明

| 参数 | 说明 | 默认 |
|------|------|------|
| `--topics` | 主题（逗号分隔多个） | 必填 |
| `--counts` | 每主题条数 | `5` |
| `--categories` | `AI/GEO/SPORT/BIZ/CUSTOM` | `AI` |
| `--title` | 卡片标题 | 自动生成 |
| `--target-user` | 飞书 open_id | 必填 |
| `--no-insight` | 跳过 AI 洞察（更快） | - |
| `--date` | 指定日期 | 今天 |

## 环境变量

| 变量 | 必须 | 说明 |
|------|------|------|
| `FEISHU_APP_ID` | ✅ | 飞书 App ID |
| `FEISHU_APP_SECRET` | ✅ | 飞书 App Secret |
| `PERPLEXITY_API_KEY` | ✅ | 联网实时搜索（Perplexity sonar） |
| `PPIO_API_KEY` | 可选 | AI 洞察生成（缺少则跳过洞察） |
| `HTTPS_PROXY` | 可选 | 代理地址 |
| `TARGET_USER_ID` | 可选 | 默认接收人 open_id |

## 典型场景

```bash
# 🤖 AI 资讯
--topics "全球AI大模型最新进展" --categories "AI" --title "🧠 AI情报简报"
--topics "OpenAI/Anthropic/DeepSeek最新动态" --categories "AI"

# ⚾ 体育追踪
--topics "大谷翔平WBC最新动态" --categories "SPORT" --title "⚾ 大谷情报"
--topics "MLB道奇最新战报" --categories "SPORT"

# 🌍 时政财经
--topics "两会最新动态" --categories "GEO" --title "🏛️ 两会简报"
--topics "中美贸易最新进展" --categories "GEO"

# 💼 行业追踪
--topics "云计算IaaS市场动态" --categories "BIZ"
--topics "苹果最新产品消息" --categories "BIZ"

# 📰 每日综合日报（推荐配置）
--topics "全球AI科技,时政要闻" --counts "5,5" --categories "AI,GEO" --title "📰 每日情报简报"
```

## 定时推送（配合 OpenClaw Cron）

每天 8:30 自动推送：
```bash
# 在 OpenClaw 中设置 cron，执行：
node /path/to/news-briefing/scripts/news-digest.mjs \
  --topics "全球AI科技,时政要闻" \
  --title "📰 早间情报简报" \
  --target-user ou_xxx
```

---

*由 [OpenClaw](https://openclaw.ai) 提供支持 · 作者: [@derekhsu529](https://clawhub.com/u/derekhsu529)*
