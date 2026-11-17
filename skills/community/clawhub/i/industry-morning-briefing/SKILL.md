---
---
name: industry-morning-briefing
description: "Generate a structured morning briefing for a given industry by检索公开网页 (public web search + fetch). Focus on today's developments: highlights, policy/regulation, supply chain/company moves, implications, and watch items. Use when the user asks for a morning briefing, daily roundup, or today's news summary for an industry. NOT for: historical deep dives, financial investment advice, or vendor-specific product pitches."
homepage: https://github.com/openclaw/clawhub
metadata:
  {
    "openclaw":
      {
        "emoji": "📈",
        "requires": {},
        "install": [],
      },
  }
---

# Industry Morning Briefing Skill

Generate a structured, day-focused briefing for a target industry using public web search and page fetch.

## When to Use

✅ **USE this skill when:**

- "Give me today's [industry] morning briefing"
- "What's the latest in [industry] today?"
- "[Industry] daily roundup / news summary"
- "新能源行业晨报" (New energy industry morning briefing)

## When NOT to Use

❌ **DON'T use this skill when:**

- Historical deep dives or trend analysis spanning weeks/months
- Investment advice, stock picks, or financial forecasts
- Vendor-specific product pitches or comparative shopping
- Severe weather, disaster response, or non-industry topics

## Briefing Structure

The output should be structured with these sections (in English or Chinese, matching the user's language):

- **重点新闻 / Highlights** — top 3–5 today's stories
- **政策 & 监管 / Policy & Regulation** — regulatory/policy moves
- **产业链 & 公司动向 / Supply Chain & Company Moves** — public announcements, orders, M&A, capacity changes
- **潜在影响 / Implications** — what this means for stakeholders (costs, timeline, risk, opportunity)
- **需跟踪事项 / Watch Items** — upcoming dates, reports, decisions to track

## Workflow

1. **Search**: Use the web search tool with query `"[industry] today news"` or localized equivalent.
   - Example: `"新能源行业 今日 新闻"`
   - Prefer results from today/yesterday (filter by `freshness=day` when available).
2. **Fetch**: For up to 3–5 top results, fetch readable content via the web fetch tool.
3. **Synthesize**: Collate into the structured briefing above.
4. **Cite**: Include source URLs inline for each claim when feasible.

## Example (New Energy Industry)

```
Query: "新能源行业 今日 新闻"
Sources: top 4 search results (人民日报财经、36氪、路透中文、公司公告).
```

Output (Chinese):

```
# 新能源行业晨报 · 今日要点

## 重点新闻
- [新闻1] …（一句话摘要） 来源：URL
- [新闻2] … 来源：URL

## 政策 & 监管
- 发改委 / 能源局 动态
- 补贴、并网、碳指标

## 产业链 & 公司动向
- 电池/材料/车企 订单、扩产、价格变动
- 海外动态（欧美限制、出口数据）

## 潜在影响
- 上游材料成本、盈利分化、装机节奏
- 出口风险与应对

## 需跟踪事项
- 下次数据发布日期（中汽协、装机数据）
- 重要会议/政策窗口期
```

## Notes

- No API key required; uses public search + fetch.
- Rate limited by search provider; avoid rapid repeated queries.
- Keep summaries factual; avoid predicting prices or giving investment advice.
- If few today results appear, use yesterday's latest and state the date explicitly.
