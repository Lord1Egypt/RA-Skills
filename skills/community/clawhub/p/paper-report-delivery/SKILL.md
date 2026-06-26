---
name: paper-report-delivery
description: Build, automate, or maintain a daily paper-report delivery pipeline that collects papers, selects A/B groups, generates Chinese summaries and detailed innovation analysis, produces readable HTML with embedded images, prepares Telegram message chunks, archives outputs, and delivers reports to Telegram with retry and HTML-then-fallback behavior. Use when asked to create or improve a paper/news digest workflow, daily report automation, Telegram delivery pipeline, readable HTML report generation, or fallback delivery logic for unstable Telegram document sending.
---

# Paper Report Delivery

Use this skill to implement or maintain an end-to-end daily paper report workflow.

## Do this

1. Read `references/workflow.md` first.
2. Keep the pipeline end-to-end: collection, selection, readable output, archive, delivery.
3. Prefer Telegram-only proxying via `channels.telegram.proxy` when Telegram API needs Clash.
4. Treat Telegram message delivery and Telegram document delivery as separate reliability paths.
5. Prefer this delivery order:
   - split HTML delivery
   - retry for a bounded window
   - Telegram message chunk fallback
6. Keep local artifacts even when remote delivery fails.

## Reusable scripts

Use these bundled scripts when they fit:

- `scripts/build_readable_html.py`
  - Build a readable single-file HTML report with embedded images.
- `scripts/build_telegram_messages.py`
  - Convert a readable report JSON into Telegram-sized message chunks.
- `scripts/send_telegram_retry.sh`
  - Retry Telegram sending for unstable transport.
- `scripts/send_html_then_fallback.py`
  - Try split HTML for up to 30 minutes, then fall back to Telegram message chunks.

## Implementation rules

- Keep HTML as the best-reading artifact.
- Keep Telegram message chunks as the most reliable delivery artifact.
- Archive HTML, PDF, and markdown even when only Telegram text is delivered.
- Do not assume Telegram document delivery is stable.
- If Telegram is unreachable, finish artifact generation and leave cached delivery files behind.

## When editing an existing repo

- Integrate into the repo’s main pipeline entrypoint instead of creating a disconnected side script.
- Add flags for skipping fetch, skipping send, and archive-only mode.
- Keep delivery logic explicit and observable in logs.
- If Telegram transport is flaky, add retries before changing report content.

## Publishing hygiene

Before public release:

- Remove hard-coded local paths
- Remove hard-coded Telegram targets and group names
- Replace fixed dates with dynamic `YYYY-MM-DD` handling
- Keep transport settings configurable

## Packaging

After the skill is complete, package it with the local `package_skill.py` helper from the OpenClaw `skill-creator` skill.
