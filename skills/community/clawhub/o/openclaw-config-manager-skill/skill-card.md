## Description:

Provides OpenClaw configuration backup, restore, migration, Git version control, encryption, permission management, scheduling, change detection, and health-check guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wisdom-wozoy](https://clawhub.ai/user/wisdom-wozoy)

### License/Terms of Use:

MIT License

## Use Case:

Developers and operators use this skill to manage OpenClaw configuration backups, restores, migrations, Git-based change history, encrypted secret handling, and recovery workflows across environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Backup, remote sync, and auto-push workflows can expose sensitive configuration or credentials.

Mitigation: Use a private reviewed Git remote, exclude or encrypt secrets before backup, and test push behavior before enabling automation.

Risk: Restore and migration workflows can overwrite files or change permissions, especially when run with elevated privileges.

Mitigation: Preview restores in a staging directory, inspect affected files before applying changes, and avoid sudo restore unless the target files are known.

Risk: Scheduled backup and change-detection automation can preserve or propagate incorrect configuration state.

Mitigation: Start with manual backups, verify restore integrity, and add review gates before automatic pushes or scheduled production restores.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wisdom-wozoy/skills/openclaw-config-manager-skill)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with shell command, JSON, and code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include backup, restore, migration, Git, secret-management, validation, and troubleshooting steps.]

## Skill Version(s):

0.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
