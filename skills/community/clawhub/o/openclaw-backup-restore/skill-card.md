## Description:

Backup and restore OpenClaw configuration, agents, sessions, and workspace to/from a private Git repository.

This skill is ready for commercial/non-commercial use.

## Publisher:

[darinrowe](https://clawhub.ai/user/darinrowe)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and administrators use this skill to manually back up OpenClaw state to a private Git repository, migrate to a new machine, or restore a previous environment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Backups can upload broad OpenClaw state, which may include secrets or private conversations.

Mitigation: Use only a private repository you fully control, review exclusions before backup, and add secret filtering or client-side encryption for safer use.

Risk: Restore can copy remote repository content into the live OpenClaw environment and run follow-up commands.

Mitigation: Restore only from a trusted repository, preview diffs first, prefer restoring into a staging directory, and gate automatic dependency installation and doctor repair commands.

## Reference(s):

- [OpenClaw Backup & Restore on ClawHub](https://clawhub.ai/darinrowe/skills/openclaw-backup-restore)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and operational steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces backup and restore instructions that may execute local shell scripts against OpenClaw state.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
