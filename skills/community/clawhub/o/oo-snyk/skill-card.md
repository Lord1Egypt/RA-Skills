## Description:

Use the connected Snyk account to search and read organization, project, principal, and issue data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security teams use this skill to read Snyk organizations, projects, and issues through an already connected account. It can help answer questions about the Snyk data available to that account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The fallback CLI installation runs unchecked remote code without separate approval and may make persistent agent skill changes.

Mitigation: Review and approve CLI installation separately, including automatic skill synchronization. Use a narrowly scoped Snyk credential and consider whether OOMOL should handle access to your security data.

## Reference(s):

- [Snyk](https://snyk.io)
- [Snyk API authentication documentation](https://docs.snyk.io/developer-tools/snyk-api/authentication-for-api)
- [oo CLI source repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Markdown]

**Output Format:** [Text summaries and structured JSON data from Snyk read actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the connected Snyk account's accessible data and permissions.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
