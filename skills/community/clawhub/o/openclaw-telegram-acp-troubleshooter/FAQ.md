# FAQ

## Why does `/new` reply but normal text does not? | 为什么 `/new` 能回，但普通文本不行？

Usually because Telegram delivered the command-style update, but did not reliably deliver normal group or topic messages to the bot.
通常是因为 Telegram 投递了命令型更新，但没有稳定投递普通群消息或话题消息给机器人。

## Does `requireMention = false` guarantee replies? | `requireMention = false` 能保证回复吗？

No. It only removes the mention requirement inside OpenClaw routing. Telegram still has to deliver the message update first.
不能。它只是在 OpenClaw 路由里取消必须 `@bot` 的限制，前提仍然是 Telegram 先把消息投递进来。

## If a topic is bound to `codex`, does every message become an ACP `codex` chat? | 话题绑定到 `codex` 后，是否每条消息都会进入 ACP `codex`？

Only if the message reaches OpenClaw.
只有消息真的到达 OpenClaw 才会。

## Is ACP the same as `codex`? | ACP 和 `codex` 是一回事吗？

No. ACP is the conversation and execution path. `codex` is the agent behind that conversation.
不是。ACP 是会话和执行通路，`codex` 是这个会话背后的 agent。

## After disabling privacy mode, do I need to re-add the bot? | 关掉 privacy mode 后，需要重新拉机器人进群吗？

Often yes. In practice, re-adding the bot is one of the most common fixes for this symptom.
很多时候需要。实战里，重新把机器人移出再拉回群，是这个问题最常见的修复动作之一。

## How do I know a message really reached ACP? | 怎么确认消息真的进了 ACP？

Check `~/.openclaw/logs/commands.log` and the matching file in `~/.openclaw/agents/codex/sessions/`.
检查 `~/.openclaw/logs/commands.log`，以及 `~/.openclaw/agents/codex/sessions/` 下对应的 session 文件。
