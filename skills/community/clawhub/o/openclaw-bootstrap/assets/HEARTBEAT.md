# HEARTBEAT.md - 心跳检查

每次心跳按需执行（不必每项都查，轮流即可）：

## 可执行检查
- [ ] 未读消息（如有重要的主动提醒）
- [ ] cron 任务状态（`openclaw cron list`，有 error 就提醒）
- [ ] memory/ 目录是否有今天的日志（没有就记一笔当前上下文）

## 自我进化检查（每周 1-2 次）
- [ ] 扫描 `.learnings/` 中 pending 高优先级条目 → promote 到 AGENTS.md / MEMORY.md
- [ ] 检查近期 `memory/YYYY-MM-DD.md` → 提炼到 MEMORY.md
- [ ] 清理 MEMORY.md 中过时信息

## 静默规则
- 23:00-08:00 不打扰（除非紧急）
- 没事就回 HEARTBEAT_OK，不要凑数
- 上次检查 <30min 前且无新消息 → HEARTBEAT_OK
