# 六道 Database Schema

The SQLite database is located at `/home/admin/.openclaw/workspace/liudao-bot/data/liudao.db`.

## Table: `persons`

This table stores all entity information (both public historical figures and private family members).

| Column Name       | Type      | Description                                                                 |
|-------------------|-----------|-----------------------------------------------------------------------------|
| `id`              | INTEGER   | Primary Key (Auto-increment)                                                |
| `name`            | TEXT      | Unique name of the person (e.g., "康熙", "李白")                            |
| `relation`        | TEXT      | Short description or title (e.g., "清圣祖", "朋友")                         |
| `linked_person`   | TEXT      | Legacy field for direct link (mostly unused now)                            |
| `relations_json`  | TEXT      | JSON string containing structured relationships.                            |
| `milestones_json` | TEXT      | JSON string containing life events `[{"date": "...", "title": "..."}]`      |
| `birth_date`      | TEXT      | Birth date (YYYY-MM-DD or general string)                                   |
| `death_date`      | TEXT      | Death date (YYYY-MM-DD or general string)                                   |
| `birth_hour`      | TEXT      | Birth time/hour (e.g., "辰时")                                              |
| `death_hour`      | TEXT      | Death time/hour                                                             |
| `gender`          | TEXT      | Gender ("男", "女")                                                         |
| `ethnicity`       | TEXT      | Ethnicity (e.g., "汉族", "满族")                                            |
| `blood_type`      | TEXT      | Blood type                                                                  |
| `zodiac`          | TEXT      | Zodiac sign                                                                 |
| `personality`     | TEXT      | Personality description                                                     |
| `calendar_type`   | TEXT      | Type of calendar used for dates ("农历", "公历")                            |
| `is_private`      | INTEGER   | Privacy flag: `0` = Public, `1` = Private                                   |
| `creator_id`      | TEXT      | The Telegram ID of the user who created/owns this private record            |
| `last_updated`    | TIMESTAMP | Auto-updated timestamp                                                      |

## JSON Structures

### `relations_json`
```json
{
  "父母": ["顺治帝 (父)", "孝康章皇后 (母)"],
  "子女": ["胤礽 (子)", "胤禛 (子)"]
}
```

### `milestones_json`
```json
[
  {
    "date": "1654-05-04",
    "title": "出生",
    "description": "生于紫禁城景仁宫"
  },
  {
    "date": "1661-02-05",
    "title": "即位",
    "description": "8岁登基"
  }
]
```