## Description:

Plan liquidity provision on PancakeSwap by gathering intent, checking token and pool data, assessing yield and risk signals, and producing a reviewable PancakeSwap liquidity deep link.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pcs-bot](https://clawhub.ai/user/pcs-bot)

### License/Terms of Use:

MIT-0

## Use Case:

External users and DeFi operators use this skill to plan PancakeSwap liquidity positions without writing code. It helps compare supported pool types, fee tiers, yield data, token verification requirements, and position ranges before the user reviews any wallet action.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends local environment metadata to pancakeswap.ai without a clear need.

Mitigation: Review the initialization behavior before installing and use the skill only if the disclosed network metadata is acceptable.

Risk: The skill can open live DeFi pages where wallet approvals or deposits may be requested.

Mitigation: Review every generated deep link, wallet approval, and deposit transaction before signing.

Risk: The security evidence flags imperfect shell-safety guidance around live commands.

Mitigation: Independently verify token addresses, approved domains, RPC URLs, and shell input handling before running commands.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/pcs-bot/skills/pcs-lp-planner)
- [Project Homepage](https://github.com/pancakeswap/pancakeswap-ai)
- [Data Providers Reference](references/data-providers.md)
- [Position Types Reference](references/position-types.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown guidance with shell command examples and PancakeSwap deep-link URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces planning guidance only; it does not execute transactions.]

## Skill Version(s):

1.0.1 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
