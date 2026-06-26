# Optional CLI Patterns

Use this file only when a `notion` binary is already installed and working.

## When the CLI Helps

- Fast workspace search
- Quick page reads by ID
- Simple page creation or property updates in older single-source databases

## Known Limitation

The community CLI documented here targets Notion API version `2022-06-28`. Newer `2025-09-03` data source workflows may require direct HTTP requests even when the CLI is installed.

## Example Commands

```bash
notion users me
notion search "content calendar" --filter database
notion databases get DATABASE_ID
notion databases query DATABASE_ID --filter '{"property":"Status","select":{"equals":"Scheduled"}}'
notion pages create --parent DATABASE_ID --title "Launch review"
notion pages update PAGE_ID --properties '{"Status":{"select":{"name":"Done"}}}'
```

## Decision Rule

- Use CLI for read-heavy or simple CRUD tasks when the database model is stable.
- Switch to direct `api.notion.com` requests when the task depends on `data_source_id`, modern schema changes, or precise version control.
