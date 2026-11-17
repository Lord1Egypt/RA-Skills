# Mystilink Router Skill

> Languages: [English](README.md) | [简体中文](docs/i18n/README.zh-CN.md) | [繁體中文](docs/i18n/README.zh-TW.md) | [日本語](docs/i18n/README.ja.md) | [한국어](docs/i18n/README.ko.md) | [Français](docs/i18n/README.fr.md) | [Español](docs/i18n/README.es.md)

## Overview

Agent Skill that picks one Mystilink metaphysics skill (BaZi, Zi Wei, tarot, Liu Yao, or western horoscope) when the user has not named a system, asks which method fits, or mixes several traditions. It does not compute charts or draws.

## Delivery type

This repository is an **Agent Skill** package (`SKILL.md` + references + examples). It does **not** implement the C / C++ / C# / Java / JavaScript / Python language matrix used by calculator libraries.

## Requirements

- An Agent Skills–compatible host (Cursor, Claude Code, OpenClaw, Hermes, or equivalent)
- The target theory skills installed when you intend to hand off after routing

## Install

Clone or copy this repository into the host skills directory as `mystilink-router` (folder name must match the skill `name` in `SKILL.md`):

| Host | Path |
|------|------|
| Cursor | `.cursor/skills/mystilink-router/` or `~/.cursor/skills/mystilink-router/` |
| Claude Code | `.claude/skills/mystilink-router/` or `~/.claude/skills/mystilink-router/` |

```bash
cp -R mystilink-router-skill /path/to/.cursor/skills/mystilink-router
```

## Usage

Follow `SKILL.md`. Routing heuristics:

| Need | Skill |
|------|--------|
| Birth date/time → long-term structure, ten gods | `mystilink-bazi` |
| Birth → twelve palaces / Zi Wei stars | `mystilink-ziwei` |
| Birth place + time → planets/houses/aspects | `mystilink-horoscope` |
| One concrete question, symbolic cards | `mystilink-tarot` |
| One concrete question, hexagram / moving lines | `mystilink-liuyao` |

Optional Wiki aid (network):

```text
GET https://wiki.mystilink.com/api/v1/pages/shared.concept.choosing-a-system?locale=en
```

After choosing, load that skill’s `SKILL.md` and continue there. Prefer one primary system per request.

## Examples

See `examples/routing-cases.md` for sample user intents and expected targets.

## Limits

- No calculation scripts in this skill
- Does not run multiple systems “just in case”
- Wiki calls are optional; omit `locale`/`lang` → `en`; missing translations may fall back to `zh-Hans`

## License

MIT. See [LICENSE](LICENSE).

## Feedback

Report defects with the user intent text (fictional only) and which skill was selected or missed.
