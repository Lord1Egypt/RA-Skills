## Description:

Use the OOMOL-connected Asana account to read, create, update, and delete Asana data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Individuals and teams use the skill to retrieve and manage Asana work, including tasks, projects, comments, users, tags, and attachments, through a connected Asana account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The fallback setup uses mutable downloaded code, and the reviewed setup does not establish clear approval or limits for local changes.

Mitigation: Review the setup steps, verify the oo CLI release, and control automatic skill synchronization before installing.

Risk: The connected account grants the workflow access to Asana data and may allow changes or deletions.

Mitigation: Connect an appropriately limited Asana account and keep confirmation requirements for changes and deletions.

## Reference(s):

- [Asana](https://asana.com)
- [Asana API documentation](https://developers.asana.com/reference/rest-api-reference)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [Asana skill on ClawHub](https://clawhub.ai/oomol/skills/oo-asana)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [JSON action requests and responses with concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions may read or change Asana data; write and destructive actions require user confirmation.]

## Skill Version(s):

1.0.7 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
