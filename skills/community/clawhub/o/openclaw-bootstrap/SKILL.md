---
name: openclaw-bootstrap
description: "One-command bootstrap for new OpenClaw installations. Sets up workspace files, self-evolution system (.learnings + hooks + crons), and community skills. Use when setting up a fresh OpenClaw or replicating setup to another machine."
---

# OpenClaw Bootstrap

一键初始化 OpenClaw 最佳实践环境。

## 使用

```bash
bash scripts/bootstrap.sh
```

## 初始化内容

| 类别 | 内容 |
|------|------|
| 工作区 | AGENTS.md, SOUL.md, USER.md, MEMORY.md, HEARTBEAT.md, BOOT.md |
| 自我进化 | `.learnings/` + self-improving-agent skill + hook |
| 定时任务 | 周度自省 (周日 22:00) + 月度学习复盘 (1号 21:00) |

## 初始化后手动完成

1. 编辑 `USER.md` — 填入个人信息
2. 编辑 `MEMORY.md` — 补充偏好
3. `clawhub login` — 登录 ClawHub
