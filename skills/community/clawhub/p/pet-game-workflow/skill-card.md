## Description:

Defines a Pet-Game project workflow for agent-managed file backups, element snapshot tracking, and post-commit backup cleanup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marszxf](https://clawhub.ai/user/marszxf)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill while working on the Pet-Game project to run prescribed backups before edits, track repeated element changes, and clean backup state after commits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow directs agents to run a local Python wrapper that imports backup_core from a hardcoded external path.

Mitigation: Review or vendor the backup_core implementation before installation and only run the wrapper in trusted project environments.

Risk: The wrapper accepts relative paths for backup, restore, list, and clean operations.

Mitigation: Restrict usage to the intended Pet-Game project directory and add confirmation before restore or clean operations.

Risk: The skill asks agents to execute backup commands automatically during edits and after commits.

Mitigation: Confirm the backup policy with the project owner and monitor command execution until the local backup behavior is trusted.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/marszxf/skills/pet-game-workflow)
- [Publisher profile](https://clawhub.ai/user/marszxf)
- [Skill instructions](artifact/SKILL.md)
- [Backup wrapper](artifact/backup_wrapper.py)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent workflow rules for local backup, restore, listing, and cleanup operations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
