---
name: mindkeeper
description: Turn a day of memory into a clear owner brief with highlights, decisions, open loops, and next-step recommendations.
validation: scripts/validate.sh
---

# Mindkeeper

Mindkeeper is an OpenClaw-oriented skill/product scaffold for turning daily memory into clarity.

## Current MVP

- Reads daily memory from a markdown file
- Reads one day's messages from the lossless-claw SQLite DB
- Extracts structured signals
- Produces a text or HTML brief
- Can write rendered output to a file with `--out`
- Runs locally with a validation script

## Usage

```bash
node src/index.js --date 2026-04-09 --memory-file ./tests/fixtures/2026-04-09.md --format text
node src/index.js --date 2026-04-09 --memory-file ./tests/fixtures/2026-04-09.md --format html --out ./tmp/mindkeeper-preview.html
node src/index.js --date 2026-04-09 --use-lcm --lcm-db ~/.openclaw/lcm.db --session-key agent:main:main --format text
node src/index.js --date 2026-04-09 --brief-mode hybrid --memory-file ./tests/fixtures/2026-04-09.md --use-lcm --lcm-db ~/.openclaw/lcm.db --session-key agent:main:main --format text
node src/index.js --date 2026-04-09 --brief-mode lossless-only --use-lcm --lcm-db ~/.openclaw/lcm.db --session-key agent:main:main --format text
node src/index.js --date 2026-04-09 --memory-file ./tests/fixtures/2026-04-09.md --prompt "Focus on lossless-claw and openclaw-mindkeeper naming" --email-to alex@example.com --email-from mindkeeper@example.com --email-out ./tmp/mindkeeper.eml
node src/index.js --date 2026-04-09 --memory-file ./tests/fixtures/2026-04-09.md --prompt "Focus on lossless-claw and openclaw-mindkeeper naming" --email-mode nexlink --email-to alex@example.com --nexlink-cli ~/.openclaw/skills/nexlink/scripts/nexlink.py
```

## Validation

```bash
npm run validate
```

## Planned integrations

- richer lossless-claw recall beyond raw day-window SQLite reads
- ranking improvements so hybrid and lossless-only briefs stay concise on heavy days
- cron scheduling for daily comparison sends
