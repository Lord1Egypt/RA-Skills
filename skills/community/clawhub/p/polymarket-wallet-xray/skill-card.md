## Description:

X-ray any Polymarket wallet for skill level, entry quality, bot detection, arbitrage research, trader-profile comparison, and edge analysis. Queries Polymarket's public APIs with no authentication; use for research, not blind copytrading, and never assume past returns predict future results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[simmer](https://clawhub.ai/user/simmer)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to inspect or compare public Polymarket wallets' historical activity, trading patterns, and heuristic metrics for research. It can also read the caller's own Simmer account status when explicitly requested and configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Historical ratings and metrics are estimates based on the fetched activity window; incomplete data, small samples, fees, slippage, and changing market conditions can make them misleading as trading signals.

Mitigation: Use reports for research, review sample size and data limits, account for fees, and validate conclusions with fresh information; do not blindly copy positions or assume past returns will continue.

Risk: The optional account-status report contains private financial information, and its API key grants access to that account data.

Mitigation: Only configure SIMMER_API_KEY outside chat when requesting your own status, never paste or print the key, and handle the resulting report as private.

## Reference(s):

- [The Autopsy: How to Read the Mind of a Polymarket Whale](https://x.com/thejayden/status/2020891572389224878)
- [Simmer API Overview](https://docs.simmer.markets/api/overview)
- [Polymarket Wallet X-Ray on ClawHub](https://clawhub.ai/simmer/skills/polymarket-wallet-xray)

## Skill Output:

**Output Type(s):** [Analysis, Text, JSON]

**Output Format:** [Console text or JSON report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Historical wallet metrics and heuristic ratings; optional two-wallet comparison and trade limit.]

## Skill Version(s):

1.1.11 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
