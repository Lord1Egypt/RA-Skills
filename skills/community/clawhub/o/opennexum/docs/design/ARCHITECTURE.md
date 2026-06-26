# OpenNexum Architecture

> Updated: 2026-03-31

## 1. System Boundary

OpenNexum 把“任务语义”和“运行时执行”明确拆开：

- `Contract YAML`: 任务静态语义，单一事实来源
- `nexum/active-tasks.json`: 运行时状态缓存，只保存当前任务状态和会话信息
- orchestrator / OpenClaw: 实际 spawn ACP session、心跳、日志采集

这意味着仓库内不再直接负责 session spawn。本地 CLI 的职责是：

- 解析和校验 contract
- 同步 contract 到 runtime state
- 生成 generator / evaluator / retry prompt
- 推进状态机
- 发送通知和 webhook

## 2. Package Layout

```text
packages/
├── core/      type, config, contract parsing, task state, sync
├── prompts/   generator / evaluator / retry prompt rendering
├── spawn/     ACP session status lookup helpers
├── notify/    notification templates + openclaw message send
└── cli/       nexum command entrypoints
```

## 3. Source of Truth

### Static truth

`docs/nexum/contracts/*.yaml` 是任务静态语义的唯一来源：

- `id`
- `name`
- `batch`
- `scope`
- `deliverables`
- `eval_strategy`
- `agent`
- `depends_on`

### Runtime truth

`nexum/active-tasks.json` 只保留动态字段：

- `status`
- `iteration`
- `base_commit` / `commit_hash`
- generator / evaluator session keys and stream logs
- timestamps
- `last_error`

### Sync rule

`nexum sync` 会把 contract 同步进 runtime state：

- 新 contract 自动注册成 `pending` 或 `blocked`
- 已有任务会更新 `name` / `contract_path` / `depends_on`
- 只有 `pending` / `blocked` 会被依赖关系重新归一化
- `running` / `evaluating` / `done` 等运行态不会被 sync 覆盖

任何公开命令都不应再要求用户手工编辑 `active-tasks.json`。

## 4. Agent Model

OpenNexum 里有两层 agent 身份：

- `agentId`: 逻辑 agent，例如 `codex-gen-01`
- `runtimeAgentId`: ACP backend，例如 `codex`

`resolveAgentExecution()` 的规则是：

- 优先读 `nexum/config.json` 的显式映射
- 标准逻辑前缀 `codex-*` / `claude-*` 可直接推断 CLI 家族
- 对未知且未配置的逻辑 agent，直接报错，不再静默回退到 `codex`

这保证了 cross-review 语义不会在单 CLI 环境里悄悄失真。

## 5. State Machine

```text
blocked -> pending -> running -> generator_done -> evaluating -> done
                                         |              |
                                         |              -> fail -> pending (retry)
                                         |
                                         -> stale duplicate callback/track -> no-op

any state -> escalated
```

核心规则：

- 只有 `track --role generator` 才能把任务推进到 `running`
- 只有 `track --role evaluator` 才能把任务推进到 `evaluating`
- `spawn` 只准备 payload，不伪造运行态
- `callback` / `track` / `complete` 必须是 replay-safe

Replay-safe 的含义：

- 重复 generator callback 不会再次派 evaluator
- 晚到 generator track 不会把 `generator_done` 打回 `running`
- stale evaluator callback 不会把已 retry 的任务重新处理一遍

## 6. Scheduling Constraints

Contract 里的约束必须被机器消费，而不是只留给人看：

- `depends_on`
- `scope.conflicts_with`
- `scope.files`
- `scope.boundaries`

`spawn payload` 会直接输出这些约束。`runSpawn()` 同时在仓库侧做基本校验：

- 非 `pending` 任务不能再次 spawn generator
- 依赖未满足时拒绝 spawn
- 与正在 `running / generator_done / evaluating` 的冲突任务互斥

因此 orchestrator 既有 payload 级约束，也有 CLI 级防线。

## 7. Dispatch and Recovery

### Happy path

```text
nexum spawn
-> orchestrator sessions_spawn(generator)
-> nexum track --role generator
-> nexum callback --role generator
-> enqueue dispatch entry + POST /hooks/agent
-> orchestrator nexum eval
-> orchestrator sessions_spawn(evaluator)
-> nexum track --role evaluator
-> nexum callback --role evaluator
-> nexum complete
```

### Recovery path

每次自动 dispatch 都会先写 `nexum/dispatch-queue.jsonl`，然后再 POST webhook。

如果 webhook 没有送达：

- queue entry 保留
- `nexum watch` 周期性重放 webhook
- `track` 或后续状态推进会 ack 对应 entry

这样 dispatch 既有实时路径，也有幂等兜底。

## 8. Session Naming

session 名称按实际 CLI 家族和阶段生成：

- `codex-gen-01`
- `claude-eval-02`
- `claude-gen-03`

命名依据不再写死为“generator=codex / evaluator=claude”，而是跟实际逻辑 agent 的执行家族保持一致。

## 9. Runtime Artifacts

这些文件都属于运行时产物，不应作为可发布模板内容被跟踪：

- `nexum/active-tasks.json`
- `nexum/config.json`
- `nexum/dispatch-queue.jsonl`
- `nexum/session-counter.json`
- `nexum/history/*.json`
- `nexum/runtime/**`

Repo 里只保留必要的 `.gitkeep` 和文档示例。

## 10. Commands

关键命令与职责：

- `nexum sync`: contract -> runtime state
- `nexum spawn`: 生成 generator payload
- `nexum eval`: 生成 evaluator payload
- `nexum track`: 记录真实 session 并推进运行态
- `nexum callback`: 处理 generator / evaluator 完成事件
- `nexum complete`: 根据 verdict 进入 done / retry / escalated
- `nexum watch`: dispatch queue replay + stuck task detection
