# data-schema.md - 经期数据格式说明

## 存储路径

```
~/.openclaw/workspace/period_tracker/data.json
```

## 顶层结构

```json
{
  "version": "1.0",
  "periods": [...],
  "settings": {...}
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| version | string | 数据格式版本，当前 "1.0" |
| periods | array | 经期记录列表，按 start_date 升序排列 |
| settings | object | 统计缓存与用户设置 |

## periods 记录结构

```json
{
  "id": 1710000000000,
  "start_date": "2024-01-15",
  "end_date": "2024-01-20",
  "duration": 6,
  "symptoms": {
    "pain_level": 3,
    "mood": "烦躁",
    "flow": "中",
    "tags": ["头痛", "腰痛"]
  },
  "notes": "这次比较规律",
  "created_at": "2024-01-15T10:00:00"
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| id | number | Unix ms 时间戳，唯一标识 |
| start_date | string | 开始日期 YYYY-MM-DD |
| end_date | string/null | 结束日期，null 表示进行中 |
| duration | number/null | 经期天数（含首尾） |
| symptoms.pain_level | number/null | 痛经程度 1（轻）~5（重） |
| symptoms.mood | string/null | 情绪：开心/平静/烦躁/低落/焦虑 |
| symptoms.flow | string/null | 经血量：少/中/多 |
| symptoms.tags | array | 症状标签，如 ["头痛","腰痛","痘痘","浮肿","失眠","乳胀"] |
| notes | string | 自由备注 |
| created_at | string | 创建时间 ISO 8601 |

## settings 结构

```json
{
  "avg_cycle": 28.5,
  "avg_duration": 5.2
}
```

| 字段 | 说明 |
|------|------|
| avg_cycle | 平均周期（天），由脚本自动计算更新 |
| avg_duration | 平均经期长度（天），自动计算更新 |

## 扩展说明

- `symptoms.tags` 为可扩展数组，可自由增加标签类型
- 未来可扩展字段：`temperature`（基础体温）、`weight`、`cervical_mucus`（宫颈黏液）等
- `version` 字段用于未来数据迁移
