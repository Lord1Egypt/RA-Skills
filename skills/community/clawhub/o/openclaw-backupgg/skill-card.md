## Description:

一键备份 OpenClaw 工作区，支持必选/可选内容，生成 ZIP 压缩包（含 SHA256 校验）

This skill is ready for commercial/non-commercial use.

## Publisher:

[hhse](https://clawhub.ai/user/hhse)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and administrators use this skill to package workspace memory, identity, agent, tool, skill, and optional project files into a portable ZIP backup and restore that archive back into an OpenClaw workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Backups are plaintext ZIP archives that may contain sensitive OpenClaw memory, identity, user, tool, and skill files.

Mitigation: Store backups privately, apply separate encryption before storage or transfer, and avoid publishing backup archives.

Risk: Restoring an archive can overwrite existing workspace files and should not be done from untrusted ZIP files.

Mitigation: Review the archive source and contents before restore, use dry-run listing when possible, and keep a separate current backup before overwriting a workspace.

Risk: Workspace symlinks or unusual file layouts can affect what is included in a backup.

Mitigation: Review the workspace for symlinks and unexpected sensitive files before creating a backup.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hhse/skills/openclaw-backupgg)
- [Publisher profile](https://clawhub.ai/user/hhse)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and Python script behavior]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces ZIP backup archives and restore guidance for an OpenClaw workspace.]

## Skill Version(s):

1.0.1 (source: server release metadata; SKILL.md frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
