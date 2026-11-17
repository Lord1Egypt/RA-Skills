---
name: "linear-sync-tool-free"
description: "管理Linear任务与项目的免费命令行工具，支持任务列表、查看与基础创建。Use when 需要项目管理、任务规划、进度跟踪、团队协作时使用。不适用于实际人员绩效评估。适用于独立开发者、企业团队和自动化工作流场景。支持中文交互，无需复杂配置即开即用。输出结果可直接使用，减少二次加工成本。提供结构化输出和错误处理机制。"
license: Proprietary
allowed-tools: read exec
compatibility: "Requires LLM with tool-use capability"
metadata:
  displayName: "Linear同步(免费版)"
  version: "1.0.0"
  summary: "管理Linear任务与项目的免费命令行工具，支持任务列表、查看与基础创建"
  tags:
    - "任务管理"
    - "项目协作"
    - "命令行工具"
    - "集成工具"
  source: "SkillHub"
  converted_at: "2026-07-22T17:58:36"
tools:
  - exec
  - read
  - write
---

> **功能说明**: 本技能涵盖 中文交互、化工作流场景 等核心能力。

# Linear同步工具（免费版）

通过命令行驱动AI Agent管理Linear任务和项目，实现任务查询、查看和基础创建。免费版提供只读查询和简单创建功能，满足个人开发者日常使用。

## 概述

Linear是一款流行的研发项目管理工具，但在命令行集成和自动化场景下，网页操作效率有限。本Skill封装了Linear CLI的命令行接口，让AI Agent能够通过自然语言指令查询任务、查看详情和创建工单，将重复性的任务管理操作自动化。

免费版聚焦查询和基础创建能力，提供任务列表、详情查看、团队和项目信息查询，适合个人开发者快速管理自己的工单。

## 核心能力

| 能力模块 | 免费版支持 | 说明 |
|:---------|:-----------|:-----|
| 任务列表 | 支持 | 按状态、团队过滤查看任务 |
| 任务详情 | 支持 | 查看任务完整信息 |
| 任务创建 | 基础 | 创建简单任务（标题+描述） |
| 团队查询 | 支持 | 列出团队和成员 |
| 项目查询 | 支持 | 列出项目信息 |
| 任务更新 | 不支持 | 专业版提供 |
| 任务评论 | 不支持 | 专业版提供 |
| 批量操作 | 不支持 | 专业版提供 |
| 文档管理 | 不支持 | 专业版提供 |
| GraphQL API | 不支持 | 专业版提供 |
| 里程碑管理 | 不支持 | 专业版提供 |
| Git集成 | 不支持 | 专业版提供 |

### 核心功能执行
用`input_params`参数进行配置。

**输出**: 返回核心功能执行的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 参数配置与调用
用`config_options`参数进行配置。

**输出**: 返回参数配置与调用的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`config_options`参数,支持修改/重置/导入操作

### 结果处理与输出
用`output_format`参数进行配置。

**输出**: 返回结果处理与输出的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`output_format`参数,支持导出/保存/转换操作
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：Linear、任务与项目的免费、命令行工具、支持任务列表、查看与基础创建、同步工具免费版是、一款面向项目管理、的命令行辅助、Skill、Agent、能够通过、CLI、管理任务工单、查看项目状态和创、建基础任务、实现研发协作的命、令行自动化、核心能力、任务列表查看、任务详情查看、基础任务创建、团队信息查询、项目列表查看、Use、when、需要项目管理、任务规划、进度跟踪、团队协作时使用、不适用于实际人员、绩效评估等。

## 使用场景

### 场景一：每日任务查看

每天早上快速查看分配给自己的待办任务，了解当天工作重点。

### 场景二：快速创建任务

在开发过程中发现bug或新需求时，通过命令行快速创建任务工单，无需切换到浏览器。

### 场景三：团队状态查看

查看团队当前的任务分布和项目进度，为站会做准备。

## 快速开始

### 前置条件

1. 已安装`linear`命令行工具并可用
2. 已在Linear设置中创建API Key
3. 已完成认证配置

### 依赖详情

```bash
# 检查linear CLI是否可用
linear --version

# 认证登录
linear auth login

# 配置项目（在项目根目录执行）
linear config
```

### 60秒上手

```bash
# 1. 查看所有任务
linear issue list

# 2. 查看指定任务
linear issue view ABC-123

# 3. 查看未完成任务
linear issue list -s started

# 4. 创建简单任务
linear issue create -t "修复登录bug" -d "用户无法通过SSO登录"

# 5. 查看团队列表
linear team list
```

**结果处理**: 执行完成后,查看输出结果确认操作状态。成功时输出包含处理摘要和结果数据;失败时根据错误信息排查问题,查阅错误处理章节获取恢复步骤。

## 示例

### 命令结构

```bash
linear <资源类型> <操作> [参数]
```

### 任务查询

```bash
# 列出所有任务
linear issue list

# 按状态过滤
linear issue list -s started        # 进行中
linear issue list -s completed      # 已完成

# 查看所有状态的任务
linear issue list -A

# 查看指定任务详情
linear issue view
linear issue view ABC-123
```

### 任务创建（基础）

```bash
# 创建简单任务
linear issue create -t "任务标题" -d "任务描述"

# 创建任务并指定状态
linear issue create -t "修复bug" -d "描述" -s "In Progress"

# 创建任务并分配给自己
linear issue create -t "新功能开发" -d "描述" -a self
```

### 团队与项目查询

```bash
# 列出所有团队
linear team list

# 查看团队成员
linear team members

# 列出所有项目
linear project list

# 查看项目详情
linear project view <projectId>
```

### 配置文件

通过`.linear.toml`配置文件设置默认参数：

```toml
# .linear.toml
team_id = "ENG"
workspace = "mycompany"
issue_sort = "priority"
vcs = "git"
```

配置文件查找顺序：
1. 当前目录的`linear.toml`或`.linear.toml`
2. 项目根目录的`linear.toml`或`.linear.toml`
3. 项目根目录的`.config/linear.toml`
4. 用户目录的`$HOME/.config/linear/linear.toml`

### 环境变量配置

| 配置项 | 环境变量 | 示例值 |
|:-------|:---------|:-------|
| 团队ID | `LINEAR_TEAM_ID` | `"ENG"` |
| 工作区 | `LINEAR_WORKSPACE` | `"mycompany"` |
| 任务排序 | `LINEAR_ISSUE_SORT` | `"priority"` 或 `"manual"` |
| 版本控制 | `LINEAR_VCS` | `"git"` 或 `"jj"` |

## 优选实践

1. **配置默认团队**：在`.linear.toml`中设置`team_id`，避免每次查询都指定团队。
2. **使用状态过滤**：日常查看用`-s started`只看进行中的任务，减少信息过载。
3. **任务标题简洁明确**：创建任务时标题用"动词+对象"格式（如"修复登录页SSO跳转"），便于检索。
4. **利用配置文件分层**：项目级配置放在项目根目录，个人偏好放在用户目录，实现配置复用。
5. **定期查看全量任务**：每周用`linear issue list -A`查看全量任务，掌握整体进度。

## 常见问题

### Q1: linear命令未找到？

请先安装linear命令行工具。安装后确保二进制文件在系统PATH中。执行`linear --version`验证安装是否成功。

### Q2: 认证失败怎么办？

在Linear网页端设置 → 账户 → 安全中创建API Key，然后执行`linear auth login`完成认证。确保API Key未过期且有足够权限。

### Q3: 查询结果为空？

检查默认团队配置是否正确。使用`linear team list`确认团队ID，在`.linear.toml`中设置正确的`team_id`。

### Q4: 创建任务时报权限错误？

确认API Key有创建任务的权限。Linear的API Key权限可在设置中管理，确保已勾选写入权限。

### Q5: 如何查看不同团队的任务？

通过`LINEAR_TEAM_ID`环境变量临时指定团队，或在命令中通过参数指定团队ID。

## 依赖说明

### 运行环境

- **Agent平台**：支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**：Windows / macOS / Linux
- **linear CLI**：已安装并通过认证

### 第三方依赖

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-------|:-----|:---------|:---------|
| linear CLI | 命令行工具 | 必需 | 通过包管理器安装 |
| Linear账户 | 在线账户 | 必需 | 在Linear官网注册 |
| Linear API Key | 认证凭据 | 必需 | 在Linear设置中创建 |
| LLM API | API | 必需 | 由Agent平台内置LLM提供 |

### API Key 配置

- **Linear API Key**：在Linear网页端设置 → 账户 → 安全中创建
- **存储方式**：通过`linear auth login`命令安全存储，或通过环境变量`LINEAR_API_KEY`配置
- **禁止**：在代码或配置文件中明文写入API Key
- **权限管理**：API Key的权限范围在Linear设置中控制，建议遵循最小权限原则

### 可用性分类

- **分类**：MD+EXEC（纯Markdown指令，需要exec命令行执行能力）
- **说明**：基于Markdown的AI Skill，通过自然语言指令驱动Agent执行Linear命令行操作

## 已知限制

本免费体验版限制以下高级功能：
- 任务更新与状态变更（专业版支持修改标题、状态、优先级等）
- 任务评论管理（专业版支持添加、查看和回复评论）
- 任务删除（专业版支持安全删除任务）
- 批量操作（专业版支持批量创建、更新和状态变更）
- 文档管理（专业版支持Linear文档的创建、查看和编辑）
- 里程碑管理（专业版支持项目里程碑的创建和查看）
- GraphQL API直接调用（专业版支持原始GraphQL查询）
- Git集成（专业版支持分支创建和PR关联）
- 任务开始与PR创建（专业版支持`issue start`和`issue pr`工作流）

解锁全部功能请使用专业版：linear-sync-tool-pro
- 当前为免费版本,如需完整功能请升级到付费版获取全部能力
## 错误处理

| 错误场景 | 原因 | 处理方式 |
|---------|------|---------|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 安全注意事项

| 风险类型 | 防范措施 |
|----------|---------|
| API密钥泄露 | 通过环境变量配置，禁止硬编码到代码或配置文件中 |
| 命令执行风险 | 仅执行白名单命令，避免拼接用户输入到命令行参数中 |
| 网络通信安全 | 使用HTTPS协议，验证SSL证书有效性 |
| 敏感数据暴露 | 输出结果中不包含密钥、令牌等敏感信息 |

使用前请确认已阅读依赖说明章节，确保运行环境满足安全要求。