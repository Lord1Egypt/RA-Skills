---
name: 菲律宾地理编码服务
description: 提供菲律宾标准地理编码（PSGC）API访问的模型上下文协议（MCP）服务器，包含完整的菲律宾地理层级数据。
version: 1.0.0
---

# 菲律宾地理编码服务

提供菲律宾标准地理编码（PSGC）API访问的模型上下文协议（MCP）服务器，包含完整的菲律宾地理层级数据。

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
| List all island groups in the Philippines | `scripts.tools.get_island_groups` |
| Get specific island group by code | `scripts.tools.get_island_group` |
| Get all regions within a specific island group | `scripts.tools.get_island_group_regions` |
| Get all provinces within a specific island group | `scripts.tools.get_island_group_provinces` |
| Get all cities within a specific island group | `scripts.tools.get_island_group_cities` |
| Get all municipalities within a specific island group | `scripts.tools.get_island_group_municipalities` |
| Get all barangays within a specific island group | `scripts.tools.get_island_group_barangays` |
| List all regions in the Philippines | `scripts.tools.get_regions` |
| Get specific region by code | `scripts.tools.get_region` |
| Get all provinces within a specific region | `scripts.tools.get_region_provinces` |
| Get all districts within a specific region | `scripts.tools.get_region_districts` |
| Get all cities within a specific region | `scripts.tools.get_region_cities` |
| Get all municipalities within a specific region | `scripts.tools.get_region_municipalities` |
| Get all cities and municipalities within a specific region | `scripts.tools.get_region_cities_municipalities` |
| Get all sub-municipalities within a specific region | `scripts.tools.get_region_sub_municipalities` |
| Get all barangays within a specific region | `scripts.tools.get_region_barangays` |
| List all provinces in the Philippines | `scripts.tools.get_provinces` |
| Get specific province by code | `scripts.tools.get_province` |
| Get all cities within a specific province | `scripts.tools.get_province_cities` |
| Get all municipalities within a specific province | `scripts.tools.get_province_municipalities` |
| Get all cities and municipalities within a specific province | `scripts.tools.get_province_cities_municipalities` |
| Get all sub-municipalities within a specific province | `scripts.tools.get_province_sub_municipalities` |
| Get all barangays within a specific province | `scripts.tools.get_province_barangays` |
| List all cities in the Philippines | `scripts.tools.get_cities` |
| Get specific city by code | `scripts.tools.get_city` |
| Get all barangays within a specific city | `scripts.tools.get_city_barangays` |
| List all municipalities in the Philippines | `scripts.tools.get_municipalities` |
| Get specific municipality by code | `scripts.tools.get_municipality` |
| Get all barangays within a specific municipality | `scripts.tools.get_municipality_barangays` |
| List all barangays in the Philippines | `scripts.tools.get_barangays` |
| Get specific barangay by code | `scripts.tools.get_barangay` |
| List all districts in the Philippines | `scripts.tools.get_districts` |
| Get specific district by code | `scripts.tools.get_district` |
| Get all cities within a specific district | `scripts.tools.get_district_cities` |
| Get all municipalities within a specific district | `scripts.tools.get_district_municipalities` |
| Get all cities and municipalities within a specific district | `scripts.tools.get_district_cities_municipalities` |
| Get all sub-municipalities within a specific district | `scripts.tools.get_district_sub_municipalities` |
| Get all barangays within a specific district | `scripts.tools.get_district_barangays` |
| Search for geographic entities by name across all levels (regions, provinces, cities, municipalities, barangays) | `scripts.tools.search_by_name` |
| Get complete geographic hierarchy for a specific code (shows parent entities) | `scripts.tools.get_hierarchy` |
| Validate if a geographic code exists and return its type | `scripts.tools.validate_code` |

**如果参数不完整，使用 AskUserQuestion 向用户询问缺失的参数。**

---

## 工具函数说明

---

## scripts.tools.get_island_groups
工具描述：List all island groups in the Philippines
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|

---

## scripts.tools.get_island_group
工具描述：Get specific island group by code
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|code|string|true| |null|

---

## scripts.tools.get_island_group_regions
工具描述：Get all regions within a specific island group
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|islandGroupCode|string|true| |null|

---

## scripts.tools.get_island_group_provinces
工具描述：Get all provinces within a specific island group
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|islandGroupCode|string|true| |null|

---

## scripts.tools.get_island_group_cities
工具描述：Get all cities within a specific island group
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|islandGroupCode|string|true| |null|

---

## scripts.tools.get_island_group_municipalities
工具描述：Get all municipalities within a specific island group
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|islandGroupCode|string|true| |null|

---

## scripts.tools.get_island_group_barangays
工具描述：Get all barangays within a specific island group
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|islandGroupCode|string|true| |null|

---

## scripts.tools.get_regions
工具描述：List all regions in the Philippines
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|

---

## scripts.tools.get_region
工具描述：Get specific region by code
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|code|string|true| |null|

---

## scripts.tools.get_region_provinces
工具描述：Get all provinces within a specific region
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|regionCode|string|true| |null|

---

## scripts.tools.get_region_districts
工具描述：Get all districts within a specific region
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|regionCode|string|true| |null|

---

## scripts.tools.get_region_cities
工具描述：Get all cities within a specific region
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|regionCode|string|true| |null|

---

## scripts.tools.get_region_municipalities
工具描述：Get all municipalities within a specific region
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|regionCode|string|true| |null|

---

## scripts.tools.get_region_cities_municipalities
工具描述：Get all cities and municipalities within a specific region
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|regionCode|string|true| |null|

---

## scripts.tools.get_region_sub_municipalities
工具描述：Get all sub-municipalities within a specific region
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|regionCode|string|true| |null|

---

## scripts.tools.get_region_barangays
工具描述：Get all barangays within a specific region
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|regionCode|string|true| |null|

---

## scripts.tools.get_provinces
工具描述：List all provinces in the Philippines
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|

---

## scripts.tools.get_province
工具描述：Get specific province by code
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|code|string|true| |null|

---

## scripts.tools.get_province_cities
工具描述：Get all cities within a specific province
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|provinceCode|string|true| |null|

---

## scripts.tools.get_province_municipalities
工具描述：Get all municipalities within a specific province
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|provinceCode|string|true| |null|

---

## scripts.tools.get_province_cities_municipalities
工具描述：Get all cities and municipalities within a specific province
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|provinceCode|string|true| |null|

---

## scripts.tools.get_province_sub_municipalities
工具描述：Get all sub-municipalities within a specific province
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|provinceCode|string|true| |null|

---

## scripts.tools.get_province_barangays
工具描述：Get all barangays within a specific province
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|provinceCode|string|true| |null|

---

## scripts.tools.get_cities
工具描述：List all cities in the Philippines
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|

---

## scripts.tools.get_city
工具描述：Get specific city by code
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|code|string|true| |null|

---

## scripts.tools.get_city_barangays
工具描述：Get all barangays within a specific city
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|cityCode|string|true| |null|

---

## scripts.tools.get_municipalities
工具描述：List all municipalities in the Philippines
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|

---

## scripts.tools.get_municipality
工具描述：Get specific municipality by code
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|code|string|true| |null|

---

## scripts.tools.get_municipality_barangays
工具描述：Get all barangays within a specific municipality
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|municipalityCode|string|true| |null|

---

## scripts.tools.get_barangays
工具描述：List all barangays in the Philippines
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|

---

## scripts.tools.get_barangay
工具描述：Get specific barangay by code
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|code|string|true| |null|

---

## scripts.tools.get_districts
工具描述：List all districts in the Philippines
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|

---

## scripts.tools.get_district
工具描述：Get specific district by code
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|code|string|true| |null|

---

## scripts.tools.get_district_cities
工具描述：Get all cities within a specific district
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|districtCode|string|true| |null|

---

## scripts.tools.get_district_municipalities
工具描述：Get all municipalities within a specific district
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|districtCode|string|true| |null|

---

## scripts.tools.get_district_cities_municipalities
工具描述：Get all cities and municipalities within a specific district
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|districtCode|string|true| |null|

---

## scripts.tools.get_district_sub_municipalities
工具描述：Get all sub-municipalities within a specific district
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|districtCode|string|true| |null|

---

## scripts.tools.get_district_barangays
工具描述：Get all barangays within a specific district
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|districtCode|string|true| |null|

---

## scripts.tools.search_by_name
工具描述：Search for geographic entities by name across all levels (regions, provinces, cities, municipalities, barangays)
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|name|string|true| |null|
|type|string|false| |null|
|limit|integer|false|10.0|null|

---

## scripts.tools.get_hierarchy
工具描述：Get complete geographic hierarchy for a specific code (shows parent entities)
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|code|string|true| |null|

---

## scripts.tools.validate_code
工具描述：Validate if a geographic code exists and return its type
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|code|string|true| |null|

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