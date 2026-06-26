# openclaw-mindkeeper

**Mindkeeper turns a day of memory into clarity.**

Mindkeeper is a small OpenClaw-oriented product scaffold that reads a day's memory inputs, extracts what mattered, and produces a structured brief with recommendations.

## MVP status

This repository currently implements a local, testable MVP pipeline:

- read a daily memory markdown file
- read one day's raw messages from the lossless-claw SQLite database
- normalize memory lines into signal candidates
- extract highlights, decisions, open loops, and recommendations
- render a text or HTML brief
- run locally from the CLI

LCM / lossless-claw integration currently uses a read-only SQLite adapter with day-window filtering. That gives us a real source boundary now, while still leaving room for future recall-tool orchestration.

## Quick start

```bash
npm test
node src/index.js --date 2026-04-09 --memory-file ./tests/fixtures/2026-04-09.md --format text
node src/index.js --date 2026-04-09 --memory-file ./tests/fixtures/2026-04-09.md --format html --out ./tmp/mindkeeper-preview.html
node src/index.js --date 2026-04-09 --use-lcm --lcm-db ~/.openclaw/lcm.db --session-key agent:main:main --format text
node src/index.js --date 2026-04-09 --brief-mode hybrid --memory-file ./tests/fixtures/2026-04-09.md --use-lcm --lcm-db ~/.openclaw/lcm.db --session-key agent:main:main --format text
node src/index.js --date 2026-04-09 --brief-mode lossless-only --use-lcm --lcm-db ~/.openclaw/lcm.db --session-key agent:main:main --format text
node src/index.js --date 2026-04-09 --memory-file ./tests/fixtures/2026-04-09.md --prompt "Focus on lossless-claw and openclaw-mindkeeper naming" --email-to alex@example.com --email-from mindkeeper@example.com --email-out ./tmp/mindkeeper.eml
node src/index.js --date 2026-04-09 --memory-file ./tests/fixtures/2026-04-09.md --prompt "Focus on lossless-claw and openclaw-mindkeeper naming" --email-mode nexlink --email-to alex@example.com --nexlink-cli ~/.openclaw/skills/nexlink/scripts/nexlink.py
npm run validate
```

## Planned next step

- improve ranking so hybrid and lossless-only briefs stay concise on heavy days
- add delivery presets and safer recipient/config management for live NexLink sends
- add cron wiring for daily comparison sends

---

Built by [Firma de AI](https://firmade.ai), supported by [Firma de IT](https://firmade.it)
