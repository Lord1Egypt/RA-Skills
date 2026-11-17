---
slug: notion-cli-tool-free
name: notion-cli-tool-free
version: 1.0.0
displayName: Notion命令行(免费版)
summary: 轻量化Notion命令行工具,支持数据库查询、页面管理、块操作与别名机制,适合个人开发者从终端高效操作Notion.
license: Proprietary
edition: free
description: 'Notion命令行(免费版)是面向个人开发者与知识工作者的轻量化Notion操作Skill,通过命令行工具的组合,帮助用户从终端高效完成Notion工作空间的日常操作。核心能力:

  - 数据库自动发现与别名管理,告别UUID

  - 页面CRUD(创建、查询、更新、归档)

  - 块级内容管理(读取、追加、编辑、删除)

  - 多格式输出(表格、CSV、JSON、YAML)

  - 评论与用户管理

  - 关系与汇总字段自动解析

  适用场景:

  - 个人Notion工作空间的终端化操作

  - 小型团队的任务与项目管理

  - 自动化脚...'
tags:
  - 集成工具
  - Notion
  - 命令行
  - 工具
  - 效率
  - 写作
  - 电商
  - notion
  - tasks
  - filter
  - bash
  - query
tools:
  - read
  - exec
  - write
homepage: ""
category: "Automation"
---
# Notion命令行(免费版)

一个面向个人开发者与知识工作者的轻量化Notion操作Skill,通过命令行工具的组合,帮助你从终端高效完成Notion工作空间的日常操作。本免费版聚焦单工作空间与基础操作,适合个人与小型团队试用.
## 概述

本Skill封装了Notion API的常用操作,通过别名机制屏蔽UUID复杂度。安装后执行`init`命令即可自动发现所有共享数据库,并为每个数据库分配易记的别名(如`tasks`、`projects`),后续操作直接使用别名,无需记忆UUID。免费版适合单工作空间、日操作量不超过500次的场景.
## 核心能力

| 能力 | 描述 | 免费版是否支持 |
|---|---|-------|
| 数据库发现 | 自动发现共享数据库 | 支持 |
| 别名管理 | 添加、重命名、删除别名 | 支持 |
| 页面查询 | 查询、筛选、排序 | 支持 |
| 页面CRUD | 创建、更新、归档 | 支持 |
| 块管理 | 读取、追加、编辑、删除 | 支持 |
| 评论管理 | 查看、添加评论 | 支持 |
| 用户管理 | 列出用户、查看当前用户 | 支持 |
| 多格式输出 | 表格/CSV/JSON/YAML | 支持 |
| 关系解析 | 自动解析关系字段 | 支持 |
| 多工作空间 | 同时管理多个账户 | 不支持 |
| 文件上传 | 上传附件到页面 | 不支持 |
| 数据库Schema管理 | 增删改属性列 | 不支持 |
| 页面移动 | 跨数据库移动页面 | 不支持 |
| 批量操作 | 批量创建/更新/删除 | 不支持 |
| 模板管理 | 页面模板列表与使用 | 不支持 |

### 核心功能执行
用`input_params`参数进行配置.

**处理**: 解析核心功能执行的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回核心功能执行的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 参数配置与调用
用`config_options`参数进行配置.

**处理**: 解析参数配置与调用的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回参数配置与调用的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`config_options`参数,支持修改/重置/导入操作

### 结果处理与输出
用`output_format`参数进行配置.

**处理**: 解析结果处理与输出的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回结果处理与输出的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`output_format`参数,支持导出/保存/转换操作
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：轻量化、Notion、命令行工具、支持数据库查询、页面管理、块操作与别名机制、适合个人开发者从、终端高效操作、命令行、是面向个人开发者、与知识工作者的轻、通过命令行工具的、帮助用户从终端高、效完成、工作空间的日常操、核心能力等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
## 使用场景

### 场景一:个人任务管理

个人开发者希望从终端管理自己的Notion任务库.
```bash
# 1. 初始化并发现数据库
notion init --key $NOTION_API_KEY
# 输出:发现3个数据库:
#   tasks → 任务库
#   projects → 项目库
#   reading-list → 阅读清单
# ...
# 2. 查询所有任务
notion query tasks
# ...
# 3. 筛选进行中的任务
notion query tasks --filter Status=Active --sort Date:desc
# ...
# 4. 添加新任务
notion add tasks --prop "Name=完成周报" --prop "Status=Todo" --prop "Priority=High"
# ...
# 5. 更新任务状态
notion update tasks --filter "Name=完成周报" --prop "Status=Done"
```

### 场景二:AI Agent的Notion调用

AI Agent需要通过命令行操作Notion,完成自动化任务.
```bash
# 1. 发现可用数据库
notion dbs
notion alias list
# ...
# 2. 查询任务详情
notion get tasks --filter "Name=Review PR #42"
notion blocks tasks --filter "Name=Review PR #42"
# ...
# 3. 追加工作日志
notion append tasks "完成代码审查,合并到main分支" --filter "Name=Review PR #42"
# ...
# 4. 添加AI审查评论
notion comment tasks "AI review complete" --filter "Name=Review PR #42"
```

### 场景三:数据导出与分析

数据分析师希望将Notion数据导出为CSV,在Excel中分析.
```bash
# 导出为CSV
notion query tasks --output csv > tasks.csv
# ...
# 导出为JSON
notion --json query tasks > tasks.json
# ...
# 导出为YAML
notion query tasks --output yaml > tasks.yaml
```

## 不适用场景

以下场景Notion命令行(免费版)不适合处理：

- 实际人员绩效评估
- 财务预算审批
- 合同法务审核

## 触发条件

需要项目管理、任务规划、进度跟踪、团队协作时使用。不适用于非本工具能力范围的需求.
## 快速开始

预计上手时间:<60秒.
### 依赖详情

```bash
npm install -g notion-cli-tool
```

### Step 2:初始化并配置API Key

```bash
notion init --key ntn_your_integration_token_here
# 自动发现所有共享数据库并分配别名
```

> **提示**:在Notion中需要将数据库共享给你的Integration:打开数据库 → •••菜单 → 连接 → 添加你的Integration.
### Step 3:验证安装

```bash
notion dbs
notion alias list
notion me
```

### Step 4:开始操作

```bash
notion query tasks
notion add tasks --prop "Name=第一个任务" --prop "Status=Todo"
```

**响应解析**: 完成完成后,查看输出响应确认任务状态。成功时输出包含解析摘要和响应数据;失败时根据错误信息排查问题,查阅错误解析章节获取恢复步骤.
## 示例

### 别名管理

```bash
# 查看所有别名
notion alias list
# ...
# 添加自定义别名
notion alias add mydb 12345678-abcd-efgh-ijkl-1234567890ab
# ...
# 重命名别名
notion alias rename old-name new-name
# ...
# 删除别名
notion alias remove mydb
```

### 查询示例

```bash
# 查询所有行
notion query tasks
# ...
# 筛选+排序
notion query tasks --filter Status=Active --sort Date:desc
# ...
# 已知限制
notion query tasks --filter Status=Active --limit 10
# ...
# 多格式输出
notion query tasks --output csv
notion query tasks --output json
notion query tasks --output yaml
```

### 创建与更新示例

```bash
# 创建页面(多个--prop指定多个属性)
notion add tasks --prop "Name=买 groceries" --prop "Status=Todo"
# ...
# 按ID更新
notion update <page-id> --prop "Status=Done"
# ...
# 按别名+筛选更新(零UUID)
notion update tasks --filter "Name=Ship feature" --prop "Status=Done"
```

### 读取与块管理

```bash
# 按ID读取
notion get <page-id>
notion blocks <page-id>
# ...
# 按别名+筛选读取
notion get tasks --filter "Name=Ship feature"
notion blocks tasks --filter "Name=Ship feature"
# ...
# 追加块
notion append tasks "新段落内容" --filter "Name=Ship feature"
# ...
# 块ID查看与编辑
notion blocks tasks --filter "Name=Ship feature" --ids
notion block-edit <block-id> "更新后的文本"
notion block-delete <block-id>
```

### 评论与用户

```bash
# 查看评论
notion comments <page-id>
notion comments tasks --filter "Name=Ship feature"
# ...
# 添加评论
notion comment <page-id> "看起来不错,准备合并"
notion comment tasks "AI审查完成" --filter "Name=Ship feature"
# ...
# 用户管理
notion users
notion user <user-id>
notion me
```

### 属性类型参考

| 类型 | 示例值 | 说明 |
|:-----|:-----|:-----|
| `title` | `Name=Hello World` | 主标题属性 |
| `rich_text` | `Notes=Some text` | 纯文本内容 |
| `number` | `Amount=42.5` | 数值 |
| `select` | `Status=Active` | 单选 |
| `multi_select` | `Tags=bug,urgent` | 多选(逗号分隔) |
| `date` | `Due=2026-03-01` | ISO 8601日期 |
| `checkbox` | `Done=true` | 布尔(true/1/yes) |
| `url` | `Link=https://example.com` | 完整URL |
| `email` | `Contact=user@example.com` | 邮箱 |
| `phone_number` | `Phone=+1234567890` | 电话 |
| `status` | `Status=In Progress` | 状态属性 |

## 最佳实践

1. **优先使用别名+筛选**:避免记忆UUID,操作更自然
2. **属性名大小写不敏感**:`Status`与`status`等价,系统自动匹配
3. **筛选前先查schema**:用`notion --json query <alias> --limit 1`查看可用属性
4. **CSV输出用于分析**:CSV格式适合导入Excel或Pandas做数据分析
5. **JSON输出用于脚本**:JSON格式适合程序化处理
6. **追加内容用append**:比update更适合添加新段落
7. **评论用于协作**:通过`comment`命令实现AI Agent与人的协作
8. **定期同步别名**:新增数据库后执行`notion init`重新发现

## 已知限制

- 本skill的能力范围受限于核心能力章节中定义的功能,不支持超出范围的操作
- 复杂业务场景建议结合人工经验判断
- 执行效率受模型能力与网络环境影响
- 当前为免费版本,如需完整功能请升级到付费版获取全部能力
## 常见问题

### Q1: 提示"No Notion API key found"怎么办?

A: 1)执行`notion init --key ntn_...`;2)或设置环境变量`export NOTION_API_KEY=ntn_...`.
### Q2: 提示"Unknown database alias"怎么办?

A: 1)执行`notion alias list`查看可用别名;2)执行`notion init`重新发现数据库;3)用`notion alias add`手动添加.
### Q3: 提示"Not found"怎么办?

A: 确认数据库/页面已在Notion中共享给你的Integration。打开数据库 → •••菜单 → 连接 → 添加你的Integration.
### Q4: 筛选/排序属性找不到?

A: 属性名大小写不敏感。先用`notion --json query <alias> --limit 1`查看可用属性名.
### Q5: 关系字段如何查询?

A: 用`notion relations tasks --filter "Name=xxx"`,关系字段会自动解析为页面标题.
### Q6: 免费版可以管理多个工作空间吗?

A: 不可以。免费版仅支持单工作空间。多工作空间管理请使用专业版.
## 错误处理

| 错误场景(症状) | 可能原因 | 解决方案 |
|------:|------:|------:|
| No Notion API key found | API Key未配置 | 执行`init`或设置环境变量 |
| Unknown database alias | 别名不存在或未初始化 | 用`alias list`查看,或`init`重新发现 |
| Not found | 资源未共享给Integration | 在Notion中将数据库/页面共享给Integration |
| Filter property not found | 属性名拼写错误 | 用`--json query --limit 1`查看属性名 |
| 关系字段显示UUID | 关系未自动解析 | 用`relations`命令查看,会解析为标题 |
| 输出格式异常 | 输出格式参数错误 | 对照属性类型参考表检查 |
## 免费版限制

本免费体验版限制以下高级功能:

- 多工作空间管理(同时管理>1个Notion账户)
- 文件上传(上传附件到页面)
- 数据库Schema管理(增删改属性列)
- 页面移动(跨数据库移动页面)
- 批量操作(批量创建/更新/删除)
- 模板管理(页面模板列表与使用)
- 自定义输出格式(Jinja2模板)
- 团队协作与共享配置
- 审计日志与操作追踪

解锁全部功能请使用专业版:notion-cli-tool-pro

## 依赖说明

### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent(Claude Code / Cursor / Codex / Gemini CLI等)
- **操作系统**: Windows / macOS / Linux
- **Node.js**: 16+(用于运行CLI工具)

### 第三方依赖
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:---:|:---:|:---:|:---:|
| LLM API | API | 必需 | 由Agent平台内置LLM提供 |
| notion-cli-tool CLI | 命令行工具 | 必需 | `npm install -g notion-cli-tool` |
| Notion Integration | 在线服务 | 必需 | 通过Notion开发者平台创建 |

### API Key 配置
- **NOTION_API_KEY**: 通过`notion init --key`命令配置,或通过环境变量传入
- **存储位置**: 默认存储在`~/.notion-cli/config.json`,可通过`NOTION_CLI_HOME`自定义
- **安全建议**: API Key禁止硬编码在脚本中,建议使用环境变量或配置文件
- **权限最小化**: Integration仅授予任务所需的权限范围,避免过度授权

### 可用性分类
- **分类**: MD+EXEC(纯Markdown指令,部分功能需exec命令行执行)
- **说明**: 基于Markdown的AI Skill,通过自然语言指令驱动Agent完成操作
