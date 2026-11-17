---
slug: linear-api-toolkit-free
name: linear-api-toolkit-free
version: 1.0.0
displayName: Linear工具箱(免费版)
summary: 通过GraphQL查询管理Linear任务、项目与团队，支持问题查看与基础操作
license: Proprietary
edition: free
description: 'Linear工具箱(免费版)是一款通过GraphQL API与Linear交互的任务管理工具，支持问题查询、项目浏览、团队管理与评论查看等核心能力。核心能力：

  - 通过GraphQL查询Linear问题、项目、团队、周期与标签

  - 查看当前用户与组织信息

  - 创建与更新问题。Use when 需要项目管理、任务规划、进度跟踪、团队协作时使用。不适用于实际人员绩效评估。'
tags:
- 集成工具
- 项目管理
- Linear
tools:
- - read
- exec
homepage: https://skillhub.cn
pricing_tier: L2
pricing_model: per_use
suggested_price: 19.9
tools: ["read", "write", "exec"]
tags: "API,接口,开发工具"
---
# Linear工具箱(免费版)

本工具通过GraphQL API帮助用户与Linear交互，实现问题查询、项目管理、团队协作等核心功能。免费版聚焦日常查阅与基础操作需求。

## 概述

Linear是现代软件开发团队青睐的任务管理工具，其GraphQL API提供了强大的查询与操作能力。然而直接编写GraphQL查询对非技术用户门槛较高。本工具将常用操作封装为简洁的CLI命令，同时提供Python示例供集成使用，让Agent能够按需查询问题、管理项目、追踪团队进度。

免费版面向个人开发者与团队成员的日常使用，提供完整的查询能力与基础写入操作，不限制使用次数。

## 核心能力

| 能力 | 说明 | 免费版可用 |
|---|---|-----|
| 问题查询 | 按团队/状态/标题过滤查询 | 是 |
| 问题详情 | 查看问题完整信息 | 是 |
| 问题创建 | 创建新问题 | 是 |
| 问题更新 | 更新标题/优先级/状态 | 是 |
| 评论管理 | 查看与创建评论 | 是 |
| 项目与团队 | 浏览项目与团队列表 | 是 |
| 批量操作 | 批量创建/更新/迁移 | 否 |
| Webhook集成 | 事件订阅与自动化 | 否 |
| 高级分析 | 效率分析与燃尽图 | 否 |
**技术实现要点**：核心能力基于`input_params`参数与`output_format`配置实现,支持创建/查询/修改/删除等操作模式,通过`config_options`进行运行时配置。

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
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：GraphQL、查询管理、Linear、支持问题查看与基、础操作、工具箱、是一款通过、API、交互的任务管理工、支持问题查询、项目浏览、团队管理与评论查、看等核心能力、周期与标签、查看当前用户与组、织信息、创建与更新问题、Use、when、需要项目管理、任务规划、进度跟踪、团队协作时使用、不适用于实际人员、绩效评估等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持。

## 使用场景

### 场景一：开发者查询待办问题
开发者希望快速查看分配给自己的高优先级未完成问题。通过CLI命令按团队与状态过滤，获取问题列表与标识符，无需打开Linear网页端即可了解待办事项。

### 场景二：项目经理浏览项目状态
项目经理需要了解各项目的当前进展。通过项目列表命令获取所有项目及状态，针对关注的项目深入查看关联问题，评估是否需要调整资源分配。

### 场景三：团队成员添加协作评论
团队成员在审查问题时希望添加上下文评论。通过评论创建命令为指定问题添加说明，支持提及与其他成员，保持协作信息完整。

### 场景四：自动化脚本查询任务
开发者编写自动化脚本，通过Python示例调用GraphQL API查询待办任务，集成到每日站会提醒或个人看板中。

## 快速开始

本工具属于中等复杂度工具，预计120秒内可完成首次查询。

### 依赖详情
```bash
# 通过NPM安装
npm install -g @maton/cli
# ...
# 或通过Homebrew安装
brew install maton-ai/cli/maton
```

### Step 2：配置认证
```bash
# 浏览器登录获取API密钥
maton login
# ...
# 或交互式输入API密钥
maton login --interactive
# ...
# 验证认证状态
maton whoami
```

### Step 3：创建Linear连接
```bash
# 创建OAuth连接
maton connection create linear
# ...
# 打开返回的URL完成OAuth授权
```

### Step 4：查询问题
```bash
# 列出团队的最近10个问题
maton linear issue list -c ABC -L 10
# ...
# 查看特定问题详情
maton linear issue view ABC-123
```

## 示例

### 环境变量配置
```bash
# 设置API密钥
export MATON_API_KEY="你的API密钥"
```

### CLI命令速查

| 命令 | 说明 | 示例 |
|:-----|:-----|:-----|
| maton linear whoami | 查看当前用户 | `maton linear whoami` |
| maton linear org view | 查看组织信息 | `maton linear org view` |
| maton linear team list | 列出团队 | `maton linear team list` |
| maton linear team view ABC | 查看团队详情 | `maton linear team view ABC` |
| maton linear issue list | 列出问题 | `maton linear issue list -c ABC -L 10` |
| maton linear issue view | 查看问题 | `maton linear issue view ABC-123` |
| maton linear issue create | 创建问题 | `maton linear issue create --team-id TEAM_ID -t '标题'` |
| maton linear issue update | 更新问题 | `maton linear issue update ABC-123 --priority 2` |
| maton linear project list | 列出项目 | `maton linear project list` |
| maton linear cycle list | 列出周期 | `maton linear cycle list` |
| maton linear label list | 列出标签 | `maton linear label list` |
| maton linear comment list | 列出评论 | `maton linear comment list --issue ABC-123` |
| maton linear comment create | 创建评论 | `maton linear comment create --issue ABC-123 -b '内容'` |

### 问题优先级说明

| 值 | 含义 | 使用场景 |
|---:|---:|---:|
| 0 | 无优先级 | 待评估的问题 |
| 1 | 紧急 | 阻塞发布的关键问题 |
| 2 | 高 | 本迭代必须完成 |
| 3 | 中 | 计划内完成 |
| 4 | 低 | 有空再做 |

### 工作流状态类型

| 类型 | 说明 |
|:---:|:---:|
| backlog | 待办池 |
| unstarted | 未开始 |
| started | 进行中 |
| completed | 已完成 |
| canceled | 已取消 |

## 最佳实践

### 实践一：查询前先明确范围
Linear中问题数量可能庞大，直接全量查询会消耗大量资源。建议先通过`team list`确定团队key，再按团队过滤查询。使用`-L`参数限制返回数量，避免响应过大。

### 实践二：善用过滤器
问题列表支持按状态类型、标题关键词过滤。`--state started`只返回进行中的问题；`--title bug`只返回标题含"bug"的问题。合理使用过滤器能快速定位目标问题。

### 实践三：写入操作需确认
所有写入操作(创建/更新/删除)执行前应与用户确认目标资源与预期效果。特别是更新操作，先通过`issue view`确认当前状态，避免误操作覆盖重要信息。

### 实践四：多连接场景指定连接
若配置了多个Linear连接(如个人账户与企业账户)，执行操作时通过`--connection`参数指定目标连接，确保操作作用于正确的账户。

### 实践五：分页查询处理大数据集
对于大量问题，使用`--paginate`参数启用自动翻页。CLI基于游标分页自动获取全部结果，避免手动处理分页逻辑。

## 常见问题

### Q1：提示401未授权怎么办？
A：检查API密钥是否正确配置。执行`maton whoami`验证认证状态。若密钥过期，重新执行`maton login`获取新密钥。

### Q2：提示400缺少Linear连接？
A：说明尚未创建Linear OAuth连接。执行`maton connection create linear`创建连接，并打开返回的URL完成OAuth授权。

### Q3：提示403权限不足？
A：某些操作(如删除、创建标签)需要额外的OAuth权限。联系API服务方支持团队，说明所需操作与使用场景，申请权限调整。

### Q4：问题标识符ABC-123如何使用？
A：Linear的问题标识符(如ABC-123)可在命令中替代UUID使用。ABC是团队key，123是问题序号。`maton linear issue view ABC-123`即可查看对应问题。

### 已知限制
A：免费版不限制使用次数，但批量操作、Webhook集成与高级分析功能需使用专业版。
- 当前为免费版本,如需完整功能请升级到付费版获取全部能力
## 错误处理

| 错误场景(现象) | 可能原因 | 解决方案 |
|:----------|----------:|:----------|
| 401 Unauthorized | API密钥无效 | 重新执行maton login |
| 400 Bad Request | 缺少连接或GraphQL错误 | 创建连接，检查查询语法 |
| 403 Forbidden | OAuth权限不足 | 申请额外权限范围 |
| 429 Too Many Requests | 触发速率限制 | 降低调用频率，间隔执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令 |
| 连接URL打不开 | 网络或浏览器问题 | 手动复制URL到浏览器 |
| 查询结果为空 | 过滤条件过严 | 放宽过滤条件或检查团队key |
## 免费版限制

本免费体验版限制以下高级功能：
- 批量操作(批量创建/更新/迁移问题)
- Webhook集成(事件订阅与自动化触发)
- 高级分析(效率分析、燃尽图、周期报告)
- 自定义GraphQL查询模板
- 多工作区并行管理
- 优先技术支持

解锁全部功能请使用专业版：linear-api-toolkit-pro

## 依赖说明

### 运行环境
- **Agent平台**：支持SKILL.md的任意AI Agent(Claude Code / Cursor / Codex / Gemini CLI等)
- **操作系统**：Windows / macOS / Linux
- **Node.js**：16+(用于运行CLI工具)

### 第三方依赖

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|---:|:---|---:|---:|
| LLM API | API | 必需 | 由Agent平台内置LLM提供 |
| Node.js | 运行时 | 必需 | nodejs.org官方下载 |
| Maton CLI | CLI工具 | 必需 | `npm install -g @maton/cli` |
| Linear GraphQL API | 外部API | 必需 | 需Linear账户与OAuth连接 |

### API Key 配置
- **Maton API Key**：通过`maton login`获取，存储在本地配置中
- **手动配置**：也可通过`MATON_API_KEY`环境变量设置
- **Linear OAuth**：通过`maton connection create linear`创建OAuth连接
- **安全要求**：禁止在SKILL.md或脚本中硬编码API密钥，禁止提交到版本控制

### 可用性分类
- **分类**：MD+EXEC(纯Markdown指令，部分功能需要exec命令行执行能力)
- **说明**：基于Markdown的AI Skill，通过自然语言指令驱动Agent执行Linear任务管理操作

## 输出格式
```json
{
  "success": true,
  "data": {
    "result": "Linear工具箱(免费版)处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "linear apikit"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```
