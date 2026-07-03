---
name: 图标数据服务
description: 提供访问Iconify超过20万开源矢量图标的MCP服务器，支持图标集浏览、搜索及多框架使用示例获取。
version: 1.0.0
---

# 图标数据服务

提供访问Iconify超过20万开源矢量图标的MCP服务器，支持图标集浏览、搜索及多框架使用示例获取。

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
| Browse all available icon collections from Iconify (200+ icon sets with 200,000+ icons). Returns a list of all icon sets with their metadata including name, total icons, author, license, and sample icons. | `scripts.tools.get_all_icon_sets` |
| Retrieve detailed information about a specific icon set including all available icons in that set. Provide the icon set prefix (e.g., 'mdi', 'fa', 'bi'). | `scripts.tools.get_icon_set` |
| Search through Iconify's icon collection with flexible query parameters. Returns matching icons from all icon sets or a specific set. | `scripts.tools.search_icons` |
| Retrieve specific icon data with usage examples for popular frameworks (React, Vue, Svelte, etc.). Provide the full icon name in format 'prefix:icon-name' (e.g., 'mdi:home', 'fa:user'). | `scripts.tools.get_icon_data` |

**如果参数不完整，使用 AskUserQuestion 向用户询问缺失的参数。**

---

## 工具函数说明

---

## scripts.tools.get_all_icon_sets
工具描述：Browse all available icon collections from Iconify (200+ icon sets with 200,000+ icons). Returns a list of all icon sets with their metadata including name, total icons, author, license, and sample icons.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|

---

## scripts.tools.get_icon_set
工具描述：Retrieve detailed information about a specific icon set including all available icons in that set. Provide the icon set prefix (e.g., 'mdi', 'fa', 'bi').
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|prefix|string|true| |The icon set prefix (e.g., 'mdi', 'fa', 'bi', 'tabler')|

---

## scripts.tools.search_icons
工具描述：Search through Iconify's icon collection with flexible query parameters. Returns matching icons from all icon sets or a specific set.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|query|string|true| |Search query (e.g., 'home', 'arrow', 'user')|
|prefix|string|false| |Optional: limit search to specific icon set prefix|
|limit|number|false| |Optional: maximum number of results (default: 64, max: 999)|

---

## scripts.tools.get_icon_data
工具描述：Retrieve specific icon data with usage examples for popular frameworks (React, Vue, Svelte, etc.). Provide the full icon name in format 'prefix:icon-name' (e.g., 'mdi:home', 'fa:user').
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|icon|string|true| |Full icon name in format 'prefix:icon-name' (e.g., 'mdi:home', 'fa:user', 'bi:heart')|

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