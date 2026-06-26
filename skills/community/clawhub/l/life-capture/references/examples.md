# Example payloads and commands

## One-command end-to-end write

```bash
python scripts/process_entry.py --root life --db life/db/life.db --today 2026-03-10 --text "今天中午吃牛肉面花了 26 元，明天下午两点去体检，想到可以做一个生活数据看板"
```

## Parse only

```bash
python scripts/parse_entries.py --text "买咖啡 18 元，改完合同，明天下午两点去体检"
```

## Single expense payload

```json
{
  "records": [
    {
      "id": "exp_20260310_001",
      "type": "expense",
      "date": "2026-03-10",
      "time": "12:30",
      "raw_text": "今天中午吃牛肉面花了 26 元",
      "summary": "午饭，消费 26 元",
      "tags": ["开销", "饮食", "午饭"],
      "payload": {
        "amount": 26,
        "currency": "CNY",
        "category": "饮食",
        "subcategory": "午饭"
      }
    }
  ]
}
```

## Mixed input split into multiple records

```json
{
  "records": [
    {
      "id": "exp_20260310_001",
      "type": "expense",
      "date": "2026-03-10",
      "time": null,
      "raw_text": "买咖啡 18 元",
      "summary": "咖啡，消费 18 元",
      "tags": ["开销", "饮食", "咖啡"],
      "payload": {
        "amount": 18,
        "currency": "CNY",
        "category": "饮食",
        "subcategory": "咖啡"
      }
    },
    {
      "id": "task_20260310_001",
      "type": "task",
      "date": "2026-03-10",
      "time": null,
      "raw_text": "改完合同",
      "summary": "改完合同",
      "tags": ["任务", "完成", "文档"],
      "payload": {
        "status": "done",
        "priority": "normal",
        "project": "文档",
        "due_date": null,
        "completed_at": "2026-03-10T10:00:00"
      }
    },
    {
      "id": "sched_20260311_001",
      "type": "schedule",
      "date": "2026-03-11",
      "time": "14:00",
      "raw_text": "明天下午两点去体检",
      "summary": "明天下午两点去体检",
      "tags": ["日程", "健康"],
      "payload": {
        "schedule_date": "2026-03-11",
        "start_time": "14:00",
        "end_time": null,
        "location": "体检",
        "status": "planned"
      }
    }
  ]
}
```


## Parse with custom config

```bash
python scripts/parse_entries.py --config references/parser_config.json --text "买咖啡 18 元，整理了书桌，想到做周复盘模板"
```


## Stable relative dates

```bash
python scripts/parse_entries.py --today 2026-03-10 --text "明天下午两点去体检"
```
