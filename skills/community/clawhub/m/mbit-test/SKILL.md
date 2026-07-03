---
name: MBTI测试服务
description: 一个用于MBTI人格测试的MCP服务器，支持AI助手引导用户完成人格测试并给出结果分析。
version: 1.0.0
---

# MBTI测试服务

一个用于MBTI人格测试的MCP服务器，支持AI助手引导用户完成人格测试并给出结果分析。

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
| 开始MBTI人格测试。用户可以选择测试类型：simplified(简化版28题)或cognitive(认知功能版48题)。返回第一道题目和测试会话状态。 | `scripts.tools.start_mbti_test` |
| 提交当前问题的答案(1-5分)，并获取下一题或测试进度。需要传入完整的测试会话状态。 | `scripts.tools.answer_question` |
| 查询当前测试进度。需要传入测试会话状态。 | `scripts.tools.get_progress` |
| 根据所有答案计算最终的MBTI类型和详细结果。需要传入完整的测试会话状态。 | `scripts.tools.calculate_mbti_result` |

**如果参数不完整，使用 AskUserQuestion 向用户询问缺失的参数。**

---

## 工具函数说明

---

## scripts.tools.start_mbti_test
工具描述：开始MBTI人格测试。用户可以选择测试类型：simplified(简化版28题)或cognitive(认知功能版48题)。返回第一道题目和测试会话状态。
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|testType|string|true| |测试类型：simplified(简化版)或cognitive(认知功能版)|

---

## scripts.tools.answer_question
工具描述：提交当前问题的答案(1-5分)，并获取下一题或测试进度。需要传入完整的测试会话状态。
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|session|object|true| |测试会话状态，包含testType、answers数组和currentQuestionIndex|
|score|number|true| |对当前问题的回答(1=强烈不同意, 2=不同意, 3=中立, 4=同意, 5=强烈同意)|

---

## scripts.tools.get_progress
工具描述：查询当前测试进度。需要传入测试会话状态。
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|session|object|true| |测试会话状态|

---

## scripts.tools.calculate_mbti_result
工具描述：根据所有答案计算最终的MBTI类型和详细结果。需要传入完整的测试会话状态。
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|session|object|true| |测试会话状态，必须包含所有题目的答案|

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