---
name: kalshi-cli
description: Use the local kalshi CLI for bounded Kalshi series and market research, keyword discovery, fixed-point portfolio and candlestick reads, order reconciliation, and explicitly confirmed demo or production order operations.
---

# Kalshi CLI

Use the compiled `kalshi` binary or `go run ./cmd/kalshi` from this repository.

## Required workflow

1. If the command is not already known from the same cached registry/binary version, run `kalshi commands list --fields registry_version,commands.name,commands.output_contract_version,commands.summary --compact` once and cache the result by `registry_version` for the task.
2. Before constructing unfamiliar parameters, run `kalshi commands describe <command.name> --fields command.name,command.output_contract_version,command.summary,command.effect,command.params_schema --compact`. Add `command.response_schema,command.docs_url` only when response semantics or upstream documentation are needed.
3. Prefer one strict `--params` JSON object for generated calls. Convenience flags are safe but must not duplicate fields in `--params`.
4. Add the narrowest useful `--fields` selection to reads. Add every field the task cannot proceed without to `--require-fields`; this makes the path present and non-null in every returned record. Paths are item-relative for collection commands and data-root-relative otherwise. Discover allowed paths and constraints offline with `kalshi commands describe <command.name> --fields command.response_schema.x-projectable-fields,command.response_schema.x-projected-field-contracts --compact`.
5. Set explicit `--max-pages`, `--max-items`, and `--max-bytes` when the defaults do not fit the task. Never emulate an unbounded `--all` loop.
6. Parse `schema_version`, `output_contract_version`, `ok`, stable `error.code`, `effect`, and `meta.truncation`. Do not scrape prose.
7. Treat a non-empty `meta.pagination.next_cursor` plus truncation reasons as an explicit continuation decision.

`markets.search` is a bounded local substring match over documented `/markets`
pages, not an upstream full-text or relevance-ranked search. A zero-match result
is complete only when its cursor is empty and truncation is false.

`portfolio.pnl` exposes Kalshi's upstream-reported realized P&L, exposure, and
fees. It does not estimate unrealized P&L, subtract fees, or combine market and
event aggregates. Current and archived candlesticks have separate commands and
field contracts; do not substitute one when the other returns not found.

## Authentication

Never place an API private key in argv, `--params`, output, logs, or prompts. Configure `KALSHI_CREDENTIALS_FILE`, or configure `KALSHI_API_KEY_ID` plus `KALSHI_PRIVATE_KEY_FILE`. Credential and PEM files must be mode `0600` or stricter.

`orderbook.get` is anonymous by default because current Kalshi public-data guidance and observed behavior allow it, despite the current endpoint schema also declaring authentication. If the server requires authentication, repeat with `--authenticated` and a configured credential source.

## Writes

Never call `orders.create` or `orders.cancel` directly on first construction.

1. Supply an explicit environment and a write policy. Prefer demo unless the operator explicitly requested production.
2. For create, supply a caller-stable `client_order_id`, count/notional policy caps, and complete params.
3. Add `--dry-run`. This performs no credential loading, DNS, HTTP, or mutation.
4. Review the canonical plan and its effect/policy metadata.
5. Repeat the identical command without `--dry-run` and pass the exact `confirmation_digest` to `--confirm`.
6. If a write returns `mutation_status: "unknown"`, do not blindly retry and do not switch client IDs. Run `orders.reconcile` for creates or `orders.get` for cancels.

`--write-policy demo-only` permits demo writes; `allow` is necessary for production. The default is `deny`. CLI flags may state finite count and notional caps; they are part of the confirmation digest.

## Output

Prefer compact JSON for model consumption. Use NDJSON only for external line-oriented processors; it is atomically buffered and repeats the envelope for each collection item, so it is usually more token-expensive. NDJSON's final summary record contains authoritative pagination/truncation metadata. Strings are sanitized so C0/C1 terminal controls, ANSI escapes, invalid UTF-8, and bidi controls appear as visible Unicode escape text.

Projection happens before sanitization and byte accounting. If the result still exceeds `--max-bytes`, the command fails atomically with `OUTPUT_LIMIT`; add or narrow fields, or increase the cap. Never treat an output-limit error as a partial page or continue from a cursor copied from error text.

Commands may declare `x-default-fields` for their canonical v1 view. An
explicit `--fields` overrides that default; continue to use `--require-fields`
for every optional value the task cannot proceed without.

Required response fields are validated before projection. Treat `UPSTREAM_SCHEMA_MISMATCH` as a contract failure, inspect `error.details.missing_fields`, `type_mismatches`, `format_mismatches`, `value_mismatches`, and `unexpected_fields`, and do not guess a renamed field. Optional fields selected only with `--fields` are emitted as `null` when absent; use `--require-fields` whenever `null` would make the task fail later.

Branch on stable error codes and exit categories documented in `README.md`. A network error is retryable only for reads. Writes are never automatically retried.

Read commands automatically handle bounded HTTP `429` retries within `--timeout`. Inspect `meta.retry` when present for attempts, completed retries, exhaustion, and the final server delay. A final `UPSTREAM_REJECTED` with HTTP `429` and `retryable: true` means the per-process retry budget was exhausted; back off before starting another CLI process. Rate-limited attempts do not count as fetched pagination pages.
