---
name: linkfox-google-trends-rising
description: 查询并分析Google Trends在指定时间范围和国家/地区的实时热门话题与热搜。当用户提到谷歌趋势、热门话题、实时热搜、流行趋势、当前热点、近期热门、病毒式话题、时间段热度、区域趋势分析、Google Trends, real-time hot topics, trending topics, popular trends, recent trending searches, trend discovery时触发此技能。即使用户未明确说"Google Trends"，只要其需求涉及发现特定市场近期热门或正在流行的话题和搜索词，也应触发此技能。
---

# Google Trends Time-Range Analysis

This skill guides you on how to query and analyze Google Trends data for trending topics within a configurable time window, helping users discover real-time popular searches and emerging trends across 18 supported regions.

## Core Concepts

Google Trends reflects real user search interest on Google. This tool retrieves **trending topics** (recently popular queries) for a chosen country/region over a specified number of recent days. It is ideal for spotting what is currently gaining traction in a market.

**Key data points per trending query**:
- **query** -- the trending search term
- **searchVolume** -- relative search volume value
- **increasePercentage** -- percentage change in search interest (-100 to 100, unit: %)
- **startTime / endTime** -- timestamps bounding the trend observation window

A positive `increasePercentage` means rising interest; a negative value means declining interest. A value near 100 signals an explosive spike.

## Parameter Guide

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| days | integer | No | 7 | Time range in days. Common values: 1 (last 24 hours), 2, 7 (past week) |
| region | string | No | US | Country/region code. See Supported Regions below |

### Supported Regions

US (United States), GB (United Kingdom), JP (Japan), CA (Canada), MX (Mexico), DE (Germany), FR (France), IT (Italy), ES (Spain), NL (Netherlands), AU (Australia), SG (Singapore), AE (United Arab Emirates), BR (Brazil), IN (India), TR (Turkey), PL (Poland), SE (Sweden)

Default region is **US**. Use US when the user does not specify a region.

## API Usage

This tool calls the LinkFox tool gateway API. See `references/api.md` for calling conventions, request parameters, and response structure. You can also execute `scripts/google_trends_rising.py` directly to run queries.

## Usage Examples

**1. What's trending in the US over the past week?**
```json
{"days": 7, "region": "US"}
```

**2. Hot topics in Japan in the last 24 hours**
```json
{"days": 1, "region": "JP"}
```

**3. Trending searches in Germany over the past 2 days**
```json
{"days": 2, "region": "DE"}
```

**4. Recent buzz in Brazil this week**
```json
{"days": 7, "region": "BR"}
```

**5. What's gaining popularity in the UK right now?**
```json
{"days": 1, "region": "GB"}
```

## Display Rules

1. **Present data clearly**: Show trending queries in a well-formatted table with columns for query, search volume, and increase percentage. Sort by search volume or increase percentage as appropriate.
2. **Highlight spikes**: When `increasePercentage` is notably high (e.g., above 50%), call attention to these breakout topics.
3. **Time context**: Always state the time range and region in your summary so the user knows exactly what window the data covers.
4. **Chart data**: If the response includes `chartOption`, describe the chart structure (title, axes, data points) so the user understands the visual trend.
5. **Error handling**: When a query fails, explain the reason based on the error response and suggest adjusting parameters (e.g., try a different region code or time range).
## Important Limitations

- **Unstructured data**: Results from this tool are unstructured and cannot be fed into secondary SQL-based query tools for further processing.
- **Relative volumes**: Search volume values are relative, not absolute counts.
- **Short time windows**: The `days` parameter controls recency; this tool is designed for recent/real-time trends, not long historical analysis.
- **Region coverage**: Only the 18 listed regions are supported. Unsupported region codes will produce errors.

## User Expression & Scenario Quick Reference

**Applicable** -- Queries about trending/popular topics on Google:

| User Says | Scenario |
|-----------|----------|
| "What's trending right now" | Real-time trending topics |
| "Hot searches in [country]" | Regional trend discovery |
| "What topics are popular this week" | Weekly popularity overview |
| "Any viral topics in [market]" | Breakout / spike detection |
| "Show me Google Trends for [region]" | Region-specific trend query |
| "What's buzzing in the last 24 hours" | Short-window trend scan |
| "Trending searches in [country] recently" | Recent trend analysis |
| "What are people searching for in [region]" | General search interest exploration |

**Not applicable** -- Needs beyond trending topic discovery:

- Historical keyword search volume over months/years (use a dedicated Google Trends historical tool)
- Amazon-specific keyword or ASIN analysis (use ABA tools)
- Advertising / PPC campaign management
- Social media trend analysis (Twitter/X, TikTok, etc.)
- SEO ranking or backlink analysis
- Competitor website traffic estimation

**Boundary judgment**: When users say "market trends" or "what's popular", if it boils down to discovering what people are currently searching for on Google in a specific region, this skill applies. If they are asking about stock market trends, social media virality, or long-term historical search patterns, it does not apply.


**Feedback:**

Auto-detect and report feedback via the Feedback API when any of the following apply:
1. The functionality or purpose described in this skill does not match actual behavior
2. The skill's results do not match the user's intent
3. The user expresses dissatisfaction or praise about this skill
4. Anything you believe could be improved

Call the feedback API as specified in `references/api.md`. Do not interrupt the user's flow.

---
*For more high-quality, professional cross-border e-commerce skills, set [LinkFox Skills](https://skill.linkfox.com/).*
