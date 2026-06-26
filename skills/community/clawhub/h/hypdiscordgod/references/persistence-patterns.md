# Persistence Patterns

Use this reference when the bot needs state that must survive restarts.

## Storage Selection

Choose based on scope:
- in-memory only for ephemeral/cache data
- JSON files only for tiny single-instance bots or prototypes
- SQLite for small to medium bots with simple persistence needs
- Postgres for multi-instance bots, dashboards, analytics, or heavier relational data

## What to Persist

Common Discord bot data:
- guild configuration
- ticket records
- moderation actions
- button/select/modal workflow state
- user preferences
- reminders/scheduled jobs

## Safe Rules

- Do not persist secrets in app data tables.
- Add unique constraints where duplicate records would be harmful.
- Add indexes for lookup-heavy fields such as `guild_id`, `user_id`, `channel_id`, `ticket_id`.
- Treat Discord snowflakes as strings in JavaScript/TypeScript.

## SQLite Good Fit

Use SQLite when:
- one bot instance is running
- the feature set is modest
- deploy simplicity matters

Good tables:
- `guild_settings`
- `tickets`
- `ticket_messages`
- `warnings`

## Postgres Good Fit

Use Postgres when:
- multiple workers or shards may exist
- external web apps share the data
- query complexity is increasing
- uptime and migration discipline matter

## Migration Guidance

Prefer a migration tool already used by the repo.
If no tool exists, keep schema creation explicit and versioned rather than hidden in ad hoc runtime logic.
