# Env Vars

Primary token:

- `OPENCLAW_NOTION_TOKEN`

Preferred local file:

- `/Users/dellymac/.openclaw/secrets/notion.env`

Database aliases used by `notion_api.mjs`:

- `research` -> `OPENCLAW_NOTION_DB_RESEARCH_SIGNALS`
- `ideas` -> `OPENCLAW_NOTION_DB_PROJECT_IDEAS`
- `projects` -> `OPENCLAW_NOTION_DB_PROJECTS`
- `runs` -> `OPENCLAW_NOTION_DB_NIGHTLY_RUNS`

Suggested record fields:

- `telegram_message_id`
- `approval_state`
- `project_session_key`
- `run_status`
- `retry_count`
- `duplicate_of`
