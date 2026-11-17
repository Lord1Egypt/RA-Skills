## Description:

Audit PancakeSwap liquidity positions before capital is deployed, evaluating depth, concentrated-liquidity setup, range risk, pool quality, and approval friction before users provide liquidity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[duclawbot](https://clawhub.ai/user/duclawbot)

### License/Terms of Use:

MIT-0

## Use Case:

External liquidity providers, DeFi users, and operators use this skill to review PancakeSwap pools and concentrated-liquidity positions before committing capital. It helps structure decisions around pool depth, range risk, fee-tier suitability, and whether to deploy, widen, reduce, monitor, or avoid a position.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat deploy, widen, reduce, monitor, or avoid language as financial advice.

Mitigation: Present outputs as educational DeFi risk analysis only and require independent review before committing capital.

Risk: Pool assessments can be incomplete when live pool data, fee tier, intended size, or range details are missing.

Mitigation: Ask for missing pool context, avoid false precision, and tell users to verify current pool data independently.

Risk: The skill does not perform smart-contract, wallet-security, tax, legal, or formal underwriting review.

Mitigation: Route those checks to qualified review processes and separate security tooling before liquidity deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/duclawbot/skills/pancakeswap)
- [ClawHub Publisher Profile](https://clawhub.ai/user/duclawbot)
- [README](artifact/README.md)
- [Examples](artifact/examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown assessment with pool quality, risk concerns, recommendation, and next-check sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only decision support; no wallet access, smart-contract calls, trade execution, or persistence.]

## Skill Version(s):

1.0.0 (source: skill.md frontmatter, skill.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
