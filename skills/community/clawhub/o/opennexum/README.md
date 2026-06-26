# OpenNexum

Contract-driven multi-agent orchestration for AI coding workflows.

OpenNexum 通过 Contract YAML 描述任务边界、交付物、评审标准和依赖关系，再把这些静态语义同步到 `nexum/active-tasks.json` 作为运行时状态。执行层完全交给 OpenClaw ACP，仓库侧只负责 contract、prompt、state、notify。

## 核心特性

- **Contract-first**: Contract 是任务静态语义的单一事实来源
- **Runtime sync**: `nexum sync` 负责把 contract 注册到运行时状态，不再手工改 `active-tasks.json`
- **Cross-review**: generator 和 evaluator 分离，支持 Codex / Claude 交叉评审
- **ACP-only**: 所有执行统一走 OpenClaw ACP
- **Dispatch queue + webhook**: 实时唤醒和兜底重放同时存在
- **Replay-safe state machine**: `track` / `callback` / `complete` 对重复和乱序事件做 no-op 防护
- **Batch progress**: `nexum status` 支持当前批次与总体进度
- **OpenClaw messaging**: 所有通知统一走 `openclaw message send`

## 安装

```bash
# 前置要求：Node.js >=20, pnpm, openclaw
git clone <repo-url>
cd OpenNexum
pnpm install
pnpm build

# 全局安装 nexum CLI
pnpm add -g ./packages/cli
```

## 快速开始

```bash
# 1. 初始化项目
nexum init --project /path/to/project

# 2. 编写 Contract
# docs/nexum/contracts/TASK-001.yaml

# 3. 同步 contract -> runtime state
nexum sync TASK-001 --project /path/to/project

# 4. 生成 generator payload
nexum spawn TASK-001 --project /path/to/project

# 5. orchestrator 使用 payload.runtimeAgentId 调用 sessions_spawn
#    成功后立刻写回真实 session
nexum track TASK-001 <sessionKey> \
  --project /path/to/project \
  --role generator \
  --stream-log /tmp/TASK-001-gen.jsonl

# 6. generator 完成后回调
nexum callback TASK-001 --project /path/to/project \
  --model gpt-5.4 \
  --input-tokens 12345 \
  --output-tokens 2048

# 7. evaluator 完成后回调
nexum callback TASK-001 --project /path/to/project --role evaluator
```

## Contract YAML

```yaml
id: TASK-001
name: "implement feature X"
type: coding
created_at: "2026-03-31T00:00:00Z"
batch: batch-1

agent:
  generator: auto
  evaluator: auto

scope:
  files:
    - src/feature.ts
    - src/feature.test.ts
  boundaries: []
  conflicts_with:
    - TASK-002

description: "..."

deliverables:
  - path: src/feature.ts
    description: "..."

eval_strategy:
  type: review
  criteria:
    - id: C1
      desc: "feature works as contracted"
      method: review
      threshold: pass
      weight: 2

max_iterations: 3
depends_on: []
```

`deliverables` 支持对象数组和旧的字符串数组。`generator` / `evaluator` 既支持顶层字段，也支持 `agent.generator` / `agent.evaluator`。

## Spawn Payload

`nexum spawn` / `nexum eval` / retry payload 都会输出统一结构：

- `agentId`: 逻辑 agent ID，用于路由、通知、归属
- `agentCli`: 逻辑 agent 对应的 CLI 家族
- `runtime`: 当前固定为 `acp`
- `runtimeAgentId`: orchestrator 真正传给 `sessions_spawn` 的 backend
- `phase`: `generator` 或 `evaluator`
- `constraints`: `dependsOn` / `conflictsWith` / `scopeFiles` / `scopeBoundaries`

对 orchestrator 的要求很简单：执行永远跟 `runtimeAgentId` 走，调度约束永远跟 `constraints` 走，不要把 `agentId` 当底层 backend。

## Dispatch Flow

```text
contract -> nexum sync -> active-tasks runtime state
        -> nexum spawn -> sessions_spawn(generator) -> nexum track
        -> nexum callback(generator)
        -> dispatch-queue + POST /hooks/agent
        -> nexum eval -> sessions_spawn(evaluator) -> nexum track
        -> nexum callback(evaluator)
        -> nexum complete(pass|fail|escalated)
        -> unlock / retry / escalate
```

`watch` 会定期重放 `dispatch-queue`，同时做卡死检测。重复 webhook、重复 callback、晚到 track 都会被归一化为 no-op，而不是把任务状态倒退。

## CLI

```bash
nexum init [--project <dir>] [--yes]
nexum sync [taskId] [--project <dir>]
nexum spawn <taskId> [--project <dir>]
nexum eval <taskId> [--project <dir>]
nexum track <taskId> <sessionKey> [--role generator|evaluator]
nexum callback <taskId> [--role generator|evaluator]
nexum complete <taskId> <pass|fail|escalated>
nexum retry <taskId> --force
nexum status [--project <dir>] [--json] [--batch <name>]
nexum archive [--project <dir>]
nexum health [--project <dir>]
nexum watch [--interval <min>] [--timeout <min>]
```

## Webhook Config

`~/.openclaw/openclaw.json`:

```json
{
  "hooks": {
    "enabled": true,
    "token": "your-secret-token"
  }
}
```

`nexum/config.json`:

```json
{
  "webhook": {
    "gatewayUrl": "http://127.0.0.1:18789",
    "token": "your-secret-token",
    "agentId": "orchestrator"
  }
}
```

也可以通过环境变量 `OPENCLAW_HOOKS_TOKEN` 提供 token。

## Git 规范

- 直接 push 到 `main`
- commit message 使用英文 Conventional Commits
- `scope.files` 会进入建议的 `git add -- ...` 命令
