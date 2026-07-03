---
name: to-prd
description: >
  Turn the current conversation into a PRD and publish it to the project issue tracker.
  当用户说"写 PRD"、"出需求文档"、"整理需求"、"写成文档"、"to-prd"、"PRD"、
  "需求文档"、"产品需求"、"功能文档"、"spec"、"写成 spec"，或在 grilling 对齐后
  需要落地实现时触发。检测 Issue Tracker 配置，先询问用户偏好，再按配置方式发布。
  失败时回退本地 markdown。
---

# To PRD — 合成 PRD 并发布

> 原始理念来自 Matt Pocock。在 Kimi 生态中，此 skill 为 model-invoked，
> 在需求对齐后自动触发，用于将对话转化为可执行的 PRD。

## 核心原则

**PRD 是供需双方对齐后的契约。** 它不应该是新信息，而是把会话中已讨论的内容**结构化、完整化**。

## 工作方式

### 1. 探索代码库（如果还没做）

如果尚未探索当前代码库，先快速了解：
- 当前代码结构
- 相关模块的现有 seams
- 项目使用的测试框架
- 已有的 PRD / spec 文件（如果有）

使用 `Read` 读取相关文件，使用 `Bash` 了解目录结构。

### 2. 确定测试 seams

列出你打算在哪些 seams 上测试这个 feature：
- 优先使用现有 seams
- 使用最高层 seam（越少 seams 越好，理想是 1 个）
- 如果需要新 seams，在最高层提出

**与用户确认**这些 seams 是否符合预期。

### 3. 撰写 PRD

使用以下模板，用项目的领域术语（参考 `CONTEXT.md`）和已确认的决策填充：

```markdown
## Problem Statement

用户面临的问题，从用户视角描述。

## Solution

解决方案，从用户视角描述。

## User Stories

1. 作为一个 <角色>，我想要 <功能>，以便 <收益>
2. ...

（列表应尽可能详尽，覆盖 feature 的所有方面）

## Implementation Decisions

- 将构建/修改的模块
- 模块的接口变化
- 技术澄清
- 架构决策
- Schema 变化
- API 契约
- 具体交互

**不包含具体文件路径或代码片段**——这些会过时。
例外：如果原型产出的代码片段（状态机、reducer、schema、类型形状）比文字更精确，可以 inline，并标注来自原型。

## Testing Decisions

- 什么是好测试（只测外部行为，不测实现细节）
- 哪些模块将测试
- 测试的参考（代码库中类似测试）

## Out of Scope

本 PRD 不包含的内容。

## Further Notes

任何其他备注。
```

### 4. Issue Tracker 发布

#### 4.1 检测配置

检查是否存在 `docs/agents/issue-tracker.md`：
- 存在：读取配置
- 不存在：询问用户偏好

#### 4.2 询问用户偏好（如无配置）

一次一个问题：

> **Issue Tracker 是什么？**
> 这是你追踪工作的地方。skills 如 `to-prd`、`to-issues`、`triage` 需要知道往哪写 Issue。

选项：
- **GitHub MCP** — 通过 Kimi 的 GitHub MCP 插件直接操作（需要已配置 OAuth）
- **GitHub Token** — 通过 `GITHUB_TOKEN` 环境变量调用 GitHub API
- **GitHub CLI** — 通过本地 `gh` 命令行工具
- **本地 Markdown** — 保存为 `.scratch/<feature>/` 下的 markdown 文件
- **其他** — 用户描述自定义工作流

如果用户选择 GitHub（MCP/Token/CLI），再问：
- 是否将外部 PR 也纳入 triage 队列？（开源项目通常 yes，个人项目通常 no）

#### 4.3 保存配置

将用户选择写入 `docs/agents/issue-tracker.md`：

```markdown
# Issue Tracker

- **类型**: GitHub MCP / GitHub Token / GitHub CLI / Local Markdown / Other
- **仓库**: <owner>/<repo>（如果是 GitHub）
- **PR as request surface**: yes / no
- **自定义说明**: <如果是 Other>
```

#### 4.4 发布 PRD

**GitHub MCP**：
- 使用 `mcp__plugin-github_github__issue_write` 创建 Issue
- 标签：`ready-for-agent`（如果已配置 triage labels）

**GitHub Token**：
- 使用 `curl` 调用 GitHub REST API
- 需要 `GITHUB_TOKEN` 环境变量

**GitHub CLI**：
- 使用 `Bash` 执行 `gh issue create`
- 需要 `gh` 已登录

**本地 Markdown**：
- 保存到 `.scratch/<feature>/prd.md`
- 创建目录结构

#### 4.5 失败回退

如果发布失败：
1. 告知用户失败原因
2. 保存为本地 markdown 文件到当前 workspace
3. 提示用户手动同步或配置 Issue Tracker

### 5. 完成

发布成功后：
- 提供 Issue URL 或本地文件路径
- 如果后续需要 `to-issues`（拆分为独立 Issue），告知用户

## 触发场景（中文关键词）

- "写 PRD"
- "出需求文档"
- "整理需求"
- "写成文档"
- "to-prd"
- "PRD"
- "需求文档"
- "产品需求"
- "功能文档"
- "spec"
- "写成 spec"
- "对齐完了，写一下吧"（grilling 后）
- "记下来"
- "形成文档"

## 关联技能

- 前置：`grilling` / `grill-with-docs`（对齐后合成 PRD）
- 后置：`to-issues`（将 PRD 拆分为独立 Issue）
- 被 `implement` 调用（读取 PRD 实现代码）
