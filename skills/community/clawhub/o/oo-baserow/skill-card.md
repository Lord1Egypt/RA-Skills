## Description:

Baserow (baserow.io). Use this skill for ANY Baserow request — reading, creating, updating, and deleting data. Whenever a task involves Baserow, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to read and manage Baserow tables and rows through an OOMOL-connected account, including creating, updating, and deleting rows when requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup executes downloads whose source and integrity are unverified, and the CLI may affect installed agent skills beyond Baserow operations.

Mitigation: Use a verified, pinned CLI installation, review the exact deployed build, and consider disabling startup syncing with OO_SKILLS_SYNC_DISABLED=1. Limit the connected Baserow token to necessary tables and permissions, and retain approval for changes and deletions.

## Reference(s):

- [Baserow](https://baserow.io)
- [Baserow Database API documentation](https://baserow.io/user-docs/database-api)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [ClawHub skill release](https://clawhub.ai/oomol/skills/oo-baserow)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [JSON connector responses and shell commands with concise usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Connector responses include data and execution metadata; write and destructive actions require user confirmation.]

## Skill Version(s):

1.0.5 (source: frontmatter and server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
