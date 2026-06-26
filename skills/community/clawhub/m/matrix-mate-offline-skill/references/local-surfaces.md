# Local Matrix Mate Surfaces

Use the local Matrix Mate app as the trusted parse engine.

## Expected local app URL

- Default base URL: `http://127.0.0.1:3000`
- Optional override: `MATRIX_MATE_BASE_URL`
- Safety default: non-loopback hosts are rejected unless `MATRIX_MATE_ALLOW_REMOTE_BASE_URL=true`

## Start the local app

```bash
npm install
npm run dev
```

## Start the local MCP runtime

From the source repo root:

```bash
node skills/matrix-mate-offline/scripts/run-offline-mcp.mjs
```

From the exported bundle root:

```bash
node scripts/run-offline-mcp.mjs
```

## Tool to API mapping

- `parse_matrix_link` -> `POST /v1/intake/matrix-link`
- `parse_manual_itinerary` -> `POST /v1/intake/ita`
- `get_trip` -> `GET /v1/trips/:id`
- `export_trip` -> `GET /v1/trips/:id/export`
- `get_future_booking_intent` -> `GET /v1/trips/:id/future-booking-intent`
- `check_local_health` -> `GET /`

## Parse statuses

- `verified`: Matrix Mate reconciled the itinerary and fare rules without blocking issues.
- `needs_review`: A blocking discrepancy exists and the result needs a human check.
- `draft_json_only`: Only manual JSON was available, so rules coverage is incomplete.
