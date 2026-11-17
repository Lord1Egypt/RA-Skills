# Mystilink BaZi Skill

> Languages: [English](README.md) | [简体中文](docs/i18n/README.zh-CN.md) | [繁體中文](docs/i18n/README.zh-TW.md) | [日本語](docs/i18n/README.ja.md) | [한국어](docs/i18n/README.ko.md) | [Français](docs/i18n/README.fr.md) | [Español](docs/i18n/README.es.md)

## Overview

Agent Skill for BaZi (Four Pillars): compute pillars, DaYun, and LiuNian from birth data via embedded scripts, then interpret using theory pages (day master, ten gods, and related concepts). Chart math scripts live under `scripts/`.

## Delivery type

This repository is an **Agent Skill** package (`SKILL.md` + `scripts/` + `references/` + `examples/`). It does **not** implement the C / C++ / C# / Java / JavaScript / Python language matrix used by calculator libraries. For a multi-language SDK/CLI, see sibling project `mystilink-bazi-calculator` (optional; not required to run this skill).

## Requirements

- Python 3.9+ (`zoneinfo`)
- Agent Skills–compatible host
- Network optional for Mystilink Wiki API during interpretation

## Install

Install as folder name `mystilink-bazi` (matches `SKILL.md` `name`):

| Host | Path |
|------|------|
| Cursor | `.cursor/skills/mystilink-bazi/` |
| Claude Code | `.claude/skills/mystilink-bazi/` |

```bash
cp -R mystilink-bazi-skill /path/to/.cursor/skills/mystilink-bazi
```

## Quick start (scripts)

From the skill directory:

```bash
python3 scripts/bazi_calculate.py --date 1990-05-15 --hour 12
python3 scripts/bazi_calculate.py --birth-json examples/profile.v0.json
python3 scripts/bazi_calculate.py --profile-json examples/profile.json
python3 scripts/bazi_dayun_calculate.py --date 1990-05-15 --gender female --count 8
python3 scripts/bazi_liunian_calculate.py --year 2026 --day-stem 甲
```

Success: JSON on stdout. Failure: non-zero exit and JSON `{"error":…}`.

Pillar objects include `stem_index`, `branch_index`, `text`, and legacy `ganzhi` (`=` `text`).

## Workflow

1. Collect birth profile — either:
   - `examples/profile.v0.json` (`mystilink.birth/0.1` BirthProfile), or
   - `examples/profile.json` (legacy skill fields)
2. Run chart scripts as needed (`--birth-json` / `--profile-json` accept both shapes)
3. Interpret with Wiki (optional):

```text
GET https://wiki.mystilink.com/api/v1/search?q=day+master&system=bazi&locale=en
GET https://wiki.mystilink.com/api/v1/pages/bazi.concept.ri-zhu?locale=en
```

4. Separate **chart facts** from **interpretation**; cite Wiki provenance when used

Full agent instructions: `SKILL.md`. Short ids: `references/wiki-ids.md`.

## Examples

- `examples/profile.v0.json` — BirthProfile (`mystilink.birth/0.1`, fictional)
- `examples/profile.json` — legacy birth profile (fictional); still accepted by scripts

## Limits

- Scripts are embedded copies for standalone skill install; they are not a multi-language SDK
- DaYun solar-term dates use approximate civil days
- True solar time needs both timezone and longitude
- Wiki locale: omit → `en`; missing translations may fall back to `zh-Hans`

## License

MIT. See [LICENSE](LICENSE).

## Feedback

Report defects with exact script command (fictional dates only) and stdout/stderr JSON.
