# Mystilink Horoscope Skill

> Languages: [English](README.md) | [简体中文](docs/i18n/README.zh-CN.md) | [繁體中文](docs/i18n/README.zh-TW.md) | [日本語](docs/i18n/README.ja.md) | [한국어](docs/i18n/README.ko.md) | [Français](docs/i18n/README.fr.md) | [Español](docs/i18n/README.es.md)

## Overview

Agent Skill for western natal astrology: compute planets, houses, and aspects from birth time and place via an embedded script, then interpret with theory pages.

## Delivery type

**Agent Skill** package. Does **not** implement the calculator language matrix. Optional sibling: `mystilink-horoscope-calculator`.

## Requirements

- Python 3.9+
- `pip install pyswisseph`
- Agent Skills–compatible host
- Network optional for Wiki API

## Install

Folder name must be `mystilink-horoscope`:

```bash
cp -R mystilink-horoscope-skill /path/to/.cursor/skills/mystilink-horoscope
```

| Host | Path |
|------|------|
| Cursor | `.cursor/skills/mystilink-horoscope/` |
| Claude Code | `.claude/skills/mystilink-horoscope/` |

## Quick start

```bash
python3 scripts/astro_chart_calculate.py \
  --datetime "1990-05-15 14:30" \
  --timezone Asia/Shanghai \
  --lat 31.23 --lon 121.47 \
  --output json

python3 scripts/astro_chart_calculate.py \
  --birth-json examples/profile.v0.json \
  --output json
```

Optional: `--zodiac tropical|sidereal`, `--true-solar-time`.

Success: JSON on stdout. Failure: non-zero exit + JSON error.

## Workflow

1. Collect birth data — `examples/profile.v0.json` (BirthProfile) or legacy `examples/profile.json`
2. Run the natal script
3. Optional Wiki:

```text
GET https://wiki.mystilink.com/api/v1/search?q=ascendant&system=horoscope&locale=en
GET https://wiki.mystilink.com/api/v1/pages/horoscope.concept.natal-chart?locale=en
```

4. Keep chart data distinct from interpretation

Details: `SKILL.md`. Orientation: `references/overview.md`.

## Examples

- `examples/profile.v0.json` — BirthProfile (`mystilink.birth/0.1`, fictional)
- `examples/profile.json` — legacy fictional natal inputs

## Limits

- Requires Swiss Ephemeris via `pyswisseph`
- Embedded script for skill install, not a multi-language SDK
- Wiki locale omit → `en`; fallback may be `zh-Hans`

## License

MIT. See [LICENSE](LICENSE).

## Feedback

Include exact command (fictional coordinates/datetime) and JSON output/error.
