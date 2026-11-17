## Description:

Gleap (gleap.io). Use this skill for ANY Gleap request — reading, creating, updating, and deleting data. Whenever a task involves Gleap, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use the skill to read and manage Gleap contacts and tickets through their connected account, including creating, updating, and deleting records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup instructions can execute downloaded software without separate approval, and the remote installers were not audited.

Mitigation: Install a verified CLI release yourself and avoid automatically executing download-to-shell commands.

Risk: Gleap requests pass through the connected OOMOL account, and write or deletion actions can change account data.

Mitigation: Connect only the account and permissions needed, and get explicit approval before creating, updating, or deleting data.

## Reference(s):

- [Gleap Server API documentation](https://docs.gleap.io/documentation/server/api-overview)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [Gleap](https://www.gleap.io)

## Skill Output:

**Output Type(s):** [API calls, JSON, Shell commands, Guidance]

**Output Format:** [JSON connector requests and responses with Markdown guidance and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses include connector data and execution metadata; state-changing actions require user confirmation.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
