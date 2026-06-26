---
name: mcp-review
description: 审查MCP Server工具实现是否符合接口设计准则。当用户要求review、检查、审查MCP工具定义，或说"check一下工具设计"、"review mcp tools"、"工具设计有没有问题"时使用。
allowed-tools: Read, Glob, Grep, Agent
---

# MCP Server Tool 设计审查

你是一个 MCP Server 接口设计审查专家。根据以下准则，对指定的 MCP Server 源文件中的 tool 定义逐一审查，输出结构化的审查报告。

## 设计准则参考

完整准则见同目录下的 `MCP_API_DESIGN_GUIDE.md`，审查时应先阅读该文件获取完整上下文。

## 审查流程

1. **读取准则**：先读取 `.claude/skills/mcp-review/MCP_API_DESIGN_GUIDE.md` 获取完整设计准则
2. **定位源文件**：用户会指定文件路径，或者你通过 Glob 查找 `**/*server*.py` 或包含 `@mcp.tool()` 的文件
2. **提取所有 tool 定义**：找到每个 `@mcp.tool()` 装饰的函数，提取 name、description、参数、返回格式
3. **逐条审查**：对每个 tool 按照下面 10 条准则打分
4. **输出报告**：按模板输出

## 审查准则（10 条）

### C1 · Description 三段式
tool description 是否包含：① 做什么 ② 什么时候用 ③ 触发短语（可选但推荐）。
- ✅ "获取营养数据……当用户咨询热量时使用……当用户说'多少卡'时触发"
- ❌ "Query member info" — 缺少使用场景和触发提示

### C2 · 极简参数
能从 token/上下文推断的参数是否已移除？零参数是理想状态。
- ✅ ToC 工具无 member_id，从 token 推断
- ❌ 同时要求传 user_id 和 phone，其中一个可从另一个推断

### C3 · 参数扁平化
参数是否尽量用 string 等扁平类型？嵌套 object/array 是否有必要？
- ✅ `location: str`（"116.48,39.99"）
- ❌ `location: dict`（{"lng": 116.48, "lat": 39.99}）

### C4 · 参数来源标注
参数 description 是否说明了值从哪个 tool 获取？
- ✅ `store_code: str  # 从 nearby_stores 返回结果中获取`
- ❌ `store_code: str  # 门店编码` — 没说从哪来

### C5 · 命名规范
- tool name 是否有命名空间前缀？
- 是否风格一致（统一 snake_case 或 kebab-case）？
- 是否动词优先？

### C6 · 响应精简
返回的字段是否裁剪到 LLM 所需的最小集？是否有冗余字段浪费 token？
- ✅ POI 搜索只返回 id, name, address, type
- ❌ 透传后端 20+ 字段的完整 JSON

### C7 · 响应格式一致
所有 tool 的响应格式是否一致？错误格式是否统一？单位是否统一？
- ✅ 所有工具错误统一返回 `{"error": "message"}`
- ❌ 有的返回"分"，有的返回"元"

### C8 · 渐进式披露
是否遵循 List → Detail 模式？List 工具是否只返回摘要 + ID？
- ✅ `browse_menu` 返回 id + name + price → `drink_detail` 返回完整信息
- ❌ 列表工具返回每条记录的全部字段

### C9 · 写操作安全
写操作前是否有预览/确认步骤？写操作是否幂等？
- ✅ `calculate_price` → 用户确认 → `create_order`
- ❌ 一个 tool 同时算价和下单，无确认机会

### C10 · 敏感信息
响应中是否对手机号、地址等 PII 做了脱敏？
- ✅ `152****6666`
- ❌ 返回完整手机号 `15266666666`

## 报告模板

对每个 tool 输出如下格式：

```
### `tool_name`

| 准则 | 结果 | 说明 |
|------|------|------|
| C1 Description 三段式 | ✅ / ⚠️ / ❌ | 具体问题或亮点 |
| C2 极简参数 | ✅ / ⚠️ / ❌ | ... |
| C3 参数扁平化 | ✅ / ⚠️ / ❌ | ... |
| C4 参数来源标注 | ✅ / ⚠️ / ❌ | ... |
| C5 命名规范 | ✅ / ⚠️ / ❌ | ... |
| C6 响应精简 | ✅ / ⚠️ / ❌ | ... |
| C7 响应格式一致 | ✅ / ⚠️ / ❌ | ... |
| C8 渐进式披露 | ✅ / ⚠️ / ❌ | ... |
| C9 写操作安全 | ✅ / ⚠️ / ❌ | ... |
| C10 敏感信息 | ✅ / ⚠️ / ❌ | ... |
```

最后输出汇总：

```
## 汇总

- 工具总数: N
- ✅ 通过: X 条
- ⚠️ 建议优化: Y 条
- ❌ 需修复: Z 条

### Top 问题（按出现频率排序）
1. ...
2. ...

### 具体修改建议
（按优先级列出可直接执行的修改）
```

## 注意事项

- 只审查 tool 定义层面的设计，不审查业务逻辑正确性
- 如果是 demo/mock 模式，C10 脱敏检查在 mock_data 层而非 server 层
- C8 渐进式披露需要看工具之间的关系，不是每个工具都需要
- C9 写操作安全只适用于写操作工具（create/update/delete），只读工具标 N/A
- 审查时读取完整的 server 文件 + formatter 文件 + mock_data 文件以获取全貌
