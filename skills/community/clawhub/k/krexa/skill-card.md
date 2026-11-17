## Description:

Research and backtest trading ideas, then request approval to deploy live agents through Krexa across supported venues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krexa](https://clawhub.ai/user/krexa)

### License/Terms of Use:

MIT-0

## Use Case:

External users can ask the agent to research a trading question, evaluate a strategy with backtests, monitor paper or live agents, and request a live deployment for their review and approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A configured daily loss control stops new buying but is not a guaranteed maximum loss; some venues also lack per-trade and daily dollar caps.

Mitigation: Check the actual venue controls before approving a deployment and consider requiring approval for each order.

Risk: Exposure of the Krexa agent key could allow unauthorized MCP actions.

Mitigation: Keep the key in an environment variable or secret store, protect it, and revoke it if exposed.

## Reference(s):

- [Krexa tools](references/tools.md)
- [Krexa limits](references/limits.md)
- [Connect Krexa to your agent](references/setup.md)
- [Krexa](https://krexa.xyz)
- [Krexa pricing](https://www.krexa.xyz/pricing)
- [Krexa Alpha Desk strategies](https://www.krexa.xyz/app/strategies)
- [Krexa Terminal](https://www.krexa.xyz/app/terminal)

## Skill Output:

**Output Type(s):** [Text, Analysis, Guidance]

**Output Format:** [Natural-language responses with research and backtest results, status details, and links when provided by Krexa.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports losses and limitations alongside results; backtests and paper runs do not promise future performance.]

## Skill Version(s):

1.5.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
