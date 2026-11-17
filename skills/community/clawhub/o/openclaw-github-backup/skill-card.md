## Description:

Automatically backs up OpenClaw configuration to a private GitHub repository with API key sanitization, activity detection, smart backup frequency, and recovery guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wang5sheng](https://clawhub.ai/user/wang5sheng)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users and developers use this skill to configure automated backups of local OpenClaw state to a private GitHub repository and to receive restore guidance for migration or disaster recovery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad OpenClaw data may be staged and uploaded to GitHub, including private agent state or configuration beyond sanitized API keys.

Mitigation: Use only a dedicated empty private repository, inspect the exact files staged from ~/.openclaw, and add a file allowlist plus secret scanning or encryption before backup.

Risk: Installer-driven Git and SSH changes may alter global Git identity, SSH keys, or known_hosts entries.

Mitigation: Review and modify the installer before execution, avoid global Git config changes, and require explicit consent for SSH key generation or known_hosts updates.

Risk: Force pushes and recursive .git deletion can lose backup history or remove nested repository metadata.

Mitigation: Remove force-push behavior and recursive .git deletion, then test backup and restore in a disposable OpenClaw profile before use.

## Reference(s):

- [OpenClaw GitHub Backup on ClawHub](https://clawhub.ai/wang5sheng/skills/openclaw-github-backup)
- [wang5sheng ClawHub profile](https://clawhub.ai/user/wang5sheng)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide commands that operate on ~/.openclaw and a user-provided GitHub repository.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
