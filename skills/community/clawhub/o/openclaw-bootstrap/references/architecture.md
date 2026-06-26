# 架构

```
~/.openclaw/workspace/
├── AGENTS.md       ← 规则 + 自我进化 SOP
├── SOUL.md         ← 人格
├── USER.md         ← 用户信息（手动填）
├── MEMORY.md       ← 长期记忆（持续更新）
├── HEARTBEAT.md    ← 心跳检查
├── BOOT.md         ← 启动自检
├── memory/         ← 每日日志
└── .learnings/     ← 自我改进日志
```

## 自我进化闭环

实时出错 → .learnings/ → 每周自省 → 每月 promote → AGENTS.md/MEMORY.md

## 迁移到新机器

1. 复制 `skills/openclaw-bootstrap/` 到新机器
2. `bash scripts/bootstrap.sh`
3. 编辑 USER.md + MEMORY.md
4. 如需同步记忆：复制 MEMORY.md + .learnings/
