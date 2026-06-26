---
name: hkipo-decision-engine
description: Score Hong Kong IPOs, build decision cards, and batch-evaluate symbols or watchlists with explainable factors and execution guidance. Use when the user wants a participation call, a position-sizing plan, or a batch decision pass across multiple IPOs.
version: 0.1.0
metadata: {"openclaw":{"emoji":"📈","requires":{"bins":["uv"],"config":["~/.hkipo-next/config/profile.json","~/.hkipo-next/config/watchlist.json","~/.hkipo-next/data/hkipo.db"]},"install":[{"id":"install-uv-brew","kind":"brew","formula":"uv","bins":["uv"],"label":"Install uv with Homebrew","os":["darwin","linux"]}]}}
---

# HK IPO Decision Engine

Use this skill for action-oriented decisions.

## Runtime

This publish bundle includes the required CLI runtime under `runtime/hkipo-next`.

From the skill folder:

```bash
cd <skill_dir>
uv run --directory runtime/hkipo-next hkipo-next ...
```

By default these commands persist review records in `~/.hkipo-next/data/hkipo.db`.

## Preconditions

- Prefer to have an active parameter version.
- Prefer to have a usable profile or explicit CLI overrides for risk, budget, and financing preference.
- If the user only wants rough market discovery, do not jump straight to this skill.

## Choose the Right Command

- Use `score` for factor-level explanation.
- Use `decision-card` for a concise execution plan.
- Use `batch` for multiple symbols or the saved watchlist.

## Commands

Score one symbol:

```bash
cd <skill_dir>
uv run --directory runtime/hkipo-next hkipo-next score 2476 --format json
```

Score with explicit scenario overrides:

```bash
cd <skill_dir>
uv run --directory runtime/hkipo-next hkipo-next score 2476 \
  --parameter-version v0003 \
  --risk-profile aggressive \
  --max-budget-hkd 120000 \
  --financing-preference margin \
  --format json
```

Generate one decision card:

```bash
cd <skill_dir>
uv run --directory runtime/hkipo-next hkipo-next decision-card 2476 --format markdown
```

Batch explicit symbols:

```bash
cd <skill_dir>
uv run --directory runtime/hkipo-next hkipo-next batch 2476 2613 2590 --format json
```

Batch the current watchlist:

```bash
cd <skill_dir>
uv run --directory runtime/hkipo-next hkipo-next batch --watchlist --format json
```

## Output Cues

- `score` returns factor contributions, cost breakdown, assumptions, and risk disclosure.
- `decision-card` adds a headline, position suggestion, and exit plan.
- `partial` outputs are often still usable; they usually mean source conflicts or incomplete upstream data, not total failure.

## Companion Skills

- Use `$hkipo-parameter-manager` if there is no active parameter version or the user wants tuning.
- Use `$hkipo-review-optimizer` after outcomes are known and the user wants to refine the model.
