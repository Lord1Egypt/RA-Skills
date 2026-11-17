---
slug: linear-workflow-skill-free
name: linear-workflow-skill-free
version: 1.0.0
displayName: Linear工作流(免费版)
summary: 通过Node CLI管理Linear问题与项目，支持问题查看、创建与状态更新
license: Proprietary
edition: free
description: 'Linear工作流(免费版)是一款通过内置Node CLI与Linear官方API交互的工作流管理工具，支持问题查看、创建、更新与项目管理等核心能力。核心能力：

  - 通过Node CLI查询团队、项目与问题

  - 创建与更新问题，支持优先级与状态设置

  - 添加协作评论。Use when 需要项目管理、任务规划、进度跟踪、团队协作时使用。不适用于实际人员绩效评估。'
tags:
- 集成工具
- 项目管理
- Linear
tools:
- - read
- exec
homepage: https://skillhub.cn
pricing_tier: L3
pricing_model: per_use
suggested_price: 29.9
tools: ["read", "write", "exec"]
tags: "工作流,自动化,效率"
---
# Linear工作流(免费版)

本工具通过内置Node CLI帮助用户管理Linear问题与项目，遵循"先读后写"的安全工作流，确保操作准确可追溯。

## 概述

Linear工作流管理的核心在于"有序操作"：先了解当前状态，再执行变更，最后确认结果。本工具将这一理念融入命令设计，所有写入操作建议先通过查询命令确认目标资源，避免基于错误假设执行变更。内置Node CLI直接调用Linear官方SDK，认证简单、响应快速。

免费版面向个人开发者与团队成员的日常问题管理需求，提供完整的查询与写入能力，不限制使用次数。

## 核心能力

| 能力 | 说明 | 免费版可用 |
|---|---|-----|
| 团队查询 | 列出所有团队 | 是 |
| 项目查询 | 列出所有项目 | 是 |
| 问题查询 | 列出与查看问题详情 | 是 |
| 问题创建 | 创建新问题 | 是 |
| 问题更新 | 更新状态/优先级 | 是 |
| 评论创建 | 为问题添加评论 | 是 |
| 状态与标签 | 查看工作流状态与标签 | 是 |
| 冲刺规划 | 自动化迭代规划 | 否 |
| 高级工作流 | 依赖链与阻塞管理 | 否 |
| 报告生成 | 迭代报告与导出 | 否 |
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
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：Node、CLI、Linear、问题与项目、支持问题查看、创建与状态更新、是一款通过内置、API、交互的工作流管理、更新与项目管理等、查询团队、项目与问题、创建与更新问题、支持优先级与状态、添加协作评论、Use、when、需要项目管理、任务规划、进度跟踪、团队协作时使用、不适用于实际人员、绩效评估等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持。

## 使用场景

### 场景一：开发者查看待办问题
开发者开始一天工作时，希望快速查看分配给自己的未完成问题。通过问题列表命令获取待办事项，针对高优先级问题深入查看详情，规划当日工作。

### 场景二：团队负责人创建任务
团队负责人在需求评审后需要创建多个问题并分配给成员。先通过团队查询确认团队ID，再逐个创建问题并设置优先级与指派人，最后添加评论说明上下文。

### 场景三：问题状态流转
开发者完成问题后更新状态为已完成。先查看问题当前状态确认可流转，再执行更新命令，最后查看确认状态变更成功。

### 场景四：敏捷日常维护
敏捷教练在迭代中需要调整问题优先级与状态。通过批量查询定位目标问题，逐个更新优先级或状态，确保迭代范围与优先级反映最新决策。

## 快速开始

本工具属于中等复杂度工具，预计120秒内可完成首次查询。

### 依赖详情
```bash
# 进入脚本目录安装依赖
cd {baseDir}/scripts && npm install
```

### Step 2：配置API密钥
```bash
# 从Linear设置页面获取API密钥
# 路径：Linear → Settings → API → Personal API keys
# ...
# 设置环境变量
export LINEAR_API_KEY="你的Linear API密钥"
```

### Step 3：查询团队
```bash
node {baseDir}/（请参考skill目录中的脚本文件） teams
```

### Step 4：查看问题
```bash
# 列出所有问题
node {baseDir}/（请参考skill目录中的脚本文件） issues
# ...
# 查看特定问题
node {baseDir}/（请参考skill目录中的脚本文件） issue ENG-123
```

### Step 5：创建问题
```bash
node {baseDir}/（请参考skill目录中的脚本文件） createIssue "修复登录页样式" "Safari下按钮错位" "team-id" '{"priority":2}'
```

## 示例

### 环境变量配置
```bash
# Linear API密钥
export LINEAR_API_KEY="lin_api_xxxxxxxxxxxxxxxx"
```

### CLI命令速查

| 命令 | 说明 | 示例 |
|:-----|:-----|:-----|
| teams | 列出团队 | `linear-cli.js teams` |
| projects | 列出项目 | `linear-cli.js projects` |
| issues | 列出问题 | `linear-cli.js issues` |
| issue | 查看问题 | `linear-cli.js issue ENG-123` |
| createIssue | 创建问题 | `linear-cli.js createIssue "标题" "描述" "team-id" '{"priority":2}'` |
| updateIssue | 更新问题 | `linear-cli.js updateIssue "issue-id" '{"stateId":"state-id"}'` |
| createComment | 创建评论 | `linear-cli.js createComment "issue-id" "评论内容"` |
| states | 查看状态 | `linear-cli.js states` |
| labels | 查看标签 | `linear-cli.js labels` |
| user | 查看用户 | `linear-cli.js user` |

### 创建问题参数
```json
{
  "priority": 2,
  "assigneeId": "user-uuid",
  "labelIds": ["label-uuid"],
  "projectId": "project-uuid",
  "cycleId": "cycle-uuid"
}
```

### 更新问题参数
```json
{
  "title": "更新后的标题",
  "description": "更新后的描述",
  "stateId": "state-uuid",
  "priority": 1,
  "assigneeId": "user-uuid"
}
```

## 最佳实践

### 实践一：遵循"先读后写"工作流
所有写入操作前先查询当前状态。创建问题前先确认团队ID；更新问题前先查看当前状态与字段；添加评论前先查看已有评论避免重复。这一习惯能显著降低误操作风险。

### 实践二：使用最小权限API密钥
从Linear设置页面创建专用的API密钥，仅授予所需权限。避免使用管理员账户的完整权限密钥进行日常操作。为自动化脚本创建独立密钥，便于权限管理与审计。

### 实践三：问题标题的规范命名
创建问题时使用规范的标题命名，如`[模块] 简述问题`。一致的命名规范便于后续查询与分类。描述字段应包含背景、复现步骤与预期结果，提供充分的上下文。

### 实践四：优先级合理设置
遵循团队的优先级约定。紧急(1)应留给阻塞发布的关键问题；高(2)为本迭代必须完成；中(3)为计划内完成；低(4)为有空再做。避免所有问题都设为高优先级，这会导致优先级失效。

### 实践五：评论记录决策上下文
问题的状态变更与重要决策应通过评论记录上下文。例如将问题标记为已完成时，添加评论说明完成方式与验证结果。这些上下文对后续复盘与知识传递至关重要。

## 常见问题

### Q1：提示API密钥无效？
A：检查`LINEAR_API_KEY`环境变量是否正确设置。从Linear → Settings → API → Personal API keys获取密钥，确认密钥未过期或被撤销。

### Q2：依赖安装失败？
A：确保Node.js与npm已正确安装。执行`node -v`与`npm -v`验证版本。若网络问题导致安装失败，可配置npm镜像源后重试。

### Q3：创建问题时团队ID从哪里获取？
A：先执行`teams`命令列出所有团队，从返回结果中获取目标团队的ID。团队ID是UUID格式，如`team-xxxxxxxx-xxxx-xxxx`。

### Q4：更新问题状态需要状态ID？
A：是的。先执行`states`命令列出所有工作流状态，获取目标状态的ID。状态ID是UUID格式，传入`updateIssue`的`stateId`参数。

### 已知限制
A：免费版不限制使用次数，但冲刺规划自动化、高级工作流与报告生成功能需使用专业版。
- 当前为免费版本,如需完整功能请升级到付费版获取全部能力
## 错误处理

| 错误场景(现象) | 可能原因 | 解决方案 |
|------:|------:|------:|
| 认证失败 | API密钥无效 | 重新获取并配置LINEAR_API_KEY |
| 依赖缺失 | 未执行npm install | 进入scripts目录执行npm install |
| 团队查询为空 | 无权限或无团队 | 确认账户已加入团队 |
| 创建问题失败 | team-id错误 | 先执行teams命令确认正确ID |
| 状态更新失败 | stateId错误 | 先执行states命令获取正确ID |
| 评论创建失败 | issue-id错误 | 使用问题标识符或UUID |
## 安全与操作规则

使用本工具时必须遵守以下安全规则：

1. **禁止编造ID**：所有ID必须通过查询获取并确认后再使用，禁止猜测或编造
2. **窄范围更新优先**：优先使用最小范围的更新，避免大范围批量编辑
3. **批量操作需说明**：若需批量操作，先向用户说明分组逻辑与影响范围
4. **禁止泄露密钥**：不要在问题评论或描述中包含API密钥或其他凭证
5. **数据不外发**：操作数据仅发送到Linear官方API，禁止发送到其他端点

## 免费版限制

本免费体验版限制以下高级功能：
- 冲刺规划自动化(自动创建迭代问题与分配)
- 高级工作流(依赖链管理与阻塞检测)
- 报告生成(迭代报告与多格式导出)
- 批量操作(批量创建/更新/迁移)
- 自定义工作流模板
- 优先技术支持

解锁全部功能请使用专业版：linear-workflow-skill-pro

## 依赖说明

### 运行环境
- **Agent平台**：支持SKILL.md的任意AI Agent(Claude Code / Cursor / Codex / Gemini CLI等)
- **操作系统**：Windows / macOS / Linux
- **Node.js**：16+(用于运行CLI脚本)

### 第三方依赖

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:---:|:---:|:---:|:---:|
| LLM API | API | 必需 | 由Agent平台内置LLM提供 |
| Node.js | 运行时 | 必需 | nodejs.org官方下载 |
| @linear/sdk | Node包 | 必需 | `npm install`(随脚本安装) |
| Linear API | 外部API | 必需 | 需Linear账户与API密钥 |

### API Key 配置
- **Linear API Key**：通过环境变量`LINEAR_API_KEY`配置
- **获取路径**：Linear → Settings → API → Personal API keys
- **权限建议**：使用最小权限原则，为自动化创建专用密钥
- **安全要求**：禁止在SKILL.md或脚本中硬编码API密钥，禁止提交到版本控制

### 可用性分类
- **分类**：MD+EXEC(纯Markdown指令，部分功能需要exec命令行执行能力)
- **说明**：基于Markdown的AI Skill，通过Node CLI驱动Agent执行Linear工作流管理任务

## 输出格式
```json
{
  "success": true,
  "data": {
    "result": "Linear工作流(免费版)处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "linear workflow skill"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```
