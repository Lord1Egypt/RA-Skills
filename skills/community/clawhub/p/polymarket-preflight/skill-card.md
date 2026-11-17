## Description:

Read-only pre-trade risk checks for Polymarket orders and wallet copy decisions using TickTape's JSON API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[padak](https://clawhub.ai/user/padak)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading agents use this skill before Polymarket trades to check slippage, depth, taker fees, safe order size, wallet copyability, and leaderboard or red-list signals. It is for preflight risk review and does not provide custody, execution, price prediction, or investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional npm SDK is an unpinned supply-chain dependency.

Mitigation: Prefer direct HTTPS calls where possible, or pin the npm package version before using the SDK.

Risk: Live x402 calls and prepaid credit purchases can spend real money.

Mitigation: Use the free sandbox first, enforce per-call and per-session spend caps, and verify payment terms before signing.

Risk: Prepaid TickTape bearer tokens grant paid API access.

Mitigation: Treat tokens like private keys: keep them in environment variables, do not log or commit them, and rotate by buying a new pack when needed.

Risk: Repeated paid calls can buy unchanged leaderboard, red-list, or queued wallet results.

Mitigation: Respect next_refresh_at and retry_after_seconds values, and avoid tight retry loops.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/padak/skills/polymarket-preflight)
- [TickTape Homepage](https://ticktape.cc)
- [TickTape Authentication and Payments](https://ticktape.cc/auth.md)
- [TickTape Verification Runbook](https://ticktape.cc/why.md)
- [TickTape OpenAPI Specification](https://ticktape.cc/openapi.json)
- [TickTape Agent Metadata](https://ticktape.cc/agent.json)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown guidance with HTTP request examples and JSON response expectations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only integration guidance; live API calls may require x402 payment or a prepaid bearer token.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
