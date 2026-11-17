## Description:

Automatically backs up OpenClaw configuration data and supports manual backups, backup listing, rollback selection, and diff review before restoration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wuyuyang2](https://clawhub.ai/user/wuyuyang2)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to maintain local OpenClaw backups, inspect available snapshots, preview selected differences, and restore a prior configuration when recovery is needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can repeatedly archive sensitive OpenClaw state into local backup files.

Mitigation: Use only on trusted local storage, restrict backup directory access, and review retention behavior before installation.

Risk: Rollback can overwrite the live OpenClaw installation and interrupt related services.

Mitigation: Validate the selected backup and diff preview before restore, and keep the automatic pre-rollback backup available for recovery.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wuyuyang2/skills/openclaw-backup-rollback)
- [Publisher profile](https://clawhub.ai/user/wuyuyang2)
- [Artifact documentation](artifact/SKILL.md)
- [Plugin manifest](artifact/openclaw.plugin.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance and command responses with JSON-formatted script output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Operates on local OpenClaw backup archives and can create, list, diff, and restore backup files.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
