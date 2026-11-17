## Description:

Ordinal (tryordinal.com). Use this skill for ANY Ordinal request — searching and reading data. Whenever a task involves Ordinal, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users can ask an agent to read and search information in a connected Ordinal workspace, including ideas, posts, users, labels, and workspace or profile details. The skill guides the agent to inspect each action's live schema and returns the connector's JSON response.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: If the oo CLI is missing, the setup guidance can lead to a remote installer running without a separate approval step; the installer contents and hosted connector behavior were not verified.

Mitigation: Review and approve a fixed installer or release separately, and inspect any bundled-skill changes before installation.

Risk: Ordinal requests pass through OOMOL and may incur usage charges.

Mitigation: Restrict the connected Ordinal account to the access needed for the task and account for applicable usage charges.

## Reference(s):

- [Ordinal homepage](https://www.tryordinal.com)
- [Ordinal API documentation](https://docs.tryordinal.com/api/introduction)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [Ordinal on ClawHub](https://clawhub.ai/oomol/skills/oo-ordinal)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [Connector JSON responses with concise Markdown action guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses contain action data and may include execution metadata.]

## Skill Version(s):

1.0.5 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
