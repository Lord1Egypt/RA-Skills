# Orchestrator Guide

本指南面向负责调度 OpenNexum 的 orchestrator、脚本或服务。

目标只有一个：把 `nexum` 产出的 payload 稳定转换成 ACP session，并在整个执行过程中维持正确、可重放的状态。

## 1. Role Split

- `nexum` CLI: contract sync、prompt 生成、状态推进、通知、评审决策
- orchestrator: 调用 `sessions_spawn`、保存流式日志、心跳轮询、在正确时机调用 `track` / `callback`

不要把这两层混起来。仓库语义归 `nexum`，运行时控制归 orchestrator。

## 2. Always Start with `sync`

在处理某个 task 前，先确保 runtime state 和 contract 对齐：

```bash
nexum sync TASK-001 --project /path/to/project
```

这一步会注册新任务、补齐依赖状态、同步 name / contract_path / depends_on。

## 3. Spawn Payload Contract

`nexum spawn <taskId>` 和 `nexum eval <taskId>` 都返回 JSON payload。关键字段如下：

| Field | Meaning |
| --- | --- |
| `agentId` | 逻辑 agent，用于路由和归属 |
| `agentCli` | 逻辑 agent 所属 CLI 家族 |
| `runtime` | 当前固定为 `acp` |
| `runtimeAgentId` | 真正传给 `sessions_spawn` 的 backend |
| `phase` | `generator` 或 `evaluator` |
| `constraints.dependsOn` | 必须先完成的上游任务 |
| `constraints.conflictsWith` | 当前不应并发的任务 |
| `constraints.scopeFiles` | 预计修改的文件 |
| `promptContent` | 实际 prompt |
| `cwd` | 工作目录 |

执行时只跟 `runtimeAgentId` 走，不要把 `agentId` 当 backend。

## 4. Recommended Sequence

```text
1. nexum sync TASK-001
2. nexum spawn TASK-001
3. sessions_spawn(runtime="acp", agentId=payload.runtimeAgentId, ...)
4. nexum track TASK-001 <sessionKey> --role generator --stream-log <path>
5. wait for generator completion
6. nexum callback TASK-001 --role generator
7. nexum eval TASK-001
8. sessions_spawn(...) for evaluator
9. nexum track TASK-001 <sessionKey> --role evaluator --stream-log <path>
10. wait for evaluator completion
11. nexum callback TASK-001 --role evaluator
```

## 5. Why `track` Matters

`track` 是任务进入真实运行态的唯一显式入口：

- generator track: `pending -> running`
- evaluator track: `generator_done -> evaluating`

如果同一个 session 被重复 track，CLI 会返回 no-op。
如果晚到 track 试图把任务从更后状态拉回去，CLI 也会返回 no-op。

## 6. Callback Expectations

`callback` 也必须按角色调用：

- generator 结束后: `nexum callback <taskId> --role generator`
- evaluator 结束后: `nexum callback <taskId> --role evaluator`

回调处理是 replay-safe 的：

- 重复 generator callback 不会再次 dispatch evaluator
- stale evaluator callback 不会重新处理已经 retry 的任务
- terminal 状态上的重复回调会返回 no-op

## 7. Dispatch Queue

每次自动 dispatch 都会：

1. 先写 `nexum/dispatch-queue.jsonl`
2. 再 POST `/hooks/agent`

如果 webhook 丢了：

- `nexum watch` 会重放 queue
- 一旦 `track` 或后续状态推进成功，对应 queue entry 会被 ack

因此 orchestrator 不需要自己维护第二套 dispatch 持久层。

## 8. Session Naming

session 名会根据实际执行家族生成：

- `codex-gen-01`
- `claude-eval-02`

这不是装饰字段。它用于日志和排障，应该跟实际 backend 一致。

## 9. Minimal Example

```text
payload = nexum spawn TASK-001
session = sessions_spawn(
  runtime="acp",
  agentId=payload.runtimeAgentId,
  task=payload.promptContent,
  cwd=payload.cwd,
  streamTo="/tmp/TASK-001-gen.jsonl"
)
nexum track TASK-001 session.sessionKey --role generator --stream-log /tmp/TASK-001-gen.jsonl
...
nexum callback TASK-001 --role generator
payload2 = nexum eval TASK-001
...
nexum callback TASK-001 --role evaluator
```

## 10. Operational Rules

- Spawn 前先检查 `constraints.dependsOn` 和 `constraints.conflictsWith`
- spawn 成功后立即 `track`
- 能保存 stream log 就一定保存
- 把 `unknown` session status 当基础设施信号，不要当业务 verdict
- 对任何 webhook / callback / track 都按幂等思路设计
