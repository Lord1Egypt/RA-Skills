## Description:

Safe OpenClaw upgrade procedure with backup, doctor fix, service migration, rollback, and post-upgrade testing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gjoham](https://clawhub.ai/user/gjoham)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to plan, execute, validate, and roll back OpenClaw upgrades while reducing risk from Dashboard upgrade failures, service entrypoint changes, and configuration migrations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential and agent backups may expose sensitive data if copied into broadly accessible workspace paths or retained longer than needed.

Mitigation: Before use, adapt the backup location and scope, store backups with owner-only permissions, avoid copying the full credentials directory unless necessary, and delete sensitive backups after rollback or verification.

Risk: Failure logs and bug reports may include sensitive operational details.

Mitigation: Redact logs and diagnostic output before sharing them in public bug reports.

Risk: Upgrade and rollback commands modify global packages and user service files, which can interrupt OpenClaw gateway availability if applied to the wrong environment.

Mitigation: Review commands against the target installation, record the old version, run the documented validation checks, and keep rollback artifacts available until the upgrade is verified.

## Reference(s):

- [OpenClaw releases](https://github.com/openclaw/openclaw/releases)
- [OpenClaw Upgrade Standard on ClawHub](https://clawhub.ai/gjoham/skills/openclaw-upgrade-standard)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown procedure with inline bash commands and validation checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes backup, upgrade, service migration, rollback, and bug-report evidence collection guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
