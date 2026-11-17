## Description:

Analyzes wallet portfolios on supported blockchains by retrieving token holdings, transaction activity, PnL statistics, total net worth, and authenticated LiberFi TEE wallet portfolio data through the LiberFi CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bombmod](https://clawhub.ai/user/bombmod)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to inspect public wallet holdings, activity, PnL, and net worth, or to review their authenticated LiberFi TEE wallet portfolio without supplying an address.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructs agents to silently install a global, unpinned LiberFi CLI.

Mitigation: Require explicit user approval before installation and prefer a pinned or locally isolated CLI package.

Risk: Authenticated me commands can access the user's LiberFi TEE wallet portfolio data.

Mitigation: Run these commands only after confirming user intent and authentication status, and never request private keys or seed phrases.

Risk: Portfolio values and PnL statistics may be historical or stale.

Mitigation: Present results as wallet analysis rather than investment advice and note when values may not reflect real-time market conditions.

## Reference(s):

- [LiberFi homepage](https://liberfi.io)
- [ClawHub skill page](https://clawhub.ai/bombmod/skills/liberfi-portfolio)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown summaries with JSON-backed LiberFi CLI command results and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses structured CLI output via --json; authenticated me commands require a valid LiberFi session.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact metadata version is 0.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
