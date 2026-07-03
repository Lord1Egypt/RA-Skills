---
name: 科学计算工具
description: math_genie_calc是一款专注于科学计算的Python应用，提供从基础运算到复杂三角函数的多种计算功能，适合学生、科研人员等使用。
version: 1.0.0
---

# 科学计算工具

math_genie_calc是一款专注于科学计算的Python应用，提供从基础运算到复杂三角函数的多种计算功能，适合学生、科研人员等使用。

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
| 两个数相加 | `scripts.tools.add` |
| 两个数相减 | `scripts.tools.subtract` |
| 两个数相乘 | `scripts.tools.multiply` |
| 两个数相除 | `scripts.tools.divide` |
| 计算正弦函数 | `scripts.tools.sine` |
| 计算余弦函数 | `scripts.tools.cos` |
| 计算正切函数 | `scripts.tools.tangent` |
| 计算余切函数 | `scripts.tools.cotangent` |
| 计算正割函数 | `scripts.tools.secant` |
| 计算余割函数 | `scripts.tools.cosecant` |
| 计算自然对数(底数为e) | `scripts.tools.natural_log` |
| 计算常用对数(底数为10) | `scripts.tools.common_log` |
| 根据给定的底数计算对数 | `scripts.tools.custom_log` |
| 使用Python内置的数学模块进行平方根计算 | `scripts.tools.math_sqrt` |
| 使用指数运算符来计算平方根 | `scripts.tools.operator_sqrt` |
| 计算复数平方根 | `scripts.tools.complex_sqrt` |
| 计算幂运算，支持负整数和小数 | `scripts.tools.exponentiation` |
| 计算反正弦函数 | `scripts.tools.arcsin` |
| 计算反余弦函数 | `scripts.tools.arccos` |
| 计算反正切函数 | `scripts.tools.arctan` |
| 求阶乘 | `scripts.tools.factorial_math` |

**如果参数不完整，使用 AskUserQuestion 向用户询问缺失的参数。**

---

## 工具函数说明

---

## scripts.tools.add
工具描述：两个数相加
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|a|number|true| |null|
|b|number|true| |null|

---

## scripts.tools.subtract
工具描述：两个数相减
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|a|number|true| |null|
|b|number|true| |null|

---

## scripts.tools.multiply
工具描述：两个数相乘
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|a|number|true| |null|
|b|number|true| |null|

---

## scripts.tools.divide
工具描述：两个数相除
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|a|number|true| |null|
|b|number|true| |null|

---

## scripts.tools.sine
工具描述：计算正弦函数
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|degree|number|true| |null|

---

## scripts.tools.cos
工具描述：计算余弦函数
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|degree|number|true| |null|

---

## scripts.tools.tangent
工具描述：计算正切函数
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|degree|number|true| |null|

---

## scripts.tools.cotangent
工具描述：计算余切函数
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|degree|number|true| |null|

---

## scripts.tools.secant
工具描述：计算正割函数
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|degree|number|true| |null|

---

## scripts.tools.cosecant
工具描述：计算余割函数
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|degree|number|true| |null|

---

## scripts.tools.natural_log
工具描述：计算自然对数(底数为e)
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|x|number|true| |null|

---

## scripts.tools.common_log
工具描述：计算常用对数(底数为10)
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|x|number|true| |null|

---

## scripts.tools.custom_log
工具描述：根据给定的底数计算对数
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|x|number|true| |null|
|base|number|true| |null|

---

## scripts.tools.math_sqrt
工具描述：使用Python内置的数学模块进行平方根计算
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|x|string|true| |null|

---

## scripts.tools.operator_sqrt
工具描述：使用指数运算符来计算平方根
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|x|number|true| |null|

---

## scripts.tools.complex_sqrt
工具描述：计算复数平方根
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|x|string|true| |null|

---

## scripts.tools.exponentiation
工具描述：计算幂运算，支持负整数和小数
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|base|number|true| |null|
|exponent|number|true| |null|

---

## scripts.tools.arcsin
工具描述：计算反正弦函数
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|value|number|true| |null|

---

## scripts.tools.arccos
工具描述：计算反余弦函数
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|value|number|true| |null|

---

## scripts.tools.arctan
工具描述：计算反正切函数
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|value|number|true| |null|

---

## scripts.tools.factorial_math
工具描述：求阶乘
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|n|integer|true| |null|

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