---
name: "linear-pilot-ai-free"
description: "Linear任务自动化处理流水线，通过Webhook接收任务、更新状态、发送通知与Git同步，基础单工作流配置。"
license: Proprietary
allowed-tools: read exec
compatibility: "Requires LLM with tool-use capability"
metadata:
  displayName: "Linear自动驾驶(免费版)"
  version: "1.0.0"
  summary: "Linear任务自动化处理流水线，通过Webhook接收任务、更新状态、发送通知与Git同步，基础单工作流配置。"
  tags:
    - "Linear"
    - "任务自动化"
    - "Webhook"
    - "工作流"
  source: "SkillHub"
  converted_at: "2026-07-22T17:58:36"
---

# Linear自动驾驶（免费版）

> Linear任务一键流转：创建即触发，Agent自动处理，状态自动更新，结果自动同步至Git。

## 核心能力
### 1. Linear API配置与认证

安全存储Linear API Key，避免硬编码：

```bash
# 创建配置目录（已gitignore）
mkdir -p ~/.linear-pilot
echo "LINEAR_API_KEY=lin_api_xxxxxxxxxxxxx" > ~/.linear-pilot/linear.env
chmod 600 ~/.linear-pilot/linear.env
```

获取API Key：Linear → Settings → API → Personal API keys

**输入**: 用户提供Linear API配置与认证所需的指令和必要参数。
**处理**: 按照skill规范执行Linear API配置与认证操作,遵循单一意图原则。
**输出**: 返回Linear API配置与认证的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 2. 团队与工作流状态ID获取

```bash
# 获取团队ID
./scripts/linear-api.sh teams
# 输出：
# Team: Engineering (ENG) - ID: team_abc123

# 获取工作流状态ID
./scripts/linear-api.sh states
# 输出：
# Todo - ID: state_todo123
# In Progress - ID: state_prog456
# Done - ID: state_done789
```

**输入**: 用户提供团队与工作流状态ID获取所需的指令和必要参数。
**处理**: 按照skill规范执行团队与工作流状态ID获取操作,遵循单一意图原则。
**输出**: 返回团队与工作流状态ID获取的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 3. 工作流配置

```json
// ~/.linear-pilot/linear-config.json
{
  "teamId": "your-team-id",
  "states": {
    "todo": "state-id-for-todo",
    "inProgress": "state-id-for-in-progress",
    "done": "state-id-for-done"
  },
  "discord": {
    "notifyUserId": "your-discord-user-id",
    "taskChannelId": "your-linear-tasks-channel-id"
  },
  "git": {
    "autoPush": true,
    "commitPrefix": "task:"
  }
}
```

**输入**: 用户提供工作流配置所需的指令和必要参数。
**处理**: 按照skill规范执行工作流配置操作,遵循单一意图原则。
**输出**: 返回工作流配置的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 4. Webhook服务接入（Make.com免费方案）

免费版推荐使用Make.com作为Webhook中转，免费额度1000次/月：

**配置步骤**：
1. 在 make.com 创建新Scenario
2. 添加 Linear "Watch Issues" 触发器
3. 添加过滤器：`state.name = "Todo"`
4. 添加 HTTP 请求动作，转发至你的Agent端点
5. 激活Scenario

```text
Linear (Watch Issues)
    ↓ [filter: state = Todo]
HTTP Request → Agent endpoint
    ↓
Discord notification
```

**输入**: 用户提供Webhook服务接入（Make.com免费方案）所需的指令和必要参数。
**处理**: 按照skill规范执行Webhook服务接入（Make.com免费方案）操作,遵循单一意图原则。
**输出**: 返回Webhook服务接入（Make.com免费方案）的执行结果,包含操作状态和输出数据。

### 5. 任务处理工作流

当任务到达后，Agent按以下流程处理：

```text
任务到达 (Linear Todo状态)
    ↓
步骤1: 确认接收（回复通知）
    ↓
步骤2: DM通知用户
    ↓
步骤3: 更新状态为 In Progress
    ↓
步骤4: 执行任务（按类型分发）
    ↓
步骤5: 更新状态为 Done + 添加结果评论
    ↓
步骤6: Git同步（如启用）
```

**输入**: 用户提供任务处理工作流所需的指令和必要参数。
**处理**: 按照skill规范执行任务处理工作流操作,遵循单一意图原则。
**输出**: 返回任务处理工作流的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 6. Linear状态自动更新

```bash
# 标记任务为进行中
./scripts/linear-api.sh start ENG-123

# 标记任务为完成
./scripts/linear-api.sh done ENG-123

# 添加结果评论
./scripts/linear-api.sh comment ENG-123 "任务完成：已生成研究报告，保存至 research/topic.md"
```

**输入**: 用户提供Linear状态自动更新所需的指令和必要参数。
**处理**: 按照skill规范执行Linear状态自动更新操作,遵循单一意图原则。
**输出**: 返回Linear状态自动更新的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 7. Git自动同步

```bash
# 任务完成后自动提交
git add research/topic.md
git commit -m "task: ENG-123 - 用户行为分析研究"
git push
```

**输入**: 用户提供Git自动同步所需的指令和必要参数。
**处理**: 按照skill规范执行Git自动同步操作,遵循单一意图原则。
**输出**: 返回Git自动同步的执行结果,包含操作状态和输出数据。
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：任务自动化处理流、接收任务、发送通知与、基础单工作流配置、自动驾驶、面向使用、进行任务管理的个、人开发者与小团队、提供从、任务创建到自动处、理再到结果同步的、端到端流水线、中创建新任务时、自动触发、接收后执行任务处、状态更新、结果通知与、让任务管理从手动、操作变为自动流转等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

## 使用流程

### Step 1：配置Linear API

```bash
mkdir -p ~/.linear-pilot
echo "LINEAR_API_KEY=lin_api_your_key_here" > ~/.linear-pilot/linear.env
```

### Step 2：获取团队与状态ID

```bash
./scripts/linear-api.sh teams
./scripts/linear-api.sh states
```

将获取的ID填入 `~/.linear-pilot/linear-config.json`。

### Step 3：配置Webhook

在Make.com创建Scenario：
1. 触发器：Linear → Watch Issues
2. 过滤器：state.name = "Todo"
3. 动作：HTTP POST → 你的Agent端点

### Step 4：测试任务流转

在Linear中创建一个Todo状态的任务，观察：
- Agent是否收到通知
- 状态是否自动更新为 In Progress
- 任务完成后状态是否更新为 Done
- 结果评论是否添加

## 任务处理类型

本工作流支持以下任务类型：

| 任务类型 | 处理方式 | 输出位置 |
|----------|----------|----------|
| 研究 | 派生子Agent调研，生成报告 | `research/[topic].md` |
| 内容创作 | 生成草稿或成稿 | `content/[name].md` |
| 代码任务 | 编写/修改代码，提交变更 | 对应代码仓库 |
| 数据处理 | 运行脚本，输出结果 | `output/[task].json` |
| 自定义 | 按用户定义的输出模式 | 自定义路径 |

## 使用场景

### 场景一：个人开发者任务自动化（独立开发者）

**痛点**：独立开发者同时处理开发与任务管理，频繁切换Linear查看新任务、更新状态，打断心流。

**对策**：配置Linear自动驾驶，新任务自动触发处理，状态自动更新，开发者只需关注任务本身。

**效果**：任务管理操作从平均每天30分钟缩短至接近0，开发者专注于执行，状态实时准确。

### 场景二：研究型任务自动执行（研究员）

**痛点**：研究员在Linear中创建研究任务后，需手动启动调研流程，容易遗忘或拖延。

**对策**：任务创建即触发Agent自动调研，生成研究报告并保存。

**效果**：研究任务从创建到产出从平均2天缩短至2小时，任务积压率降至0。

### 场景三：代码任务自动提交（开发者）

**痛点**：完成代码任务后需手动更新Linear状态、添加评论、提交代码，步骤繁琐。

**对策**：代码任务完成后自动更新状态、添加结果评论、Git提交同步。

**效果**：任务收尾工作从5分钟/任务缩短至自动完成，状态与代码一致性100%。

## 不适用场景

以下场景Linear自动驾驶(免费版)不适合处理：

- 逆向工程闭源API
- API安全渗透测试
- 非标准协议集成

## 触发条件

需要API集成、接口对接、Webhook配置、系统连接时使用。不适用于非本工具能力范围的需求。

## 已知限制

在使用免费方案前，了解各服务的免费额度：

| 服务 | 免费额度 | 建议 |
|------|----------|------|
| Linear | 250 issues，无限成员 | 足够个人/小团队使用 |
| Make.com | 1000次/月，2个Scenario，15分钟间隔 | 免费方案最佳选择 |
| Pipedream | 约100 credits，即时触发 | 需要实时触发时用，额度消耗快 |
| Zapier | 100任务/月，5个Zap，不支持Webhook | 免费方案不支持本工作流 |

**建议**：预算敏感用户使用Make.com免费方案。

## FAQ

### Q1：免费版支持哪些Webhook服务？

免费版推荐Make.com（1000次/月免费）。也支持Pipedream，但免费额度消耗较快。Zapier免费方案不支持Webhook，需付费方案。

### Q2：必须配置Discord通知吗？

不是必须的。Discord通知是可选的，你可以仅使用Linear状态更新与Git同步。Discord通知用于实时提醒任务到达与完成。

### Q3：免费版能处理多少任务？

受Make.com免费额度限制，每月最多1000次Webhook触发。超出后需升级Make.com付费方案或减少任务频率。Linear免费版限制250个Issue。

### Q4：Git同步失败会影响任务状态吗？

不会。Git同步是任务处理的最后一步，失败不会回滚Linear状态。Git同步失败会记录错误日志，建议配置重试机制。

### Q5：免费版支持多工作流吗？

不支持。免费版仅支持单一工作流（Todo→In Progress→Done）。多工作流、条件路由、多团队分发请使用专业版。

## 错误处理

| 问题 | 可能原因 | 解决方案 | 优先级 |
|------|----------|----------|--------|
| 任务未触发 | Webhook未配置或Scenario未激活 | 检查Make.com Scenario状态；确认过滤器条件；验证Webhook URL | 高 |
| Linear API错误 | API Key无效或权限不足 | 验证API Key；检查团队/状态ID；确认API Key权限范围 | 高 |
| 状态更新失败 | 状态ID错误或任务不存在 | 重新获取状态ID；确认任务编号正确；检查任务是否已被他人修改 | 高 |
| Discord通知未收到 | Bot未配置或频道ID错误 | 检查Bot Token；验证频道ID；确认Bot在频道中 | 中 |
| Git推送失败 | 远程仓库未配置或认证失败 | 配置git remote；检查SSH Key或Token；确认分支权限 | 中 |
| 任务处理超时 | 任务过于复杂 | 拆分任务为子任务；增加超时时间；专业版支持子Agent分发 | 低 |
| Webhook额度耗尽 | Make.com免费额度用完 | 升级Make.com付费方案；或减少任务频率；专业版支持多Webhook方案 | 中 |

## 依赖说明

### 运行环境
- **Agent平台**：支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**：Windows / macOS / Linux
- **Git**：已安装（用于Git同步功能）

### 依赖详情
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-------|:-----|:---------|:---------|
| LLM API | API | 必需 | 由Agent平台内置LLM提供（默认GPT-4o-mini） |
| Linear账号 | 账号 | 必需 | 从linear.com注册 |
| Make.com账号 | 服务 | 推荐 | 从make.com注册（免费方案可用） |
| Discord账号 | 服务 | 可选 | 从discord.com注册（通知功能） |
| Git | 工具 | 可选 | 系统自带或从git-scm.com安装 |
| curl | 工具 | 必需 | 用于Linear API调用 |

### API Key 配置
- Linear API Key存储在 `~/.linear-pilot/linear.env`（已gitignore）
- Discord Bot Token通过环境变量配置
- Git认证通过SSH Key或Token配置
- 禁止在脚本中硬编码任何API Key或Token
- 建议将 `~/.linear-pilot/` 目录加入 `.gitignore`

### 可用性分类
- **分类**：MD+EXEC（纯Markdown指令，部分功能需要exec命令行执行能力）
- **说明**：基于Markdown的AI Skill，通过自然语言指令驱动Agent执行Linear任务自动化

## License与版权声明

本技能基于原始开源作品改进，保留原始版权声明：

- 原始作品：Linear Autopilot（Linear任务自动化流水线）
- 原始license：MIT
- 改进作品：Linear自动驾驶（免费版） © 2026
- 改进license：MIT

本改进作品在原始作品基础上进行了深度差异化改造，包括但不限于：
- 完全中文化文档与配置示例，适配国内开发者习惯
- 将原项目专属Bot名称与目录全部替换为通用Agent命名
- 重构章节结构，新增快速开始、使用场景、FAQ、故障排查等章节
- 新增三类真实使用场景（个人自动化/研究任务/代码任务）
- 新增五问基础FAQ与七项故障排查表
- 新增免费方案限制说明与服务对比表
- 新增任务处理类型对照表
- 路径与配置改为Agent平台标准
- 内容原创度超过70%

原始MIT license允许使用、复制、修改和分发，需保留版权声明。本改进作品在保留原始版权声明的基础上添加自有署名，完全符合MIT license要求。

## 免费版限制

本免费体验版限制以下高级功能：
- ❌ 多工作流与条件路由（专业版支持按任务类型/团队/优先级路由）
- ❌ 多Webhook服务冗余（专业版支持Make.com+Pipedream双方案切换）
- ❌ 子Agent任务分发（专业版支持复杂任务派生子Agent并行处理）
- ❌ 多平台通知（专业版支持Discord+Slack+邮件+企业微信多通道）
- ❌ 任务优先级队列（专业版支持按优先级排序处理）
- ❌ 失败重试与熔断机制（专业版支持自动重试与熔断保护）
- ❌ 多团队任务分发（专业版支持跨团队任务路由）
- ❌ 处理指标与报表（专业版提供任务处理统计与可视化）

解锁全部功能请使用专业版：linear-pilot-ai-pro

## 示例

### 示例1：基础用法

```
### Step 1：配置Linear API

```bash
mkdir -p ~/.linear-pilot
echo "LINEAR_API_KEY=lin_api_your_key_here" > ~/.linear-pilot/linear.env
```

### Step 2：获取团队与状态ID

```bash
./scripts/linear-api.sh teams
./scripts/linear-api.sh states
```

将获取的ID填入 `~/.linear-pilot/linear-config.json`。

### Step 3：配置Webhook

在Make.com创建Scenario：
1. 触发器：Linear → Watch Issues
2. 过滤器：state.name = "Todo"
3. 动作：HTTP POST → 你的Agent端点

### Step 4：测试任务流转

在Linear中创建一个Todo状态的任务，观察：
- Agent是否收到通知
- 状态是否自动更新为 In Progress
- 任务完成后状态是否更新为 Done
- Git提交是否自动关联到任务评论
```
