---
name: health-tracker
description: 健康追踪技能 - 追踪饮水、睡眠、步数等健康数据，JSON存储。
metadata: {"openclaw": {"requires": {}, "install": []}}
tags: [health, tracking, water, sleep, fitness]
version: 1.0.0
author: laosi
source: adapted
---

# Health Tracker - 健康追踪

> 激活词: 健康追踪 / 记录饮水 / 睡眠追踪

## 功能

- 饮水记录
- 睡眠追踪
- 步数记录
- 体重追踪
- 数据统计

## 数据存储

```json
{
  "water": [
    {"time": "2026-04-28T08:00:00", "amount": 250}
  ],
  "sleep": [
    {"date": "2026-04-27", "start": "23:00", "end": "07:00", "hours": 8}
  ],
  "steps": [
    {"date": "2026-04-28", "count": 8000}
  ]
}
```

## Python实现

```python
import json
from datetime import datetime
from pathlib import Path

class HealthTracker:
    def __init__(self, data_file: str = "health_data.json"):
        self.data_file = data_file
        self.data = self._load()
    
    def _load(self) -> dict:
        if Path(self.data_file).exists():
            with open(self.data_file, 'r') as f:
                return json.load(f)
        return {'water': [], 'sleep': [], 'steps': []}
    
    def _save(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def log_water(self, amount: int):
        self.data['water'].append({
            'time': datetime.now().isoformat(),
            'amount': amount
        })
        self._save()
    
    def log_sleep(self, start: str, end: str):
        hours = self._calc_hours(start, end)
        self.data['sleep'].append({
            'date': datetime.now().date().isoformat(),
            'start': start,
            'end': end,
            'hours': hours
        })
        self._save()
    
    def log_steps(self, count: int):
        today = datetime.now().date().isoformat()
        # ���新今日数据
        for entry in self.data['steps']:
            if entry['date'] == today:
                entry['count'] = count
                break
        else:
            self.data['steps'].append({'date': today, 'count': count})
        self._save()
    
    def get_stats(self) -> dict:
        # 今日饮水
        today = datetime.now().date().isoformat()
        water_today = sum(e['amount'] for e in self.data['water'] 
                         if e['time'].startswith(today))
        
        # 平均睡眠
        if self.data['sleep']:
            avg_sleep = sum(e['hours'] for e in self.data['sleep']) / len(self.data['sleep'])
        else:
            avg_sleep = 0
        
        return {
            'water_today': water_today,
            'water_goal': 2000,
            'avg_sleep': avg_sleep,
            'steps_today': self._get_steps_today(),
        }
    
    def _calc_hours(self, start: str, end: str) -> float:
        start_h, start_m = map(int, start.split(':'))
        end_h, end_m = map(int, end.split(':'))
        hours = end_h - start_h
        if end_h < start_h:
            hours += 24
        return hours - start_m/60 + end_m/60
    
    def _get_steps_today(self) -> int:
        today = datetime.now().date().isoformat()
        for entry in self.data['steps']:
            if entry['date'] == today:
                return entry['count']
        return 0
```

## 使用命令

```python
tracker = HealthTracker()

# 记录饮水
tracker.log_water(250)  # 250ml

# 记录睡眠
tracker.log_sleep("23:00", "07:00")

# 记录步数
tracker.log_steps(8000)

# 获取统计
stats = tracker.get_stats()
print(f"今日饮水: {stats['water_today']}ml / {stats['water_goal']}ml")
print(f"平均睡眠: {stats['avg_sleep']:.1f}小时")
```

## 输出格式

```markdown
## 健康数据

### 今日
- 饮水: 1500ml / 2000ml (75%)
- 步数: 8000步
- 睡眠: 7.5小时 (平均)

### 周报
- 平均饮水: 1800ml/天
- 平均睡眠: 7.2小时/天
- 总步数: 56,000步
```