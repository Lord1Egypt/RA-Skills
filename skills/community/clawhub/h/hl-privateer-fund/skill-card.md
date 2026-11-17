## Description:

Access HL Privateer, an open agentic Hyperliquid discretionary trading desk, to read live positions, AI analysis, copy-trade signals, and risk state through x402 pay-per-call endpoints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adwilkinson](https://clawhub.ai/user/adwilkinson)

### License/Terms of Use:

proprietary

## Use Case:

External agents and developers use this skill to read HL Privateer trading positions, AI analysis, risk state, copy-trade signals, and WebSocket floor events for copy trading, signal integration, monitoring, or portfolio research. Paid agent routes use x402 payments in USDC on Base; public routes expose limited status without payment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill involves paid x402 requests for trading data and may cause unintended wallet spending if calls are automated without review.

Mitigation: Use an isolated low-balance wallet, require explicit confirmation for each paid request, and verify payment recipient, asset, network, amount, and resource before signing.

Risk: Trading signals, copy-trade data, and AI analysis may be interpreted as actionable financial advice or copied without independent risk review.

Mitigation: Use outputs as informational trading data only, apply independent risk controls, and require human approval before any live trading action.

Risk: Artifact documentation includes operator and command surfaces that could affect trading controls if credentials or live command channels are exposed to an autonomous agent.

Mitigation: Do not provide operator credentials or live trading command channels to autonomous agents; restrict use to user-requested read-only trading-data lookups unless separately reviewed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/adwilkinson/skills/hl-privateer-fund)
- [HL Privateer Web UI](https://hlprivateer.xyz)
- [Skill Definition](https://hlprivateer.xyz/skills/hl-privateer.md)
- [API Reference](https://hlprivateer.xyz/skills/api.md)
- [x402 Payment Guide](https://hlprivateer.xyz/skills/x402.md)
- [Machine-Readable Discovery](https://hlprivateer.xyz/skills/agents.json)
- [Agent Quick Start](https://hlprivateer.xyz/skills/llms.txt)
- [x402 Protocol Documentation](https://x402.org)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, API calls]

**Output Format:** [Markdown guidance with JSON schemas, REST and WebSocket endpoint descriptions, and code or curl examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires network access to api.hlprivateer.xyz and paid x402 requests for agent endpoints.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
