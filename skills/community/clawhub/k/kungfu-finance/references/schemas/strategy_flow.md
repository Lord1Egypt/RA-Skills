# Strategy Flow Contract

This file documents the current strategy flow for `kungfu_finance`.
It is an internal contract for implementation and maintenance.
It is not the primary user-facing routing surface.

Use [SKILL.md](../../SKILL.md) for high-level intent routing first.

## Purpose

The strategy flow currently supports five actions only:

- list public strategies, grouped market modes, and current-user private strategies
- query one strategy on one instrument across a target-date window
- query one select strategy's whole-market results for one day or one date range
- count buy signals for the current instrument across eligible public paid strategies
- batch scan one public paid strategy across multiple instruments

It does not cover strategy CRUD, subscriptions, realtime push, trade-record download, or private-strategy batch scan.

## Router Entry

Use the router command:

```bash
node scripts/router/run_router.mjs strategy ...
```

## Actions

### `list`

Required input:

- `--strategy-action list`

Optional input:

- `--strategy-scope public|private|all`
- `--strategy-market-mode`

Behavior:

- fetch public strategies from `/api/strategy/public`
- fetch current-user private strategies from `/api/strategy`
- return grouped public strategies, private strategies, and market-mode groups

### `signal`

Resolved query path requires:

- `--strategy-action signal`
- exactly one of:
  - `--strategy-id`
  - `--strategy-name`
- exactly one stock input mode:
  - `--instrument-name`
  - `--instrument-id` + `--exchange-id`
- `--target-date`
- optional `--visual-days-len`

Behavior:

- support both public and private strategies
- keep the model-side date surface narrow: `target_date + visual_days_len`
- preserve `plan_level_satisfied` from upstream when querying paid public strategies

### `count`

Required input:

- `--strategy-action count`
- exactly one stock input mode
- `--target-date`

Behavior:

- call `/api/visualization/strategy-buy-signals`
- only counts paid public strategies whose `lago_plan` is available to the current user

### `market-select`

Resolved query path requires:

- `--strategy-action market-select`
- exactly one of:
  - `--strategy-id`
  - `--strategy-name`
- optional one date mode:
  - `--target-date`
  - `--strategy-start-date` + `--strategy-end-date`

Behavior:

- support both public and private strategies when `strategy_type` is `InstrumentSelect`, `TemplateInstrumentSelect`, `BuySell`, or `TemplateBuySell`
- when the selected strategy is `BuySell` or `TemplateBuySell`, whole-market results only return buy points
- if no date input is provided, let the backend default to the latest trading day
- do not mix single-day mode and date-range mode
- preserve `start_date`, `end_date`, `requested_end_date`, `plan_level_satisfied`, `results`, and `summary` from upstream

### `batch-scan`

Resolved query path requires:

- `--strategy-action batch-scan`
- exactly one of:
  - `--strategy-id`
  - `--strategy-name`
- one or more instruments via either:
  - repeated `--strategy-instrument`
  - `--strategy-instruments` with comma/newline separated values
- `--target-date`

Supported instrument token forms:

- plain stock name such as `贵州茅台`
- `600519.SSE`
- `SSE:600519`

Behavior:

- only support public strategies with non-empty `lago_plan`
- resolve each instrument token before batch submission
- if the selected strategy is private, return `needs_input` and ask for a public paid strategy instead
- if upstream returns batch-scan permission denial, return `status: "blocked"`

## Resolution Rules

Before `signal`, `batch-scan`, or `market-select`, the flow must:

1. fetch public strategies and current-user private strategies
2. resolve the requested strategy selector against those lists
3. for `batch-scan`, resolve and deduplicate input instruments before writing the batch body

If required information is still incomplete, the flow must not throw a normal business error.
It must return a structured dialogue continuation payload.

## Error Handling Rules

- If strategy selector is missing, return `status: "needs_input"` with available strategy options.
- If strategy selector is ambiguous, return `status: "needs_input"` and require `strategy_id`.
- If strategy is not found, return `status: "needs_input"` with available strategy options.
- If single-instrument input is missing, return `status: "needs_input"` and ask for one target instrument.
- If `market-select` uses a strategy type outside the supported whole-market set, return `status: "needs_input"` and require a supported strategy.
- If `market-select` mixes `target_date` with range input, return `status: "needs_input"`.
- If `market-select` only provides half of a date range, return `status: "needs_input"`.
- If `batch-scan` instruments are missing, return `status: "needs_input"` and preserve the resolved strategy.
- If all `batch-scan` instruments are invalid, return `status: "needs_input"` with invalid entries.
- If the selected strategy is private for `batch-scan`, return `status: "needs_input"` and require a public paid strategy.
- If the batch-scan upstream returns permission denial, return `status: "blocked"`.
- If upstream returns `401` or `403`, surface the auth or permission error directly.

## Output Shape

### `needs_input`

- `action`
- `status: "needs_input"`
- `prompt`
- `missing`
- optional `reason`
- optional `strategy`
- optional `options`
- optional `attempted`
- optional `skipped_invalid`
- optional `skipped_duplicate`

### `blocked`

- `action`
- `status: "blocked"`
- `reason`
- `message`
- optional `strategy`

### `completed`

List returns:

- `action`
- `status: "completed"`
- `public_strategies`
- `private_strategies`
- `market_mode_groups`

Signal returns:

- `action`
- `status: "completed"`
- `strategy`
- `instrument`
- `start_date`
- `end_date`
- `plan_level_satisfied`
- `signals`

Market select returns:

- `action`
- `status: "completed"`
- `strategy`
- `start_date`
- `end_date`
- `requested_end_date`
- `plan_level_satisfied`
- `results`
- `summary`

Count returns:

- `action`
- `status: "completed"`
- `instrument`
- `target_date`
- `count`
- optional `error`

Batch scan returns:

- `action`
- `status: "completed"`
- `strategy`
- `target_date`
- `results`
- `skipped_invalid`
- `skipped_duplicate`
