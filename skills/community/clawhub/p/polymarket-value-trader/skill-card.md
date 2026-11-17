## Description:

Trade prediction markets on Simmer/Polymarket using value-based analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[czm200](https://clawhub.ai/user/czm200)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to research prediction markets, review Simmer or Polymarket positions, identify value-based opportunities, and prepare or execute trades through the Simmer API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use credentials to place real-money Polymarket trades, cancel orders, and redeem positions.

Mitigation: Default to paper-trading mode, use least-privilege credentials where available, and require explicit user confirmation before every live trade, venue switch, redemption, or order cancellation.

Risk: The required API key could be exposed if printed, logged, or stored in plaintext.

Mitigation: Store SIMMER_API_KEY only in approved secret storage and avoid echoing, logging, or embedding it in files.

Risk: The heartbeat workflow can create recurring authenticated monitoring and trading-related prompts.

Mitigation: Add heartbeat monitoring only when recurring checks are intended and document how to disable or remove the workflow.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/czm200/skills/polymarket-value-trader)
- [Publisher Profile](https://clawhub.ai/user/czm200)
- [Simmer Markets](https://simmer.markets)
- [Simmer API Base URL](https://api.simmer.markets)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration, API calls]

**Output Format:** [Markdown with shell command examples and concise trading analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include market tables, position summaries, trade theses, API requests, and configuration guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
