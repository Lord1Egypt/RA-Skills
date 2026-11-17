# Mystilink Tarot Skill

> Languages: [English](README.md) | [简体中文](docs/i18n/README.zh-CN.md) | [繁體中文](docs/i18n/README.zh-TW.md) | [日本語](docs/i18n/README.ja.md) | [한국어](docs/i18n/README.ko.md) | [Français](docs/i18n/README.fr.md) | [Español](docs/i18n/README.es.md)

## Overview

Agent Skill for tarot: draw upright/reversed cards for a spread with an embedded Node script, then interpret using card theory pages. Prefer a real draw (script or user-provided cards); do not invent draws silently.

## Delivery type

**Agent Skill** package. Does **not** implement the calculator language matrix. Draw/validate logic is embedded in `scripts/` only (no separate tarot calculator repository).

## Requirements

- Node.js 18+
- Agent Skills–compatible host
- Network optional for Wiki API

## Install

Folder name must be `mystilink-tarot`:

```bash
cp -R mystilink-tarot-skill /path/to/.cursor/skills/mystilink-tarot
```

| Host | Path |
|------|------|
| Cursor | `.cursor/skills/mystilink-tarot/` |
| Claude Code | `.claude/skills/mystilink-tarot/` |

## Quick start

```bash
node scripts/draw.mjs --spread three-card --seed 42
# or: echo '{"spread":"three-card","seed":42}' | node scripts/draw.mjs
```

Stdout JSON: cards with `id`, `name`, `orientation` (`upright`|`reversed`), positions. Card `id` values align with Wiki `tarot.card.*` pages.

## Workflow

1. Clarify question and spread (default: three-card); see `examples/draw-request.json`
2. Draw via script or accept user-provided cards
3. For each card, optional Wiki:

```text
GET https://wiki.mystilink.com/api/v1/search?q=The+Fool&system=tarot&locale=en
GET https://wiki.mystilink.com/api/v1/pages/<card.id>?locale=en
```

4. Tie each position to the question; cite Wiki when used

Details: `SKILL.md`. Draw method notes: `references/method-draw.md`.

## Examples

- `examples/draw-request.json` — sample draw request

## Limits

- Do not claim medical or legal certainty
- Prefer one clear question per draw
- Wiki locale omit → `en`

## License

MIT. See [LICENSE](LICENSE).

## Feedback

Include spread flags/seed (or stdin JSON) and stdout JSON (fictional questions only).
