## Description:

Automates hourly OpenClaw workspace backups with SQLite database export, optional NAS sync, and GitHub commit and push guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lancelot3777-svg](https://clawhub.ai/user/lancelot3777-svg)

### License/Terms of Use:

MIT

## Use Case:

Developers and workspace operators use this skill to set up repeatable OpenClaw workspace backups across a local SQLite database, a NAS target, and a GitHub repository.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automated schedules can repeatedly send broad workspace contents to remote NAS or cloud-synced storage.

Mitigation: Do not enable the cron or OpenClaw schedule as written; restrict backups to explicitly approved paths and verify the final NAS or cloud storage location.

Risk: Backups and Git pushes can include secrets, databases, or other sensitive workspace data.

Mitigation: Exclude secrets and databases unless intentionally protected, use a private repository for sensitive material, and review staged changes before automated pushes.

Risk: Hard-coded paths, hosts, and workspace names can send data to unintended local or remote destinations.

Mitigation: Replace hard-coded paths and remote hosts before use and test the backup flow manually with non-sensitive data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lancelot3777-svg/skills/openclaw-backup-guide)
- [Release changelog](https://github.com/lancelot3777-svg/openclaw-backup-guide)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Code, Configuration]

**Output Format:** [Markdown guidance with bash commands and Node.js backup scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes setup steps for cron or OpenClaw scheduling, NAS destination configuration, database backup execution, and Git commit/push workflow.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
