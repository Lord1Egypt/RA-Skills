# Open Memory System

三层记忆框架 — 适用于 AI Agent 的持久化记忆系统。

## 功能特性

- **Working Memory** — 会话级临时记忆
- **Short-Term Memory** — 跨会话短期记忆
- **Long-Term Memory** — 持久化记忆（偏好/实体/事件）
- **自动过期清理** — 避免记忆无限膨胀
- **Hook 自动触发** — 自动捕捉用户偏好和重要事件
- **Cron 定期整理** — 保持记忆系统健康

## 安装

```bash
# 1. 解压到 skills 目录
cd ~/.openclaw/workspace/skills
unzip open-memory-system.zip -d open-memory-system

# 2. 部署 Hook 到 ~/.openclaw/hooks/
cp -r open-memory-system/scripts/auto-save-memory ~/.openclaw/hooks/
# load-memory-on-start 已在 ~/.openclaw/hooks/ 中预装，无需重复部署

# 3. 初始化记忆目录
mkdir -p ~/.openclaw/workspace/memory/{user/{preferences,entities,events},agent/{persona,episodic},short-term}

# 4. 创建 Cron（参考 crons/memory-crons.txt）
```

## 使用示例

```bash
# 记录用户偏好
python3 scripts/memory.py pref "沟通方式" "直接高效" "用户明确表示"

# 记录重要事件
python3 scripts/memory.py event "项目启动" "Miloya 开发公司正式成立" "成功"

# 记录经验教训
python3 scripts/memory.py episode "第一次部署失败" "negative" "需要检查依赖版本"

# 读取核心记忆
python3 scripts/memory.py read

# 每日统计
python3 scripts/memory.py summary
```

## 项目结构

```
open-memory-system/
├── SKILL.md              # Skill 说明文档
├── README.md             # 本文件
├── scripts/
│   ├── memory.py         # 核心记忆 CLI
│   ├── distill_l2.py     # L2 自动提炼
│   └── auto-save-memory/ # Hook: session end → 保存 learnings
│       ├── handler.js
│       └── HOOK.md
└── crons/
    └── memory-crons.txt  # Cron 配置指南
```

## 已有内置 Hook

`load-memory-on-start` 已在 `~/.openclaw/hooks/` 中预装，会话启动时自动运行 `memory/memory.py read` 加载记忆，无需额外配置。

## 设计说明

- `auto-save-memory` 在 `session:end` 时将 `.learnings/` 中的 md 文件保存到 `memory/user/events/`
- `distill_l2.py` 在每日 20:00 从 `short-term/` 提炼有价值内容到 `user/events/`

## License

MIT
