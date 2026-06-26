---
name: cron-parser
version: 1.0.0
description: Cron解析 - 解析cron表达式，翻译为自然语言，计算下次执行时间，支持标准和扩展语法
tags: [cron, schedule, parser, time, automation]
author: laosi
source: original
---

# Cron Parser - Cron表达式解析

> 激活词: cron / 解析cron / 定时表达式

## 功能

- 解析5字段标准cron表达式
- 翻译为自然语言描述
- 计算下次N次执行时间
- 验证cron表达式合法性
- 生成常用cron模板

## Python 实现

```python
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import calendar

WEEKDAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
MONTHS = ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

class CronParser:
    def __init__(self):
        self.presets = {
            "every_minute": "* * * * *",
            "every_5min": "*/5 * * * *",
            "every_15min": "*/15 * * * *",
            "every_30min": "*/30 * * * *",
            "hourly": "0 * * * *",
            "every_2hours": "0 */2 * * *",
            "daily_midnight": "0 0 * * *",
            "daily_9am": "0 9 * * *",
            "daily_2pm": "0 14 * * *",
            "weekdays_9am": "0 9 * * 1-5",
            "weekdays_6pm": "0 18 * * 1-5",
            "weekly_sunday": "0 0 * * 0",
            "weekly_monday": "0 9 * * 1",
            "monthly_1st": "0 0 1 * *",
            "monthly_15th": "0 0 15 * *",
            "quarterly": "0 0 1 1,4,7,10 *",
            "yearly_jan1": "0 0 1 1 *",
        }
    
    def parse(self, cron_expr: str) -> dict:
        """解析cron表达式"""
        parts = cron_expr.strip().split()
        if len(parts) != 5:
            return {"error": f"Invalid cron expression: {cron_expr}", "valid": False}
        
        minute, hour, day, month, weekday = parts
        
        # 验证
        if not self._validate_field(minute, 0, 59):
            return {"error": f"Invalid minute: {minute}", "valid": False}
        if not self._validate_field(hour, 0, 23):
            return {"error": f"Invalid hour: {hour}", "valid": False}
        if not self._validate_field(day, 1, 31):
            return {"error": f"Invalid day: {day}", "valid": False}
        if not self._validate_field(month, 1, 12):
            return {"error": f"Invalid month: {month}", "valid": False}
        if not self._validate_field(weekday, 0, 7):
            return {"error": f"Invalid weekday: {weekday}", "valid": False}
        
        # 翻译
        description = self._translate(minute, hour, day, month, weekday)
        
        # 下次执行
        next_runs = self._next_runs(cron_expr, count=5)
        
        return {
            "expression": cron_expr,
            "fields": {
                "minute": minute,
                "hour": hour,
                "day": day,
                "month": month,
                "weekday": weekday,
            },
            "description": description,
            "next_runs": [r.isoformat() for r in next_runs],
            "valid": True,
        }
    
    def _validate_field(self, field: str, min_val: int, max_val: int) -> bool:
        """验证单个字段"""
        if field == "*":
            return True
        if "/" in field:
            parts = field.split("/")
            return self._validate_field(parts[0], min_val, max_val) and parts[1].isdigit()
        if "-" in field:
            parts = field.split("-")
            return all(p.isdigit() for p in parts) and len(parts) == 2
        if "," in field:
            return all(self._validate_field(p, min_val, max_val) for p in field.split(","))
        return field.isdigit() and min_val <= int(field) <= max_val
    
    def _translate(self, minute: str, hour: str, day: str, month: str, weekday: str) -> str:
        """翻译为自然语言"""
        parts = []
        
        # 时间部分
        if minute == "*" and hour == "*":
            parts.append("Every minute")
        elif minute == "*":
            parts.append(f"Every hour at minute {hour}")
        elif hour == "*":
            m = minute if "/" not in minute else f"every {minute.split('/')[1]} minutes"
            parts.append(f"Every hour at {m} past")
        else:
            m = minute.zfill(2)
            h = hour.zfill(2)
            parts.append(f"At {h}:{m}")
        
        # 日期部分
        if day == "*" and month == "*" and weekday == "*":
            pass  # daily
        elif day != "*" and month == "*":
            parts.append(f"on day {day} of every month")
        elif month != "*":
            month_names = [MONTHS[int(m)] for m in month.split(",") if m.isdigit()]
            parts.append(f"in {', '.join(month_names)}")
        
        if weekday != "*":
            if "-" in weekday:
                start, end = weekday.split("-")
                parts.append(f"on {WEEKDAYS[int(start)]}-{WEEKDAYS[int(end)]}")
            elif "," in weekday:
                days = [WEEKDAYS[int(w)] for w in weekday.split(",")]
                parts.append(f"on {', '.join(days)}")
            else:
                parts.append(f"every {WEEKDAYS[int(weekday)]}")
        
        return " ".join(parts)
    
    def _next_runs(self, cron_expr: str, count: int = 5) -> List[datetime]:
        """计算下次执行时间"""
        parts = cron_expr.strip().split()
        minute, hour, day, month, weekday = parts
        now = datetime.now()
        runs = []
        
        # 简化实现：向前搜索最多366天
        check = now + timedelta(minutes=1)
        check = check.replace(second=0, microsecond=0)
        
        max_days = 366
        day_count = 0
        while len(runs) < count and day_count < max_days:
            if self._matches(check, parts):
                runs.append(check)
            check += timedelta(minutes=1)
            if check.hour == 0 and check.minute == 0:
                day_count += 1
        
        return runs
    
    def _matches(self, dt: datetime, parts: list) -> bool:
        """检查时间是否匹配cron表达式"""
        minute, hour, day, month, weekday = parts
        return (
            self._field_match(dt.minute, minute, 0, 59) and
            self._field_match(dt.hour, hour, 0, 23) and
            self._field_match(dt.day, day, 1, 31) and
            self._field_match(dt.month, month, 1, 12) and
            self._field_match(dt.isoweekday() % 7, weekday, 0, 7)
        )
    
    def _field_match(self, value: int, field: str, min_val: int, max_val: int) -> bool:
        if field == "*":
            return True
        if "/" in field:
            base, step = field.split("/")
            step = int(step)
            if base == "*":
                return value % step == 0
            return self._field_match(value, base, min_val, max_val) and value % step == 0
        if "-" in field:
            start, end = map(int, field.split("-"))
            return start <= value <= end
        if "," in field:
            return any(self._field_match(value, f, min_val, max_val) for f in field.split(","))
        return field.isdigit() and int(field) == value
    
    def get_presets(self) -> Dict[str, str]:
        """获取预设cron表达式"""
        return self.presets

# 使用示例
parser = CronParser()

# 解析表达式
result = parser.parse("0 9 * * 1-5")
print(f"表达式: {result['expression']}")
print(f"含义: {result['description']}")
print(f"有效: {result['valid']}")
print("下次执行:")
for r in result["next_runs"]:
    print(f"  {r}")

# 查看预设
print("\n常用预设:")
for name, expr in parser.get_presets().items():
    parsed = parser.parse(expr)
    print(f"  {name:20} {expr:15} -> {parsed['description']}")
```

## Cron速查

```
* * * * *
│ │ │ │ │
│ │ │ │ └── 星期 (0=Sun, 1=Mon, ..., 6=Sat)
│ │ │ └──── 月份 (1-12)
│ │ └────── 日期 (1-31)
│ └──────── 小时 (0-23)
└────────── 分钟 (0-59)
```

| 表达式 | 含义 |
|--------|------|
| `* * * * *` | 每分钟 |
| `*/5 * * * *` | 每5分钟 |
| `0 * * * *` | 每小时整点 |
| `0 9 * * *` | 每天9点 |
| `0 9 * * 1-5` | 工作日9点 |
| `0 0 * * 0` | 每周日零点 |
| `0 0 1 * *` | 每月1日零点 |

## 使用场景

1. **任务调度**: 理解cron表达式的含义
2. **调度器开发**: 验证和生成调度规则
3. **自动化脚本**: 设置定时执行计划
4. **监控告警**: 配置周期性检查

## 依赖

- Python 3.8+
- 标准库（datetime, calendar）
