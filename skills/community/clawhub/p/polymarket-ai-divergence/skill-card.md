## Description:

Find markets where Simmer's AI consensus diverges from the real market price, then trade on the mispriced side using Kelly sizing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[simmer](https://clawhub.ai/user/simmer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and trading agents use this skill to scan Polymarket and Kalshi-related market opportunities where Simmer AI consensus differs from external market prices, review divergence signals, and optionally execute position-sized trades.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live mode can place real-money trades and the artifact may redeem positions automatically when run.

Mitigation: Review settings before execution, run dry scans first, and use a dedicated low-balance wallet with conservative max bet, daily budget, and trade count limits.

Risk: WALLET_PRIVATE_KEY is highly sensitive when external-wallet trading is enabled.

Mitigation: Store private keys only in a trusted secret store or environment, never commit them, and rotate funds away from any exposed wallet.

Risk: The current artifact should not be relied on to trade only zero-fee markets.

Mitigation: Verify fee checks and configured endpoints before live trading, and independently confirm market fees when real funds are at risk.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/simmer/skills/polymarket-ai-divergence)
- [Simmer SDK API](https://api.simmer.markets)
- [Polymarket Gamma API](https://gamma-api.polymarket.com)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [CLI text tables, Markdown instructions, and optional JSON output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May place live trades when run with --live or when configured for a paper trading venue; requires SIMMER_API_KEY and may use WALLET_PRIVATE_KEY for external-wallet trading.]

## Skill Version(s):

2.3.0 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
