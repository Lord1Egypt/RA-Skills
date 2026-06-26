# inbox-to-action-closer

Orchestration skill that processes raw work-item data from Slack, GitHub, calendar, Notion, Trello, and email — supplied by the caller or other OpenClaw tools — into a single merged, prioritised action board. Does not connect to external APIs directly; it normalises, deduplicates, scores, and renders data provided to it. See `SKILL.md` for full specification.

Built with [Saturnday](https://saturnday.com) governance.

```
npm install
npm run build
```

## Trade-offs

- **Draft-only by default**: Every write action requires explicit user confirmation — safety over speed.
- **Conservative deduplication**: Prefers showing near-duplicates over accidentally merging distinct items.
- **Source-level fault tolerance**: A failing source is skipped, not fatal. The board may be incomplete.

## Limitations

- Point-in-time snapshot, no streaming.
- Heuristic urgency scoring; edge cases may rank unexpectedly.
- Surface-level dedup (titles, URLs, timestamps) — no semantic matching.

## Non-goals

- Auto-sending replies or write-backs without confirmation.
- Replacing dedicated project management tools.
- ML-based classification.
- API connectors or credential management — bring your own data or use upstream tools.

## License

MIT. See [LICENSE](LICENSE).
