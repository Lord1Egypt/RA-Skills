# OpenNexum TS / OpenNexum TS 使用文档

OpenNexum TS 是一个基于 TypeScript 和 Node.js 的 contract-driven 多 agent 编排工具。它面向需要把任务拆成明确 Contract、交给不同编码 agent 执行、再由 evaluator 回收结果的工作流。项目通过 `nexum` CLI 管理任务状态，通过 OpenClaw ACP 会话承载实际执行，并通过 Telegram 可选地推送派发与完成通知。对于需要可追踪、可重试、可审计的 AI coding orchestration，这个仓库提供了相对简洁但结构清晰的基础设施。

OpenNexum TS is a contract-driven orchestration toolkit for AI coding agents. It is built as a pnpm monorepo with TypeScript packages for core task management, prompt rendering, session spawning, notification delivery, and the CLI surface. The intended workflow is simple: define a task contract, generate a spawn payload, hand that payload to an ACP-capable orchestrator, track the returned session, evaluate the result, and finally mark the task as complete, failed, or escalated. This makes the system suitable for multi-agent coding pipelines where reproducibility matters more than ad hoc prompting.

## 项目介绍 / Project Overview

仓库的核心思想是“先定义 Contract，再运行 agent”。Contract 决定任务边界、交付物、评估标准、依赖关系，以及 generator / evaluator 的分工。CLI 侧的 `nexum spawn` 和 `nexum eval` 只负责生成 prompt 与 spawn payload，不直接替你调度 ACP；真正的编排者可以是另一个 agent、脚本、服务端调度器，或者任何能够调用 `sessions_spawn` 的外部系统。这样设计的好处是职责边界清楚：Nexum 负责任务语义和状态文件，OpenClaw 负责执行会话。

The repository is organized as a small monorepo:

- `packages/core`: contract parsing, task status, config loading, git helpers
- `packages/prompts`: generator, evaluator, and retry prompt rendering
- `packages/spawn`: OpenClaw session spawn/status helpers
- `packages/notify`: Telegram notification utilities
- `packages/cli`: the `nexum` command surface

运行时状态主要保存在 `nexum/active-tasks.json`。任务进入 `running`、`evaluating`、`done`、`failed` 等状态时，CLI 会原子更新这个文件。`nexum status` 还会在有 `acp_stream_log` 时读取最近两条文本事件，用于展示 session 的最新活动片段。

## 安装 / Installation

前置要求 / Requirements:

- Node.js `>=20`
- `pnpm`
- `openclaw`

安装与构建:

```bash
pnpm install
pnpm build
```

如果你希望通过 `nexum` 直接在本地调用 OpenClaw CLI，请确保 `openclaw` 已在 `PATH` 中可用。虽然当前 README 重点描述 orchestrator 驱动的 `sessions_spawn` 流程，但仓库内部的 `@nexum/spawn` 也提供了与 OpenClaw CLI 交互的能力，适合后续自动化扩展。

If you want to use Telegram notifications, export the following variables before running the workflow:

```bash
export TELEGRAM_BOT_TOKEN=your_bot_token
export TELEGRAM_CHAT_ID=your_chat_id
```

这两个变量都是可选的。未设置时，任务流程仍可正常运行，只是不会发送派发通知与完成通知。

## 初始化 / Initialization

执行初始化命令:

```bash
nexum init
```

该命令会在项目中准备基础目录与文件，包括：

- `nexum/active-tasks.json`
- `nexum/config.json`
- `docs/nexum/contracts/.gitkeep`
- `nexum/runtime/eval/.gitkeep`

`nexum/config.json` 默认包含 `codex` 和 `claude` 两个 agent 配置示例。你可以按需扩展 `agents` 字段，把 contract 中的 `generator` 或 `evaluator` 映射到具体 CLI。

## 工作流程 / Workflow

典型工作流程如下：

```text
nexum init
  -> create Contract YAML
  -> nexum spawn <taskId>
  -> orchestrator calls sessions_spawn
  -> nexum track <taskId> <sessionKey> --stream-log <path>
  -> heartbeat polls session status
  -> nexum eval <taskId>
  -> orchestrator calls sessions_spawn for evaluator
  -> nexum complete <taskId> <pass|fail|escalated>
```

中文说明：

1. 编写 Contract YAML，放入 `docs/nexum/contracts/`。
2. 通过 `nexum spawn <taskId>` 生成 generator 的 prompt 与 spawn payload。
3. 外部 orchestrator 将 payload 转换为 `sessions_spawn` 请求，并获取 `sessionKey`。
4. 调用 `nexum track` 记录 `sessionKey` 与可选 `streamLogPath`。
5. 编排者执行 heartbeat，周期性检查该 session 是否完成。
6. 完成后调用 `nexum eval <taskId>`，生成 evaluator payload 并再次调度。
7. evaluator 写出评估结果文件后，调用 `nexum complete <taskId> <verdict>`。
8. 若 verdict 为 `fail` 且未超过 `max_iterations`，CLI 会返回 retry payload；否则任务进入 `done`、`failed` 或 `escalated`。

English summary:

1. Author a Contract YAML file under `docs/nexum/contracts/`.
2. Run `nexum spawn <taskId>` to prepare the generator prompt and spawn payload.
3. Let your orchestrator call `sessions_spawn` and capture the returned session key.
4. Persist that key with `nexum track`.
5. Poll session state until completion.
6. Run `nexum eval <taskId>` to prepare the evaluator prompt.
7. Spawn the evaluator session and wait for the evaluation artifact.
8. Finalize with `nexum complete`, which may unlock downstream tasks or return a retry payload.

## 命令参考 / Command Reference

### `nexum init`

初始化项目结构。若目标文件已存在，则不会覆盖。

Initialize the standard project structure and seed default config/state files.

```bash
nexum init
nexum init --project /path/to/project
```

### `nexum spawn <taskId>`

读取任务与 Contract，渲染 generator prompt，写入 `nexum/runtime/prompts/`，并输出 JSON payload。当前 payload 包含：

- `taskId`
- `taskName`
- `agentId`
- `agentCli`
- `promptFile`
- `promptContent`
- `label`
- `cwd`

```bash
nexum spawn NX2-005
```

### `nexum track <taskId> <sessionKey>`

在 session 创建成功后记录会话标识。若编排者有日志流文件，也应同时传入 `--stream-log`，以便 `nexum status` 展示活动摘要。

```bash
nexum track NX2-005 sess_123456 --stream-log /tmp/nx2-005.jsonl
```

### `nexum eval <taskId>`

为 evaluator 生成 prompt 与 spawn payload，并把任务状态切到 `evaluating`。

```bash
nexum eval NX2-005
```

### `nexum complete <taskId> <verdict>`

处理 evaluator 结果。支持的 verdict 为 `pass`、`fail`、`escalated`。

- `pass`: 标记任务完成，并尝试解锁依赖它的下游任务
- `fail`: 若当前 iteration 小于 `max_iterations`，返回 retry payload
- `escalated`: 标记失败并要求人工介入

```bash
nexum complete NX2-005 pass
nexum complete NX2-005 fail
nexum complete NX2-005 escalated
```

### `nexum status`

展示任务状态总览。若记录了 `acp_stream_log`，还会展示最近的文本活动片段。`--json` 可用于机器读取。

```bash
nexum status
nexum status --json
```

## 环境变量 / Environment Variables

支持的环境变量如下：

| Variable | Required | Description |
| --- | --- | --- |
| `TELEGRAM_BOT_TOKEN` | No | Telegram bot token for dispatch/failure/completion notifications |
| `TELEGRAM_CHAT_ID` | No | Telegram chat ID receiving the messages |

通知由 `packages/notify` 提供；如果任一变量缺失，CLI 会跳过消息发送，不影响主流程。

## Contract YAML 示例 / Contract YAML Example

下面是一个与当前实现兼容的 Contract 示例。注意：`created_at` 在实际解析和校验时是必填字段，尽管很多高层说明只强调核心业务字段。

```yaml
id: NX2-005
name: "Document OpenNexum skill and orchestration flow"
type: coding
created_at: "2026-03-29T09:00:00Z"

scope:
  files:
    - SKILL.md
    - README.md
    - references/contract-schema.md
    - references/orchestrator-guide.md
  boundaries:
    - packages/
    - nexum/
  conflicts_with: []

deliverables:
  - "Skill description for ClawHub-compatible discovery"
  - "Bilingual README with workflow and command reference"
  - "Contract schema reference aligned with @nexum/core"
  - "Orchestrator guide for sessions_spawn and heartbeat"

eval_strategy:
  type: review
  criteria:
    - id: C1
      desc: "Skill frontmatter and quick start are complete"
      method: "review"
      threshold: pass
    - id: C2
      desc: "README covers install, env, workflow, commands, and examples"
      method: "review"
      threshold: pass

generator: codex
evaluator: claude
max_iterations: 3
depends_on:
  - NX2-003
  - NX2-004
```

## 编排建议 / Orchestration Notes

推荐把 `nexum spawn` 与 `nexum eval` 当作“生成任务描述”的步骤，而不是把 CLI 直接绑死到某个单一执行器。这样你可以根据实际环境选择本地 agent、远程 ACP runtime、队列系统，或自定义的 `sessions_spawn` wrapper。核心原则是：Nexum 输出结构化 payload，orchestrator 负责启动、观察和回填 session 信息。

Treat the CLI as the source of truth for task semantics, not as the sole execution engine. In practice, the most robust setup is a thin orchestrator that:

1. calls `nexum spawn`
2. translates the payload into a `sessions_spawn` request
3. records `sessionKey` and `streamLogPath` with `nexum track`
4. polls until the session ends
5. repeats the same pattern for evaluation
6. finalizes with `nexum complete`

这种分层方式让 Contract、状态管理、通知、重试和依赖解锁逻辑都保持在仓库内，而 ACP runtime 的细节则留给编排层处理。
