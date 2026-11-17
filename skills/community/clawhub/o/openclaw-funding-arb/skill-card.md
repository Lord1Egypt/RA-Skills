## Description:

Runs and maintains a MEXC stock-contract funding-rate arbitrage bot with timed opening and closing, funding-rate threshold filtering, stock whitelist filtering, U.S. regular-session shutdown windows, and persisted open-position recovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linshengyyy](https://clawhub.ai/user/linshengyyy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and trading operators use this skill to deploy, run, tune, troubleshoot, or modify a MEXC funding-rate arbitrage workflow that can place live market orders with user-provided API credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place live leveraged MEXC trades with user credentials, which can expose funds to market, liquidation, and automation risk.

Mitigation: Use a restricted MEXC API key with no withdrawal permission, set explicit exposure caps before live runs, and test with the smallest possible balance or sandbox-like setup first.

Risk: The security summary says the bot lacks mandatory safety controls for live automated trading.

Mitigation: Review all trading parameters before execution, configure conservative exposure limits such as maximum open volume or notional value, and monitor persisted open-position state during operation.

Risk: Overriding the API base URL can send credentials or orders to an unintended endpoint.

Mitigation: Do not override the default MEXC contract API base URL unless the endpoint has been explicitly reviewed and approved.

## Reference(s):

- [MEXC Contract API Endpoint](https://contract.mexc.com)
- [OpenClaw 资金费套利 on ClawHub](https://clawhub.ai/linshengyyy/skills/openclaw-funding-arb)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands, code snippets, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include environment variable settings, Python execution commands, troubleshooting steps, and focused script modification guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
