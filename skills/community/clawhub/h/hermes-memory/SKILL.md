---
name: hermes-memory
version: 1.0.0
description: Hermes风格自驱记忆系统。模仿Hermes Agent的记忆机制，定期自检记忆健康度、自动提醒整理、保持记忆精简高效。
author: 林林
tags:
  - memory
  - self-improving
  - hermes
  - 记忆系统
---

# Hermes风格自驱记忆系统

模仿Hermes Agent的记忆自检机制，定期检查记忆健康度并主动整理。

## 核心机制

| 文件 | 用途 | 建议大小 |
|------|------|---------|
| MEMORY.md | Agent长期记忆 | ≤2200字 |
| USER.md | 用户画像 | ≤1375字 |
| ~/self-improving/ | 技能记忆 | 按需 |

## 功能

- 📊 记忆使用率监控
- 💡 整理建议提醒
- 🔄 自动存档旧记忆
- ⏰ 定时自检（每天1次）

## 运行方式

**手动自检：**
```bash
python3 ~/self-improving/hermes-memory/memory_health.py
```

**自动定时（每天收盘后17:30自检一次）：**
```bash
# 添加到crontab
crontab -e
# 写入：
30 17 * * 1-5 /home/linuxbrew/.linuxbrew/bin/python3 /home/jdvrommel/self-improving/hermes-memory/memory_health.py >> /home/jdvrommel/self-improving/hermes-memory/health.log 2>&1
```

## 触发整理的条件

- MEMORY.md使用率 ≥70% → 建议精简
- MEMORY.md使用率 ≥90% → 必须整理
- USER.md使用率 ≥90% → 必须整理

## 和Hermes的区别

| 功能 | Hermes | 这个Skill |
|------|--------|---------|
| 记忆限制 | 固定2200/1375字 | 建议上限 |
| 自动整理 | Agent自动 | 提示+手动 |
| 记忆工具 | add/replace/remove | 文件编辑 |
| 快照机制 | 冻结快照 | 实时更新 |
