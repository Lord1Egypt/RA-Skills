## Description:

Generates a comprehensive portfolio report for a wallet's Uniswap positions across supported chains, covering total value, PnL, fee earnings, impermanent loss, and composition.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wpank](https://clawhub.ai/user/wpank)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to summarize Uniswap liquidity positions for a wallet, including portfolio value, PnL, fees, impermanent loss, position status, and rebalance considerations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Portfolio reporting does not require private keys or seed phrases, but the security guidance warns users to avoid entering them for this skill.

Mitigation: Use a public wallet address for reporting and do not provide private keys, seed phrases, or signing credentials.

Risk: The skill relies on a delegated portfolio-analyst agent for the actual analysis.

Mitigation: Verify that the delegated portfolio-analyst agent is trusted and has appropriate permissions before running reports.

Risk: The security summary flags mutable install commands.

Mitigation: Prefer a pinned or signed install source and review release artifacts before installation.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/wpank/skills/portfolio-report)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown portfolio report with tabular and summary sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may include wallet-level totals, position details, PnL, fee earnings, impermanent loss, chain filters, and user-facing recommendations.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
