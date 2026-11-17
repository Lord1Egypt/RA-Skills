# Snapshot and stream integration

Use SSE for a backend that already consumes HTTP streams. A WebSocket alternative exists for matching public stream routes. Both transports carry an event name and JSON data. The JavaScript starter includes a finite `stream.mjs` consumer that emits JSON lines and reconnects from its latest resume token. It is a transport example, not a materialized odds cache or a background service. The Python starter covers REST; use this contract when adding a Python stream consumer.

## Required sequence

1. Discover the event, fetch every page of its odds snapshot, and emit or store the initial state with the exact filter set. Keep the earliest page's resume token when loading sequential pages so catch-up can cover updates during pagination. Do not call the combined pages an atomic snapshot.
2. Connect to `/events/{event_id}/odds/stream` with the same bookmaker/market/period filters, `since=<resume>`, and `catchup=true`. Use the `X-API-Key` header. The starter uses `heartbeat_sec=15` and a finite run duration.
3. Parse SSE as framed events: comments are not messages; `data:` may span multiple lines; network chunks can split a UTF-8 character or a frame. The starter handles these cases. Reject malformed frames or a mismatched event ID.
4. On `delta`, apply the documented ordered `changes` list idempotently using each odd's stable `id`. A delta batch may have `snapshot_id`, `batch_index`, and `batch_count`; do not expose a partially applied multi-batch update as a complete atomic state. Commit the resume token after the relevant state changes have been processed. The starter emits the frame before advancing its in-memory token; a production cache must persist state and token consistently.
5. On `heartbeat`, update freshness and connection health. SSE tokens advance from delta messages; do not replace a valid token with null. Unknown fields should not break a parser, but unknown mutation operations require a schema check or resync rather than guesswork.
6. On `resync`, discard the unusable continuation token, fetch fresh snapshot pages, and reconnect. Do not attempt to rebuild live state from history.
7. On disconnect, reconnect with bounded exponential backoff and the last processed token. If no complete valid token exists, fetch a new snapshot. Honour rate-limit headers. Stop or surface an error after the retry budget is exhausted.

A heartbeat interval is the maximum expected idle gap, not a polling schedule. Treat a gap longer than the interval plus a margin as a dead connection even if the TCP connection remains open. The starter's watchdog resets on bytes received and aborts after 35 seconds without data; an application should also track the last valid message.

WebSocket messages mirror SSE with JSON envelopes such as `{"event":"delta","data":{...}}`. Prefer header authentication in server-side clients. Browser WebSocket APIs cannot attach arbitrary headers; proxy through a backend so API keys never enter browser code or URL query strings. On `resync`, reload the corresponding snapshot before processing more updates.

References: [streaming guide and endpoint contracts](https://odds-api.net/docs#sse-and-websocket), [public OpenAPI](https://api.odds-api.net/v1/openapi.json).
