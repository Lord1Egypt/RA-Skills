# State Format

Default path:

```text
~/.openclaw/workspace/state/github-release-analyzer/{stateKey}.json
```

Schema:

```json
{
  "repo": "openclaw/openclaw",
  "processed_tags": [],
  "latest_processed_release_id": null,
  "latest_processed_published_at": null,
  "last_checked_at": null,
  "last_success_at": null,
  "initialized_at": null
}
```

Rules:

- derive `stateKey` from normalized repo unless explicitly overridden
- missing file or empty `initialized_at` means first run
- first cron run summarizes the latest formal release only
- `prepare` updates `last_checked_at`
- `commit` updates processed tags and latest processed metadata only after successful delivery
- failed fetch, summarize, render, or delivery must not mark releases as processed
