# Orchestrator Guide

本指南面向负责调度 OpenNexum TS 的 AI 编排者、脚本或服务。目标是把 `nexum` CLI 生成的 payload 安全地转换为 ACP session，并在整个执行过程中维护可追踪状态。

## Role Split

OpenNexum TS 和 orchestrator 的职责边界应当明确：

- `nexum` CLI: 生成 prompt、管理任务状态、处理评估结果、发送通知
- orchestrator: 调用 `sessions_spawn`、保存 session 输出、执行 heartbeat、在适当时机调用 `track` / `eval` / `complete`

这样做的原因很简单：任务语义属于仓库，运行时控制属于编排层。

## From `nexum spawn` to `sessions_spawn`

`nexum spawn <taskId>` 和 `nexum eval <taskId>` 都会输出 JSON payload。编排者应读取其中的关键字段并映射到 `sessions_spawn` 参数。

常见映射关系如下：

| `sessions_spawn` param | Source | Meaning |
| --- | --- | --- |
| `runtime` | fixed value | Usually `acp` |
| `agentId` | `payload.agentId` | Contract-selected generator or evaluator |
| `task` | `payload.promptContent` or task file wrapper | The actual prompt/instruction payload |
| `cwd` | `payload.cwd` | Working directory for the agent |
| `streamTo` | orchestrator-defined path or sink | Where streaming logs should be written |

一个推荐的概念请求如下：

```json
{
  "runtime": "acp",
  "agentId": "codex",
  "task": "contents of payload.promptContent",
  "cwd": "/Users/tongyaojin/code/nexum-ts",
  "streamTo": "/tmp/nexum/NX2-005-gen.jsonl"
}
```

如果你的环境不是直接把 prompt 文本放进 `task` 字段，而是传 `task-file`、URI 或附件句柄，也可以做适配。关键点不是字段名表面一致，而是要保留这五个语义：运行时、目标 agent、任务内容、工作目录、日志流目标。

## Recommended Spawn Sequence

1. Run `nexum spawn <taskId>` or `nexum eval <taskId>`.
2. Parse the JSON payload.
3. Call `sessions_spawn` with `runtime`, `agentId`, `task`, `cwd`, and `streamTo`.
4. Capture `sessionKey`.
5. Capture `streamLogPath` if the ACP runtime returns one.
6. Persist both by calling:

```bash
nexum track <taskId> <sessionKey> --stream-log <streamLogPath>
```

`track` 会写回 `nexum/active-tasks.json`，把 `acp_session_key` 和 `acp_stream_log` 记录下来。随后 `nexum status` 就能展示 session key 尾部和最近的流式文本片段。

## Heartbeat / Polling Logic

当前仓库里已有一套明确的 heartbeat 逻辑，来源于 `packages/spawn/src/status.ts`：

- 默认超时: `5 * 60 * 1000` ms，即 5 分钟
- 默认轮询间隔: `1000` ms，即 1 秒
- 状态来源: `openclaw sessions list --json`
- session 匹配键: `key`、`sessionKey`、`childSessionKey`

归一化后的状态只有四种：

- `running`
- `done`
- `failed`
- `unknown`

状态归一化规则摘要：

- 若原始状态是 `running`、`done`、`failed`，直接使用
- 若原始状态是 `completed`、`complete`、`succeeded`，归一化为 `done`
- 若原始状态是 `error`、`aborted`，归一化为 `failed`
- 若记录中存在 `endedAt` 或 `completedAt`，则视为结束；若同时带有错误字段则记为 `failed`
- 若不存在匹配 session，则返回 `unknown`

推荐心跳伪流程：

```text
while before deadline:
  query sessions list
  find record by sessionKey
  normalize status
  if done:
    continue workflow
  if failed:
    mark failure / escalate
  if unknown:
    decide whether to retry lookup or inspect stream log
  sleep 1s
timeout => escalate or mark infrastructure failure
```

## Stream Log Handling

如果 `sessions_spawn` 支持把流式输出写入 JSONL，编排者应始终启用。当前 `nexum status` 的展示逻辑会：

- 读取 `acp_stream_log`
- 解析 JSONL
- 选取含有 `text` 字段的最近两条非空事件
- 每条截断到 80 个字符
- 组合为单行活动摘要

这意味着 `streamTo` 最好指向一个稳定可读的文件路径，而不是仅发送到标准输出。

## Generator and Evaluator Loop

推荐把 generator 和 evaluator 看作同一套编排模板的两次实例化：

1. `nexum spawn <taskId>`
2. spawn generator session
3. `nexum track ...`
4. heartbeat until generator finishes
5. `nexum eval <taskId>`
6. spawn evaluator session
7. `nexum track ...` for evaluator if you maintain a separate stream
8. heartbeat until evaluator finishes
9. `nexum complete <taskId> <verdict>`

如果 `complete` 返回：

- `action: "done"`: task closed, optional downstream tasks unlocked
- `action: "retry"`: use `retryPayload` to spawn the next generator iteration
- `action: "failed"`: no more retries, task stops
- `action: "escalated"`: human intervention required

## Practical Guidance

- Always persist `sessionKey` immediately after spawn succeeds.
- Always store a stream log path if the runtime can provide one.
- Treat `unknown` as an infrastructure signal, not a business verdict.
- Keep `cwd` equal to the project root returned by the payload unless you have a strong reason not to.
- Prefer idempotent orchestration steps so you can resume after partial failure.

## Minimal Example

```text
payload = nexum spawn NX2-005
session = sessions_spawn(
  runtime="acp",
  agentId=payload.agentId,
  task=payload.promptContent,
  cwd=payload.cwd,
  streamTo="/tmp/nexum/NX2-005-gen.jsonl"
)
nexum track NX2-005 session.sessionKey --stream-log /tmp/nexum/NX2-005-gen.jsonl
heartbeat(session.sessionKey)
payload2 = nexum eval NX2-005
...
nexum complete NX2-005 pass
```

把这套顺序稳定下来后，OpenNexum TS 就能作为一个清晰的 contract engine，而 ACP runtime 则作为纯执行层被复用。这样最容易扩展，也最容易排错。
