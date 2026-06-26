---
name: hkipo-parameter-manager
description: Save, inspect, activate, and compare Hong Kong IPO scoring parameter versions across weights, thresholds, and cost assumptions. Use when the user wants to tune HK IPO rules or prepare an active scoring version before generating recommendations.
version: 0.1.0
metadata: {"openclaw":{"emoji":"⚙️","requires":{"bins":["uv"],"config":["~/.hkipo-next/data/hkipo.db"]},"install":[{"id":"install-uv-brew","kind":"brew","formula":"uv","bins":["uv"],"label":"Install uv with Homebrew","os":["darwin","linux"]}]}}
---

# HK IPO Parameter Manager

Use this skill for stateful scoring-rule management.

## Runtime

This publish bundle includes the required CLI runtime under `runtime/hkipo-next`.

From the skill folder:

```bash
cd <skill_dir>
uv run --directory runtime/hkipo-next hkipo-next ...
```

By default parameter versions are stored in `~/.hkipo-next/data/hkipo.db`.

## Parameter Model

- Weights: `snapshot-quality-weight`, `affordability-weight`, `pricing-stability-weight`, `sponsor-support-weight`, `cost-efficiency-weight`
- Thresholds: `participate-min`, `cautious-min`
- Costs: `handling-fee-hkd`, `financing-rate-annual-pct`, `cash-opportunity-rate-annual-pct`, `lockup-days`

## Workflow

1. Inspect current versions with `params list` or `params show`.
2. Save new candidates instead of mutating old versions.
3. Activate a version only when the user wants it to become the new default.
4. Compare candidate versions on a representative symbol before broad rollout.

## Commands

List versions:

```bash
cd <skill_dir>
uv run --directory runtime/hkipo-next hkipo-next params list --format json
```

Show the active version:

```bash
cd <skill_dir>
uv run --directory runtime/hkipo-next hkipo-next params show --format json
```

Save and activate a tuned version:

```bash
cd <skill_dir>
uv run --directory runtime/hkipo-next hkipo-next params save \
  --name conservative-margin \
  --sponsor-support-weight 0.20 \
  --cost-efficiency-weight 0.25 \
  --participate-min 78 \
  --cautious-min 62 \
  --lockup-days 6 \
  --notes "Bias toward sponsor quality and lower carrying cost" \
  --activate \
  --format json
```

Compare two versions:

```bash
cd <skill_dir>
uv run --directory runtime/hkipo-next hkipo-next params compare 2476 v0002 v0003 --format json
```

## Output Cues

- `active_version` is the default version used by later scoring commands.
- `action_changed` in compare output tells you whether a tuning change would alter the recommendation.
- `factor_deltas` shows which factor scores moved between versions.

## Companion Skills

- Use `$hkipo-decision-engine` after an active version is ready.
- Use `$hkipo-review-optimizer` when tuning changes come from real-world review feedback.
