---
name: habit-checkin
version: 1.0.0
description: 习惯追踪 - 每天打卡，自动计算连续天数/历史最佳/总打卡数，多习惯管理，本地JSON持久化
tags: [habit, tracking, daily-life, health, motivation, streak]
author: laosi
source: original
---

# Habit Checkin - 习惯追踪

> 激活词: 打卡 / 签到 / 习惯 / checkin

## 功能

- 每日一键打卡
- 自动计算连续天数（streak）
- 历史最佳记录
- 多习惯独立追踪
- 本地 JSON 持久化

## Python 实现

```python
import os, json
from datetime import datetime, date

HABIT_FILE = os.path.join(os.path.dirname(__file__), "habit_streaks.json")

class HabitTracker:
    def __init__(self):
        os.makedirs(os.path.dirname(HABIT_FILE), exist_ok=True)
        self.habits = self._load()
    
    def _load(self):
        if os.path.exists(HABIT_FILE):
            with open(HABIT_FILE, encoding="utf-8") as f:
                return json.load(f)
        return {}
    
    def _save(self):
        with open(HABIT_FILE, "w", encoding="utf-8") as f:
            json.dump(self.habits, f, ensure_ascii=False, indent=2)
    
    def _today(self):
        return date.today().isoformat()
    
    def checkin(self, name: str = "default") -> dict:
        """打卡一次"""
        today = self._today()
        if name not in self.habits:
            self.habits[name] = {
                "dates": [],
                "streak": 0,
                "best": 0,
                "total": 0,
                "created": today
            }
        
        h = self.habits[name]
        
        if today in h["dates"]:
            return {"status": "already_done", "habit": name, "streak": h["streak"]}
        
        # 检查是否连续
        h["dates"].append(today)
        h["total"] += 1
        
        if h["dates"]:
            last_date = h["dates"][-2] if len(h["dates"]) >= 2 else None
            from datetime import timedelta
            if last_date and date.fromisoformat(last_date) == date.today() - timedelta(days=1):
                h["streak"] += 1
            else:
                h["streak"] = 1
        else:
            h["streak"] = 1
        
        if h["streak"] > h["best"]:
            h["best"] = h["streak"]
        
        self._save()
        return {
            "status": "checked_in",
            "habit": name,
            "streak": h["streak"],
            "best": h["best"],
            "total": h["total"]
        }
    
    def stats(self, name: str = "default") -> dict:
        """查看习惯统计"""
        if name not in self.habits:
            return {"exists": False}
        h = self.habits[name]
        return {
            "exists": True,
            "habit": name,
            "streak": h["streak"],
            "best": h["best"],
            "total": h["total"],
            "last_checkin": h["dates"][-1] if h["dates"] else None,
            "created": h["created"]
        }
    
    def list_all(self) -> list:
        """列出所有习惯"""
        return [self.stats(n) for n in self.habits]

# 使用示例
tracker = HabitTracker()

# 每天早上打卡
result = tracker.checkin("阅读")
if result["status"] == "checked_in":
    print(f"✅ {result['habit']} 打卡成功！连续 {result['streak']} 天")
elif result["status"] == "already_done":
    print(f"✅ 今天已打卡，连续 {result['streak']} 天")

# 查看统计
s = tracker.stats("阅读")
print(f"📊 {s['habit']}: 连续{s['streak']}天 🏆最佳{s['best']}天 📅共{s['total']}天")

# 一周戒糖打卡
tracker.checkin("戒糖")
```

## 命令行用法

```bash
# 阅读打卡
python -c "from habit_tracker import HabitTracker; r=HabitTracker().checkin('阅读'); print(f'连续{r[\"streak\"]}天')"

# 查看所有习惯
python -c "from habit_tracker import HabitTracker; [print(f'{s[\"habit\"]}: {s[\"streak\"]}d') for s in HabitTracker().list_all()]"
```

## 数据格式

```json
{
  "阅读": {
    "dates": ["2026-05-26", "2026-05-27", "2026-05-28"],
    "streak": 3,
    "best": 7,
    "total": 15,
    "created": "2026-05-01"
  }
}
```

## 使用场景

1. **阅读习惯**: 每天读10分钟书，打卡记录
2. **健身打卡**: 跑步/健身/拉伸，坚持看得见
3. **早睡早起**: 23点前睡+7点前起，双重打卡
4. **戒断习惯**: 戒糖/戒烟/戒刷短视频，天数就是动力
5. **学习追踪**: 每天学英语/编程，连续天数激励

## 核心心理机制

- **不要断链**(Don't break the chain) — Jerry Seinfeld 的经典方法
- **连续天数 > 总天数** — streak 比 total 更有激励性
- **最佳记录** — 激励你超越自己的历史高点

## 依赖

- Python 3.8+
- 无第三方依赖
