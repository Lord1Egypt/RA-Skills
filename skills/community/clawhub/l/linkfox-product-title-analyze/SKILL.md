---
name: linkfox-product-title-analyze
description: 对产品标题进行分词分析，提取词频、场景词、人群词、材质词等属性维度。当用户想分析产品标题、提取标题高频词、进行标题分词、发现场景词或人群词、对比不同商品的标题关键词用法、基于词频优化Listing标题、识别一组ASIN中的常见属性规律、title tokenization, word frequency analysis, scene keyword extraction, audience keyword analysis, title optimization, attribute keyword extraction, keyword frequency时触发此技能。即使用户未明确说"标题分析"，只要其需求涉及将产品标题拆解为有意义的词组、统计关键词频率或按提取的属性对商品分组，也应触发此技能。
---

# Product Title Analyzer

This skill guides you on how to tokenize and analyze product titles from previously queried products, helping Amazon sellers extract keyword patterns, scene words, audience words, and other attribute dimensions from product listing titles.

## Core Concepts

Product Title Analysis performs intelligent tokenization on product titles that have already been retrieved in the current conversation. It uses LLM-powered analysis to extract structured attributes (scene words, audience words, materials, colors, etc.) from free-text titles, then groups and counts them for pattern discovery.

**Automatic data aggregation**: The tool automatically collects products from all prior steps in the current conversation turn -- even across paginated queries. You do NOT need to manually pass product data unless you are referencing data from a previous conversation turn.

**One dimension per request**: Each call should analyze exactly ONE attribute dimension (e.g., scene words OR audience words). Do NOT request multiple dimensions in a single call.

## Data Fields

### Request Fields

| Field | API Name | Required | Description | Example |
|-------|----------|----------|-------------|---------|
| Analysis Request | tokenizationAndCountingRequest | Yes | Natural-language instruction describing which attribute dimension to extract from titles | "Count scene words in product titles" |
| Output Mode | outputMode | No | How multi-value attributes are returned. `MULTIPLE_RECORDS` (default): one record per value. `COMMA_SEPARATED`: all values in one record | MULTIPLE_RECORDS |
| Reference Data | refResultData | No | Externally supplied product data (only needed when referencing data from a previous conversation turn) | (JSON string) |

### Response Fields -- Product Attributes

| Field | API Name | Description | Example |
|-------|----------|-------------|---------|
| ASIN | asin | Product ASIN identifier | B0XXXXXXXX |
| Product Title | title | Original product title | Portable Camping Lantern... |
| Attribute Name | attributeName | Extracted attribute category | Scene Word |
| Attribute Value | attributeValue | Extracted attribute value | Outdoor / Camping |
| Price | price | Product price | 29.99 |
| Monthly Sales | monthlySalesUnits | Monthly unit sales | 1200 |
| Monthly Revenue | monthlySalesRevenue | Monthly sales revenue | 35988 |
| Rating | rating | Product rating | 4.5 |
| Rating Count | ratings | Number of ratings | 3820 |
| Available Date | availableDate | Listing date | 2024-03-15 |
| Brand | brand | Brand name | BrandX |
| Image URL | imageUrl | Main product image | https://... |

### Response Fields -- Attribute Groups

| Field | API Name | Description |
|-------|----------|-------------|
| Attribute Name | attributeName | The attribute category for this group (e.g., "Scene Word") |
| Attribute Value | attributeValue | A specific value within the group (e.g., "Outdoor") |
| Count | count | Number of products sharing this attribute value |
| ASIN List | asins | List of ASINs that share this attribute value |

### Response Metadata

| Field | API Name | Description |
|-------|----------|-------------|
| Render Type | type | UI rendering style |
| Columns | columns | Column definitions for table rendering |
| Source Type | sourceType | Data source type |
| Token Cost | costToken | Total LLM tokens consumed (input + output) |

## Parameter Guide

### tokenizationAndCountingRequest Examples

The `tokenizationAndCountingRequest` parameter is a natural-language instruction telling the tool which dimension to analyze. Keep it focused on a single dimension.

**Scene words (where / when the product is used)**
```
Count scene words appearing in product titles
```

**Audience / target-user words (who the product is for)**
```
Count audience words appearing in product titles
```

**Material words**
```
Count material-related words appearing in product titles
```

**Function / feature words**
```
Count function or feature words appearing in product titles
```

**Incorrect -- multiple dimensions in one request (do NOT do this)**
```
Count scene words AND audience words in product titles
```
Split this into two separate calls instead.

### outputMode

| Value | Behavior | When to Use |
|-------|----------|-------------|
| MULTIPLE_RECORDS | Each attribute value becomes its own record (default) | Most analysis -- easier to count, sort, and group |
| COMMA_SEPARATED | Multiple values stay in one record, comma-separated | When you want to see all attributes per ASIN at a glance |

## Display Rules

1. **Present data in tables**: Show extracted attributes and their frequencies in clear, sortable tables
2. **Highlight top keywords**: Call out the most frequent attribute values so patterns are immediately visible
3. **Group summary first**: When `attributeGroups` is returned, present the grouped summary before the per-product detail
4. **One dimension at a time**: If the user wants multiple dimensions analyzed, run separate calls and present results sequentially
5. **Token cost awareness**: The response includes `costToken`; do not display it unless the user asks about usage
6. **Error handling**: If the tool returns an error, explain the reason and suggest corrective action (e.g., "No products found in current conversation -- please query products first")
## Applicable Scenarios

| User Says | Scenario |
|-----------|----------|
| "What scene words appear in these titles?" | Scene-word extraction |
| "Analyze title keywords", "title word frequency" | General title tokenization |
| "What audience are these products targeting?" | Audience-word extraction |
| "Common materials in these listings" | Material-word extraction |
| "Help me optimize my title based on competitors" | Competitive title keyword analysis |
| "What words do top sellers use in titles?" | High-frequency keyword discovery |
| "Group these products by title attributes" | Attribute-based product grouping |

## Not Applicable Scenarios

- **No products queried yet**: The tool requires products to already exist in the conversation context. Prompt the user to search for products first.
- **Advertising / PPC keyword suggestions**: This tool analyzes existing titles, not ad keywords.
- **Full listing copywriting**: This tool extracts and counts words; it does not generate new titles.
- **Backend search term analysis**: This is for visible title analysis, not hidden search terms.
- **ABA search term data**: Use the ABA Data Explorer skill instead.

## API Usage

This tool calls the LinkFox tool gateway API. See `references/api.md` for calling conventions, request parameters, and response structure. You can also execute `scripts/title_analyze.py` directly to run queries.


**Feedback:**

Auto-detect and report feedback via the Feedback API when any of the following apply:
1. The functionality or purpose described in this skill does not match actual behavior
2. The skill's results do not match the user's intent
3. The user expresses dissatisfaction or praise about this skill
4. Anything you believe could be improved

Call the feedback API as specified in `references/api.md`. Do not interrupt the user's flow.

---
*For more high-quality, professional cross-border e-commerce skills, set [LinkFox Skills](https://skill.linkfox.com/).*
