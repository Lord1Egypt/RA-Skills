## Description:

Securely migrate OpenClaw Agent configuration, memory, and skills to a new machine.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wenjie2024](https://clawhub.ai/user/wenjie2024)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to package existing agent state into an encrypted portable archive and restore it on another machine.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Restoring an archive can overwrite persistent OpenClaw agent state.

Mitigation: Restore into a clean or temporary destination first and keep backups of existing OpenClaw state before importing.

Risk: Archives may contain sensitive configuration, credentials, memory, and workspace data.

Mitigation: Use only archives you created and trust, store archive passwords securely, and avoid passing passwords directly on the command line.

Risk: The server security verdict is suspicious because restore behavior and secret handling are not scoped enough for automatic approval.

Mitigation: Review and test the tool before installation or deployment in any environment that contains sensitive agent data.

## Reference(s):

- [Artifact README](artifact/README.md)
- [OpenClaw Migrator ClawHub Page](https://clawhub.ai/wenjie2024/skills/openclaw-migrator)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with shell commands; encrypted .oca archive files when executed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Archives may contain sensitive OpenClaw configuration, credentials, memory, and workspace state.]

## Skill Version(s):

1.0.0 (source: server release metadata; package.json reports 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
