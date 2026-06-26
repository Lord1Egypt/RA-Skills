# Matter CLI — Full Command Reference

CLI binary: `matter` (install via GitHub releases — see SKILL.md setup instructions)

## account
```
matter account [--plain]
```
Returns account info: id, name, email, rate limits.

## items list
```
matter items list [options]
  --status <status>        inbox | queue | archive | all
  --tag <tag_id>           Filter by tag ID
  --content-type <type>    article | podcast | video | pdf | tweet | newsletter
  --favorite               Only favorites
  --order <order>          updated | library_position | inbox_position
  --updated-since <date>   ISO 8601 date
  --limit <n>              Max per page
  --cursor <cursor>        Pagination cursor
  --all                    Fetch all pages
  --plain                  Human-readable output
```
**Order notes:**
- Queue/reading list: `--status queue --order library_position`
- Inbox feed: `--status inbox --order inbox_position`
- Finished: `--status archive --order library_position`
- Sync only: `--order updated`

## items get
```
matter items get <id> [--include markdown] [--plain]
```
`--include markdown` fetches full article text. Use for summaries/analysis.

## items save
```
matter items save --url <url> [--status queue|archive] [--plain]
```

## items update
```
matter items update <id> [--status <status>] [--favorite true|false] [--progress 0.0-1.0] [--plain]
```

## items delete
```
matter items delete <id>
```

## annotations list
```
matter annotations list [--item <item_id>] [--all] [--limit <n>] [--cursor <cursor>] [--plain]
```
Returns highlights and notes for an item.

## annotations get
```
matter annotations get <id> [--plain]
```

## annotations update
```
matter annotations update <id> [--plain]
```

## annotations delete
```
matter annotations delete <id>
```

## tags list
```
matter tags list [--plain]
```
Returns all tags with id, name, item_count.

## tags add
```
matter tags add --item <item_id> --name <tag_name> [--plain]
```
Creates tag if it doesn't exist; reuses if name matches.

## tags remove
```
matter tags remove --item <item_id> [--plain]
```

## tags rename
```
matter tags rename <id> [--plain]
```

## tags delete
```
matter tags delete <id>
```

## search
```
matter search "<query>" --type items [--status queue|archive] [--limit <n>] [--all] [--plain]
```
Full-text search. `--type items` is required.

## reading-sessions
```
matter reading-sessions [--plain]
```
Lists reading sessions (time spent per item).

## Rate Limits (from account)
- Read: 120 req/min
- Write: 30 req/min
- Save: 10 req/min
- Markdown: 20 req/min
- Search: 30 req/min
- Burst: 5 req/min
