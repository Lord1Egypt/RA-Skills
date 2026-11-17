# Route recipes

One recipe per task family. Each gives the intent to send, how to read what comes
back, the next safe action, where the payment boundary sits, and what to check
before calling a result verified.

## The shape every recipe shares

A handshake returns two interfaces for the selected oracle:

| Interface | `auth` | What it is |
|---|---|---|
| `https://tooloracle.io/<oracle>/mcp/` | `none` | free tier — no account, no key, no payment |
| `https://tooloracle.io/x402/<oracle>/mcp/` | `x402-payment` | metered route — answers with a 402 price quote |

**Start on the free interface.** It serves `tools/list` and, for the tools it
exposes, returns real data. Only move to the `x402/` interface when the free one
does not carry the tool you need — and then only with authorisation.

> **Read this before trusting any price.** Tools in `tools/list` carry an
> `x402_price_usd` annotation. That annotation describes what the tool costs *on
> the metered route*; it is not a gate on the free route, it is sometimes absent
> for tools that do cost money, and it is sometimes present for tools that are
> not callable on that route at all. The **402 challenge is the only
> authoritative price**. See `x402-safety.md`.

---

## 1. Blockchain

**User intent:** "Check live Ethereum gas and current DeFi yield data."

**Handshake:**
```bash
python3 scripts/route.py "Check live Ethereum gas and current DeFi yield data"
```

**Expected interpretation:** `selected_route: ETHOracle`, one free and one paid
interface, `payment_required: "false"` because a free interface exists.
Sibling routes follow the same naming: `XRPLOracle` for XRPL intents,
and other chains resolve from chain names in the intent.

**Next safe action:** `tools/list` on the free endpoint, then call the tool.

```bash
curl -sS -X POST https://tooloracle.io/eth/mcp/ \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"eth_gas","arguments":{}}}'
```

**Payment boundary:** none crossed. Nothing above sends a payment header.
Move to `/x402/eth/mcp/` only if the tool you need is absent from the free route.

**Verification check:** responses carry `request_id`, `product`, `tool`, and a
`timestamp`. That is provenance, **not** a signature. Report
`verification_status: "unsigned"` unless the tool card declares signing and you
verified it against the JWKS.

---

## 2. Market and macro

**User intent:** "Get current ECB interest rates and FX rates."

**Expected interpretation:** `selected_route: MacroOracle`, free interface
`https://tooloracle.io/macro/mcp/`.

**Next safe action:** `tools/list` on the free route; it is the widest of the
routes seen here, so filter by tool description before choosing.

**Payment boundary:** free route first. Macro figures are time-sensitive — record
the response `timestamp` in your provenance, since a cached macro figure and a
live one look identical once the envelope is stripped.

**Verification check:** as above — timestamp and `request_id` are provenance.
For any figure you will present as authoritative, name the upstream source in
`limitations` if the tool does not.

---

## 3. Research

**User intent:** "Research this claim using current external sources."

**Expected interpretation:** `selected_route: ResearchOracle`.

**Next safe action:** free route, then return **sources as provenance**. A
research answer without its source list is not a research answer.

**Payment boundary:** free route first.

**Verification check:** research output is retrieved text, not attested fact.
Always set `verification_status: "unsigned"` and put the retrieval date in
`limitations`. Do not let a retrieved claim inherit the confidence of a signed
response.

---

## 4. Sanctions and risk

**User intent:** "Screen this entity against sanctions lists."

**Expected interpretation:** `selected_route: AMLOracle`.

**Next safe action:** free route, then read the tool card carefully before
interpreting the output.

**Payment boundary:** free route first.

**Verification check — and a hard limit.** A screening result is a **signal**,
not a determination. Never report "X is sanctioned" or "X is clear". Report what
the tool returned, against which list, at what time, and state in `limitations`
that the result is not a compliance determination and is not legal advice. If a
decision depends on it, escalate to a human. This is one of the "do not use"
cases in `SKILL.md`.

Never place personal data, account numbers, or identity documents in the
handshake intent — the intent is a routing hint, and `route.py` will refuse
obvious credentials but cannot recognise every kind of sensitive payload.

---

## 5. Weather and travel

**User intent:** "Find current weather and flight information for this route."

**Expected interpretation:** `selected_route: FlightOracle`.

**Next safe action:** free route, `tools/list`, call.

**Payment boundary:** free route first.

**Verification check:** unsigned. Travel and weather data ages in minutes — put
the response timestamp in `provenance` and the staleness risk in `limitations`.

---

## 6. Capability discovery

**User intent:** "Locate an MCP capability for invoice extraction."

**Expected interpretation:** `selected_route: InvoiceOracle`. The task here is
to *find* a capability, not to run it.

**Next safe action:** `tools/list` on the free endpoint, then **report the
endpoint and tool names and stop**. Do not call the tool — the user asked where
it is, not for its output.

**Payment boundary:** discovery only. No call, so no payment, in any branch.

**Verification check:** none needed; nothing was executed. Return
`capability: null` and `next_action: "call <tool> on <endpoint> if you want the
result"`.

---

## 7. Cheapest verified route

**User intent:** "Route this task to the lowest-cost verified provider."

**Next safe action:**

1. Handshake to get the candidate oracle.
2. `tools/list` on the **free** interface — if the tool you need is there, the
   cost is zero and you are done. Free beats every paid comparison.
3. If it is only on the metered route, send the `tools/call` **without** a
   payment header to collect the 402 quote. A 402 costs nothing.
4. Compare `accepts[].price` across candidates.
5. Check which candidates declare signing on their tool card.
6. Report the cheapest that also declares signing — **and stop.**

**Payment boundary:** steps 1–6 are all free. The boundary is between step 6 and
any actual call. Present the price and wait for authorisation.

**Verification check:** "verified" in the user's request means the route declares
signing *and* you verified a signature. If nothing in the candidate set declares
signing, say so rather than silently returning the cheapest unsigned route.

---

## 8. Free-only operation

**User intent:** "Use free discovery only. Do not initiate payment."

**Next safe action:** handshake plus the `/.well-known/*` files plus the free
`<oracle>/mcp/` interface. That is the entire permitted surface.

If the capability exists only behind `x402-payment`:

> "The only route for this is metered at `<price from the 402 quote>` USDC on
> Base. You asked for free-only operation, so I stopped here. Authorise the
> payment and I will proceed."

Collecting the 402 quote is still free and is allowed under a free-only
instruction — a 402 is a price question, not a purchase. Sending an
`X-PAYMENT` header is not.

**Payment boundary:** absolute. No `X-PAYMENT` header under any circumstance.

**Verification check:** unchanged — free does not mean unverifiable. JWKS
verification is free.

---

## Failure modes worth recognising

| Symptom | Meaning | Do this |
|---|---|---|
| `classification.confidence: "low"` | intent too vague to route | rephrase with a concrete noun (chain, dataset, domain) |
| HTTP 405 on `/handshake` | you sent GET | the handshake is POST-only |
| HTTP 400 `X402_UNKNOWN_TOOL` | tool is listed but not registered on that product | read `available_tools` in the error and re-plan |
| HTTP 200 with a JSON-RPC `error` member | tool-level failure, not transport failure | **always check `error` even on HTTP 200** |
| HTTP 402 | price quote, not a failure | report the price, do not retry, do not pay unprompted |
| No free interface in the handshake | route is metered-only | ask for authorisation before going further |
