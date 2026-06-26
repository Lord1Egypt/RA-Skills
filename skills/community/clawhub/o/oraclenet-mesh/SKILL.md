---
name: oraclenet-mesh
description: >
  OracleNet is a mesh capability router for autonomous agents. Use when an
  agent needs to discover, route, verify, or pay for external capabilities
  through ToolOracle's machine-readable mesh — for example: blockchain
  intelligence, market and macro data, GPU pricing, research, sanctions
  screening, signed structured outputs, or optional regulated-evidence
  routing. Not a tool list. Not a single product. A routing layer.
tags:
  - capability-routing
  - agent-infrastructure
  - mcp
  - verification
  - x402
  - autonomous-agents
  - external-data
  - blockchain
  - mesh
category: infrastructure
license: MIT-0
homepage: https://tooloracle.io
repository: https://github.com/ToolOracle
---

# OracleNet — Mesh Capability Router

> A machine-readable entry point for autonomous agents to discover, route,
> verify, and (where supported) pay for external capabilities.

OracleNet is **not a tool list and not a single product**. It is a routing
layer. An agent describes what it needs in natural language; OracleNet
classifies the intent and returns a recommended capability route, along with
available pricing, verification, and contact metadata.

- **Identity:** `did:web:tooloracle.io`
- **Primary discovery card:** `https://tooloracle.io/.well-known/agent.json`
- **Live mesh snapshot:** `https://tooloracle.io/.well-known/agent-pulse`
- **Generic agent skill:** `https://tooloracle.io/skill.md`

## When to use this skill

Use OracleNet when an agent needs:

- **Blockchain intelligence** across multiple chains (read-only data, risk signals, DEX/DeFi state)
- **Research and external API access** without integrating dozens of providers individually
- **Verification metadata** for structured outputs (signatures and content hashes, where supported)
- **Workflow enrichment** (macro data, news, jobs, weather, maps, search)
- **Compute discovery** (GPU pricing and availability)
- **Market and macro intelligence** (FX, rates, commodities, indices)
- **Optional regulated-evidence capabilities** — available as a routed
  sub-layer (FeedOracle), explicitly opt-in. Most agents will not need it.

OracleNet returns structured data; interpretation is the agent's
responsibility. It is not a substitute for legal, financial, or compliance
advice.

## First call: soft handshake

The recommended first contact is a free, stateless soft handshake. No auth,
no payment, no registration:

```bash
curl -X POST https://tooloracle.io/handshake \
  -H "Content-Type: application/json" \
  -d '{"intent":"<one sentence describing what you need>"}'
```

The response includes a recommended `oracle`, a `routing` block with one or
more endpoints, and suggested `next_steps`. The handshake is intended for
machine-readable use only.

## After the handshake — discovery files

Read these. They are static, cached at the edge, and free to fetch:

| File | Purpose |
|---|---|
| `https://tooloracle.io/.well-known/deal-capabilities.json` | Supported interaction types and rules |
| `https://tooloracle.io/.well-known/pricing.json` | What is free, what may incur a charge |
| `https://tooloracle.io/.well-known/rewards.json` | Originator and referrer credit model (policy + enforcement status) |
| `https://tooloracle.io/.well-known/verification-policy.json` | Issuer, JWKS, signature handling |
| `https://tooloracle.io/.well-known/do-not-contact.json` | Domains and DIDs that must not be contacted |
| `https://tooloracle.io/.well-known/agent-pulse` | Live mesh snapshot (servers, tools, gravity score) |

Treat each `enforcement_status` field as authoritative. Where it says
`partial`, `planned`, or `may_be_available`, do not assume the mechanism is
fully operational on every route.

## Connecting OracleNet as an MCP server

OracleNet exposes a single LLM-routed MCP entry point:

```bash
# IronClaw / OpenClaw
ironclaw mcp add oraclenet https://tooloracle.io/quantum/mcp/

# Other MCP-aware agents: register the URL in your usual MCP config
```

After this, the agent can call `quantum_intent` with a natural-language
description and OracleNet will route to the appropriate underlying oracle.

## Payment

A free tier is available without registration; specifics are
route-dependent. Where a paid call is required, settlement uses the **x402**
protocol with USDC on Base. Common baseline is 0.01 USD per call, but
per-tool overrides apply — consult the per-tool MCP card.

Machine-to-machine access is designed around x402 and usage units. Any
legacy human checkout references are outside this agent pricing policy.

## Verification

```bash
curl https://tooloracle.io/.well-known/jwks.json
```

Where the per-tool MCP card declares signing support, the response carries
a signature (transport varies by tool — headers, body metadata, or
endpoint-specific receipts). The current JWKS is shared with the FeedOracle
layer (legacy state); a dedicated ToolOracle issuer key is planned but not
yet deployed. Verifiers should consult `verification-policy.json` for
authoritative guidance.

## Rewards and originator credits

OracleNet credits the agent that first surfaces a capability and the agent
that brings new paying users. Settlement is in **usage units, not cash**.
See `rewards.json` for current categories and per-mechanism
`enforcement_status`. Some mechanisms are policy-declared with partial
enforcement and are still being hardened.

## Rules of engagement

- OracleNet **respects** `https://tooloracle.io/.well-known/do-not-contact.json` for any outbound flow
- OracleNet **does not** initiate human outreach. Targets must be machine-readable
- Rate limits are route-specific and may be published in endpoint headers or MCP cards
- Opt-out is supported via the machine-readable inbox at `https://tooloracle.io/a2a/inbox` (consult inbox metadata before posting)

## What OracleNet does not claim

- Not an official NEAR partner or NEAR-integrated product
- Not affiliated with OpenClaw, IronClaw, or NEAR.ai as a partnership
- Does not guarantee that every listed capability is paid-call-ready in every interaction
- Does not provide investment, legal, or compliance advice
- Does not certify regulatory status for any third party

## Optional: regulated-evidence layer

For regulated-evidence flows (for example MiCA, DORA, AMLR scoring with full
evidence bundles), OracleNet routes to the FeedOracle sub-layer, which has
its own pricing and terms. Most agents will not need this. See `pricing.json
→ tiers.evidence_response` if it comes up.

## Quick reference

| Need | URL |
|---|---|
| Soft handshake | `POST https://tooloracle.io/handshake` |
| Capabilities & rules | `https://tooloracle.io/.well-known/deal-capabilities.json` |
| Pricing | `https://tooloracle.io/.well-known/pricing.json` |
| Rewards | `https://tooloracle.io/.well-known/rewards.json` |
| Verification | `https://tooloracle.io/.well-known/verification-policy.json` |
| JWKS | `https://tooloracle.io/.well-known/jwks.json` |
| Do-not-contact | `https://tooloracle.io/.well-known/do-not-contact.json` |
| Live mesh snapshot | `https://tooloracle.io/.well-known/agent-pulse` |
| Agent card (A2A v0.3) | `https://tooloracle.io/.well-known/agent.json` |
| Generic skill (NEAR/Agent-Market style) | `https://tooloracle.io/skill.md` |
| MCP entry point | `https://tooloracle.io/quantum/mcp/` |
| Partnership inbox (machine, supports opt_out) | `https://tooloracle.io/a2a/inbox` |
