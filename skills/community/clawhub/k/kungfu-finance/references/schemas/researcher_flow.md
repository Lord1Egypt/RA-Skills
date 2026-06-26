# Researcher Flow Contract

This file documents the first-stage researcher flow for `kungfu_finance`.
It is an internal contract for implementation and maintenance.
It is not the primary user-facing routing surface.

Use [SKILL.md](../../SKILL.md) for high-level intent routing first.

## Purpose

The researcher flow currently supports three actions only:

- list top researchers by score
- query one stock's covered researchers and aggregate their report titles
- query one researcher's reports

It does not cover industry researcher ranking, concept researcher ranking, researcher-covered stock sets, or report full text.

## Router Entry

Use the router command:

```bash
node scripts/router/run_router.mjs researcher ...
```

## Actions

### `rank`

Required input:

- `--researcher-action rank`

Optional input:

- `--researcher-rank-by total|1m|3m|6m|1y`
- `--researcher-limit`
- `--researcher-min-reports`

Behavior:

- fetch `/api/researcher/rank`
- return researcher score rows directly

### `stock-reports`

Required input:

- `--researcher-action stock-reports`
- exactly one stock input mode:
  - `--instrument-name`
  - `--instrument-id` + `--exchange-id`

Optional input:

- `--researcher-rank-by total|1m|3m|6m|1y`
- `--researcher-limit`
- `--researcher-min-reports`

Behavior:

- resolve stock input to `instrument_id + exchange_id`
- fetch `/api/researcher/stock`
- for each returned researcher, fetch `/api/researcher/reports` with:
  - `author_id`
  - `instrument_id`
  - current researcher `org_name`
  - fixed first-stage `limit=10`
- return researcher score rows plus simplified report titles

### `author-reports`

Required input:

- `--researcher-action author-reports`
- exactly one of:
  - `--researcher-author-id`
  - `--researcher-name`

Optional input:

- `--researcher-org-name`

Behavior:

- if `researcher-author-id` is given:
  - fetch `/api/researcher/detail`
  - fetch `/api/researcher/reports`
- if only `researcher-name` is given:
  - perform controlled resolution through `/api/researcher/rank?rank_by=total&limit=50&min_reports=1`
  - if exactly one candidate matches, continue with that `author_id`
  - if no candidate or multiple candidates match, return `needs_input`

## Error Handling Rules

- Researcher flow must require OpenKey before local validation branches.
- If `researcher-rank-by` is invalid, return `status: "needs_input"`.
- If stock input is missing or unresolved, return `status: "needs_input"`.
- If researcher selector is missing, return `status: "needs_input"`.
- If both `researcher-author-id` and `researcher-name` are given, return `status: "needs_input"`.
- If researcher name resolution is ambiguous, return `status: "needs_input"` and provide candidate researchers.
- If upstream returns `401` or `403`, surface the auth or permission error directly.

## Output Shape

### `needs_input`

- `action`
- `status: "needs_input"`
- `prompt`
- `missing`
- optional `reason`
- optional `options`
- optional `attempted`
- optional `researcher`
- optional `instrument`

### `completed`

Rank returns:

- `action`
- `status: "completed"`
- `rank_by`
- `total`
- `researchers`

Stock reports returns:

- `action`
- `status: "completed"`
- `instrument`
- `forecast`
- `rank_by`
- `total`
- `researchers`
  - each researcher row keeps score fields
  - each researcher row also contains simplified `reports`

Author reports returns:

- `action`
- `status: "completed"`
- `researcher`
- `total`
- `reports`
