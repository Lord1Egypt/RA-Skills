# Data Schema

Default storage root: `~/.pet-companion/`

## Directory layout

```text
~/.pet-companion/
├── pets/
├── records/
├── reminders/
├── media/
└── reports/
```

## Pet profile JSON

One file per pet in `pets/<pet_id>.json`.

Required fields:
- `pet_id`
- `name`
- `species`
- `created_at`
- `updated_at`

Common optional fields:
- `nickname`
- `breed`
- `gender`
- `birthday`
- `adoption_date`
- `neutered`
- `color_markings`
- `personality_tags`
- `notes`
- `avatar_media`

Example:

```json
{
  "pet_id": "kele",
  "name": "可乐",
  "nickname": ["可可"],
  "species": "cat",
  "breed": "英短蓝猫",
  "gender": "male",
  "birthday": "2023-05-12",
  "adoption_date": "2023-07-01",
  "neutered": true,
  "color_markings": "蓝灰色",
  "personality_tags": ["粘人", "贪吃"],
  "notes": "对鸡肉冻干敏感",
  "avatar_media": "media/2026/03/kele-avatar.jpg",
  "created_at": "2026-03-15T09:00:00+08:00",
  "updated_at": "2026-03-15T09:00:00+08:00"
}
```

## Record markdown files

Store records under `records/YYYY/MM/` using Markdown with JSON frontmatter.

Supported `type` values:
- `daily`
- `moment`
- `photo`
- `feeding`
- `health`
- `reminder-note`

Frontmatter fields:
- `record_id`
- `pet_id`
- `type`
- `title`
- `created_at`
- `tags`
- `media`
- `extra`

Example:

```markdown
---
{"record_id":"rec_123","pet_id":"kele","type":"daily","title":"第一次学会握手","created_at":"2026-03-15T09:10:00+08:00","tags":["训练","成长"],"media":[],"extra":{"mood":"开心"}}
---

今天训练了 5 分钟，终于会主动抬爪了。
```

## Reminders JSON

Store per-pet reminders in `reminders/<pet_id>.json`.

```json
{
  "pet_id": "kele",
  "reminders": [
    {
      "reminder_id": "rem_001",
      "title": "体内驱虫",
      "reminder_type": "deworming",
      "due_at": "2026-04-01T09:00:00+08:00",
      "recurrence": {"type": "monthly", "interval": 3},
      "status": "active",
      "notes": "按季度驱虫",
      "created_at": "2026-03-15T09:00:00+08:00"
    }
  ]
}
```

## Media files

Store photo and attachment files in `media/YYYY/MM/`. Reference them with relative paths from the storage root.
