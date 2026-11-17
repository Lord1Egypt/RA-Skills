## Description:

Provides agents with AIsa-backed commands and examples for querying Polymarket and Kalshi markets, prices, trades, orderbooks, positions, wallet data, and cross-platform sports market matches.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chaimengphp](https://clawhub.ai/user/chaimengphp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve prediction-market data for research, market monitoring, trading analysis, portfolio review, and cross-platform comparison across Polymarket and Kalshi.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries can send market searches, wallet addresses, portfolio data, and P&L lookups to the AIsa API using a bearer API key.

Mitigation: Use the skill only with wallets you own or are authorized to analyze, avoid retaining wallet results unnecessarily, and keep AISA_API_KEY out of logs and shared transcripts.

Risk: The supplied security summary flags insufficient privacy and credential-safety guardrails for a valuable API key.

Mitigation: Review credential handling before deployment, restrict the API key's exposure, and harden redirect handling before using the skill in sensitive or high-value environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chaimengphp/skills/openclaw-aisa-prediction-market)
- [AIsa API Reference](https://docs.aisa.one/reference/)
- [OpenClaw homepage](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, Python CLI examples, curl examples, and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AISA_API_KEY; examples query AIsa endpoints for market, price, trade, orderbook, wallet, position, P&L, and sports matching data.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
