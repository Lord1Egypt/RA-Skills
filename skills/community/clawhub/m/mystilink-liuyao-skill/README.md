# Mystilink Liu Yao Skill

> Languages: [English](README.md) | [简体中文](docs/i18n/README.zh-CN.md) | [繁體中文](docs/i18n/README.zh-TW.md) | [日本語](docs/i18n/README.ja.md) | [한국어](docs/i18n/README.ko.md) | [Français](docs/i18n/README.fr.md) | [Español](docs/i18n/README.es.md)

## Overview

Agent Skill for Liu Yao (six-line casting): form hexagrams from six casts with an embedded Node script, then interpret with method pages and Zhouyi chapters from Wiki. One matter, one cast. Do not invent classic quotations.

## Delivery type

**Agent Skill** package. Does **not** implement the calculator language matrix. Casting logic is embedded in `scripts/` only (no separate Liu Yao calculator repository).

## Requirements

- Node.js 18+
- Agent Skills–compatible host
- Network recommended for Wiki method pages and classics

## Install

Folder name must be `mystilink-liuyao`:

```bash
cp -R mystilink-liuyao-skill /path/to/.cursor/skills/mystilink-liuyao
```

| Host | Path |
|------|------|
| Cursor | `.cursor/skills/mystilink-liuyao/` |
| Claude Code | `.claude/skills/mystilink-liuyao/` |

## Quick start

```bash
node scripts/cast.mjs --seed 42
# or fixed throws: node scripts/cast.mjs --throws "3,2,3,3,2,3"
```

Stdout JSON: six lines (bottom→top), moving flags, hexagram keys when available. Coin model follows script help (heads=3, tails=2 sums).

## Workflow

1. One clear matter (`examples/cast-request.json`); refuse multi-topic shotgun casting
2. Cast via script or accept user-provided throws
3. Read via Wiki, for example:

```text
GET https://wiki.mystilink.com/api/v1/pages/liuyao.method.six-casts?locale=en
GET https://wiki.mystilink.com/api/v1/pages/liuyao.rule.ben-zhi-bian?locale=en
GET https://wiki.mystilink.com/api/v1/pages/shared.work.yijing.gua.01-qian?locale=zh-Hans
```

4. Prefer Wiki references / cites for Zhouyi passages

Details: `SKILL.md`. Orientation: `references/overview.md`.

## Examples

- `examples/cast-request.json` — sample cast request

## Limits

- Classics often fall back to `zh-Hans` when other locales lack text
- Embedded cast helper mirrors product coin→line semantics in simplified form
- Wiki locale omit → `en`

## License

MIT. See [LICENSE](LICENSE).

## Feedback

Include seed/throws and stdout JSON (fictional matters only).
