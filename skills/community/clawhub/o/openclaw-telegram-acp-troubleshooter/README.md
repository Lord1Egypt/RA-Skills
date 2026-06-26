# OpenClaw Telegram ACP Troubleshooter

This skill helps diagnose why Telegram forum topics do not reliably reach an OpenClaw ACP session backed by `codex`.
这个 skill 用来诊断 Telegram forum 话题为什么不能稳定进入由 `codex` 驱动的 OpenClaw ACP 会话。

## What This Skill Is For | 适用场景

Use it when:
适用于：

- `/new` replies in a Telegram topic, but normal text does not
- the bot can send outbound messages, but user messages do not trigger replies
- topic routing is configured, but the wrong agent responds
- you need to distinguish Telegram delivery problems from ACP or `codex` problems

中文概括：

- `/new` 有回复，但普通文本没回复
- 机器人能主动发消息，但用户消息不触发回复
- 话题路由已经配置，但回应的 agent 不对
- 需要区分到底是 Telegram 投递问题，还是 ACP / `codex` 执行问题

## What It Checks | 它会检查什么

The skill is built around a practical decision order:
这个 skill 按实战顺序检查：

1. confirm routing and topic binding
2. confirm gateway health
3. confirm whether input reached OpenClaw at all
4. separate Telegram delivery issues from ACP execution issues
5. recommend the next single best fix

## Included Files | 包含文件

- `SKILL.md`: the executable skill instructions
- `TROUBLESHOOTING.md`: the full runbook
- `FAQ.md`: the short operator FAQ

## Typical Conclusion Pattern | 常见结论模式

If `/new` works but plain text does not appear in `commands.log`, the most likely problem is Telegram delivery rather than ACP or `codex`.
如果 `/new` 正常，但普通文本没有进入 `commands.log`，最可能的问题是 Telegram 投递，而不是 ACP 或 `codex`。

## Local Use | 本地使用

Place this folder under one of these locations:
把这个目录放到以下任一位置：

- `<workspace>/skills/`
- `~/.openclaw/skills/`

Then start a new OpenClaw session or refresh skills.
然后重新开始一个 OpenClaw 会话，或刷新 skills。

## ClawHub Publish Shape | ClawHub 发布方式

This folder is self-contained so it can be published to ClawHub as a single skill bundle.
这个目录是自包含的，可以直接作为一个 skill 包发布到 ClawHub。

Example publish command:
发布示例命令：

```bash
clawhub publish ./skills/shared/openclaw-telegram-acp-troubleshooter \
  --slug openclaw-telegram-acp-troubleshooter \
  --name "OpenClaw Telegram ACP Troubleshooter" \
  --version 1.0.0 \
  --tags latest,telegram,acp,troubleshooting
```

## Recommended Companion Docs | 配套文档建议

If you are maintaining a shared workspace, also keep the canonical source docs in Markdown under your knowledge tree so they can be versioned and mirrored into OpenClaw memory.
如果你在维护共享工作区，建议同时把规范文档保存在知识库 Markdown 里，这样可以做版本管理，并同步到 OpenClaw memory。
