---
name: 数学计算引擎
description: MCP Mathematics 是一个全面的数学计算服务器，可将任何AI助手转变为强大的数学计算引擎，提供高级数学函数、单位转换和财务计算等功能。
version: 1.0.0
---

# 数学计算引擎

MCP Mathematics 是一个全面的数学计算服务器，可将任何AI助手转变为强大的数学计算引擎，提供高级数学函数、单位转换和财务计算等功能。

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
| Get performance metrics | `scripts.tools.performance_metrics` |
| Get security status | `scripts.tools.security_status` |
| Get memory statistics | `scripts.tools.memory_statistics` |
| Evaluate math expression | `scripts.tools.calculate_expression` |
| Batch calculate expressions | `scripts.tools.batch_calculate` |
| Calculate statistics | `scripts.tools.calculate_statistics` |
| Matrix operations | `scripts.tools.matrix_operation` |
| Unit conversion | `scripts.tools.convert_units` |
| Natural language conversion | `scripts.tools.convert_natural_language` |
| Number theory operations | `scripts.tools.analyze_number_theory` |
| Create session | `scripts.tools.create_session` |
| Session calculation | `scripts.tools.session_calculate` |
| List session variables | `scripts.tools.list_session_variables` |
| Delete session | `scripts.tools.delete_session` |
| Get calculation history | `scripts.tools.get_calculation_history` |
| Clear history | `scripts.tools.clear_history` |
| Optimize memory | `scripts.tools.optimize_memory` |
| List functions | `scripts.tools.list_functions` |

**如果参数不完整，使用 AskUserQuestion 向用户询问缺失的参数。**

---

## 工具函数说明

---

## scripts.tools.performance_metrics
工具描述：Get performance metrics
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|

---

## scripts.tools.security_status
工具描述：Get security status
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|

---

## scripts.tools.memory_statistics
工具描述：Get memory statistics
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|

---

## scripts.tools.calculate_expression
工具描述：Evaluate math expression
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|expr|string|true| |Mathematical expression to evaluate|

---

## scripts.tools.batch_calculate
工具描述：Batch calculate expressions
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|expressions|array|true| |List of mathematical expressions to evaluate|

---

## scripts.tools.calculate_statistics
工具描述：Calculate statistics
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|data|array|true| |List of numbers to analyze|
|operation|string|true| |Statistical operation (mean, median, mode, stdev, etc.)|

---

## scripts.tools.matrix_operation
工具描述：Matrix operations
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|matrices|array|true| |List of matrices for operation|
|operation|string|true| |Matrix operation (multiply, determinant, inverse)|

---

## scripts.tools.convert_units
工具描述：Unit conversion
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|value|number|true| |Numeric value to convert|
|from_unit|string|true| |Source unit|
|to_unit|string|true| |Target unit|
|unit_type|string|true| |Unit category (length, mass, time, temperature, etc.)|

---

## scripts.tools.convert_natural_language
工具描述：Natural language conversion
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|query|string|true| |Natural language conversion request|

---

## scripts.tools.analyze_number_theory
工具描述：Number theory operations
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|number|integer|true| |Integer to analyze|
|operation|string|true| |Number theory operation (is_prime, prime_factors, divisors, totient)|

---

## scripts.tools.create_session
工具描述：Create session
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|session_id|null|false| |Optional session identifier|
|variables|null|false| |Initial session variables|

---

## scripts.tools.session_calculate
工具描述：Session calculation
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|session_id|string|true| |Session identifier|
|expr|string|true| |Mathematical expression to evaluate|
|var_name|null|false| |Variable name to store result|

---

## scripts.tools.list_session_variables
工具描述：List session variables
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|session_id|string|true| |Session identifier|

---

## scripts.tools.delete_session
工具描述：Delete session
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|session_id|string|true| |Session identifier|

---

## scripts.tools.get_calculation_history
工具描述：Get calculation history
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|limit|integer|false|10.0|Number of recent calculations to retrieve|

---

## scripts.tools.clear_history
工具描述：Clear history
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|

---

## scripts.tools.optimize_memory
工具描述：Optimize memory
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|

---

## scripts.tools.list_functions
工具描述：List functions
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