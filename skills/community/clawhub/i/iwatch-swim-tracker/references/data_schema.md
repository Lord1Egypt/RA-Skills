# 游泳训练数据结构定义

本文档定义从 Apple Watch 健身（泳池游泳）截图中提取的结构化数据格式。

## 顶层字段

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `date` | string | ✅ | 训练日期，格式 `YYYY-MM-DD` |
| `time_range` | string | ✅ | 训练时段，格式 `HH:MM-HH:MM` |
| `pool_length` | int | ✅ | 泳池长度（米），通常 25 或 50 |
| `total_distance` | int | ✅ | 总距离（米） |
| `laps` | int | ✅ | 趟数 |
| `strokes` | object | ✅ | 各泳姿距离分布 |
| `duration` | string | ✅ | 体能训练时间，格式 `H:MM:SS` |
| `duration_seconds` | int | ✅ | 时长（秒） |
| `avg_pace` | string | ✅ | 平均配速，格式 `M:SS/100m` |
| `avg_pace_seconds` | int | ✅ | 平均配速（秒/100m） |
| `avg_heart_rate` | int | ✅ | 平均心率（次/分） |
| `active_calories` | int | ❌ | 动态千卡 |
| `total_calories` | int | ❌ | 总千卡数 |
| `effort_score` | int | ❌ | 耗能评分（1-10） |
| `effort_level` | string | ❌ | 耗能等级，如「适中」「困难」等 |
| `session_number` | int | ❌ | 第 N 次游泳（累计次数，如用户提供） |
| `auto_sets` | array | ❌ | 自动组合数据 |

## strokes 泳姿对象

```json
{
  "kickboard": {"distance": 500},
  "breaststroke": {"distance": 500},
  "freestyle": {"distance": 1500}
}
```

支持的泳姿键名：`freestyle`（自由泳）、`breaststroke`（蛙泳）、`backstroke`（仰泳）、`butterfly`（蝶泳）、`medley`（混合泳）、`kickboard`（浮板）。

## auto_sets 自动组合

```json
[
  {
    "stroke": "freestyle",
    "distance": 400,
    "time": "23'",
    "swolf": 55.5
  },
  {
    "stroke": "breaststroke",
    "distance": 200,
    "time": "2'10\"",
    "swolf": 42.0
  }
]
```

## 完整示例（Apple Watch 截图）

```json
{
  "date": "2026-01-01",
  "time_range": "18:43-20:09",
  "pool_length": 50,
  "total_distance": 2500,
  "laps": 50,
  "strokes": {
    "kickboard": {"distance": 500},
    "breaststroke": {"distance": 500},
    "freestyle": {"distance": 1500}
  },
  "duration": "1:25:22",
  "duration_seconds": 5122,
  "avg_pace": "3:24/100m",
  "avg_pace_seconds": 204,
  "avg_heart_rate": 148,
  "active_calories": 607,
  "total_calories": 739,
  "effort_score": 6,
  "effort_level": "适中"
}
```
