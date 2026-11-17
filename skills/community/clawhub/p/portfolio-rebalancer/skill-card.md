## Description:

Calculate portfolio rebalancing trades to hit target allocations. Supports stocks, crypto, and mixed portfolios.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ianalloway](https://clawhub.ai/user/ianalloway)

### License/Terms of Use:

MIT-0

## Use Case:

Investors and portfolio managers can use the skill's Python examples to compare holdings with target allocations, inspect drift, and calculate proposed buy or sell quantities. The calculations run locally from supplied holdings, prices, and targets without accessing an account or placing trades.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Calculated trade proposals may be misleading when holdings are incomplete or prices and targets are invalid or out of date.

Mitigation: Provide every holding, current positive prices, and target allocations totaling 100%; review calculated trades manually before acting.

Risk: The examples do not account for transaction fees, taxes, or trading restrictions.

Mitigation: Account for applicable costs, tax consequences, and trading restrictions before acting on a proposal.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ianalloway/skills/portfolio-rebalancer)
- [Publisher profile](https://clawhub.ai/user/ianalloway)
- [Project homepage listed in skill metadata](https://github.com/ianalloway/openclaw-skills)

## Skill Output:

**Output Type(s):** [Text, Code, Shell commands, Guidance]

**Output Format:** [Textual portfolio summaries and proposed trade quantities, with Python code examples in Markdown instructions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Calculations use manually supplied holdings, target allocations, and prices; no account connection or trade execution.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
