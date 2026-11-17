## Description:

Multi-device OpenClaw data synchronization using GitHub for managing workspace data sync across machines with automatic push on file changes, periodic pull, and conflict detection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[regulusz](https://clawhub.ai/user/regulusz)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to synchronize workspace data across multiple devices, configure GitHub-backed sync, monitor sync status, and resolve sync conflicts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run mutable remote shell code during installation.

Mitigation: Use the clone-and-inspect installation path and review the scripts before execution.

Risk: Default sync targets can include sensitive agent memory, instructions, and skills.

Mitigation: Use a private repository with tightly controlled write access, and avoid syncing SOUL.md, MEMORY.md, memory/, or skills/ unless remote changes to those files are intentional.

Risk: A persistent background process can automatically push and pull workspace changes.

Mitigation: Do not start the daemon until the auto-push and auto-pull behavior is understood and configured for the intended workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/regulusz/skills/multi-device-sync-github)
- [Troubleshooting](artifact/references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, markdown]

**Output Format:** [Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides operational guidance for installing, configuring, running, checking, and resolving GitHub-backed OpenClaw sync.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
