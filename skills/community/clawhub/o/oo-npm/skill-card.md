## Description:

npm (npmjs.com). Use this skill for ANY npm request — searching and reading data. Whenever a task involves npm, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and npm users can search the registry and retrieve package and version details, download statistics, the connected account name, and security advisories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: If the oo CLI is missing, setup instructions point to an online installer, while the external installer and hosted service remain unverified.

Mitigation: Independently verify the CLI release and require user approval before running a downloaded installer.

Risk: Using the connected npm account involves credential handling, npm permissions, and OOMOL billing.

Mitigation: Review the connection's scopes and permissions, and check billing before use.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [npm](https://www.npmjs.com/)
- [npm API documentation](https://api-docs.npmjs.com/)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Structured npm data and advisory results, with text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
