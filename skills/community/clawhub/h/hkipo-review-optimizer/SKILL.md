---
name: hkipo-review-optimizer
description: Review past Hong Kong IPO decisions, update actual outcomes, export review datasets, and accept or reject tuning suggestions. Use when the user wants to learn from completed IPO calls and improve later scoring behavior.
version: 0.1.0
metadata: {"openclaw":{"emoji":"🔁","requires":{"bins":["uv"],"config":["~/.hkipo-next/data/hkipo.db"]},"install":[{"id":"install-uv-brew","kind":"brew","formula":"uv","bins":["uv"],"label":"Install uv with Homebrew","os":["darwin","linux"]}]}}
---

# HK IPO Review Optimizer

Use this skill for the post-decision feedback loop.

## Runtime

This publish bundle includes the required CLI runtime under `runtime/hkipo-next`.

From the skill folder:

```bash
cd <skill_dir>
uv run --directory runtime/hkipo-next hkipo-next ...
```

By default review history is stored in `~/.hkipo-next/data/hkipo.db`.

## Workflow

1. Use `review list` to find target records.
2. Use `review show` before updating a record.
3. Use `review update` to add actual results and variance notes.
4. Use `review export` when another tool needs a JSON dataset.
5. Use `apply-suggestions show` before accepting or rejecting imported suggestions.

## Commands

List recent review records:

```bash
cd <skill_dir>
uv run --directory runtime/hkipo-next hkipo-next review list --limit 20 --format json
```

Show a record:

```bash
cd <skill_dir>
uv run --directory runtime/hkipo-next hkipo-next review show rvw_123 --format json
```

Update actual results:

```bash
cd <skill_dir>
uv run --directory runtime/hkipo-next hkipo-next review update rvw_123 \
  --allocated-lots 2 \
  --listing-return-pct 14.2 \
  --exit-return-pct 9.8 \
  --realized-pnl-hkd 1860 \
  --notes "Sold into first-day strength" \
  --variance-note "Grey market was weaker than expected but sponsor demand held" \
  --format json
```

Export a review dataset:

```bash
cd <skill_dir>
uv run --directory runtime/hkipo-next hkipo-next review export --from 2026-04-01 --to 2026-04-16 --output /tmp/hkipo-review.json --format text
```

Preview and accept a suggestion:

```bash
cd <skill_dir>
uv run --directory runtime/hkipo-next hkipo-next apply-suggestions show sgg_123 --format json
uv run --directory runtime/hkipo-next hkipo-next apply-suggestions accept sgg_123 --reason "Matches observed listing-day slippage" --format json
```

## Output Cues

- Review records preserve the original prediction payload, data status, and source issue count.
- Suggestion detail output shows whether a proposed change would create a new parameter version.

## Companion Skills

- Use `$hkipo-parameter-manager` when a review conclusion needs manual tuning work.
- Use `$hkipo-decision-engine` to rerun fresh decisions after a rule change.
