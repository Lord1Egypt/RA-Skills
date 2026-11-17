## Description:

Backup and restore OpenClaw workspace state and agents across machines using git.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anthonyfrancis](https://clawhub.ai/user/anthonyfrancis)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to back up, restore, migrate, and schedule recovery checkpoints for OpenClaw workspaces and agent folders across macOS and Linux systems.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented quick install and recovery flows pipe an unverified remote installer directly into a shell.

Mitigation: Use the clone-and-inspect installation path, review scripts before execution, and verify the remote repository before copying commands into a shell.

Risk: Backups can include identity, memory, agent files, scripts, configuration, and scheduled-task definitions.

Mitigation: Store checkpoints only in a private repository, keep credentials and tokens out of backups, and verify the generated ignore rules before the first backup.

Risk: Backup and restore commands modify local workspace state, agent folders, git history, and optional user-level scheduling.

Mitigation: Check status before restore, inspect the selected checkpoint, keep a separate copy of critical files, and disable scheduled backups when testing changes.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/anthonyfrancis/skills/openclaw-checkpoint)
- [OpenClaw Checkpoint Project Documentation](https://github.com/AnthonyFrancis/openclaw-checkpoint)
- [OpenClaw Project](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes platform-specific setup, backup, restore, scheduling, status, and recovery commands.]

## Skill Version(s):

1.0.5 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
