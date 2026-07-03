---
name: OECD数据查询服务
description: 一个通过SDMX API提供OECD全面统计数据的模型上下文协议（MCP）服务器，支持AI助手和聊天机器人查询经济、健康、教育、环境等OECD数据集。
version: 1.0.0
---

# OECD数据查询服务

一个通过SDMX API提供OECD全面统计数据的模型上下文协议（MCP）服务器，支持AI助手和聊天机器人查询经济、健康、教育、环境等OECD数据集。

---

## ⚠️ 强制要求：API 密钥

**此 Skill 必须配置 API 密钥才能使用。**

- 首次使用时，如果 `.env` 中没有 `XBY_APIKEY`，**必须使用 AskUserQuestion 工具向用户询问 API 密钥**
- 拿到用户提供的密钥后，调用 `scripts.config.set_api_key(api_key)` 保存，然后继续处理
- 获取 API 密钥：https://xiaobenyang.com
- **禁止**在缺少 API 密钥时自行搜索或编造数据

---

## 工作流程（必须遵守）

你（大模型）是路由层，负责理解用户意图、选择工具、提取参数。代码只负责调用API。

```
用户输入 → 你选择工具 → 提取该工具需要的参数 → 调用 scripts.tools 中的函数 → 返回结果给用户
```

### 步骤

1. **检查 API 密钥**：如果 `scripts.config.settings.api_key` 为空，使用 AskUserQuestion 询问用户，拿到后调用 `scripts.config.set_api_key(key)` 保存
2. **选择工具**：根据用户意图从下方工具列表中选择对应的工具函数
3. **提取参数**：根据选中的工具，提取该工具需要的参数
4. **调用工具**：使用**关键字参数**调用 `scripts.tools` 中的函数，例如 `scripts.tools.search_schools(score='520', province='北京', category='综合')`
5. **返回结果**：将工具返回的 `raw` 数据整理后展示给用户

---
## 工具选择规则

根据用户意图选择对应的工具函数：

| 用户意图 | 工具函数 | 
|---------|---------|
| Search for OECD datasets (dataflows) by keyword. Returns matching datasets with their IDs, names, and descriptions. | `scripts.tools.search_dataflows` |
| List available OECD dataflows (datasets), optionally filtered by category. Use this to browse datasets by topic area. | `scripts.tools.list_dataflows` |
| Get the metadata and structure of a specific OECD dataset. Returns dimensions, attributes, and valid values for querying data. | `scripts.tools.get_data_structure` |
| Query actual statistical data from an OECD dataset. ⚠️ IMPORTANT: Defaults to last 100 observations (max 1000) to protect context window. Use filters, time periods, or last_n_observations to control data size. Large datasets (e.g. SOCX_AGG) can have 70,000+ observations - always specify limits! | `scripts.tools.query_data` |
| Get all available OECD data categories (17 categories covering all topics: Economy, Health, Education, Environment, etc.) | `scripts.tools.get_categories` |
| Get a curated list of commonly used OECD datasets across all categories. | `scripts.tools.get_popular_datasets` |
| Search for specific economic or social indicators by keyword (e.g., "inflation", "unemployment", "GDP"). | `scripts.tools.search_indicators` |
| Generate an OECD Data Explorer URL for a dataset. Use this to provide users with a direct link to explore data visually in their browser. | `scripts.tools.get_dataflow_url` |
| Get all OECD data categories with example datasets for each category. Returns comprehensive information about all 17 categories. | `scripts.tools.list_categories_detailed` |

**如果参数不完整，使用 AskUserQuestion 向用户询问缺失的参数。**

---

## 工具函数说明

---

## scripts.tools.search_dataflows
工具描述：Search for OECD datasets (dataflows) by keyword. Returns matching datasets with their IDs, names, and descriptions.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|query|string|true| |Search query to find relevant datasets|
|limit|number|false|20.0|Maximum number of results to return (default: 20)|

---

## scripts.tools.list_dataflows
工具描述：List available OECD dataflows (datasets), optionally filtered by category. Use this to browse datasets by topic area.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|category|string|false| |Optional category filter: ECO, HEA, EDU, ENV, TRD, JOB, NRG, AGR, GOV, SOC, DEV, STI, TAX, FIN, TRA, IND, REG|
|limit|number|false|50.0|Maximum number of results (default: 50)|

---

## scripts.tools.get_data_structure
工具描述：Get the metadata and structure of a specific OECD dataset. Returns dimensions, attributes, and valid values for querying data.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|dataflow_id|string|true| |Dataflow ID (e.g., "QNA", "MEI", "HEALTH_STAT")|

---

## scripts.tools.query_data
工具描述：Query actual statistical data from an OECD dataset. ⚠️ IMPORTANT: Defaults to last 100 observations (max 1000) to protect context window. Use filters, time periods, or last_n_observations to control data size. Large datasets (e.g. SOCX_AGG) can have 70,000+ observations - always specify limits!
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|dataflow_id|string|true| |Dataflow ID to query|
|filter|string|false| |Dimension filter (e.g., "USA.GDP.." for US GDP). Use "*" or "all" for all values. Get structure first to see valid dimensions.|
|start_period|string|false| |Start period (e.g., "2020-Q1", "2020-01")|
|end_period|string|false| |End period (e.g., "2023-Q4", "2023-12")|
|last_n_observations|number|false| |Get only the last N observations (default: 100, max: 1000 to protect against context overflow)|

---

## scripts.tools.get_categories
工具描述：Get all available OECD data categories (17 categories covering all topics: Economy, Health, Education, Environment, etc.)
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|

---

## scripts.tools.get_popular_datasets
工具描述：Get a curated list of commonly used OECD datasets across all categories.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|

---

## scripts.tools.search_indicators
工具描述：Search for specific economic or social indicators by keyword (e.g., "inflation", "unemployment", "GDP").
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|indicator|string|true| |Indicator to search for|
|category|string|false| |Optional category filter|

---

## scripts.tools.get_dataflow_url
工具描述：Generate an OECD Data Explorer URL for a dataset. Use this to provide users with a direct link to explore data visually in their browser.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|dataflow_id|string|true| |Dataflow ID|
|filter|string|false| |Optional dimension filter|

---

## scripts.tools.list_categories_detailed
工具描述：Get all OECD data categories with example datasets for each category. Returns comprehensive information about all 17 categories.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|

---


---

## 返回值处理

工具函数返回 `dict` 对象：
- `result["raw"]` - API 原始返回数据（JSON），**直接将此数据整理后展示给用户**
- `result["success"]` - 是否成功（True/False）
- `result["message"]` - 状态消息

---

## 项目结构

```
xiaobenyang_gaokao_skill/
├── scripts/
│   ├── __init__.py
│   ├── config.py       # 配置管理 + set_api_key()
│   ├── call_api.py      # API 客户端 + call_api()
│   └── tools.py         # 工具函数（直接调用）
├── requirements.txt
└── SKILL.md
```

---

## 注意事项

1. **API 密钥是必需的**，无密钥时必须通过 AskUserQuestion 询问用户
2. **禁止**在缺少 API 密钥时自行搜索或编造数据