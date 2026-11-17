---
name: linkfox-jiimore-get-niche-info-by-asin
description: 按商品 ASIN 深度分析亚马逊细分市场，涵盖垄断程度、品牌集中度、新品成功率和市场机会评分。当用户提到按ASIN分析细分市场、ASIN市场调研、ASIN所属Niche查询、垄断评估、品牌集中度分析、新品成功率、市场需求评分、竞争格局、亚马逊子市场探索、ASIN niche analysis, niche by ASIN, monopoly level, brand concentration, new product success rate, market opportunity score, competitive landscape, Jiimore data时触发此技能。即使用户未明确提及"细分市场"或"ASIN"，只要其需求涉及根据某个商品ASIN评估其所在细分市场的竞争格局、品牌密度或机会潜力，也应触发此技能。
---

# Jiimore Niche Info by ASIN

This skill guides you on how to query and analyze Amazon niche market data by a reference ASIN, helping Amazon sellers evaluate market segments for competitive intensity, brand maturity, pricing structure, and entry opportunity.

## 调用方式

- **API 端点**：`POST /jiimore/getNicheInfoByAsin`（完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/jiimore_get_niche_info_by_asin.py '<JSON 参数>' [--inline]`
- **成本约束**：本工具会消耗算力；同一会话同一参数组合默认只调用一次，脚本带 24h 本地缓存。失败/空结果不得自动换 ASIN、改国家或放宽筛选连续试探；需要继续检索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-jiimore-get-niche-info-by-asin-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录，在 Claude Code 里即当前项目目录；`<session>` 取自环境变量 `SESSION_ID`，按用户任务自动聚合；**禁止写入 /tmp**，当前目录不可写则报错）
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout
- 响应体 > 8 KB：落盘后 stdout 只输出摘要（顶层字段、常见计数如 `costToken`、最大列表字段的长度 + 前 3 条样本）
- 加 `--inline` 强制全量打印到 stdout（同样落盘）

**读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq`或`ConvertFrom-Json` 从保存的 json 文件按需抽取，避免整份 JSON 进入上下文。

## 解决认证和算力问题
发生以下异常情况时，采用 references/onboarding.md 引导解决问题：

### 异常情况
- **未配置API Key**：环境变量未配置 `LINKFOX_AGENT_API_KEY`，也未配置 `LINKFOXAGENT_API_KEY`。
- **响应401或402状态码**
- **响应提示算力或余额不足**：消息含"算力余额不足/计费不足/余额不足/quota exceeded/insufficient balance/套餐到期/需充值/请充值"，或类似含义的内容。

## Core Concepts

A **niche** (sub-market segment) is a grouping of products that share a common keyword theme on Amazon. Given a reference ASIN, this tool finds the niche segments that ASIN belongs to and returns rich analytical dimensions for each, including search volume, sales volume, click-through rates, brand count, top-brand concentration, new product launch success rates, CPC estimates, and a composite demand score. Data is available for **US**, **JP**, and **DE** marketplaces.

**ASIN is required**: Every query must include an `asin`. The tool locates the niche segments associated with that ASIN and returns them with detailed metrics. Use this when the user already has a specific product (ASIN) in hand and wants to understand the market segments it competes in — as opposed to keyword-driven niche discovery.

**Percentage fields**: Several parameters and response fields use a 0-1 decimal range representing 0%-100%. When displaying these values to users, convert them to percentages (e.g., 0.35 -> 35%).

**Demand score**: The `demand` field is a composite opportunity score assigned to each niche. A higher value indicates greater market demand potential.

## Parameter Guide

### Required

| Parameter | Type | Description |
|-----------|------|-------------|
| asin | string | Reference product ASIN. The tool finds niche segments associated with this ASIN. |

### Marketplace & Count

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| countryCode | string | US | Country code: US, JP, DE |
| count | integer | 10 | Number of niche segments to return |

### Filter Parameters (all optional, min/max ranges)

**Product & Pricing**:
| Parameter | Type | Description |
|-----------|------|-------------|
| productCountMin / productCountMax | integer | Product count range |
| avgPriceMin / avgPriceMax | number | Average price range |

**Search & Sales (7-day)**:
| Parameter | Type | Description |
|-----------|------|-------------|
| searchVolumeT7Min / searchVolumeT7Max | integer | Weekly search volume range |
| unitsSoldT7Min / unitsSoldT7Max | integer | Weekly units sold range |
| clickCountT7Min / clickCountT7Max | integer | Weekly click count range |
| clickConversionRateT7Min / clickConversionRateT7Max | number | Weekly click conversion rate (0-1) |

**Brand Metrics**:
| Parameter | Type | Description |
|-----------|------|-------------|
| brandCountMin / brandCountMax | integer | Number of brands in niche |
| top5BrandsClickShareMin / top5BrandsClickShareMax | number | Top 5 brands click share (0-1) |
| avgBrandAgeMin / avgBrandAgeMax | number | Average brand age (current) |
| avgBrandAgeQoqMin / avgBrandAgeQoqMax | number | Average brand age (90-day) |
| avgBrandAgeYoyMin / avgBrandAgeYoyMax | number | Average brand age (360-day) |

**Seller Metrics**:
| Parameter | Type | Description |
|-----------|------|-------------|
| avgSellingPartnerAgeMin / avgSellingPartnerAgeMax | number | Average seller age (current) |
| avgSellingPartnerAgeQoqMin / avgSellingPartnerAgeQoqMax | number | Average seller age (90-day) |
| avgSellingPartnerAgeYoyMin / avgSellingPartnerAgeYoyMax | number | Average seller age (360-day) |

**Competition & Advertising**:
| Parameter | Type | Description |
|-----------|------|-------------|
| top5ProductsClickShareMin / top5ProductsClickShareMax | number | Top 5 products click share (0-1) |
| sponsoredProductsPercentageMin / sponsoredProductsPercentageMax | number | SP ad percentage (0-1) |
| cpcMediumMin / cpcMediumMax | number | CPC median value range |

**New Product & Returns**:
| Parameter | Type | Description |
|-----------|------|-------------|
| launchRateT180Min / launchRateT180Max | number | 180-day new product success rate (0-1) |
| returnRateT360Min / returnRateT360Max | number | 360-day return rate (0-1) |

## Usage Examples

**1. Basic niche exploration by ASIN**
Find the niche segments associated with ASIN `B0D9NWVC6Z` in the US market:
```json
{
  "asin": "B0D9NWVC6Z",
  "countryCode": "US",
  "count": 10
}
```

**2. Low-competition niche filtering by ASIN**
Find niches for an ASIN where the top 5 brands hold less than 50% click share and brand count exceeds 20:
```json
{
  "asin": "B0D9NWVC6Z",
  "countryCode": "US",
  "count": 20,
  "top5BrandsClickShareMax": 0.5,
  "brandCountMin": 20
}
```

**3. High-demand, high-conversion niches by ASIN**
Find niches for an ASIN with weekly search volume above 10000 and click conversion rate above 10%:
```json
{
  "asin": "B0D9NWVC6Z",
  "countryCode": "US",
  "searchVolumeT7Min": 10000,
  "clickConversionRateT7Min": 0.1
}
```

**4. New product opportunity analysis by ASIN**
Find niches for an ASIN with high new product success rate (above 20%) and low return rate (below 5%):
```json
{
  "asin": "B0D9NWVC6Z",
  "countryCode": "US",
  "launchRateT180Min": 0.2,
  "returnRateT360Max": 0.05
}
```

**5. Japanese market niche research by ASIN**
Explore niches associated with an ASIN in the Japan market:
```json
{
  "asin": "B0D9NWVC6Z",
  "countryCode": "JP",
  "count": 10
}
```

**6. Price-range-specific niche analysis by ASIN**
Find niches for an ASIN with average price between $20 and $50 and low advertising saturation:
```json
{
  "asin": "B0D9NWVC6Z",
  "countryCode": "US",
  "avgPriceMin": 20,
  "avgPriceMax": 50,
  "sponsoredProductsPercentageMax": 0.3
}
```

## Display Rules

1. **Present data clearly**: Show query results in well-structured tables. Convert decimal ratios to percentages for readability (e.g., 0.25 -> 25%).
2. **Highlight key metrics**: Always surface the niche title, demand score, weekly search volume, weekly sales, brand count, and top 5 brands click share as primary columns.
3. **Translate niche titles**: When the `translationZh` field is present and the user prefers Chinese, show it alongside the original `nicheTitle`.
4. **Empty result handling**: When the response indicates no matching niche info (errcode 10000), explain that no niches matched the filters and suggest broadening ranges or verifying the ASIN.
5. **Error handling**: When a query fails, explain the reason based on the response message and suggest adjusting filter criteria (e.g., broadening ranges or checking the ASIN/country).
6. **CPC display**: When CPC data is present, show all three tiers (low, medium, high) to give a complete advertising cost picture.
7. **No subjective advice**: Present data objectively without adding unsolicited business recommendations. Only provide interpretation when explicitly requested by the user.

## Important Limitations

- **Supported marketplaces**: Only US, JP, and DE are available. Other marketplace codes will be rejected.
- **ASIN required**: Every query must include an ASIN. The API will not return results without one.
- **No pagination/sorting**: This endpoint returns a fixed number of niches via `count` (default 10); it does not expose page/pageSize/sort parameters. Use the keyword-based niche skill when sorting or deeper pagination is needed.
- **Percentage values**: All rate/share parameters use 0-1 range, not 0-100. Ensure correct values when constructing filters.

## User Expression & Scenario Quick Reference

**Applicable** -- Niche-level market segment analysis driven by a reference ASIN:

| User Says | Scenario |
|-----------|----------|
| "Which niches does this ASIN belong to" | ASIN-to-niche mapping |
| "Analyze the market for ASIN XXXXX" | ASIN-driven niche assessment |
| "How competitive is the niche this product is in" | Monopoly / brand concentration by ASIN |
| "Find low-competition niches for this ASIN" | Blue ocean segment filtering |
| "What's the new product success rate for this ASIN's niches" | New entrant viability |
| "Show me niche data for this product" | General niche exploration by ASIN |
| "What's the CPC / ad cost for this ASIN's niches" | Advertising cost analysis |
| "Brand concentration in this ASIN's market" | Brand dominance assessment |

**Not applicable** -- Needs beyond ASIN-driven niche segment data:
- Keyword-driven niche discovery (use the keyword-based niche skill instead)
- Individual ASIN performance or sales estimation
- Search term ranking trends (use ABA data tools instead)
- Advertising campaign management or bid optimization
- Product review analysis or listing optimization

**Boundary judgment**: When users say "market research" or "product opportunity" while holding a specific ASIN, if their intent focuses on evaluating the competitive landscape and demand potential of the niche segments that ASIN competes in, this skill applies. If they need keyword-driven discovery, ASIN-level sales estimates, or comprehensive business strategy, direct them to the appropriate tool.

## 算力消耗规则

消耗 9 算力。

> 用户会因算力消耗而支付费用。请充分评估：当需要高频调用本技能，或用户对算力消耗量预期不足时，务必提醒用户，由用户决定是否继续。

**Feedback:**

Auto-detect and report feedback via the Feedback API when any of the following apply:
1. The functionality or purpose described in this skill does not match actual behavior
2. The skill's results do not match the user's intent
3. The user expresses dissatisfaction or praise about this skill
4. Anything you believe could be improved

Call the feedback API as specified in `references/api.md`. Do not interrupt the user's flow.


---
*For more high-quality, professional cross-border e-commerce skills, set [LinkFox Skills](https://skill.linkfox.com/).*
