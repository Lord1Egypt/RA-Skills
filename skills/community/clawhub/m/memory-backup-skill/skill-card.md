## Description:

Lobster Memory Backup & Sync helps an agent write important conversation context into structured memory files, synchronize memories across channels, and back them up to a user-configured Git remote.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nmww](https://clawhub.ai/user/nmww)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to preserve useful agent conversation memory, project context, and reusable workflows across OpenClaw sessions. It is intended for users who want Git-backed backup and restore of structured memory files across machines or channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conversation memory, profile files, and workflow notes can be committed and pushed to a user-configured Git remote, which may expose sensitive personal or project context.

Mitigation: Use a private repository, a dedicated least-privilege SSH key, and review diffs before each push.

Risk: Automatic or scheduled backup can push memory files without reliable user confirmation.

Mitigation: Avoid cron or other unattended execution until the backup flow fails closed without approval.

Risk: The built-in secret scanner is not complete protection against leaking credentials.

Mitigation: Do not write actual API keys, passwords, tokens, or private keys into memory files; store only credential locations or rotation status and independently review content before syncing.

## Reference(s):

- [Lobster Memory Backup & Sync ClawHub release](https://clawhub.ai/nmww/skills/memory-backup-skill)
- [Memory structure reference](references/memory-structure.md)
- [Setup guide](references/setup-guide.md)
- [Workflow backup guide](references/workflows.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces or updates structured local memory files and can invoke bundled shell scripts for synchronization and Git backup.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
