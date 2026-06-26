---
name: intelica
version: 4.5.2
description: >
  Competitive intelligence API for autonomous AI agents. Analyzes any URL or
  company description and returns structured JSON with market positioning, pain points,
  competitors, battlecard, verified sources, market signals, and executable Market Score.
  Pay-per-call via x402 on Base and Solana mainnet. Trial key available — no wallet required for first 5 calls.
  WARNING: Submitted data is sent to api.intelica.dev (third party). Use only for public companies. Do not submit confidential, regulated, or proprietary data. Paid calls ($0.05-$1.00 USDC) require budget controls before autonomous use.
trigger: >
  Use ONLY when an agent explicitly needs structured competitive intelligence on a specific named company, product, or market — and the user or pipeline has approved external data submission and potential paid API calls. Do NOT invoke for general questions, internal strategy, confidential data, or when local reasoning is sufficient.
requires: []
env: []
---

# Intelica — Competitive Intelligence Skill

> **⚠️ DATA PRIVACY NOTICE:** This skill sends the provided company name, URL, description, and context to the Intelica API (api.intelica.dev), a third-party service. Do NOT submit confidential business plans, proprietary strategy, regulated data (HIPAA, GDPR-sensitive), or personally identifiable information. Use only for publicly available companies and markets. Paid calls ($0.05–$1.00 USDC) are made autonomously when a payment method is configured — set budget controls before enabling autonomous use.

Intelica returns structured competitive intelligence for a specific named company or market. Invoke only when the agent has a clear, scoped target and the user has approved external data submission.

## When to use

- Agent needs competitor analysis on a **specific named company** before a strategic decision
- Founder needs a market entry report for a specific new geography
- Agent is evaluating a **specific** DeFi protocol before entering a position
- Sales agent needs a battlecard for a **specific** upcoming demo
- VC agent screening a **specific** investment opportunity
- Compliance officer evaluating regulatory risk for a **specific** company or product

## When NOT to use

- General market questions without a specific named target
- Internal strategy or confidential business planning
- Regulated or sensitive data (medical records, financial PII, legal documents)
- When local reasoning or public knowledge is sufficient
- Without explicit user approval for third-party data submission

## Budget controls (important for autonomous agents)

- Standard analysis: $0.05 USDC per call
- Elite analysis: $1.00 USDC per call
- Batch (up to 10): $0.20 USDC
- Always use `/demo` (free) to validate before enabling paid autonomous calls
- Set `operator_id` to enforce daily budget limits per pipeline
- Results cached 6 hours — same company twice costs once

## How to call

### Step 0 — Get free trial key (no wallet needed)
```
GET https://api.intelica.dev/api-keys/trial
→ {"key": "ikey_trial_...", "calls_remaining": 5, "expires_at": "..."}

# Use immediately — extract response.key and pass as X-API-KEY header
```

### Step 1 — Free demo (no payment, no key)
```
POST https://api.intelica.dev/demo
Content-Type: application/json

{
  "text": "Notion is an all-in-one workspace for teams",
  "mode": "competitive"
}
```

### Step 2 — Full analysis with trial key
```
POST https://api.intelica.dev/intel
X-API-KEY: ikey_trial_...
Content-Type: application/json

{
  "text": "Notion is an all-in-one workspace for teams",
  "mode": "competitive"
}
```

### Step 3 — Full analysis with x402 payment
```
POST https://api.intelica.dev/intel
Content-Type: application/json

{
  "url": "https://notion.so",
  "mode": "competitive",
  "context": "I'm building a note-taking app for developers"
}
# Returns HTTP 402 with Base + Solana payment options
# After payment, retry with X-PAYMENT header
```

### Step 4 — Batch (up to 10 analyses for $0.20)
```
POST https://api.intelica.dev/batch
X-PAYMENT: <x402 signed payment>
Content-Type: application/json

{
  "items": [
    { "url": "https://notion.so", "mode": "competitive" },
    { "text": "Coda collaborative doc platform", "mode": "acquisition" }
  ]
}
```

## Context Modes

| Mode | Price | Use when |
|------|-------|----------|
| `competitive` | $0.05 | Standard competitor analysis (default) |
| `fundraising` | $0.05 | Investor narrative, TAM, traction signals |
| `partnership` | $0.05 | Strategic fit — complement or rival? |
| `acquisition` | $0.05 | Due diligence — moat, technical risk |
| `market_entry` | $0.05 | Market gaps, saturation, barriers to entry |
| `crypto_protocol` | $0.05 | DeFi moat, tokenomics, regulatory risk |
| `market_entry_execution` | $1.00 | Execution plan — partners, budget, week-1 actions |
| `venture_screening` | $1.00 | Investment thesis + deal-breakers |
| `regulatory_compliance` | $1.00 | EU AI Act, GDPR, HIPAA exposure |
| `risk_assessment` | $1.00 | Business model stability, operational risk |
| `sales_enablement` | $1.00 | Battlecard + objection handler |

## Response trust protocol (M2M)

The response includes root-level fields for programmatic trust validation:

```json
{
  "sources": ["url1", "url2"],
  "confidence": "high | medium | low",
  "market_score": {
    "threat_level": "high | medium | low",
    "moat_strength": 0.72,
    "agent_recommendation": "monitor | counter | partner | acquire"
  },
  "analysis": { ... }
}
```

Agent decision pipeline:
1. Check `sources[]` — if fewer than 2 URLs, treat confidence as low
2. Check `confidence` — if low, do not execute autonomous actions
3. Check `market_score.agent_recommendation` — use as primary action signal
4. Read `analysis{}` for full context

## Output fields

```json
{
  "analysis": {
    "company_or_product": "string",
    "positioning_summary": "string",
    "target_customer": "string",
    "core_value_props": ["string"],
    "user_pain_points": ["string"],
    "detected_competitors": ["string"],
    "unique_angle": "string",
    "confidence": "high | medium | low",
    "sources": ["url1", "url2", "url3"],
    "market_score": {
      "threat_level": "high | medium | low",
      "moat_strength": 0.0,
      "market_maturity": "emerging | growing | mature | declining",
      "agent_recommendation": "monitor | counter | ignore | partner"
    }
  },
  "model": "claude-sonnet-4-6 | claude-haiku-4-5-20251001",
  "tier": "elite | standard",
  "mode": "string",
  "detected_language": "en | es | pt | de | fr | it | ja | ko | zh"
}
```

## Payment details

- Networks: Base mainnet + Solana mainnet
- Standard: $0.05 USDC / Elite: $1.00 USDC / Batch: $0.20 USDC
- Trial: GET /api-keys/trial — 5 free calls, no wallet required
- x402 manifest: https://api.intelica.dev/.well-known/x402.json

## Links

- Live API: https://api.intelica.dev
- OpenAPI: https://api.intelica.dev/openapi.json
- Full reference: https://api.intelica.dev/llms-full.txt
- Try: https://teodorofodocrispin-cmyk.github.io/Intelica-docs/try.html
