## Description:

Find and analyze arbitrage opportunities across prediction markets like Polymarket and Kalshi.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aisadocs](https://clawhub.ai/user/aisadocs)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use this skill to find matching prediction markets, compare Polymarket and Kalshi prices, and evaluate whether observed spreads have enough orderbook depth to be actionable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API-key exposure could matter in environments where redirects or shared execution logs are not controlled.

Mitigation: Use a scoped, low-credit AIsa API key and wrap or harden HTTP clients so Authorization headers are not forwarded after cross-origin redirects.

Risk: Wallet, position, and P&L lookups can reveal sensitive wallet activity beyond the core arbitrage workflow.

Mitigation: Query only wallets the operator is authorized to analyze, minimize retained output, and avoid sharing results outside the approved workflow.

Risk: Example cURL commands contain brace placeholders that can be interpreted by curl if executed literally.

Mitigation: Check that every placeholder such as {token_id}, {market_ticker}, {sport}, and {date} is replaced with a concrete value before command execution.

Risk: Displayed spreads may be misleading if liquidity, fees, slippage, or market-resolution terms are not checked before trading.

Mitigation: Verify orderbook depth and market terms on each platform before treating any spread as actionable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/aisadocs/skills/polymarket-arb)
- [AIsa API Reference](https://docs.aisa.one/reference/)
- [AIsa](https://aisa.one)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, shell commands, and JSON CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AISA_API_KEY; the bundled CLIs call read-oriented market, orderbook, wallet, and P&L endpoints and can emit JSON.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
