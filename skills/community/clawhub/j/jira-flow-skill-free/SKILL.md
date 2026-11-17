---
slug: jira-flow-skill-free
name: jira-flow-skill-free
version: 1.0.0
displayName: Jira Flow 免费版
summary: 通过Jira Cloud REST API管理任务、状态流转与工时记录，适合个人开发者日常追踪。
license: Proprietary
edition: free
description: Jira Flow Skill 是面向个人开发者与小型团队的 Jira 任务管理辅助工具，通过命令行脚本驱动 Jira Cloud REST
  API 完成日常事务流转。核心能力：任务检索与详情查看、状态流转与分配、工时记录与统计、评论与创建任务，覆盖一名开发者日常所需的 Jira 操作。Use when
  需要项目管理、任务规划、进度跟踪、团队协作时使用。不适用于实际人员绩效评估。
tags:
- 集成工具
- 任务管理
- 效率提升
tools:
- - read
- exec
homepage: https://skillhub.cn
pricing_tier: L3
pricing_model: per_use
suggested_price: 29.9
tools: ["read", "exec", "glob", "grep"]
tags: "工具,效率,自动化"
---
# Jira Flow Skill（免费版）

面向个人开发者与小型团队的 Jira 任务管理工具，通过命令行脚本完成日常任务流转、工时记录与检索查询。

## 概述

Jira Flow Skill 将 Jira Cloud REST API 封装为简洁的命令行调用，让开发者在终端即可完成"查任务、改状态、记工时、看汇总"的完整闭环。免费版覆盖个人开发者 90% 的日常 Jira 操作，无需切换浏览器即可保持工作流连续。

### 核心价值

- **命令行即工作流**：单条命令完成一个完整操作，无需多步点击
- **状态流转校验**：自动拉取服务端允许的流转列表，杜绝无效状态变更
- **工时 JSON 输出**：工时统计结果直接输出 JSON，可被其他脚本消费
- **零侵入集成**：基于环境变量配置，不修改 Jira 项目配置

## 核心能力

| 能力域 | 命令族 | 说明 |
|---|---|---|
| 任务检索 | `search` / `my` | 模糊搜索任务摘要或键值，列出分配给自己的任务 |
| 任务详情 | `issue` / `link` | 查看任务详情，生成浏览器跳转链接 |
| 状态管理 | `status` / `transitions` | 列出可用流转、应用状态变更（带校验） |
| 任务分配 | `assign` / `assign-me` | 按用户搜索分配任务，或一键指派给自己 |
| 评论与创建 | `comment` / `create` | 添加评论、在指定项目内创建任务 |
| 工时记录 | `log` | 按小时数与日期记录工时 |
| 工时统计 | `hours` / `hours-day` / `hours-issue` | 按时间区间、按日、按任务汇总工时 |

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
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：Jira、Cloud、REST、API、管理任务、状态流转与工时记、适合个人开发者日、常追踪、Flow、Skill、是面向个人开发者、与小型团队的、任务管理辅助工具、通过命令行脚本驱、完成日常事务流转、核心能力、任务检索与详情查、状态流转与分配、工时记录与统计、评论与创建任务、覆盖一名开发者日、常所需的、Use、when、需要项目管理、任务规划、进度跟踪、团队协作时使用、不适用于实际人员、绩效评估等。

## 使用场景

### 场景一：每日站会前快速查看自己未完成的任务

开发者每天站会前需要回顾自己当前的待办。执行 `my` 命令即可列出所有分配给自己且未关闭的任务，包括键值、摘要与状态，10 秒内完成站会准备。

### 场景二：修复缺陷后记录工时并更新状态

完成一个缺陷修复后，需要同时记录工时与更新状态。两条命令串联即可：
1. `log BUG-456 2.5` 记录 2.5 小时工时（默认今天）
2. `status BUG-456 "Done"` 更新状态为完成（自动校验流转合法性）

### 场景三：周报工时汇总

每周五需要汇总本周工时投入分布。执行 `hours 2025-01-06 2025-01-12` 即可获得本周按任务分组的工时 JSON，可直接喂给周报生成脚本。

### 场景四：模糊检索历史任务

只记得任务摘要里的关键词，想快速定位任务键值。执行 `search "支付超时"` 即可模糊匹配包含该关键词的任务。

## 快速开始

### 前置准备（约 60 秒）

1. 访问 Atlassian API Token 管理页：`https://id.atlassian.com/manage-profile/security/api-tokens`
2. 点击"Create API Token"生成令牌
3. 配置环境变量：

```bash
export JIRA_EMAIL="you@example.com"
export JIRA_API_TOKEN="你的API令牌"
export JIRA_URL="https://your-domain.atlassian.net"
# 可选：限定项目范围（逗号分隔），留空则搜索全部项目
export JIRA_BOARD="ABC"
```

### 依赖详情

执行以下命令，能正常返回任务列表即代表配置成功：

```bash
bash {baseDir}/（请参考skill目录中的脚本文件） my 5
```

### 运行环境要求

- 命令行工具：`curl`、`jq`、`bc`、`python3`
- 操作系统：Windows（需 WSL 或 Git Bash）/ macOS / Linux
- 网络：可访问 `atlassian.net` 域名

## 示例

### 环境变量配置表

| 变量名 | 必填 | 默认值 | 说明 |
|:-----|:-----|:-----|:-----|
| `JIRA_EMAIL` | 是 | 无 | 登录 Jira 的邮箱 |
| `JIRA_API_TOKEN` | 是 | 无 | Atlassian API 令牌 |
| `JIRA_URL` | 是 | 无 | Jira 实例地址（含 https://） |
| `JIRA_BOARD` | 否 | 空 | 项目键值过滤，多个用逗号分隔 |

### 常用命令速查

```bash
# 检索任务
bash {baseDir}/（请参考skill目录中的脚本文件） search "登录超时" 10
# ...
# 查看任务详情
bash {baseDir}/（请参考skill目录中的脚本文件） issue ABC-123
# ...
# 更新状态（自动校验流转）
bash {baseDir}/（请参考skill目录中的脚本文件） status ABC-123 "In Progress"
# ...
# 分配给自己
bash {baseDir}/（请参考skill目录中的脚本文件） assign-me ABC-123
# ...
# 添加评论
bash {baseDir}/（请参考skill目录中的脚本文件） comment ABC-123 "已修复并部署到预发"
# ...
# 创建任务
bash {baseDir}/（请参考skill目录中的脚本文件） create "修复登录超时" "用户登录5分钟后被登出"
# ...
# 记录工时
bash {baseDir}/（请参考skill目录中的脚本文件） log ABC-123 2.5 2025-01-18
# ...
# 工时统计（按时间区间）
bash {baseDir}/（请参考skill目录中的脚本文件） hours 2025-01-01 2025-01-07
```

## 最佳实践

### 1. 使用 JIRA_BOARD 限定项目范围

不设置 `JIRA_BOARD` 时，检索会扫描所有可见项目，结果可能包含大量噪音。建议根据当前工作重点设置项目范围，例如 `JIRA_BOARD="ABC,XYZ"`。

### 2. 状态变更前先查 transitions

不同工作流下允许的流转路径不同。在批量更新状态前，先用 `transitions ABC-123` 确认可用的目标状态，避免脚本因校验失败中断。

### 3. 工时记录使用 ISO 日期

`log` 命令的日期参数推荐使用 `YYYY-MM-DD` 格式（ISO 8601），避免与本地日期格式冲突。不传日期时默认使用当天 UTC。

### 4. hours 命令输出 JSON 便于二次加工

`hours` 系列命令输出 JSON 格式，可直接通过管道传递给 `jq` 或其他脚本进一步处理，例如生成 Markdown 周报。

### 5. 大型项目工时查询需耐心等待

Worklog 命令使用 Jira 的 worklog/updated + worklog/list 组合接口，在大型项目上可能需要数秒。建议在非高峰时段执行批量工时统计。

## 常见问题

### Q1：执行命令报 401 未授权怎么办？

检查三项：`JIRA_EMAIL` 是否与登录邮箱一致、`JIRA_API_TOKEN` 是否完整复制（不含空格）、`JIRA_URL` 是否包含 `https://` 前缀。

### Q2：状态更新失败提示"无可用流转"？

说明当前状态不允许直接流转到目标状态。先用 `transitions <ISSUE_KEY>` 查看允许的目标状态列表，再选择合法的目标。

### Q3：search 搜不到我确定存在的任务？

检查 `JIRA_BOARD` 是否限定了错误的项目范围。留空时会搜索全部可见项目；如果设置过窄，会过滤掉其他项目的任务。

### Q4：hours-day 与 hours 的区别？

`hours` 只统计 `JIRA_EMAIL` 对应用户的工时；`hours-day` 返回当天所有用户的工时，并按用户与任务分组汇总，适合团队视角查看。

### Q5：在 Windows 上无法运行脚本？

脚本依赖 bash 环境，Windows 原生 cmd 不支持。请使用 WSL、Git Bash 或 Windows Terminal 中的 bash 子系统。

## 依赖说明

### 运行环境

- **Agent 平台**：支持 SKILL.md 的任意 AI Agent（Claude Code / Cursor / Codex / Gemini CLI 等）
- **操作系统**：Windows（需 WSL 或 Git Bash）/ macOS / Linux
- **Shell**：bash 4.0+

### 第三方依赖

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|---:|---:|---:|---:|
| curl | 命令行工具 | 必需 | 系统自带或通过包管理器安装 |
| jq | JSON 处理工具 | 必需 | `apt install jq` / `brew install jq` |
| bc | 数值计算工具 | 必需 | `apt install bc` / `brew install bc` |
| python3 | 运行时 | 必需 | `apt install python3` / 官网下载 |
| LLM API | API | 必需 | 由 Agent 内置 LLM 提供 |

### API Key 配置

- **JIRA_EMAIL**：通过环境变量配置，存储于 Shell 配置文件（如 `~/.bashrc`）
- **JIRA_API_TOKEN**：通过环境变量配置，禁止明文写入脚本或提交到版本库
- **JIRA_URL**：通过环境变量配置
- **JIRA_BOARD**：可选，通过环境变量配置

### 可用性分类

- **分类**：MD+EXEC（纯 Markdown 指令，功能需要 exec 命令行执行能力）
- **说明**：基于 Markdown 的 AI Skill，通过自然语言指令驱动 Agent 调用脚本完成任务

## 已知限制

本免费体验版限制以下高级功能：

- 批量任务操作（一次处理超过 10 条任务）
- 多项目并行工时统计与对比
- 自定义工时报表模板与导出格式
- 团队成员工时聚合视图
- Webhook 集成与自动化触发

解锁全部功能请使用专业版：`jira-flow-skill-pro`
- 当前为免费版本,如需完整功能请升级到付费版获取全部能力
## License 与版权声明

本 skill 基于原始作品 Jira Flow Skill 改进，保留原始版权声明：

- 原始作品：Jira Flow Skill
- 原始 license：MIT
- 改进作品：Jira Flow Skill（免费版）
- 改进 license：MIT

本改进作品在原始作品基础上进行了深度差异化改造，包括但不限于：

- 完全重写中文化文档与使用指南
- 新增场景化最佳实践与故障排查
- 完善依赖说明与配置示例
- 增加免费版/专业版分层策略

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|:---:|:---:|:---:|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |
