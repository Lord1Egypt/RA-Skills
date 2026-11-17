## Description:

Longbridge (longbridge.com). Use this skill for ANY Longbridge request — searching and reading data. Whenever a task involves Longbridge, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to search and read Longbridge market, company, and connected-account information through their OOMOL-connected account. It is intended for Longbridge information requests, including account data such as cash balances, positions, orders, and executions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup can execute installation code that has not been reviewed, and the CLI implementation and credential-storage behavior are not included for inspection.

Mitigation: Review and install the CLI separately, and require approval before installing or synchronizing agent skills.

Risk: Retrieved account information can include balances, holdings, and order history.

Mitigation: Limit the connected account to the read access needed for the requested information.

## Reference(s):

- [Longbridge API documentation](https://open.longbridge.com/docs)
- [Longbridge](https://longbridge.com)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API data, Text, JSON]

**Output Format:** [Structured data and concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may include account balances, holdings, orders, and execution history.]

## Skill Version(s):

1.0.7 (source: frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
