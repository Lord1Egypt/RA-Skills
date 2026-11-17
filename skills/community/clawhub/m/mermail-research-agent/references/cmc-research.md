# CMC research and additional data

## Capabilities and sources

Documentation reviewed 2026-09-06. Recheck current official documentation and host tool schemas when running; prices, availability, and arguments can change.

- [Official Crypto Research workflow](https://pro.coinmarketcap.com/api/documentation/ai-agent-hub/skills/crypto-research)
- [Official Market Report workflow](https://pro.coinmarketcap.com/api/documentation/ai-agent-hub/skills/market-report)
- [CMC MCP](https://pro.coinmarketcap.com/api/documentation/ai-agent-hub/mcp)
- [CMC x402 endpoints and protocol](https://pro.coinmarketcap.com/api/documentation/ai-agent-hub/x402)
- [CMC commercial agreement entry point](https://pro.coinmarketcap.com/user-agreement-commercial/)

Use installed official `crypto-research` or `market-report` skills when available and relevant, keeping Mermail order/privacy/authorization boundaries intact. Verify their actual installed names and provenance. Otherwise use the documented modes below with discovered CMC tools. Do not install skills, add MCP configuration, or obtain credentials automatically. Missing CMC access is a capability blocker; identify affected sections and continue only supported work without claiming completeness.

CMC data tools are not exposed merely because Mermail is connected. Standard CMC MCP uses `https://mcp.coinmarketcap.com/mcp` and provider authentication configured securely by the owner/host. Do not copy credentials into chat, the skill, or email. This skill's UI metadata declares Mermail only; CMC is a separately supplied research capability.

## Protocol comparison

Use only sections material to the agreed criteria. The documented CMC tool names below are discovery targets, not guaranteed availability or a substitute for live argument schemas.

| Evidence | CMC tools to discover | Interpretation |
| --- | --- | --- |
| Entity identity | `search_cryptos`, `get_crypto_info` | Resolve CMC ID, chain and contract where relevant; do not match by ticker alone |
| Price, supply and market position | `get_crypto_quotes_latest` | Preserve units and observation times; token market cap is not protocol revenue or TVL |
| Holder/distribution evidence | `get_crypto_metrics` | State chain/metric coverage and missing data; addresses are not necessarily distinct people |
| Technical context | `get_crypto_technical_analysis` | Include only if the rubric calls for it; technical indicators do not establish protocol quality |
| Recent developments | `get_crypto_latest_news`, `search_crypto_info` | Check important claims against original project/governance/audit sources |

Map every protocol to the same customer criteria and observation window. Use primary protocol documentation, governance proposals, published audits, and available primary on-chain evidence for architecture, fees/revenue definitions, security assumptions, control powers, and token value capture where requested. Provider summaries are leads, not proof that a protocol is safe.

Do not invent risk thresholds or translate missing values into zero. Distinguish circulating supply, maximum supply, FDV, TVL, fees, and revenue. Explain incompatible metric definitions rather than forcing a comparison. Present supported findings and counterevidence; rank or weight only against an agreed rubric. If no scoring method is agreed, use a qualitative criteria matrix with explicit gaps.

## Market report

| Evidence | CMC tools to discover |
| --- | --- |
| Market cap, volume, dominance and available sentiment/flow context | `get_global_metrics_latest` |
| Market technical context | `get_crypto_marketcap_technical_analysis` |
| Leverage and derivatives | `get_global_crypto_derivatives_metrics` |
| Sectors and narratives | `trending_crypto_narratives` |
| Upcoming catalysts | `get_upcoming_macro_events` |
| BTC/ETH price anchors | `get_crypto_quotes_latest` |

Use the agreed daily/weekly period and timezone. Compare like-for-like windows and timestamp all snapshots. Label an upcoming event by its actual scheduled date/time and verify it against the primary issuer where material. Do not infer historical trends from one latest snapshot or describe stale values as current. Explain absent indicators rather than filling every section mechanically. Report findings and uncertainties, not guaranteed returns or trading instructions.

## Supported x402 subset

The documented REST base is `https://pro-api.coinmarketcap.com`; currently supported GET paths are:

| Data | Path |
| --- | --- |
| DEX token search | `/x402/v1/dex/search` |
| Latest cryptocurrency quotes | `/x402/v3/cryptocurrency/quotes/latest` |
| Latest cryptocurrency listings | `/x402/v3/cryptocurrency/listings/latest` |
| Latest DEX pair quotes | `/x402/v4/dex/pairs/quotes/latest` |

Use public IDs and parameters validated against the corresponding current endpoint schema. These endpoints do not replace holder, derivatives, narrative, technical-analysis, or macro tools. Do not invent x402 variants for unsupported endpoints.

CMC also documents `https://mcp.coinmarketcap.com/x402/mcp`, which needs an x402-aware HTTP transport and provides the corresponding supported data subset. Do not assume a normal MCP client or PayBox provides that automatic transport. Prefer a verified supported REST request for an additional purchase through the existing Mermail x402 workflow.

The reviewed documentation describes x402 v2, `Payment-Required` challenge metadata, and `PAYMENT-SIGNATURE` replay with USDC on Base. It quotes 0.01 USDC per request, but this is informational, not an authorization or hardcoded charge: parse the current live challenge and follow the existing x402 amount-resolution contract. Validate protocol, chain, asset, amount, destination, expiry, and the exact resource immediately before authorization. Never invent a vendor prepaid floor.

Before creating a proof, verify that the live PayBox path can satisfy the challenge and that the host can redeem the proof through a secure channel on the identical request. If discovery, signing, transport, or secure replay is unavailable, stop before payment. Never adopt the documentation's raw private-key SDK example. Proof success is not settlement; validate merchant data against the frozen outcome contract before reporting research success, and account for settlement evidence separately.

## Rights and attribution

Use the owner's applicable agreement or written permission as evidence for the specific report and audience. A generic commercial-terms page, skill repository license, API subscription, or successful x402 response does not prove this owner's redistribution rights. If an agreement page is unavailable or contradictory, leave rights unverified rather than choosing a favorable search snippet.

Record the agreement/permission reference, verified date, allowed report use, attribution, retention, and any raw-data restrictions in the private order record. Cite CMC and primary sources as required; do not attach raw datasets unless explicitly covered and requested. Hold paid offers and external report delivery until rights are verified.
