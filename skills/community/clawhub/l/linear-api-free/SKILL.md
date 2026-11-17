---
slug: "linear-api-free"
name: "linear-api-free"
version: "1.0.0"
displayName: "Linear API引擎(免费版)"
summary: "Linear问题跟踪与项目管理，通过GraphQL API操作Issue/Cycle/Project与工作流。免费版"
summary_zh: "Linear问题跟踪与项目管理，通过GraphQL API操作Issue/Cycle/Project与工作流。免费版"
license: "MIT"
description: "|-. 适用于需要linear api相关能力的开发场景,包含结构化的工作流程和可复用的模板,帮助用户快速完成任务并保持代码质量.该技能适用于相关开发场景,包含结构化的工作流程和配置指引.经过深度差异化处置,针对用户反馈和使用痛点进行了改进,提升了实用性和可操作性.该技能适用于相关开发场景,包含结构化的工作流程和配置指引.经过深度差异化处置,针对用户反馈和使用痛点进行了改进,提升了实用性和可操作性."
  Linear项目管理集成引擎（免费版），通过GraphQL API操作Linear实例。覆盖Issue管理、
  Cycle规划、Project跟踪与工作流自动化。核心能力：
  - Issue管理（创建/更新/查询/批量操作）
  - Cycle与Project管理（Sprint规划/项目跟踪）
  - 工作流与状态流转（状态更新/分配/标签）
  - GraphQL高级查询与批量操作
tools:
  - read
  - exec
  - write
homepage: ""
tags:
  - 研发工具
  - linear
  - automation
  - productivity
  - 接口
  - 开发工具
  - graphql
  - issue
  - https
category: "Development"
pricing_tier: free
---
# Linear API引擎(免费版)

Linear项目管理集成引擎，通过GraphQL API操作Linear实例，覆盖Issue管理、Cycle规划与工作流自动化.
## 输入格式

| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| input | string | 是 | Linear API引擎(免费版)处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

## 依赖说明

### 运行环境
- **Agent 平台**: 支持 SKILL.md 的任意 AI Agent（Claude Code / Cursor / Codex / Gemini CLI 等）
- **操作系统**: Windows / macOS / Linux
- **网络**: 需可访问 Linear API（https://api.linear.app/graphql）

### 依赖项
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-----|:-----|:-----|:-----|
| Agent 平台 | 运行环境 | 必需 | 任意支持 SKILL.md 的 AI Agent |
| Linear 账户 | 服务 | 必需 | https://linear.app 注册 |
| Linear API Key | 认证凭证 | 必需 | Linear Settings → API → Personal API keys 生成 |
| curl | 命令行工具 | 必需 | 系统自带或安装，用于执行 GraphQL 请求 |

### 可用性分类
- **分类**: MD+EXEC（Markdown 指令驱动，需 exec 执行 curl 命令调用 GraphQL API）
- **说明**: 基于自然语言指令驱动 Agent 执行 Linear Issue 管理、Cycle 规划与查询

**API Key配置方式**:
```bash
export API_KEY=${API_KEY:?请设置环境变量}
```
配置后需重启会话或开启新终端生效。API Key应妥善保管,避免泄露到版本控制系统.
## 核心能力

### 1. Issue管理
通过Linear GraphQL API管理Issue：

```bash
# 创建Issue
curl -X POST "https://api.linear.app/graphql" \
  -H "Authorization: $PARAM" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "mutation { issueCreate(input: { title: \"实现用户登录功能\", description: \"需要实现OAuth登录\", teamId: \"team-uuid\", priority: 2, assigneeId: \"user-uuid\" }) { success issue { id identifier title } } }"
  }'
# ...
# 查询Issue
linear.app/graphql" \
  -H "Authorization: $PARAM" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "{ issue(id: \"issue-uuid\") { identifier title description state { name } assignee { name } priority labels { nodes { name } } } }"
  }'
# ...
# 更新Issue
linear.app/graphql" \
  -H "Authorization: $PARAM" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "mutation { issueUpdate(id: \"issue-uuid\", input: { title: \"更新后的标题\", priority: 3 }) { success issue { id title } } }"
  }'
```

### 2. Cycle与Project管理
```bash
# 获取当前活跃Cycle
linear.app/graphql" \
  -H "Authorization: $PARAM" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "{ team(id: \"team-uuid\") { cycles(filter: { active: { eq: true } }) { nodes { id name number startDate endDate } } } }"
  }'
# ...
# 将Issue加入Cycle
linear.app/graphql" \
  -H "Authorization: $PARAM" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "mutation { issueUpdate(id: \"issue-uuid\", input: { cycleId: \"cycle-uuid\" }) { success } }"
  }'
# ...
# 查询Project及其Issues
linear.app/graphql" \
  -H "Authorization: $PARAM" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "{ project(id: \"project-uuid\") { name description state { name } issues { nodes { identifier title state { name } assignee { name } } } } }"
  }'
```

- 异常时参考错误处理章节进行恢复
- 关键参数: `cycle与project管理` 选项

### 3. 工作流与状态流转
```bash
# 获取团队的工作流状态
linear.app/graphql" \
  -H "Authorization: $PARAM" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "{ team(id: \"team-uuid\") { states { nodes { id name type } } } }"
  }'
# ...
# 更新Issue状态
linear.app/graphql" \
  -H "Authorization: $PARAM" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "mutation { issueUpdate(id: \"issue-uuid\", input: { stateId: \"state-uuid\" }) { success issue { state { name } } } }"
  }'
# ...
# 添加标签
linear.app/graphql" \
  -H "Authorization: $PARAM" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "mutation { issueUpdate(id: \"issue-uuid\", input: { labelIds: [\"label-uuid-1\", \"label-uuid-2\"] }) { success } }"
  }'
```

- 异常时参考错误处理章节进行恢复
- 关键参数: `工作流与状态流转` 选项

### 4. GraphQL高级查询
```bash
# 查询我的待办Issue
linear.app/graphql" \
  -H "Authorization: $PARAM" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "{ viewer { assignedIssues(filter: { state: { type: { eq: \"started\" } } } }) { nodes { identifier title priority state { name } team { key } } } }"
  }'
# ...
# 批量查询多个团队Issue
linear.app/graphql" \
  -H "Authorization: $PARAM" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "{ teams { nodes { key name issues(filter: { priority: { gte: 2 } }) { nodes { identifier title priority state { name } } } } } }"
  }'
```

- 异常时参考错误处理章节进行恢复
- 关键参数: `graphql高级查询` 选项

#
## 快速开始

1. 确认运行环境满足依赖说明中的要求
2. 在AI Agent对话中调用本技能,提供必要的输入参数
3. 检查输出结果,根据需要进行后续处理

> 详细的输入输出格式请参考下方章节说明。

## 适用场景

| 场景 | 输入 | 输出 |
|---:|---:|---:|
| 批量创建Issue | 需求列表+团队ID | 批量GraphQL mutation+结果汇总 |
| Cycle报告 | Cycle ID | Cycle进度+Issue状态分布 |
| 跨团队查询 | 查询条件 | 多团队Issue聚合列表 |
| 工作流自动化 | 触发条件+动作 | 状态流转+分配+标签脚本 |

**不适用于**：Linear账户管理、Linear工作区配置、Linear计费操作.
## 使用流程

1. 获取API Key（Linear Settings → API → Personal API keys）
2. 确定团队ID和项目ID
3. 构造GraphQL query/mutation
4. 通过curl发送请求到 `https://api.linear.app/graphql`
5. 解析JSON响应并格式化输出

#
## 示例

### 示例1：查询当前Cycle进度
```bash
curl -s -X POST "https://api.linear.app/graphql" \
  -H "Authorization: $PARAM" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "{ team(id: \"team-uuid\") { cycles(filter: { active: { eq: true } }) { nodes { name number issues { nodes { identifier title state { name type } } } } } } }"
  }' | jq '.data.team.cycles.nodes[0].issues.nodes | group_by(.state.type) | map({type: .[0].state.type, count: length})'
```
输出：当前Cycle的Issue按状态类型（backlog/started/completed/canceled）分组统计.
## 错误处理

| 错误场景 | 原因 | 处理方式 |
|:---:|:---:|:---:|
| `401 Unauthorized` | API Key无效或过期 | 在Linear Settings → API中重新生成Personal API Key，确认请求头使用 `Authorization: $PARAM` 格式（无需Bearer前缀） |
| `400 Bad Request` "Parse error" | GraphQL语法错误 | 检查query字符串中的引号转义，确保mutation/query语法正确，使用JSON验证工具检查请求体格式 |
| `404 Not Found` "Entity not found" | ID不存在或无权限 | 确认teamId/issueId/projectId为有效UUID，检查API Key关联的账户是否有目标团队的访问权限 |
| `429 Too Many Requests` | 触发速率限制 | Linear API限制为每分钟1500请求（复杂度计算），减少批量操作的并发数，添加请求间隔，使用分页查询而非全量拉取 |

## 常见问题

### Q1: 如何获取Linear API Key？
登录Linear，进入Settings → API → Personal API keys，点击"Create key"，输入标签名后复制Key。使用时放在请求头：`-H "Authorization: lin_api_key"`（注意：Linear API Key直接作为Authorization值，不需要"Bearer"前缀）。Key不会过期但可以随时撤销。建议为不同用途创建不同的Key（如自动化脚本用独立Key）.
### Q2: Linear的GraphQL API和REST API有什么区别？
Linear主要使用GraphQL API（`https://api.linear.app/graphql`），所有操作通过POST请求发送query/mutation。优势：可以精确指定返回字段（避免over-fetching），单次请求可查询关联数据（Issue+Assignee+Team+Labels）。Linear没有独立的REST API文档，GraphQL是官方推荐方式。对于不熟悉GraphQL的用户，可以在Linear的API Playground（https://api.linear.app）交互式测试query.
### Q3: 如何处理GraphQL的分页查询？
Linear使用Relay风格的分页（cursor-based）。查询时使用`first`参数限制数量（默认50，最大100），返回`pageInfo.hasNextPage`和`pageInfo.endCursor`。翻页时传入`after: "endCursor值"`。示例：`issues(first: 100, after: "cursor-xyz") { nodes { id title } pageInfo { hasNextPage endCursor } }`。遍历所有结果时循环请求直到`hasNextPage`为false.
## 已知限制

- 需要Linear账户和API Key
- API Key权限受账户角色限制
- GraphQL查询复杂度有上限，复杂查询可能被拒绝

## 升级提示

本免费版提供基础功能。升级到完整版 linear-api 获取全部能力和高级特性.
## 输出格式

```json
{
  "success": true,
  "data": {
    "result": "Linear API引擎(免费版)处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "linear-api"
    }
  },
  "execution_log": [
    "解析输入参数",
    "执行核心处理",
    "格式化输出结果"
  ],
  "error": null
}
```
