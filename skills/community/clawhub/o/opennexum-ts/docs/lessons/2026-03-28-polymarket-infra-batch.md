
---

## Lesson: claude CLI 在 ACP 非交互模式下会卡住，必须用 codex
- trigger: sessions_spawn 用 agentId="claude" 时，claude session 启动后60秒无输出，卡在交互式权限确认
- wrong: `sessions_spawn(agentId="claude", runtime="acp")` — claude CLI 需要 TTY 才能正常工作
- right: 所有 ACP sessions_spawn 任务统一用 `agentId="codex"`；claude 只在 tmux PTY 模式（cc-frontend）下使用
- affected: nexum-ts/packages/cli/src/commands/spawn.ts（agentCli 字段），sessions_spawn 调用
- agent_note: NX2 系列任务的 contract generator 全部改为 codex；cc-frontend 只在 tmux dispatch 时用
- tags: acp, claude, codex, sessions_spawn, non-interactive
