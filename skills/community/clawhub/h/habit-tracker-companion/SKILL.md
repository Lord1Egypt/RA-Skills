---
name: habit-tracker-companion
slug: habit-tracker-companion
version: 1.0.0
description: 习惯养成打卡助手，连续激励、数据统计、陪你养成好习惯。
homepage: https://github.com/786793119/miya-skills
metadata: {"openclaw":{"emoji":"🎯","requires":{"bins":["python3"]},"os":["linux","darwin","win32"]}}
---

# 习惯养成打卡 (Habit Tracker Companion)

陪你养成好习惯的打卡助手。

## 功能

- 添加新习惯
- 打卡记录
- 连续打卡天数统计
- 完成率数据分析
- 连续激励（里程碑鼓励）

## 使用示例

```bash
# 添加习惯
python habit-tracker-companion.py add_habit "每天喝水" "每天喝8杯水"

# 打卡
python habit-tracker-companion.py check_in 1

# 查看连续天数
python habit-tracker-companion.py get_streak 1

# 查看统计
python habit-tracker-companion.py get_stats 1
```

## 数据存储

- 习惯数据: `~/.memory/habits/habits.json`

---

*By Miya - 2026*
