## Description:

SureContact (surecontact.com). Use this skill for ANY SureContact request — reading, creating, updating, and deleting data. Whenever a task involves SureContact, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

SureContact users and their agents use this skill to retrieve and manage contacts, lists, and tags, including creating, updating, and deleting records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute remote CLI installers whose contents have not been verified.

Mitigation: Review the CLI installation separately and use a verified release.

Risk: Automatic skill synchronization may introduce broader changes to agent skills.

Mitigation: Decide whether to permit synchronization and use the documented disable setting when appropriate.

Risk: Write and destructive actions can change or remove SureContact data.

Mitigation: Connect only the intended SureContact account and approve the exact changes and deletion targets.

## Reference(s):

- [SureContact homepage](https://surecontact.com/)
- [SureContact API documentation](https://api.surecontact.com/docs)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [oo CLI environment variables](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md#environment-variables)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [SureContact connector results as JSON with concise text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions can read or modify contacts, lists, and tags; write and destructive operations require confirmation.]

## Skill Version(s):

1.0.5 (source: server-resolved release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
