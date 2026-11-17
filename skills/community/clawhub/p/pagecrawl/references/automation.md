# Automating with PageCrawl

## Contents
- Webhooks
- Scheduled reports
- Polling for new changes
- Push data sources
- No-code tools

## Webhooks

A webhook makes PageCrawl POST a JSON payload to another system when a monitor changes. Use it for agents, internal tools and automations that should react on their own.

1. `manage-webhooks(action="list")` first, to see what already exists.
2. `manage-webhooks(action="create", target_url="https://example.com/hooks/pagecrawl", match_type="tags", tag_ids=[...], events=["change_detected"])`.
   - `target_url` must be HTTPS. Slack, Discord and Microsoft Teams URLs are rejected: use `notifications` on the monitor for those.
   - `match_type` is `all`, `monitors`, `tags`, `folders` or `domains`, with `monitor_ids`, `tag_ids`, `folder_ids` or `domains` to match. It defaults to `all`.
   - `events` is `change_detected` and/or `error`.
   - `payload_fields` trims the payload to the fields the receiver needs.
3. `manage-webhooks(action="test", hook_id=...)` sends one real delivery using the latest check. Confirm before running it.
4. `manage-webhooks(action="logs", hook_id=...)` shows recent deliveries with status codes, for a webhook that is not arriving.

Every delivery is signed. The signing secret is never returned through these tools: the user copies it from the webhook in the PageCrawl app (https://pagecrawl.io/app/settings/webhooks) into the receiver's configuration. Code that verifies the signature is covered by the `pagecrawl-api` skill and by https://pagecrawl.io/help/tutorials/article/reference-implementations.

## Scheduled reports

A report sends a digest of what changed across a set of monitors on a schedule.

- `manage-reports(action="create", name="Weekly competitor digest", match_type="tags", tag_ids=[...], schedule="weekly", schedule_hour=8, channels=["email"], recipient_user_ids=[...], filter_mode="important", ai_summary=true)`.
  - `match_type` is `all`, `monitors`, `tags`, `folders` or `domains`.
  - `schedule` is `daily`, `daily_except_weekends`, `daily_weekends`, `weekly`, `monthly` (with `schedule_day`) or `none` for on-demand only.
  - `channels` are `email`, `slack`, `discord`, `teams`, `telegram`, `webpush`. Email needs `recipient_user_ids`. With no channels, digests are kept in the app only.
  - `filter_mode="important"` keeps changes at or above `important_threshold`.
- `manage-reports(action="list")` returns reports with their `slug`, which the other actions use.
- `manage-reports(action="generate", slug="...", period_start="...", period_end="...")` builds a digest now and delivers it to the report's channels when there is content. Confirm first.
- `manage-reports(action="digests", slug="...")` reads digests already produced.
- Creating and editing reports needs the team owner or manager role.

Help: https://pagecrawl.io/help/notifications/article/scheduled-reports

## Polling for new changes

When an automation must pull rather than receive, use the cursor:

1. `get-changes-since(since="24 hours ago")` once, and store `next_cursor`.
2. Then `get-changes-since(after_check_id=<stored next_cursor>)` on each run, storing the new `next_cursor` each time. It is returned even when nothing changed.

Never advance `since` by hand between runs; the cursor cannot miss or repeat a change.

## Push data sources

When a value cannot be crawled (an internal metric, a partner API response, a number from a spreadsheet), create a data source and push values to it. Pushed values get the same history, charts, alerts and AI summaries as any monitor.

1. `create-data-source(name="Warehouse stock", fields=[{"label": "units", "type": "number"}], ai_prompt="Flag drops below 100 units")`. Field types are `number`, `price` and `text`. Without `fields`, a single field is created on the first value.
2. `record-data(monitor_id="...", value="128")`, or several fields at once with `record-data(monitor_id="...", values={"units": "128", "status": "ok"})`. Unknown field names are created automatically.
3. Recording the same value again returns `changed=false` and adds nothing to the history.

- Set `ai_summaries_enabled=false` for frequent numeric metrics that only need charts and thresholds.
- The response includes a private `ingest_url` (accepts a plain POST without a header) and an `ingest_email` address. Both act like passwords: give them to the user for their own systems and never publish them.
- `trigger-check` does not apply to data sources. Every read tool works on them like any monitor.

Help: https://pagecrawl.io/help/integrations/article/push-api-data-sources

## No-code tools

PageCrawl also connects to n8n, Zapier and Make:

- https://pagecrawl.io/help/integrations/article/pagecrawl-n8n-integration
- https://pagecrawl.io/help/integrations/article/pagecrawl-zapier-integration
- https://pagecrawl.io/help/integrations/article/pagecrawl-make-integration
