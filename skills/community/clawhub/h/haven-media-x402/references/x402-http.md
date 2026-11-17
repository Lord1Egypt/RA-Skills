# Haven Media — direct x402 HTTP flow

The raw HTTP contract, for agents with their own funded x402 **v2** client.
If your agent can run the Haven MCP server instead, use it: it does all of
this for you. Rules, limits, and prices are in `SKILL.md`.

1. **Discover**: `GET https://api.havenagent.ai/x402/api/v1/catalog` (free) —
   returns every endpoint, price, request schema, and limits.
2. **Request**: `POST` the endpoint with a JSON body. With no payment you
   get **HTTP 402** and a machine-readable price quote.
3. **Pay**: sign the x402 payment and retry with the `Payment-Signature`
   header (x402 v2; your x402 client library does this automatically —
   ensure it's a v2 client, which uses `Payment-Signature`, not the v1
   `X-PAYMENT` header). You get **202** with
   a `jobId`, `statusUrl`, `resultUrl`, and an `etaSeconds` estimate. **This
   payment is only verified, not charged yet** — see step 4b.

   **Verified working client** (end-to-end on 2026-07-27): the official
   x402 v2 SDK — `@x402/core` ^2.18 (`x402Client` + `x402HTTPClient`)
   with `@x402/evm`'s `registerExactEvmScheme` and a viem account signer.
   The flow is: read the 402's `PAYMENT-REQUIRED` header via
   `getPaymentRequiredResponse`, `createPaymentPayload(paymentRequired)`,
   then retry with `encodePaymentSignatureHeader(payload)` spread into the
   request headers. Anything built on the same SDK line also works —
   `@x402/fetch` / `@x402/axios` ^2.x (what current CDP buyer docs
   instruct), or ClawRouter (`@blockrun/clawrouter`, which bundles
   `@x402/*` v2). These clients read this gateway's v2 `PAYMENT-REQUIRED`
   header and respond with `Payment-Signature` automatically. Clients on
   the v1-era unscoped packages (`x402-fetch`/`x402-axios` 1.x, or
   anything that sends `X-PAYMENT`) will NOT work: the gateway responds
   `402` with `error: "unsupported_payment_header"` telling you to
   switch — it never accepts the v1 header. The same v2 client also
   answers step 4b's 402 automatically.
4. **Poll**: `GET statusUrl`. Free while `status` is `"queued"` or
   `"running"` (or `"failed"`/`"expired"`, if the job never made it).
4b. **When the artifact is ready, the same status poll answers another
   HTTP 402** — that is the actual charge point, for the same amount you
   already agreed to at step 3. Pay it the same way as step 3 and you get
   **200** with `status: "completed"` and `resultUrl`. Two payments-worth
   of protocol, one charge: only step 4b's authorization ever settles. If
   your client is a plain `fetch`/`curl` rather than a wrapped x402 client,
   it will not auto-retry this 402 — handle it explicitly, or the poll loop
   will stop here forever.
5. **Download**: `GET resultUrl` (free) for the bytes (audio/mpeg, image/*,
   or video/mp4). For video, check the response headers — see
   [use-terms.md](use-terms.md).

GPU workers scale to zero, so a cold start can add several minutes before a
job begins running. Polling `statusUrl` is free and needs no auth, so
persist the `jobId` and resume the poll in a later turn rather than
re-POSTing — re-POSTing isn't a second charge here, but it does spend one of
your wallet's limited submitted-but-undelivered slots on a duplicate job.
Each status response's `pollBudgetSeconds` is the give-up deadline, counted
from when a worker actually picks the job up (a still-queued job reports
the full budget) — unlike `etaSeconds`, which is just the typical warm-run
estimate.

## Example

```
# 1. Quote
POST https://api.havenagent.ai/x402/api/v1/music
{ "prompt": "upbeat synthwave, driving at night", "durationSeconds": 20 }
→ 402  (price quote in the PAYMENT-REQUIRED header)

# 2. Pay + retry (client attaches the Payment-Signature header) — this
#    VERIFIES the authorization; you are not charged yet
→ 202 { "jobId": "…", "statusUrl": "…", "resultUrl": "…", "etaSeconds": 60, "pollBudgetSeconds": 900 }

# 3. Poll — free while the job is still queued or running
GET {statusUrl} → { "status": "queued" }
GET {statusUrl} → { "status": "running" }

# 4. The poll that finds the artifact ready IS the charge point
GET {statusUrl} → 402  (same price quote as step 1)
# Pay + retry again (same flow as step 2) →
GET {statusUrl} → 200 { "status": "completed", "resultUrl": "…" }

# 5. Download (free)
GET {resultUrl} → audio/mpeg bytes
```
