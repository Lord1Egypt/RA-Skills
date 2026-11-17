## Description:

Sendbird (sendbird.com). Use this skill for ANY Sendbird request — reading, creating, updating, and deleting data. Whenever a task involves Sendbird, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use the skill to read and manage Sendbird users, channels, and messages through an OOMOL-connected account. Changes and deletions require confirmation before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The missing-command fallback runs a remote CLI installer without a separate approval step; the remote installer and hosted connector were not audited in the supplied evidence.

Mitigation: Review and approve CLI installation before allowing the fallback, check settings for installing or synchronizing other agent skills, and use narrowly scoped Sendbird access. Keep the documented confirmation step for changes and deletions.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Sendbird Platform API documentation](https://sendbird.com/docs/chat/platform-api/v3/prepare-to-use-api)
- [Sendbird](https://sendbird.com)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Guidance]

**Output Format:** [JSON responses and Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read results and action outcomes; writes and deletions require user confirmation]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
