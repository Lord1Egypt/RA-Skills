# Paper Report Delivery Workflow

## Goal

Automate a daily paper report pipeline that:

1. Collects candidate papers for two groups
2. Selects 5 papers per group
3. Generates Chinese report content
4. Builds a readable single-file HTML report with embedded images
5. Generates Telegram message chunks for direct reading
6. Archives all outputs locally
7. Delivers to Telegram with a robust fallback strategy

## Current delivery strategy

Preferred order:

1. Try split HTML delivery first (`part1` for group A, `part2` for group B)
2. Retry HTML delivery for up to 30 minutes
3. If HTML delivery does not fully succeed, fall back to Telegram message chunks

All delivery targets should be treated as configurable inputs rather than hard-coded chat ids.

## Key artifacts

- Readable HTML: `output/readable/paper_report_readable_YYYY-MM-DD.html`
- Split HTML: `output/readable/paper_report_readable_YYYY-MM-DD.part1.html`, `part2.html`
- Telegram message cache: `output/telegram/telegram_messages_YYYY-MM-DD.json`
- Chinese markdown: `output/cn/paper_report_cn_YYYY-MM-DD.md`
- PDF archive: `output/cn/paper_report_cn_YYYY-MM-DD.pdf`

## Telegram transport notes

- Telegram document sending may be unstable even when plain text sending works.
- Use a retry wrapper for every Telegram send attempt.
- Prefer a Telegram-only proxy rather than global OpenClaw proxying.
- In OpenClaw config, use `channels.telegram.proxy` for Clash-style proxy routing.

## Recommended integration points

- Main pipeline orchestrator: a `run_pipeline.js`-style script
- Report text formatter: a `build_telegram_messages.py`-style script
- Readable HTML generator: a `build_readable_html.py`-style script
- Robust Telegram transport: a retry shell wrapper plus HTML-then-fallback script
