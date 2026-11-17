# Mystilink Zi Wei Skill

> Languages: [English](README.md) | [简体中文](docs/i18n/README.zh-CN.md) | [繁體中文](docs/i18n/README.zh-TW.md) | [日本語](docs/i18n/README.ja.md) | [한국어](docs/i18n/README.ko.md) | [Français](docs/i18n/README.fr.md) | [Español](docs/i18n/README.es.md)

## Overview

Agent Skill for Zi Wei Dou Shu: build a twelve-palace chart (optional Si Hua) with an embedded Python script, then interpret with theory pages. Chart math lives under `scripts/`.

## Delivery type

**Agent Skill** package. Does **not** implement the calculator language matrix (C / C++ / C# / Java / JS / Python SDK). Optional sibling: `mystilink-ziwei-calculator`.

## Requirements

- Python 3.9+
- `pip install zhdate`
- Agent Skills–compatible host
- Network optional for Wiki API

## Install

Folder name must be `mystilink-ziwei`:

```bash
cp -R mystilink-ziwei-skill /path/to/.cursor/skills/mystilink-ziwei
```

| Host | Path |
|------|------|
| Cursor | `.cursor/skills/mystilink-ziwei/` |
| Claude Code | `.claude/skills/mystilink-ziwei/` |

## Quick start

```bash
python3 scripts/ziwei_chart_calculate.py \
  --datetime "1990-05-15 14:30" \
  --timezone Asia/Shanghai \
  --gender female \
  --output json

python3 scripts/ziwei_chart_calculate.py \
  --birth-json examples/profile.v0.json \
  --output json
```

Optional flags: `--si-hua`, `--year YYYY`, `--longitude E`, `--midnight-zi`.

Success: JSON on stdout. Failure: non-zero exit + JSON error.

## Workflow

1. Collect birth data — `examples/profile.v0.json` (BirthProfile) or legacy `examples/profile.json`
2. Run the chart script
3. Optional Wiki:

```text
GET https://wiki.mystilink.com/api/v1/search?q=life+palace&system=ziwei&locale=en
GET https://wiki.mystilink.com/api/v1/pages/ziwei.concept.ming-gong?locale=en
```

4. Separate chart facts from interpretation

Details: `SKILL.md`. Orientation: `references/overview.md`.

## Examples

- `examples/profile.v0.json` — BirthProfile (`mystilink.birth/0.1`, fictional)
- `examples/profile.json` — legacy fictional birth inputs

## Limits

- Depends on `zhdate` for lunar conversion
- Embedded script for standalone skill use, not a multi-language SDK
- Wiki locale omit → `en`; fallback may be `zh-Hans`

## License

MIT. See [LICENSE](LICENSE).

## Feedback

Include exact command (fictional datetime) and JSON output/error.
