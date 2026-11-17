---
name: "openwebui-regression-test"
description: "Regression-test Open WebUI tools, adapters, streaming, reconnects, provider limits, and TTS through the real browser path."
---

# Open WebUI Regression Test

Use the real logged-in Open WebUI browser/app path for functional verification. Treat configuration, service status, HTTP 200 responses, and database integrity as supporting evidence, not proof of user-visible success.

## Establish the failure boundary

1. Reproduce the user's exact model, prompt shape, enabled toggles, and tool path.
2. Record whether the failure is:
   - provider/API error such as HTTP 429;
   - adapter or OpenClaw routing error;
   - Open WebUI backend exception;
   - Socket.IO heartbeat/reconnect warning;
   - duplicated visible answer;
   - missing or duplicated TTS;
   - tool-call refusal, truncation, or repeated tool turns.
3. Correlate browser-visible timing with service logs. Do not label a reconnect banner a backend crash unless a process restart or failed request proves it.
4. Preserve the existing database and unrelated user state.

## Inspect the complete request chain

Check, in order:

1. Browser DOM and console-visible behavior.
2. Open WebUI request and Socket.IO lifecycle.
3. Open WebUI middleware/tool execution.
4. Local adapter request/stream translation.
5. OpenClaw gateway routing.
6. Upstream provider response and rate-limit headers.
7. Stored assistant message structure, including legacy `content`, structured `output`, tool receipts, and error fields.
8. TTS request and audio playback state when voice mode is involved.

Use timestamps or request IDs to join evidence across layers.

## Apply narrow fixes

Prefer the smallest fix at the layer that owns the fault.

- Run blocking synchronous tool work outside the event loop so Socket.IO heartbeats remain responsive.
- For provider 429s, use bounded retries with server-directed or exponential backoff only when retrying is safe.
- Disable incidental title, tag, follow-up, or metadata model calls when they create avoidable concurrency or rate pressure.
- Batch independent retrieval calls in one parallel tool round when supported.
- Keep intermediate tool-loop prose in structured receipts, but expose and speak only the final assistant answer.
- Preserve tool calls, citations, and receipts; do not hide failures by discarding evidence.
- Avoid automatic Knowledge/RAG injection unless explicitly required.
- Do not modify account data or replace the live database to solve a request-path bug.

## Validate through the real user path

After each material change:

1. Restart only the services that require it.
2. Open or reuse the actual logged-in Chrome/Open WebUI app profile.
3. Submit a prompt that forces the affected behavior.
4. Monitor the live DOM for reconnect banners, duplicated answer blocks, provider error cards, and completion.
5. Confirm the expected tool calls occurred and inspect their stored receipts.
6. Confirm the final stored message has no unexpected error and that visible `content` matches the final answer once.
7. For voice mode, confirm a real TTS request returns valid audio and the app plays it unmuted.
8. Check service restart counts and HTTP statuses.
9. Remove only disposable test chats created by this test.
10. Run database integrity checks and confirm the user's chat count/state remain plausible.

## Test matrix

Use the smallest matrix covering the changed behavior:

- One ordinary response without tools.
- One forced single-tool response.
- One multi-tool or multi-search response.
- One streaming response from an OpenClaw-routed model.
- One provider likely to exercise the affected adapter path, such as NIM.
- Voice/TTS only when audio behavior changed.

For rate-limit fixes, test enough consecutive requests to exercise retry logic without deliberately hammering the provider.

## Report receipts honestly

Report:

- exact browser path tested;
- model/provider;
- number and type of tool calls;
- reconnect banners observed;
- duplicate visible answers observed;
- upstream errors and retries;
- final request status;
- service restart evidence;
- database integrity and retained chat state;
- any untested boundary.

Never claim “verified” from static configuration or a direct backend call when the bug occurs in the browser path.
