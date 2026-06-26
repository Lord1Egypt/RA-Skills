---
name: groundapi-web-researcher
description: Deep web research assistant — search, scrape, check trending topics, get daily briefings, and synthesize information from multiple sources into a structured report. Powered by GroundAPI MCP tools.
metadata:
  openclaw:
    requires:
      env: ["GROUNDAPI_KEY"]
    emoji: "🌐"
    homepage: "https://groundapi.net"
    primaryEnv: "GROUNDAPI_KEY"
---

# 网络调研助手

当用户需要对某个话题做深入了解，或类似以下表达时自动触发：
- "帮我调研一下 XXX"、"查一下 XXX 的情况"
- "XXX 的最新进展是什么"、"帮我了解一下 XXX"
- "对比一下 A 和 B"、"总结一下这个话题"
- "帮我搜一下..."、"研究一下..."
- "现在什么最火"、"今天有什么热点"

## 前置条件

本 Skill 依赖 GroundAPI MCP Server 提供的工具。确保已配置 GroundAPI MCP 连接：

```json
{
  "mcpServers": {
    "groundapi": {
      "url": "https://mcp.groundapi.net/mcp",
      "headers": {
        "X-API-Key": "sk_gapi_xxxxx"
      }
    }
  }
}
```

## 执行流程

### Step 1 — 拆解调研问题

将用户的调研需求拆解为 1-3 个搜索查询，覆盖不同角度。

示例：用户说"帮我调研一下固态电池的发展现状"
- 查询 1：`固态电池 技术进展 2026`（技术角度）
- 查询 2：`固态电池 产业链 公司 量产`（产业角度）
- 查询 3：`固态电池 市场规模 预测`（市场角度）

### Step 1.5 — 热度预判（可选）

调用 `info_trending()` 查看该话题是否在全网热搜中，了解当前舆论热度。
调用 `info_bulletin()` 获取每日新闻简报，看该话题是否在今日重点事件中。

如果话题正在热搜，优先使用 `recency="oneDay"` 获取最新信息。

### Step 2 — 搜索

对每个查询调用 `info_search(query="...", count=10, recency="oneMonth")`。

如果话题有时效性或正在热搜中，使用更短的 recency（`oneWeek` 或 `oneDay`）。

### Step 3 — 筛选与抓取

从搜索结果中挑选最相关、最权威的 3-5 个链接（优先选择：官方来源 > 权威媒体 > 行业报告 > 博客），调用 `info_scrape(url="...")` 获取全文。

如果某个 URL 抓取失败，跳过并使用搜索摘要代替。

### Step 4 — 综合输出

```
## 🌐 调研报告：{话题}

### 概述
（2-3 句话的核心结论）

### 关键发现

**1. {角度一标题}**
- 要点 A（来源：XXX）
- 要点 B（来源：XXX）

**2. {角度二标题}**
- 要点 A（来源：XXX）
- 要点 B（来源：XXX）

**3. {角度三标题}**
- 要点 A（来源：XXX）
- 要点 B（来源：XXX）

### 总结与观点
（基于多源信息的综合判断，标注哪些是事实、哪些是推测）

### 信息来源
1. [标题](URL) — 简要说明
2. [标题](URL) — 简要说明
3. ...
```

## 对比调研模式

当用户要求对比两个或多个事物时（如"对比 React 和 Vue"），调整流程：

1. 对每个对比对象分别搜索
2. 抓取各自最相关的 2-3 篇内容
3. 按统一维度做对比表格输出：

```
### 对比：A vs B

| 维度 | A | B |
|------|---|---|
| 维度1 | ... | ... |
| 维度2 | ... | ... |
| ... |

### 结论
（根据使用场景给出建议）
```

## 注意事项

- 始终标注信息来源，不要把不同来源的信息混在一起而不注明
- 区分"事实"（有明确数据支撑）和"观点"（来自分析/预测）
- 如果搜索结果质量不佳或信息过少，如实告知用户，不要编造内容
- 抓取网页时尊重内容：不要抓取明显需要付费阅读的内容
- 输出语言跟随用户
