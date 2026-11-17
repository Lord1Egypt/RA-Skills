## Description:

Risk assessment engine for AI agents. Value at Risk (VaR), CVaR, stress testing, and multi-factor risk scoring. Monte Carlo powered. Built for trading agents, lending agents, and portfolio managers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[whatsonyourmind](https://clawhub.ai/user/whatsonyourmind)

### License/Terms of Use:

MIT-0

## Use Case:

External agents and developers use this skill to estimate downside financial exposure for portfolios, trades, lending decisions, and stress scenarios. It produces decision-support risk measures such as VaR, CVaR, per-asset contribution, default probability, and stress-test outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Portfolio, trading, or credit-risk data may be shared with the OraClaw service.

Mitigation: Confirm the service is trusted for the data being submitted, and avoid sending sensitive data unless appropriate controls and approvals are in place.

Risk: Financial risk outputs may be mistaken for guaranteed loss limits or financial advice.

Mitigation: Treat VaR, CVaR, default probability, and stress-test results as decision support and review assumptions before acting on them.

Risk: The skill discloses paid API usage.

Mitigation: Review pricing and API-key access before enabling the skill in an automated workflow.

## Reference(s):

- [OraClaw Risk homepage](https://oraclaw.dev/risk)
- [ClawHub skill page](https://clawhub.ai/whatsonyourmind/skills/oraclaw-risk)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown or text guidance with structured risk metrics and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ORACLAW_API_KEY and discloses paid API usage in USDC.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
