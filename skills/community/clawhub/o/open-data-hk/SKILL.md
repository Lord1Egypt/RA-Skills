---
name: 香港开放数据访问服务
description: 一个提供香港政府官方开放数据门户DATA.GOV.HK数据访问的MCP服务器，支持数据集列表、详情查询、分类检索及格式筛选等功能。
version: 1.0.0
---

# 香港开放数据访问服务

一个提供香港政府官方开放数据门户DATA.GOV.HK数据访问的MCP服务器，支持数据集列表、详情查询、分类检索及格式筛选等功能。

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
| Get a list of dataset IDs from data.gov.hk

Args:
    limit: Maximum number of datasets to return (default: 1000)
    offset: Offset of the first dataset to return
    language: Language code (en, tc, sc) | `scripts.tools.list_datasets` |
| Get detailed information about a specific dataset

Args:
    dataset_id: The ID or name of the dataset to retrieve
    language: Language code (en, tc, sc)
    include_tracking: Add tracking information to dataset and resources | `scripts.tools.get_dataset_details` |
| Get a list of data categories (groups)

Args:
    order_by: Field to sort by ('name' or 'packages') - deprecated, use sort instead
    sort: Sorting of results ('name asc', 'package_count desc', etc.)
    limit: Maximum number of categories to return
    offset: Offset for pagination
    all_fields: Return full group dictionaries instead of just names
    language: Language code (en, tc, sc) | `scripts.tools.list_categories` |
| Get detailed information about a specific category (group)

Args:
    category_id: The ID or name of the category to retrieve
    include_datasets: Include a truncated list of the category's datasets
    include_dataset_count: Include the full package count
    include_extras: Include the category's extra fields
    include_users: Include the category's users
    include_groups: Include the category's sub groups
    include_tags: Include the category's tags
    include_followers: Include the category's number of followers
    language: Language code (en, tc, sc) | `scripts.tools.get_category_details` |
| Search for datasets by query term using the package_search API.

This function searches across dataset titles, descriptions, and other metadata
to find datasets matching the query term.

Args:
    query: The solr query string (e.g., "transport", "weather", "*:*" for all)
    limit: Maximum number of datasets to return (default: 10, max: 1000)
    offset: Offset for pagination
    language: Language code (en, tc, sc)

Returns:
    A dictionary containing:
    - count: Total number of matching datasets
    - results: List of matching datasets (up to limit)
    - has_more: Boolean indicating if there are more results available | `scripts.tools.search_datasets` |
| Get a list of file formats supported by data.gov.hk

Returns:
    A list of supported file formats | `scripts.tools.get_supported_formats` |
| Search for datasets and return faceted results for better data exploration.

Args:
    query: The solr query string
    language: Language code (en, tc, sc)

Returns:
    A dictionary containing:
    - count: Total number of matching datasets
    - search_facets: Faceted information about the results
    - sample_results: First 3 matching datasets | `scripts.tools.search_datasets_with_facets` |
| Get datasets that have resources in a specific file format.

Args:
    file_format: The file format to filter by (e.g., "CSV", "JSON", "GeoJSON")
    limit: Maximum number of datasets to return
    language: Language code (en, tc, sc)

Returns:
    A dictionary containing:
    - count: Total number of matching datasets
    - results: List of matching datasets | `scripts.tools.get_datasets_by_format` |

**如果参数不完整，使用 AskUserQuestion 向用户询问缺失的参数。**

---

## 工具函数说明

---

## scripts.tools.list_datasets
工具描述：Get a list of dataset IDs from data.gov.hk

Args:
    limit: Maximum number of datasets to return (default: 1000)
    offset: Offset of the first dataset to return
    language: Language code (en, tc, sc)
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|limit|null|false| |null|
|offset|null|false| |null|
|language|string|false|"en"|null|

---

## scripts.tools.get_dataset_details
工具描述：Get detailed information about a specific dataset

Args:
    dataset_id: The ID or name of the dataset to retrieve
    language: Language code (en, tc, sc)
    include_tracking: Add tracking information to dataset and resources
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|dataset_id|string|true| |null|
|language|string|false|"en"|null|
|include_tracking|boolean|false|false|null|

---

## scripts.tools.list_categories
工具描述：Get a list of data categories (groups)

Args:
    order_by: Field to sort by ('name' or 'packages') - deprecated, use sort instead
    sort: Sorting of results ('name asc', 'package_count desc', etc.)
    limit: Maximum number of categories to return
    offset: Offset for pagination
    all_fields: Return full group dictionaries instead of just names
    language: Language code (en, tc, sc)
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|order_by|string|false|"name"|null|
|sort|string|false|"title asc"|null|
|limit|null|false| |null|
|offset|null|false| |null|
|all_fields|boolean|false|false|null|
|language|string|false|"en"|null|

---

## scripts.tools.get_category_details
工具描述：Get detailed information about a specific category (group)

Args:
    category_id: The ID or name of the category to retrieve
    include_datasets: Include a truncated list of the category's datasets
    include_dataset_count: Include the full package count
    include_extras: Include the category's extra fields
    include_users: Include the category's users
    include_groups: Include the category's sub groups
    include_tags: Include the category's tags
    include_followers: Include the category's number of followers
    language: Language code (en, tc, sc)
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|category_id|string|true| |null|
|include_datasets|boolean|false|false|null|
|include_dataset_count|boolean|false|true|null|
|include_extras|boolean|false|true|null|
|include_users|boolean|false|true|null|
|include_groups|boolean|false|true|null|
|include_tags|boolean|false|true|null|
|include_followers|boolean|false|true|null|
|language|string|false|"en"|null|

---

## scripts.tools.search_datasets
工具描述：Search for datasets by query term using the package_search API.

This function searches across dataset titles, descriptions, and other metadata
to find datasets matching the query term.

Args:
    query: The solr query string (e.g., "transport", "weather", "*:*" for all)
    limit: Maximum number of datasets to return (default: 10, max: 1000)
    offset: Offset for pagination
    language: Language code (en, tc, sc)

Returns:
    A dictionary containing:
    - count: Total number of matching datasets
    - results: List of matching datasets (up to limit)
    - has_more: Boolean indicating if there are more results available
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|query|string|false|"*:*"|null|
|limit|integer|false|10.0|null|
|offset|integer|false|0.0|null|
|language|string|false|"en"|null|

---

## scripts.tools.get_supported_formats
工具描述：Get a list of file formats supported by data.gov.hk

Returns:
    A list of supported file formats
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|

---

## scripts.tools.search_datasets_with_facets
工具描述：Search for datasets and return faceted results for better data exploration.

Args:
    query: The solr query string
    language: Language code (en, tc, sc)

Returns:
    A dictionary containing:
    - count: Total number of matching datasets
    - search_facets: Faceted information about the results
    - sample_results: First 3 matching datasets
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|query|string|false|"*:*"|null|
|language|string|false|"en"|null|

---

## scripts.tools.get_datasets_by_format
工具描述：Get datasets that have resources in a specific file format.

Args:
    file_format: The file format to filter by (e.g., "CSV", "JSON", "GeoJSON")
    limit: Maximum number of datasets to return
    language: Language code (en, tc, sc)

Returns:
    A dictionary containing:
    - count: Total number of matching datasets
    - results: List of matching datasets
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|file_format|string|true| |null|
|limit|integer|false|10.0|null|
|language|string|false|"en"|null|

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