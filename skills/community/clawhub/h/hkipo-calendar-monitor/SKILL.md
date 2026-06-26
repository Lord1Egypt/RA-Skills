---
name: hkipo-calendar-monitor
description: Monitor Hong Kong IPO deadline and listing windows and return structured discovery results for near-term IPO scanning. Use when the user asks what is currently open, which IPOs are closing soon, or which listings are coming up next in Hong Kong.
version: 0.1.0
metadata: {"openclaw":{"emoji":"📅","requires":{"bins":["uv"]},"install":[{"id":"install-uv-brew","kind":"brew","formula":"uv","bins":["uv"],"label":"Install uv with Homebrew","os":["darwin","linux"]}]}}
---

# HK IPO Calendar Monitor

Use this skill for read-only IPO discovery.

## Runtime

This publish bundle includes the required CLI runtime under `runtime/hkipo-next`.

From the skill folder:

```bash
cd <skill_dir>
uv run --directory runtime/hkipo-next hkipo-next ...
```

## Workflow

1. Choose `deadline` when the user cares about subscription cutoffs.
2. Choose `listing` when the user cares about debut dates.
3. Default to `--days 7` unless the user asked for another horizon.
4. Prefer `--format json` for downstream machine use.
5. Prefer `--format text` or `--format markdown` for direct human summaries.

## Commands

Upcoming subscription deadlines:

```bash
cd <skill_dir>
uv run --directory runtime/hkipo-next hkipo-next calendar --window deadline --days 7 --format json
```

Upcoming listings:

```bash
cd <skill_dir>
uv run --directory runtime/hkipo-next hkipo-next calendar --window listing --days 7 --format markdown
```

Export a report:

```bash
cd <skill_dir>
uv run --directory runtime/hkipo-next hkipo-next calendar --window deadline --days 14 --format markdown --output /tmp/hkipo-deadlines.md
```

## Output Cues

- `data.items` is the authoritative IPO event list.
- `item.data_status`, `data.issues`, `meta.degraded`, and `meta.data_status` tell you whether upstream data was partial.
- `entry_fee_hkd` and `total_margin_hkd_100m` are useful ranking hints, but this skill does not score participation attractiveness.

## Companion Skills

- Use `$hkipo-snapshot-extractor` for one-symbol fact extraction.
- Use `$hkipo-decision-engine` for participation advice.
