# BOOT.md - Gateway 启动检查

> 每次 gateway 重启时自动执行（由 boot-md hook 触发）

## 启动检查清单

1. **Cron 健康**: 运行 `openclaw cron list`，检查有无 error 状态的任务
2. **Hook 状态**: 确认 self-improvement hook 已加载
3. **记忆连续性**: 检查 `memory/` 目录是否有昨天的日志，没有就补一条

## 如果发现问题
- Cron error → 尝试 `openclaw cron run <id>` 重跑
- Hook 缺失 → `openclaw hooks enable self-improvement`
- 记忆断档 → 在当天日志里标注"无上下文恢复"

## 不做的事
- 不主动打扰用户
- 不发消息，只做内部检查
- 检查完回复 HEARTBEAT_OK
