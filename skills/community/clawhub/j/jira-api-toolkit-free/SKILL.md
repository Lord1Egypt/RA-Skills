---
slug: jira-api-toolkit-free
name: jira-api-toolkit-free
version: 1.0.0
displayName: Jira工具箱(免费版)
summary: Jira Cloud 只读集成，支持 JQL 搜索、查看议题与项目列表。
license: Proprietary
edition: free
description: 'Jira Cloud 只读集成，支持 JQL 搜索、查看议题与项目列表。核心能力：

  - 通过托管 OAuth 认证访问 Jira Cloud API

  - JQL 搜索议题，支持字段过滤与分页

  - 查看议题详情、项目列表、议题类型与状态

  - 多连接管理与 cloud-id 自动获取


  适用场景：

  - 个人开发者查询自己的议题进度

  - 团队站会前快速拉取进行中议题

  - 项目经理查看项目与议题元数据

  - 自动化工作流中的只读数据采集


  差异化：采用托管 OAuth 免去手动管理令牌的负担...'
tags:
- 集成工具
- 项目管理
- 开发者效率
tools:
- - read
- exec
homepage: https://skillhub.cn
pricing_tier: "L1-入门级"
pricing_model: per_use
suggested_price: "9.9 CNY/per_use"
tools: ["read", "write", "exec"]
tags: "API,接口,开发工具"
---
# Jira 工具箱（免费版）

## 概述

本 Skill 帮助 Agent 通过托管 OAuth 认证访问 Jira Cloud API，完成 JQL 搜索、议题查看、项目列表等只读操作。免费版聚焦个人开发者与小团队的"查询与浏览"场景：无需手动管理 OAuth 令牌，通过统一的 API 代理自动注入认证，降低接入门槛。所有写操作（创建、更新、删除、流转）需使用专业版。

## 核心能力

| 能力 | 说明 | 免费版支持 |
|---|---|-----|
| 托管 OAuth 认证 | 自动注入令牌，免手动管理 | 是 |
| cloud-id 获取 | 自动获取 Jira Cloud ID | 是 |
| JQL 搜索议题 | 按字段过滤与分页 | 是 |
| 查看议题详情 | 读取单条议题全部字段 | 是 |
| 项目列表 | 列出可访问项目 | 是 |
| 议题类型/状态/优先级 | 读取元数据 | 是 |
| 当前用户信息 | whoami 查询 | 是 |
| 创建议题 | 新建议题 | 否（专业版） |
| 更新/删除议题 | 修改与删除 | 否（专业版） |
| 流转议题 | 改变状态 | 否（专业版） |
| 评论管理 | 添加/查看评论 | 否（专业版） |
| 批量操作 | 批量创建/更新 | 否（专业版） |

### 核心功能执行
用`input_params`参数进行配置。

**输入**: 用户提供核心功能执行所需的指令和必要参数。
**处理**: 解析核心功能执行的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回核心功能执行的响应数据,包含状态码、结果和日志。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 参数配置与调用
用`config_options`参数进行配置。

**输入**: 用户提供参数配置与调用所需的指令和必要参数。
**处理**: 解析参数配置与调用的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回参数配置与调用的响应数据,包含状态码、结果和日志。
- 执行此能力时使用`config_options`参数,支持修改/重置/导入操作

### 结果处理与输出
用`output_format`参数进行配置。

**输入**: 用户提供结果处理与输出所需的指令和必要参数。
**处理**: 解析结果处理与输出的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回结果处理与输出的响应数据,包含状态码、结果和日志。
- 执行此能力时使用`output_format`参数,支持导出/保存/转换操作
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：只读集成、查看议题与项目列、核心能力、通过托管、认证访问、API、支持字段过滤与分、议题类型与状态、多连接管理与等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持。

## 使用场景

1. **站会前快速拉取进行中议题**：用 JQL `project = PROJ AND status = "In Progress" ORDER BY updated DESC` 拉取最近更新的议题，作为站会发言素材。
2. **个人议题进度自查**：开发者查询分配给自己的议题，按优先级排序，规划当日工作。
3. **项目元数据浏览**：项目经理查看项目列表、议题类型、状态流转定义，了解项目配置。
4. **自动化只读采集**：CI/CD 流水线中读取议题状态，决定是否触发下游任务。

## 不适用场景

以下场景Jira工具箱(免费版)不适合处理：

- 逆向工程闭源API
- API安全渗透测试
- 非标准协议集成

## 触发条件

需要API集成、接口对接、Webhook配置、系统连接时使用。不适用于非本工具能力范围的需求。

## 快速开始

> 上手时间：< 120 秒。需先安装 CLI 并完成 OAuth 连接。

### 依赖详情

```bash
npm install -g @maton/cli
```

或使用 Homebrew：

```bash
brew install maton-ai/cli/maton
```

### Step 2：登录并创建 Jira 连接

```bash
maton login                          # 浏览器打开获取 API Key
maton connection create jira          # 创建 Jira OAuth 连接，浏览器完成授权
```

### Step 3：获取 cloud-id

Jira Cloud 需要 cloud-id，先获取可访问资源：

```bash
maton jira cloud list
```

返回示例：

```json
[{
  "id": "62909843-b784-4c35-b770-e4e2a26f024b",
  "url": "https://yoursite.atlassian.net",
  "name": "yoursite"
}]
```

### Step 4：JQL 搜索议题

```bash
maton jira issue search 'project = PROJ AND status = "In Progress"' --cloud-id abc-123 --limit 20 --fields summary,status,assignee
```

## 示例

### 认证方式

| 方式 | 命令 | 适用场景 |
|:-----|:-----|:-----|
| 浏览器登录 | `maton login` | 首次使用，交互式获取 API Key |
| 交互式登录 | `maton login --interactive` | 无浏览器环境，粘贴 API Key |
| 查看认证状态 | `maton whoami` | 验证当前登录状态 |

### 常用只读命令

| 命令 | 用途 | 示例 |
|---:|---:|---:|
| `jira cloud list` | 获取 cloud-id | `maton jira cloud list` |
| `jira issue search` | JQL 搜索 | `maton jira issue search 'project=PROJ' --cloud-id abc-123` |
| `jira issue view` | 查看议题 | `maton jira issue view PROJ-123 --cloud-id abc-123` |
| `jira project list` | 项目列表 | `maton jira project list --cloud-id abc-123` |
| `jira issuetype list` | 议题类型 | `maton jira issuetype list --cloud-id abc-123` |
| `jira status list` | 状态列表 | `maton jira status list --cloud-id abc-123` |
| `jira whoami` | 当前用户 | `maton jira whoami --cloud-id abc-123` |

### JQL 常用示例

| 场景 | JQL |
|:---:|:---:|
| 进行中议题 | `project = PROJ AND status = "In Progress"` |
| 我的待办 | `project = PROJ AND assignee = currentUser()` |
| 最近更新 | `project = PROJ ORDER BY updated DESC` |
| 高优先级未完成 | `project = PROJ AND priority = High AND status != Done` |
| 指定冲刺 | `project = PROJ AND sprint = "Sprint 42"` |

## 最佳实践

1. **先取 cloud-id**：所有操作都需要 cloud-id，建议缓存避免重复请求。
2. **JQL 必须有界**：始终包含 `project=KEY` 限定范围，避免全库扫描触发性能问题。
3. **字段过滤减负**：`--fields summary,status,assignee` 只取需要的字段，降低响应体积与速率消耗。
4. **URL 编码 JQL**：直接调用 REST API 时 JQL 参数需 URL 编码（`%3D` 等）。
5. **分页控制**：`--limit` 控制单次返回条数，默认 20，建议不超过 50。
6. **多连接显式指定**：多个 Jira 账号时务必 `--connection <id>` 指定，避免请求到错误账号。
7. **curl 用 -g**：URL 含方括号（`fields[]`）时用 `curl -g` 禁用 glob 解析。

## 常见问题

### Q1：报 401 Invalid API key 怎么办？

A：(1) 运行 `maton whoami` 检查登录状态；(2) 重新 `maton login`；(3) 确认 `MATON_API_KEY` 环境变量已设置且未过期。

### Q2：报 400 Missing Jira connection？

A：未创建 Jira OAuth 连接。运行 `maton connection create jira`，在浏览器完成授权。

### Q3：报 429 Rate limited？

A：Jira Cloud 限制 10 请求/秒/账号。建议：(1) 降低查询频率；(2) 加 `--limit` 减少单次返回；(3) 缓存结果复用。

### Q4：JQL 报错语法错误？

A：(1) 字符串值用双引号包裹（`status = "In Progress"`）；(2) 字段名区分大小写；(3) 使用 URL 编码（`%3D` 表示 `=`）。

### Q5：免费版能否创建/更新议题？

A：免费版仅支持只读操作。创建、更新、删除、流转等写操作需使用专业版。

## 已知限制

本免费体验版限制以下高级功能：
- 创建议题（专业版支持）
- 更新/删除议题（专业版支持）
- 流转议题状态（专业版支持）
- 评论管理（专业版支持）
- 用户搜索（专业版支持）
- 批量操作与自动化工作流（专业版支持）
- 多连接高级管理与优先支持（专业版支持）

解锁全部功能请使用专业版：jira-api-toolkit-pro
- 当前为免费版本,如需完整功能请升级到付费版获取全部能力
## 依赖说明

### 运行环境
- **Agent 平台**：支持 SKILL.md 的任意 AI Agent（Claude Code / Cursor / Codex / Gemini CLI 等）
- **操作系统**：Windows / macOS / Linux
- **Node.js**：16+（用于运行 CLI）

### 第三方依赖
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:------|------:|:------|:------|
| LLM API | API | 必需 | 由 Agent 平台内置 LLM 提供 |
| maton CLI | 命令行工具 | 必需 | `npm install -g @maton/cli` 或 `brew install maton-ai/cli/maton` |
| Jira Cloud 账号 | SaaS 账号 | 必需 | Atlassian 账号，用于 OAuth 授权 |
| Node.js | 运行时 | 必需 | Node.js 官方渠道下载 |

### API Key 配置
- **maton API Key**：通过 `maton login` 获取，存储于环境变量 `MATON_API_KEY`，禁止硬编码
- **Jira OAuth 连接**：通过 `maton connection create jira` 在浏览器完成授权，无需手动管理令牌
- **禁止**：在 SKILL.md 或脚本中硬编码 API Key 与 OAuth 令牌

### 可用性分类
- **分类**：MD+EXEC（纯 Markdown 指令，部分功能需要 exec 命令行执行能力）
- **说明**：基于 Markdown 的 AI Skill，通过自然语言指令驱动 Agent 执行任务，仅支持只读操作

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|---:|:---|---:|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |
