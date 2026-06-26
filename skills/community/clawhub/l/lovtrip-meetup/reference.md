# 聚会规划工具参数参考

## amap_calculate_midpoint

```json
{
  "members": [
    { "name": "Alice", "location": "北京市海淀区中关村" },
    { "name": "Bob", "location": "116.461,39.909" }
  ],
  "city": "北京"
}
```

`location` 支持地址字符串或 `lng,lat` 坐标格式。

## amap_find_optimal_venue

```json
{
  "members": [
    { "name": "Alice", "location": "中关村" },
    { "name": "Bob", "location": "国贸" }
  ],
  "activity_type": "咖啡馆",
  "preferences": {
    "max_radius": 5000,
    "min_rating": 3.5,
    "sort_by": "balanced",
    "budget": { "min_price": 30, "max_price": 100 }
  },
  "city": "北京"
}
```

`sort_by` 选项:
- `balanced`（默认）: 综合距离、评分、公平性
- `distance`: 距离优先
- `rating`: 评分优先

## parse_schedule

```json
{
  "text": "周六下午3点到6点",
  "reference_date": "2026-03-08"
}
```

支持的时间表达式:
- "周六下午"、"明天3点后"、"周末全天"
- "下周一上午"、"后天晚上8点"
- "这个周末"、"下个月15号"

## match_interests

```json
{
  "members": [
    { "name": "Alice", "interests": ["咖啡", "桌游", "电影"] },
    { "name": "Bob", "interests": ["桌游", "密室逃脱", "电影"] },
    { "name": "Carol", "interests": ["咖啡", "逛街", "电影"] }
  ]
}
```

返回共同兴趣和推荐活动类型。

## suggest_time_slots

```json
{
  "venue_business_hours": "09:00-22:00",
  "date": "2026-03-08",
  "duration_minutes": 120,
  "member_count": 4,
  "avoid_peak_hours": true
}
```

高峰期定义: 11:30-13:30（午餐）、17:30-19:30（晚餐）。

## generate_plan

```json
{
  "time_slot": {
    "start": "2026-03-08T14:00:00",
    "end": "2026-03-08T18:00:00"
  },
  "venue": {
    "name": "星巴克中关村店",
    "address": "北京市海淀区中关村大街1号",
    "location": { "lng": 116.32, "lat": 39.98 },
    "avg_duration_minutes": 25
  },
  "activities": ["咖啡", "桌游"],
  "members": ["Alice", "Bob"]
}
```

## export_calendar

```json
{
  "title": "周六咖啡聚会",
  "start_time": "2026-03-08T14:00:00+08:00",
  "end_time": "2026-03-08T18:00:00+08:00",
  "location": "星巴克中关村店, 北京市海淀区中关村大街1号",
  "description": "和 Alice、Bob 一起喝咖啡、玩桌游",
  "attendees": ["Alice", "Bob"]
}
```

输出标准 iCal (.ics) 格式，可导入 Apple Calendar、Google Calendar 等。

## generate_backup_plans

```json
{
  "primary_plan": {
    "venue_name": "星巴克中关村店",
    "venue_location": { "lng": 116.32, "lat": 39.98 },
    "activity_type": "咖啡馆",
    "time_slot": { "start": "2026-03-08T14:00:00", "end": "2026-03-08T18:00:00" }
  },
  "reason": "weather",
  "city": "北京"
}
```

`reason` 选项: `weather`（天气恶劣）、`traffic`（交通拥堵）、`full`（客满）、`general`（一般）。

## check_weather

```json
{
  "location": { "lng": 116.32, "lat": 39.98 },
  "city": "北京",
  "date": "2026-03-08"
}
```

## check_traffic

```json
{
  "location": { "lng": 116.32, "lat": 39.98 },
  "city": "北京",
  "radius": 1000
}
```
