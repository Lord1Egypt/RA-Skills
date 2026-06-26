---
name: my_stock_watchlist_skill
description: 当用户提到“观察列表”或“股票观察”时触发。用于管理钉钉多维表格中的股票观察名单。
---

# My Stock Watchlist Skill (股票观察列表管理技能)

## 核心规则与触发条件
- **触发条件**：仅当用户提到“观察列表”或“股票观察”相关话题时触发。
- **必要前置**：明确的操作意图（查看、新增、删除）和标的代码（如 NVDA）。

## 工作流程
所有操作均基于指定的钉钉多维表格进行：
- **表格 URL**: https://alidocs.dingtalk.com/i/nodes/1OQX0akWmxpyBpnaCQQQoYkY8GlDd3mE
- **Base ID (nodeId)**: `1OQX0akWmxpyBpnaCQQQoYkY8GlDd3mE`
- **Sheet ID**: `hERWDMS`

### 1. 列表新增
- 动作：在表格末尾新增一行，将标的字段填入用户提供的标的简码。
- **执行方式**：调用 `dingtalk-ai-table` 技能中的 API 规范，构造 `POST /v1.0/notable/bases/{base_id}/sheets/{sheet_id}/records` 请求。请求体中的 `fields` 必须包含标的名称字段。

### 2. 列表删除
- 动作：查询表格中对应的标的行，定位其 `recordId`，然后执行删除操作。
- **执行方式**：
  1. 调用 `dingtalk-ai-table` 获取记录列表 `GET /v1.0/notable/bases/{base_id}/sheets/{sheet_id}/records`，遍历查找到目标标的所在行的 `id`。
  2. 调用删除记录 API `DELETE /v1.0/notable/bases/{base_id}/sheets/{sheet_id}/records/{record_id}` 进行删除。

### 3. 列表查询
- 动作：获取当前所有观察标的，或查询某个标的是否在观察列表中。
- **执行方式**：
  1. 调用 `dingtalk-ai-table` 获取记录列表 `GET /v1.0/notable/bases/{base_id}/sheets/{sheet_id}/records`。
  2. 解析返回的 JSON 数据，提取出所有的 `标的` 字段的值并进行总结。
  3. 如果用户询问某个特定标的（如“NVDA 在列表中吗？”），则匹配提取的数据并给出明确答复。

## 字段映射说明
- **股票代码字段名**：`标的` （在调用 `dingtalk-ai-table` 技能的 records API 时，`fields` 字典的键必须严格使用此名称，例如 `{"fields": {"标的": "NVDA"}}`）。