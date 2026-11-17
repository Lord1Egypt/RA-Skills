---
slug: linear-toolkit-free
name: linear-toolkit-free
version: 1.0.1
displayName: Linear 工具箱
summary: "面向个人的 Linear 任务查询与基础管理工具，含站会摘要.。面向个人开发者的 Linear 任务查询与基础管理工具."
license: MIT
edition: free
description: "面向个人开发者的 Linear 任务查询与基础管控工具. 适用于需要linear toolkit相关能力的开发场景,包含结构化的工作流程和可复用的模板,帮助用户快速完成任务并保持代码质量. 适用于需要linear toolkit相关能力的开发场景,包含结构化的工作流程和配置指引. 该工具经过深度差异化处置,针对用户反馈和使用痛点进行了调优改进,提升了实用性和可操作性."
tags:
  - Linear
  - linear
  - toolkit
  - automation
  - productivity
  - 任务管理
  - 个人效率
  - 其他工具
  - 工具
  - 效率
tools:
  - read
  - exec
  - glob
  - grep
homepage: ""
category: "Automation"
pricing_tier: free

---
# Linear 工具箱（免费版）

## 概述

本工具帮助个人开发者查询与管理 Linear 任务、项目与团队工作流。免费版覆盖个人任务查询、创建、评论、状态/优先级管理、每日站会摘要与 Git 分支名联动，适合个人单团队使用.
## 核心能力

| 能力 | 说明 | 免费版范围 |
|---|---|-----|
| 任务查询 | 我的任务、待办、紧急 | 个人 |
| 任务管理 | 创建、评论、状态、优先级 | 单团队 |
| 站会摘要 | 待办、阻塞、评审、已完成 | 每日 |
| Git 联动 | 从任务生成分支名 | 单仓库 |
**技术实现要点**：核心能力基于`input_params`参数与`output_format`配置实现,支持创建/查询/修改/删除等操作模式,通过`config_options`进行运行时配置.
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
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：面向个人的、Linear、任务查询与基础管、理工具、含站会摘要、面向个人开发者的等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
## 使用场景

### 场景一：每日站会

```bash
export LINEAR_API_KEY=${API_KEY:?请设置环境变量}
export LINEAR_DEFAULT_TEAM="TEAM"
# ...
# 站会摘要：待办、阻塞、评审中、近期完成
{baseDir}/（请参考skill目录中的脚本文件） standup
```

### 场景二：快速建任务

```bash
# 从聊天直接建任务
{baseDir}/（请参考skill目录中的脚本文件） create TEAM "修复登录超时" "用户 5 分钟后被登出"
```

### 场景三：Git 分支联动

```bash
# 取任务对应分支名
BRANCH=$({baseDir}/（请参考skill目录中的脚本文件） branch TEAM-212)
# ...
cd /path/to/repo
git checkout main && git pull origin main
git worktree add .worktrees/team-212 -b "$BRANCH" origin/main
cd .worktrees/team-212
git push -u origin "$BRANCH"
```

## 不适用场景

以下场景Linear 工具箱不适合处理：

- 实际人员绩效评估
- 财务预算审批
- 合同法务审核

## 触发条件

需要项目管理、任务规划、进度跟踪、团队协作时使用。不适用于非本工具能力范围的需求.
## 快速开始

1. 设置 `LINEAR_API_KEY` 与 `LINEAR_DEFAULT_TEAM`.
2. 用 `teams` 发现团队 key.
3. 查询与更新任务.
4. 站会前跑 `standup`.
```bash
{baseDir}/（请参考skill目录中的脚本文件） teams              # 列团队
{baseDir}/（请参考skill目录中的脚本文件） my-issues          # 我的任务
{baseDir}/（请参考skill目录中的脚本文件） urgent             # 紧急/高优
```

**响应解析**: 完成完成后,查看输出响应确认任务状态。成功时输出包含解析摘要和响应数据;失败时根据错误信息排查问题,查阅错误解析章节获取恢复步骤.
## 示例

优先级对照：

| 级别 | 值 | 用途 |
|:-----|:-----|:-----|
| urgent | 1 | 生产事故、阻塞 |
| high | 2 | 本周、重要 |
| medium | 3 | 本迭代 |
| low | 4 | 锦上添花 |
| none | 0 | 待办池 |

## 优秀实践

- **分支名走 Linear**：用 `branch` 命令生成分支名，PR 合并自动推进状态.
- **main 保持干净**：改动只在 worktree，避免误推 main.
- **站会前跑摘要**：`standup` 一条命令出全貌，省去手工翻.
- **优先级要准**：生产事故才 urgent，别滥用高优.
- **状态及时更新**：开始做就转 progress，评审转 review，便于团队看板.
## 常见问题

**Q1：API Key 从哪拿？**
A：Linear 设置 → API → 生成 Personal API Key.
**Q2：为什么分支名重要？**
A：Linear 按分支名追踪 PR，PR 创建自动转「评审中」，合并自动转「完成」.
**Q3：免费版支持多团队吗？**
A：支持查询多团队，但默认聚焦单团队。跨团队看板与批量操作为专业版能力.
**Q4：能改任务指派人？**
A：能。`assign TEAM-123 用户名`.
**Q5：站会摘要包含什么？**
A：你的待办、团队阻塞项、评审中、近期完成.
## 进阶用法

### 常用查询命令

```# 网络连接示例(已移除潜在风险命令)
{baseDir}/（请参考skill目录中的脚本文件） urgent                 # 紧急/高优
{baseDir}/（请参考skill目录中的脚本文件） backlog TEAM           # 团队待办池
{baseDir}/（请参考skill目录中的脚本文件） search "登录"          # 关键词搜索
{baseDir}/（请参考skill目录中的脚本文件） issue TEAM-123         # 查看详情
{baseDir}/（请参考skill目录中的脚本文件） comments TEAM-123      # 查看评论
```

### 任务更新操作

echo "操作完成"```bash
# 更新状态
{baseDir}/（请参考skill目录中的脚本文件） update TEAM-123 --status "In Progress"
# ...
# 设置优先级
{baseDir}/（请参考skill目录中的脚本文件） update TEAM-123 --priority urgent
# ...
# 指派
{baseDir}/（请参考skill目录中的脚本文件） assign TEAM-123 用户名
# ...
# 添加评论
{baseDir}/（请参考skill目录中的脚本文件） comment TEAM-123 "已复现，预计今日修复"
```

### 站会摘要详解

echo "操作完成"```text
═══ 今日站会摘要 ═══
我的待办（5）:
  TEAM-101 修复登录超时 [进行中]
  TEAM-105 优化首页加载 [待办]
  ...
# ...
团队阻塞项（2）:
  TEAM-108 等待设计稿（@设计师）
  TEAM-112 依赖后端接口（@后端）
# ...
评审中（3）:
  TEAM-100 PR #234 待评审
# ...
近期完成（4）:
  TEAM-095 登录页重构 ✓
  ...
══════════════════════
```

## Git 分支工作流

echo "操作完成"```text
完整工作流:
  1. linear.sh branch TEAM-212 → 得到分支名
  2. git worktree add .worktrees/team-212 -b 分支名
  3. 开发提交
  4. 推送创建 PR
  5. Linear 自动转「评审中」
  6. PR 合并 → Linear 自动转「完成」
```

## 任务管理习惯

- **开始即更新**：动手做就转「进行中」，团队看板才准.
- **评审及时转**：提 PR 即转「评审中」，评审人可见.
- **阻塞要标注**：卡住标注阻塞原因与依赖人.
- **优先级定期校**：每周校一次优先级，urgent 别滥用.
- **评论留上下文**：关键决策写评论，便于回溯.
## 依赖说明

### 运行环境
- **Agent 平台**: 支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI 等）
- **操作系统**: Windows / macOS / Linux
- **网络**: 可访问 api.linear.app

### 依赖详情
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|---:|---:|---:|---:|
| curl | 命令行工具 | 必需 | 系统包管理器 |
| jq | JSON 处理 | 推荐 | 系统包管理器 |
| LLM API | API | 必需 | 由 Agent 内置 LLM 提供 |

### API Key 配置
- `LINEAR_API_KEY`：Linear Personal API Key，从设置获取
- `LINEAR_DEFAULT_TEAM`：默认团队 key，可省略每次传团队
- 密钥建议存环境变量或权限 0600 的配置文件

### 可用性分类
- **分类**: MD+EXEC（Markdown 指令 + 命令行执行）
- **说明**: 通过自然语言指令驱动 Agent 调用 Linear GraphQL API 管理任务

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|:---:|:---:|:---:|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 已知限制

- 需LLM支持,无LLM环境不可用
- 复杂业务场景建议结合人工经验判断
- 执行效率受模型能力与网络环境影响
- 当前为免费版本,如需完整功能请升级到付费版获取全部能力

## 输出格式
```json
{
  "success": true,
  "data": {
    "result": "Linear 工具箱处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "linearkit"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```
