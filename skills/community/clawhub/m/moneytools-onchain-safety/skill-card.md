## Description:

Provides read-only EVM token facts and honeypot/sell-tax checks, plus an optional paid Wallet Risk Card for wallet sanctions, approvals, and risk grade that requires user approval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joe1993119](https://clawhub.ai/user/joe1993119)

### License/Terms of Use:

MIT-0

## Use Case:

People assessing an EVM token before buying it can review token facts and honeypot or sell-tax checks. People considering a wallet payment can request a Wallet Risk Card for sanctions and approval signals, with explicit approval required before the paid check.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan flags an unpinned `npx agentcash` invocation and a possible gap between paid-call confirmation claims and the call shown.

Mitigation: Review the paid-call flow and package installation method before installing; confirm the exact charge with the user before any paid call and review the AgentCash package/version being run.

## Reference(s):

- [MoneyTools agent documentation](https://tools.moneytools.dev/agents.md)
- [MoneyTools](https://tools.moneytools.dev)

## Skill Output:

**Output Type(s):** [Analysis, Guidance]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summarizes token or wallet risk indicators and stated scan limits.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
