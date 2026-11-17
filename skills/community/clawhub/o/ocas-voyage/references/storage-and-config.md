# Storage Layout and Default Config

## Directory Structure

```
{agent_root}/commons/data/ocas-voyage/
  config.json
  state.json
  events.jsonl
  decisions.jsonl
  plans/

{agent_root}/commons/journals/ocas-voyage/
  YYYY-MM-DD/
    {run_id}.json
```

## Default config.json

```json
{
  "skill_id": "ocas-voyage",
  "skill_version": "2.3.0",
  "config_version": "1",
  "created_at": "",
  "updated_at": "",
  "defaults": {
    "diet": "vegetarian",
    "pace": "moderate",
    "auto_book": false
  },
  "retention": {
    "days": 0,
    "max_records": 10000
  }
}
```
