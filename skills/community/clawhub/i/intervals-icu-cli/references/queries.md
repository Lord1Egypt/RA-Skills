# Query Guidance

## Search vs List

- Use `activities search` for text or tag queries such as `tempo` or `#threshold`.
- Use `activities list` when the user asks for semantic filters that may not appear in the activity name.

Examples where `list` is better:
- weekend long runs
- hard sessions from the current block
- rides on a known route

## Examples

Text/tag search:

```bash
intervals activities search --query "#threshold" --oldest 2026-03-01 --newest 2026-03-12 --format json
intervals activities search --query "tempo" --oldest 2026-03-01 --format json
```

Structured list:

```bash
intervals activities list --oldest 2026-03-01 --newest 2026-03-12 --format json
```

Then filter locally on fields like:
- `type`
- `start_date_local`
- `distance`
- `moving_time`
- `tags`

## Other Common Reads

```bash
intervals whoami --format json
intervals athlete get --format json
intervals athlete training-plan --format json
intervals events list --oldest 2026-03-10 --newest 2026-03-16 --format json
intervals workouts list --format json
intervals wellness list --oldest 2026-03-01 --newest 2026-03-12 --format json
```
