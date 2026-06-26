# Bucket Flow Contract

This file documents the first-stage bucket flow for `kungfu_finance`.
It is an internal contract for implementation and maintenance.
It is not the primary user-facing routing surface.

Use [SKILL.md](../../SKILL.md) for high-level intent routing first.

## Purpose

The bucket flow currently supports two actions only:

- list current-user buckets
- add a batch of instruments into one target bucket

It does not cover bucket creation, deletion, rename, index, MA, leaders, or reverse lookup.

## Router Entry

Use the router command:

```bash
node scripts/router/run_router.mjs bucket ...
```

## Actions

### `list`

Required input:

- `--bucket-action list`

Behavior:

- fetch current-user buckets from `/api/instrument-buckets/buckets`
- return `{ action, status, buckets, total }`
- when the user has no buckets, return an empty list plus a message

### `add`

Resolved write path requires:

- `--bucket-action add`
- exactly one of:
  - `--bucket-id`
  - `--bucket-name`
- one or more instruments via either:
  - repeated `--bucket-instrument`
  - `--bucket-instruments` with comma/newline separated values

Supported instrument token forms:

- plain stock name such as `贵州茅台`
- `600519.SSE`
- `SSE:600519`

Dialogue continuation rule:

- if bucket selector or instrument list is still missing, do not fail the flow
- instead return `status: "needs_input"` and let the host continue collecting the missing fields

## Resolution Rules

Before writing to the bucket, the flow must:

1. resolve the target bucket from current-user bucket list
2. fetch current bucket instruments
3. resolve each instrument input through `instrument_profile`
4. split results into:
   - `added`
   - `skipped_invalid`
   - `skipped_duplicate`

If required information is still incomplete, the flow must not throw a normal business error.
It must return a structured dialogue continuation payload.

## Error Handling Rules

- If some instruments are invalid but at least one is valid, continue with valid ones and return invalid entries explicitly.
- If all provided instruments are invalid, do not call the write API and return `status: "needs_input"` with corrected-instrument prompt.
- If bucket selector is missing, return `status: "needs_input"` with current bucket options.
- If a bucket name is ambiguous, return `status: "needs_input"` and require `bucket_id`.
- If a bucket name or `bucket_id` is not found, return `status: "needs_input"` with current bucket options.
- If instrument list is missing, return `status: "needs_input"` and preserve the resolved target bucket in the response.
- If the upstream returns `401` or `403`, surface the auth or permission error directly.

## Output Shape

### `needs_input`

- `action`
- `status: "needs_input"`
- `prompt`
- `missing`
- optional `reason`
- optional `bucket`
- optional `options`
- optional `attempted`
- optional `skipped_invalid`
- optional `skipped_duplicate`

### `completed`

Successful `add` returns:

- `action`
- `status: "completed"`
- `bucket`
- `added`
- `skipped_invalid`
- `skipped_duplicate`
- `upstream`
- `summary`
