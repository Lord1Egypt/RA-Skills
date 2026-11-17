## Description:

Massive (Polygon.io) (massive.com). Use this skill for ANY Massive (Polygon.io) request — searching and reading data. Whenever a task involves Massive (Polygon.io), use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and market researchers use this skill to retrieve stock, options, company, and economic data from Massive (Polygon.io) through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup executes downloaded code and its effects on the agent environment are not fully verified.

Mitigation: Review the CLI separately, approve installation, and prefer a pinned, verified release. Consider setting OO_SKILLS_SYNC_DISABLED=1 to prevent startup skill synchronization.

Risk: Connecting an account and running actions can incur OOMOL credit costs.

Mitigation: Connect only the intended account and consider credit costs before running actions.

## Reference(s):

- [Massive API documentation](https://massive.com/docs)
- [Massive](https://massive.com/)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [JSON, Text, Guidance]

**Output Format:** [JSON market-data responses with concise text summaries or guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Data fields vary by requested action and asset class.]

## Skill Version(s):

1.0.6 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
