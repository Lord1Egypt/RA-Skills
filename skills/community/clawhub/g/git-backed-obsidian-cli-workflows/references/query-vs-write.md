# Query vs write

## Read/query operations

These inspect the vault and should not trigger Git sync.

Examples:
- `search`
- `read`
- `daily:read`
- `links`
- `outline`
- `tags`
- `tasks`
- `vault`

## Write/update operations

These change note contents and should trigger Git sync after success.

Examples:
- `daily:append`
- `create`
- lightweight note append/create workflows
- memo/inbox capture

## Rule

Only sync after successful writes. Never sync after pure queries.
