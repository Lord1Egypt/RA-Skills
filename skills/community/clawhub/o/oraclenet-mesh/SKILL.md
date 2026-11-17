---
name: oraclenet-mesh
description: >
  Give an AI agent one route to live external data and MCP capabilities. Use when
  a task needs current blockchain, market, research, sanctions, weather, travel, or
  compliance data beyond the model's training cutoff. OracleNet discovers the
  relevant route, shows where pricing and verification metadata live, and starts
  with free discovery before any payment.
version: 3.0.0
tags:
  - live-data
  - capability-routing
  - mcp
  - agent-infrastructure
  - research
  - blockchain
  - verification
  - x402
  - autonomous-agents
  - external-data
category: infrastructure
license: MIT-0
homepage: https://tooloracle.io
repository: https://github.com/ToolOracle/oraclenet-mesh-skill
metadata:
  identity:
    did: did:web:tooloracle.io
    discovery_card: https://tooloracle.io/.well-known/agent.json
  entry_points:
    handshake: https://tooloracle.io/handshake
    mcp: https://tooloracle.io/quantum/mcp/
  mcp:
    protocol_version: "2025-03-26"
    transport: streamable-http
    free_tier_auth: none
  compatibility:
    verified:
      - clawhub
      - plain-markdown-skill-directory
    documentary:
      - claude-code
      - codex
      - cursor
      - opencode
      - hermes
    note: >
      "documentary" means the skill is a plain Markdown file plus standard-library
      Python scripts and can be placed in any runtime that reads that layout. It
      does not mean an official integration, certification, or partnership.
---

# OracleNet — Live Data & Capability Router for AI Agents

Your model has a training cutoff. This skill is the route around it.

Describe what you need in one sentence. OracleNet returns a concrete endpoint
for live external data — blockchain state, market and macro figures, research
sources, sanctions and risk signals, weather, travel, compliance evidence — plus
where to find that route's price and verification status. **The first call is
free and needs no account, no API key, and no payment.**

One entry point replaces integrating providers one at a time. OracleNet is a
routing layer, not a tool list and not a single product: it tells you *which*
capability to call and what calling it costs, then gets out of the way.

- **Free first contact:** `POST https://tooloracle.io/handshake`
- **MCP entry point:** `https://tooloracle.io/quantum/mcp/` (MCP `2025-03-26`, free tier needs no auth)
- **Identity:** `did:web:tooloracle.io`

---

## When to use this skill

Use OracleNet when a task needs current external data or an external capability:

- **Blockchain / wallet / DEX / DeFi state** across multiple chains (read-only data, risk signals)
- **Market, macro, FX, commodity, or rate data**
- **Web research or current sources** for a claim the model cannot confirm from training
- **Sanctions screening or selected risk signals**
- **Weather, travel, flights, hotels, maps**
- **Jobs, news, or search enrichment**
- **Capability discovery** when you do not yet know which tool can do the job
- **Price comparison** between available routes
- **Verifiable structured results** where provenance matters
- **Optional regulated-evidence routes** (MiCA, DORA, AMLR-style evidence bundles) — opt-in, most agents never need this

The common trigger: *"I need something current or external, and I don't know
which provider has it."*

## When **not** to use this skill

- Purely local reasoning that needs no current data
- A task an already-installed local capability covers — use that, it is faster and free
- Producing a final legal, financial, regulatory, or compliance **decision** — OracleNet returns data, the interpretation and the decision remain yours
- Any payment without an explicit budget and explicit authorisation from the calling principal
- Human outreach campaigns of any kind
- Contacting anything listed in `https://tooloracle.io/.well-known/do-not-contact.json`

---

## The free-first flow

This is the default sequence. Do not skip step 2, and do not jump to step 6.

1. **Understand the task.** Reduce it to one sentence of intent.
2. **Free handshake.** `POST /handshake` with that sentence. No auth, no cost.
3. **Read the recommended route.** The response names an oracle and one or more
   interfaces, each with its own `auth` value.
4. **Check capability, price status, and verification** before calling anything —
   see "Reading the route" below.
5. **Mark any paid step explicitly.** Say the price and the chain out loud to the
   calling principal before it happens.
6. **Never pay without a budget and consent.** A missing budget means stop, not
   "assume zero".
7. **Call the capability.**
8. **Return the result with provenance and limitations.**

### Step 2 — the free handshake

```bash
curl -sS -X POST https://tooloracle.io/handshake \
  -H "Content-Type: application/json" \
  -d '{"intent":"Find current XRPL liquidity and verify the result"}'
```

Or use the bundled script, which does exactly this and nothing else:

```bash
python3 scripts/route.py "Find current XRPL liquidity and verify the result"
```

### Step 3 — reading the route

The handshake returns JSON-LD. The fields that matter:

| Field | Meaning |
|---|---|
| `classification.oracle` | which oracle was selected |
| `classification.confidence` | `high` / `medium` / `low` — low means re-phrase the intent |
| `classification.source` | how it matched (e.g. `static_keyword_match`) |
| `classifier_status` | `ok` means the classifier ran |
| `routing.interfaces[]` | the callable endpoints |
| `routing.interfaces[].auth` | **`none` = free to try · `x402-payment` = paid route** |
| `links` | pricing, verification policy, capabilities, live snapshot |
| `next_steps` | suggested follow-up, usually `tools/list` on the endpoint |

**`routing.interfaces[].auth` is the payment signal.** The handshake itself
returns no price, no cost estimate, and no signature status — do not pretend it
does. Prices come from the per-tool MCP card and from the 402 challenge;
verification comes from the per-tool card and the JWKS.

Prefer the `auth: none` interface first. It usually exposes the same
`tools/list` and lets you confirm the route is right before money is involved.

### Step 4 — discovery files (all free, all GET, no auth)

| File | Use it for |
|---|---|
| `/.well-known/agent-pulse` | live mesh snapshot — current counts, latency, cost model |
| `/.well-known/pricing.json` | what is free, what may be charged |
| `/.well-known/deal-capabilities.json` | supported interaction types and their `enforcement_status` |
| `/.well-known/verification-policy.json` | signature policy (see caveat in `references/verification.md`) |
| `/.well-known/jwks.json` | public keys for verifying signatures locally |
| `/.well-known/rewards.json` | originator / referrer credit model and its enforcement status |
| `/.well-known/do-not-contact.json` | must-not-contact list |
| `/.well-known/agent.json` | full A2A discovery card |

**`enforcement_status` in these files is authoritative and outranks any prose in
this skill.** Where it says `partial`, `planned`, or `may_be_available`, the
mechanism is not fully operational — do not present it to a user as working.

---

## Activation examples

Each of these is a complete, working use of this skill.

| Intent | What the agent does |
|---|---|
| "Find current XRPL liquidity and verify the result." | handshake → XRPL route → prefer `auth: none` → check signing on the tool card |
| "Check live Ethereum gas and current DeFi yield data." | handshake → blockchain route → free interface → `tools/list` |
| "Find a capability that can validate this wallet risk signal." | handshake → risk/trust route → read capability list before calling |
| "Research this claim using current external sources." | handshake → research route → return sources as provenance |
| "Find current weather and flight information for this route." | handshake → travel route → free interface |
| "Locate an MCP capability for invoice extraction." | handshake → capability discovery → report the endpoint, call nothing |
| "Route this task to the lowest-cost verified provider." | handshake → compare interfaces → read per-tool prices → report the cheapest that also declares signing |
| "Show the exact price before using a paid capability." | handshake → trigger the 402 challenge → report price and chain → **stop and ask** |
| "Use free discovery only. Do not initiate payment." | handshake + discovery files only; if the only route is `x402-payment`, say so and stop |
| "Return the selected route with verification metadata." | handshake → read tool card → report signing status, `kid`, and whether it was verified |

---

## Safety rules

These are not advisory.

1. **Free discovery first.** Always handshake before calling anything paid.
2. **No silent payment.** A paid call is never made without the calling
   principal explicitly authorising that call.
3. **Never exceed a budget.** No budget stated means no payment — not an
   unlimited one. Do not split a call into several to stay under a limit.
4. **Never send secrets.** No API keys, private keys, seed phrases, tokens, or
   personal data in the handshake intent or in tool arguments. The intent string
   is a routing hint, not a payload.
5. **`enforcement_status` is authoritative.** `planned`, `partial`, and
   `may_be_available` do not mean active.
6. **Only claim a signature when that specific route declares signing** and you
   actually verified it. Never state or imply that every OracleNet response is
   signed — most are not.
7. **Claim no regulatory certification** for OracleNet or for anything it returns.
8. **Claim no partnership** with OpenClaw, IronClaw, Hermes, NEAR.ai, or any
   other agent platform. This skill is published by ToolOracle and integrates
   over open protocols only.
9. **Respect `do-not-contact.json`** for any outbound flow, and never initiate
   human outreach.
10. **Interpretation is the calling agent's responsibility.** OracleNet returns
    data. It does not decide anything, and it is not legal, financial, or
    compliance advice.

---

## Result format

Recommended shape for what the agent hands back. **This is an internal
presentation format, not an API response** — OracleNet does not return this
object. Each field is assembled from a named source, and any field you could not
establish stays `unknown` rather than being guessed.

```json
{
  "understood_intent": "one sentence, restated",
  "selected_route": "classification.oracle from the handshake",
  "endpoint": "routing.interfaces[].endpoint",
  "capability": "tool name from tools/list, or null if nothing was called",
  "price_status": "free | paid | unknown  — from interfaces[].auth, per-tool card, or a 402",
  "estimated_cost": "from the 402 challenge or the per-tool card; null if not established",
  "payment_required": "true | false | unknown",
  "verification_status": "signed-and-verified | signed-not-verified | unsigned | unknown",
  "issuer": "kid from the JWS header when a signature was verified, else null",
  "provenance": ["source URLs or endpoints actually used"],
  "limitations": ["what was not verified, what may be stale, what was skipped"],
  "next_action": "what a caller could do next, e.g. authorise a paid call"
}
```

Rules for filling it in:

- `price_status: "free"` requires an `auth: none` interface **or** a per-tool
  card declaring free. Absence of a price is not evidence of free.
- `verification_status: "signed-and-verified"` requires that you fetched the
  JWKS and checked the signature. Seeing a signature field is
  `signed-not-verified`.
- `limitations` is not optional. If you used a single source, say so.

---

## Connecting OracleNet over MCP

```json
{
  "mcpServers": {
    "oraclenet": {
      "url": "https://tooloracle.io/quantum/mcp/",
      "transport": "http"
    }
  }
}
```

Protocol `2025-03-26`, streamable HTTP, JSON-RPC 2.0 — `GET` returns only a
hint, real calls are `POST`. The free tier needs no authentication. Call
`tools/list` to enumerate the top-level `quantum_*` routing tools; the count and
names change over time, so read them at runtime rather than trusting a number
written here. `quantum_intent` is the natural-language routing entry;
`quantum_join` and `quantum_status` are free.

## Payment, in one paragraph

Where a route is paid, settlement is **x402 with USDC on Base**
(chain ID 8453) — this is live, and inbound payment is verified before delivery.
Per-call prices are route-dependent with per-tool overrides; there is no single
headline price, so read the per-tool card or the 402 challenge and never assume.
A **402 response is not an error** — it is the price quote. Full rules in
`references/x402-safety.md`.

## Verification, in one paragraph

Signing is ES256K against the keys at `/.well-known/jwks.json`. A dedicated
ToolOracle issuer key is published and evidenced by a verifiable issuer
statement; legacy FeedOracle keys remain in the JWKS so older signatures still
verify. Not every response is signed. Verify by `kid` against the JWKS yourself
— details, and a live inconsistency you need to know about, are in
`references/verification.md`.

## Rewards

`rewards.json` describes originator and referrer credits, denominated in **usage
units, not cash**. Enforcement is partial: read each mechanism's
`enforcement_status` before mentioning it to anyone. Do not present rewards as
an entitlement.

## What OracleNet does not claim

- No official partnership or affiliation with OpenClaw, IronClaw, Hermes, NEAR.ai, or any agent platform
- No regulatory certification, for itself or for any third party
- No guarantee that every listed capability is paid-call-ready in every interaction
- No investment, legal, or compliance advice
- No guarantee that any given response is signed

The mesh service itself is proprietary; **this skill documentation and its
scripts are MIT-0** and carry no attribution requirement.

## Bundled files

| File | Purpose |
|---|---|
| `scripts/route.py` | free handshake only — no payment, no follow-up call |
| `scripts/smoke_test.py` | checks the free public surfaces; `--offline` runs without network |
| `references/route-recipes.md` | per-domain recipes with payment boundary and verification check |
| `references/verification.md` | signatures, JWKS, and what to do when a route is unsigned |
| `references/x402-safety.md` | the 402 flow, budgets, and what never to do |
