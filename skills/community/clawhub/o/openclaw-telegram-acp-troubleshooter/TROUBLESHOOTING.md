# Troubleshooting

## Goal | 目标

Stabilize OpenClaw replies in Telegram forum topics when the topic is expected to route into an ACP session backed by `codex`.
当 Telegram forum 话题本应路由到由 `codex` 驱动的 ACP 会话时，稳定 OpenClaw 的回复行为。

## Typical Symptoms | 典型症状

- `/new` replies in the topic, but plain text like `111` does not
- the bot can send outbound messages into the topic, but user messages do not produce a reply
- `requireMention = false` is already set, but non-command text still does not reach the agent
- topic routing is configured, but the topic does not behave like a normal ACP chat

## Fast Diagnosis | 快速判断

### Case 1

- `/new` replies
- plain text does not reply

Most likely cause:

- Telegram is not delivering normal topic messages to the bot reliably
- this is usually not an ACP or `codex` problem

最可能原因：

- Telegram 没有稳定把普通话题消息投递给机器人
- 这通常不是 ACP 或 `codex` 本身的问题

### Case 2

- nothing replies
- outbound send also fails

Most likely cause:

- bot token, webhook, gateway, or Telegram connectivity issue

最可能原因：

- bot token、webhook、gateway 或 Telegram 连通性问题

### Case 3

- messages arrive, but the wrong agent answers

Most likely cause:

- routing or default agent binding issue

最可能原因：

- 路由配置或默认 agent 绑定有误

## Required Checks | 必查项

- confirm the group default agent
- confirm topic-level `agentId` binding for important topics
- confirm `requireMention = false`
- confirm ACP default agent is `codex`

## Runtime Checks | 运行态检查

### Gateway Health | 网关状态

```bash
systemctl --user is-active openclaw-gateway
systemctl --user show -p MainPID -p ActiveEnterTimestamp openclaw-gateway
```

### Main Log | 主日志

```bash
tail -f /tmp/openclaw/openclaw-$(date +%F).log
```

Watch for:
重点看：

- `401 Unauthorized`
- `409 Conflict`
- routing load issues
- agent execution failures

### Command Log | 命令日志

```bash
tail -f ~/.openclaw/logs/commands.log
```

Expected topic session key shape:

```text
agent:codex:telegram:group:<group_id>:topic:<topic_id>
```

### Session Proof | 会话证据

Inspect the matching file under:
检查以下目录中的对应 session 文件：

```text
~/.openclaw/agents/codex/sessions/
```

If `/new` appears there but later plain text does not, the issue is upstream of ACP.
如果这里能看到 `/new`，却看不到后续普通文本，问题就在 ACP 上游。

## Telegram-side Checks | Telegram 侧检查

### Privacy Mode | 隐私模式

If privacy mode was previously enabled, disabling it in BotFather may not be enough for an already-joined group.
如果之前开过 privacy mode，只在 BotFather 里关掉，往往不足以让已加入的群立即恢复正常。

Recommended repair:
推荐修复动作：

1. remove the bot from the group
2. re-add the bot after privacy mode is disabled
3. promote the bot to admin if possible

### Polling Conflict | 轮询冲突

If logs show `409 Conflict: terminated by other getUpdates request`, another process is polling the same bot token.
如果日志里出现 `409 Conflict: terminated by other getUpdates request`，说明还有别的进程在轮询同一个 bot token。

Fix:
修复动作：

- stop the duplicate poller
- restart `openclaw-gateway`

### Bot Identity | 机器人身份校验

After token rotation, confirm the running gateway really restarted and is using the intended token and bot identity.
如果你轮换过 token，要确认运行中的 gateway 确实重启过，并且加载的是新的目标 token 和 bot 身份。

## Interpretation Rules | 解释规则

- if `/new` works, ACP is working
- if outbound `sendMessage` works, the token is valid enough for sends
- if plain text never appears in `commands.log`, the message did not stably enter OpenClaw
- `requireMention = false` only matters after Telegram delivers the update

## Repair Order | 修复顺序

1. verify gateway is active
2. verify `/new` in the topic
3. watch `commands.log`
4. send plain text such as `111`
5. if plain text does not appear in logs, remove and re-add the bot
6. promote the bot to admin if possible
7. re-test plain text in the same topic
8. only after that, consider source-level Telegram plugin investigation

## Verification Checklist | 验证清单

- `/new` replies in the topic
- plain text replies without `@bot`
- `commands.log` records the topic session
- the matching `codex` session file contains the user text
- no `401 Unauthorized`
- no `409 Conflict`
