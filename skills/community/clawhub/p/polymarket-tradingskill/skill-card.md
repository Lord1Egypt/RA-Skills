## Description:

OpenClaw Decision Support helps users scan NBA and basic soccer Polymarket opportunities, view NBA fair pricing, and analyze a specific Polymarket market or event without making the final trading decision.

This skill is ready for commercial/non-commercial use.

## Publisher:

[a1594834522-coder](https://clawhub.ai/user/a1594834522-coder)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and agents use this skill to produce compact prediction-market review candidates, NBA fair-price views, and single-market analysis while leaving execution and final trading decisions to the user or a separate execution layer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Implicit invocation combined with bearer-token API use can expose prediction-market analysis in contexts the user did not intend.

Mitigation: Install only when implicit invocation is desired, keep tokens in user-managed configuration, use a narrow read-only token, and rotate any exposed token.

Risk: Plain HTTP endpoint examples are unsafe for non-local API hosts.

Mitigation: Use HTTPS for any non-local API endpoint.

Risk: Prediction-market analysis can be mistaken for a trading instruction.

Mitigation: Treat outputs as review candidates only; the skill should not place orders, manage wallets, or make final buy/sell decisions.

## Reference(s):

- [OpenClaw Decision-Support API Quick Reference](references/agent-api.md)
- [Decision-Support Contract](references/decision-contract.md)
- [ClawHub Skill Page](https://clawhub.ai/a1594834522-coder/skills/polymarket-tradingskill)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with structured JSON-style blocks and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only decision-support output; identifies review candidates and does not issue trade execution commands.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
