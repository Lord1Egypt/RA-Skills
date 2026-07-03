---
name: Maven依赖管理服务
description: Maven MCP Server是一个通过自然语言交互的AI驱动Maven依赖管理工具，提供版本检查、安全扫描和依赖分析功能。
version: 1.0.0
---

# Maven依赖管理服务

Maven MCP Server是一个通过自然语言交互的AI驱动Maven依赖管理工具，提供版本检查、安全扫描和依赖分析功能。

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
| Check a Maven version and get all version update information in a single call | `scripts.tools.check_version_tool` |
| Process multiple Maven dependency version checks in a single batch request | `scripts.tools.check_version_batch_tool` |
| List all available versions of a Maven artifact grouped by minor version tracks | `scripts.tools.list_available_versions_tool` |
| Java-specific tool for scanning Maven projects for vulnerabilities | `scripts.tools.scan_java_project_tool` |
| Analyze a single Maven POM file without scanning the entire workspace | `scripts.tools.analyze_pom_file_tool` |

**如果参数不完整，使用 AskUserQuestion 向用户询问缺失的参数。**

---

## 工具函数说明

---

## scripts.tools.check_version_tool
工具描述：Check a Maven version and get all version update information in a single call
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|dependency|string|true| |null|
|version|string|true| |null|
|packaging|string|false|"jar"|null|
|classifier|null|false| |null|

---

## scripts.tools.check_version_batch_tool
工具描述：Process multiple Maven dependency version checks in a single batch request
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|dependencies|array|true| |null|

---

## scripts.tools.list_available_versions_tool
工具描述：List all available versions of a Maven artifact grouped by minor version tracks
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|dependency|string|true| |null|
|version|string|true| |null|
|packaging|string|false|"jar"|null|
|classifier|null|false| |null|
|include_all_versions|boolean|false|false|null|

---

## scripts.tools.scan_java_project_tool
工具描述：Java-specific tool for scanning Maven projects for vulnerabilities
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|workspace|string|true| |null|
|include_profiles|null|false| |List of Maven profiles to activate|
|scan_all_modules|boolean|false|true|null|
|scan_mode|string|false|"workspace"|null|
|pom_file|null|false| |null|
|severity_filter|null|false| |List of severity levels to include (CRITICAL, HIGH, MEDIUM, LOW)|
|max_results|integer|false|100.0|null|
|offset|integer|false|0.0|null|

---

## scripts.tools.analyze_pom_file_tool
工具描述：Analyze a single Maven POM file without scanning the entire workspace
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|pom_file_path|string|true| |null|
|include_vulnerability_check|boolean|false|true|null|

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