---
name: 菜谱推荐服务
description: 基于MCP协议的AI菜谱推荐服务器，提供菜谱查询、分类筛选、智能膳食规划和每日菜单推荐功能。
version: 1.0.0
---

# 菜谱推荐服务

基于MCP协议的AI菜谱推荐服务器，提供菜谱查询、分类筛选、智能膳食规划和每日菜单推荐功能。

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
| 获取所有菜谱 | `scripts.tools.mcp_howtocook_getAllRecipes` |
| 根据分类查询菜谱，可选分类有: 水产, 早餐, 调料, 甜品, 饮品, 荤菜, 半成品加工, 汤, 主食, 素菜 | `scripts.tools.mcp_howtocook_getRecipesByCategory` |
| 根据用户的忌口、过敏原、人数智能推荐菜谱，创建一周的膳食计划以及大致的购物清单 | `scripts.tools.mcp_howtocook_recommendMeals` |
| 不知道吃什么？根据人数直接推荐适合的菜品组合 | `scripts.tools.mcp_howtocook_whatToEat` |
| 根据菜谱名称或ID查询指定菜谱的完整详情，包括食材、步骤等 | `scripts.tools.mcp_howtocook_getRecipeById` |

**如果参数不完整，使用 AskUserQuestion 向用户询问缺失的参数。**

---

## 工具函数说明

---

## scripts.tools.mcp_howtocook_getAllRecipes
工具描述：获取所有菜谱
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|no_param|string|false| |无参数|

---

## scripts.tools.mcp_howtocook_getRecipesByCategory
工具描述：根据分类查询菜谱，可选分类有: 水产, 早餐, 调料, 甜品, 饮品, 荤菜, 半成品加工, 汤, 主食, 素菜
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|category|string|true| |菜谱分类名称，如水产、早餐、荤菜、主食等|

---

## scripts.tools.mcp_howtocook_recommendMeals
工具描述：根据用户的忌口、过敏原、人数智能推荐菜谱，创建一周的膳食计划以及大致的购物清单
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|allergies|array|false| |过敏原列表，如["大蒜", "虾"]|
|avoidItems|array|false| |忌口食材列表，如["葱", "姜"]|
|peopleCount|integer|true| |用餐人数，1-10之间的整数|

---

## scripts.tools.mcp_howtocook_whatToEat
工具描述：不知道吃什么？根据人数直接推荐适合的菜品组合
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|peopleCount|integer|true| |用餐人数，1-10之间的整数，会根据人数推荐合适数量的菜品|

---

## scripts.tools.mcp_howtocook_getRecipeById
工具描述：根据菜谱名称或ID查询指定菜谱的完整详情，包括食材、步骤等
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|query|string|true| |菜谱名称或ID，支持模糊匹配菜谱名称|

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