## Description:

Chattermill (chattermill.com). Use this skill for ANY Chattermill request — reading, creating, updating, and deleting data. Whenever a task involves Chattermill, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to inspect Chattermill projects and feedback data, and to create, update, or delete responses through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Initial setup directs users to run a remote CLI installer whose behavior is unverified.

Mitigation: Review the installer and release integrity before installing the CLI; do not allow automatic installation of additional skills without review.

Risk: The connected account can access Chattermill data and perform response writes or deletions.

Mitigation: Use appropriately limited account access and keep the skill's confirmation requirement for write and destructive actions.

## Reference(s):

- [Chattermill homepage](https://chattermill.com)
- [Chattermill API documentation](https://apidocs.chattermill.com/)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)
- [Chattermill skill release](https://clawhub.ai/oomol/skills/oo-chattermill)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [Markdown instructions with inline shell commands and JSON payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action schemas guide requests; writes and deletions require user confirmation.]

## Skill Version(s):

1.0.4 (source: frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
