# State Format

Default paths:

```text
Hermes: $HERMES_HOME/state/github-release-analyzer/{stateKey}.json
OpenClaw legacy (when populated): ~/.openclaw/workspace/state/github-release-analyzer/{stateKey}.json
OpenClaw persistent: ~/.openclaw/state/github-release-analyzer/{stateKey}.json
```

`GITHUB_RELEASE_ANALYZER_STATE_ROOT` overrides the default root on either
platform. When `HERMES_HOME` is set, the Hermes path is used. Otherwise,
OpenClaw preserves its existing legacy-then-persistent fallback behavior.

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
