---
name: openclaw-telegram-acp-troubleshooter
description: Diagnose why Telegram forum topics do not reliably route into OpenClaw ACP sessions backed by codex. 诊断 Telegram 话题为何无法稳定进入 OpenClaw 的 codex ACP 会话。
homepage: https://docs.openclaw.ai/tools/clawhub
---

# OpenClaw Telegram ACP Troubleshooter

Use this skill when Telegram group topics are expected to talk directly to an ACP session, but the bot does not reply reliably.
当 Telegram 群组话题本应直接进入 ACP 会话，但机器人回复不稳定时，使用这个 skill。

This skill is designed to be self-contained for workspace use and ClawHub publishing.
这个 skill 设计为可独立打包，既可在本地工作区使用，也可直接发布到 ClawHub。

## Read First | 先读这些

Review these files before concluding anything:
在下结论之前，先看这些文件：

- `{baseDir}/README.md`
- `{baseDir}/TROUBLESHOOTING.md`
- `{baseDir}/FAQ.md`

## Primary Rule | 核心判断

If `/new` works but normal topic text does not, do not blame ACP first. Treat Telegram delivery as the leading suspect until logs prove otherwise.
如果 `/new` 能工作，但普通话题文本不工作，先不要怀疑 ACP。除非日志证明不是，否则优先把 Telegram 投递当成头号嫌疑。

## Workflow | 诊断顺序

1. Confirm the routing target:
   确认路由目标：
   - group default agent
   - topic-level `agentId`
   - `requireMention` setting
2. Confirm gateway health:
   确认 gateway 健康状态：
   - `systemctl --user is-active openclaw-gateway`
   - inspect the current gateway log
3. Confirm OpenClaw ingestion:
   确认 OpenClaw 是否真的收到了输入：
   - watch `~/.openclaw/logs/commands.log`
   - inspect the relevant session file under `~/.openclaw/agents/codex/sessions/`
4. Separate the failure class:
   区分故障类别：
   - token or auth
   - duplicate poller
   - Telegram not delivering normal text
   - routing bound to the wrong agent
5. Recommend the next action in priority order, with evidence.
   按概率和证据给出下一步动作。
6. If the user wants durable documentation, point them to:
   如果用户想要长期保存文档，指向：
   - `{baseDir}/README.md` for usage
   - `{baseDir}/TROUBLESHOOTING.md` for the full runbook
   - `{baseDir}/FAQ.md` for short operator answers

## Strong Heuristics | 强判断规则

- `/new` works: ACP path is alive.
- `/new` works: ACP path is alive.
- outbound send works: token is valid enough for sends.
- plain text missing from `commands.log`: Telegram delivery problem or upstream filter.
- `409 Conflict`: another poller is active.
- privacy mode was recently changed: re-add the bot before patching code.

中文解释：

- `/new` 能回复：ACP 通路正常。
- 能主动发消息：token 至少对发送是有效的。
- 普通文本没进 `commands.log`：大概率是 Telegram 投递或更上游的过滤问题。
- `409 Conflict`：还有别的轮询器在抢同一个 bot token。
- 刚改过 privacy mode：先移除并重新拉机器人入群，再谈改代码。

## Safe Commands | 安全命令

```bash
systemctl --user show -p MainPID -p ActiveEnterTimestamp openclaw-gateway
tail -f ~/.openclaw/logs/commands.log
tail -f /tmp/openclaw/openclaw-$(date +%F).log
```

## Response Format | 输出格式

Always return:
始终按下面格式返回：

1. current conclusion
2. evidence
3. next single best action
4. what to test after that

## Constraints | 约束

- Do not reveal secret values from env vars, 1Password, or config.
- Do not recommend source patches before Telegram delivery checks are exhausted.
- Prefer topic-level binding for important threads.
- Keep recommendations actionable and ordered by probability.

中文约束：

- 不要泄露 env、1Password 或配置中的密钥值。
- 在 Telegram 投递问题没排干净前，不要先建议改源码。
- 重要话题优先使用 topic 级绑定。
- 建议必须可执行，并按概率高低排序。
