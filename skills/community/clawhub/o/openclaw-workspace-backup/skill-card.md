## Description:

Backs up configured local git workspaces to GitHub branches using .env-defined directories and an OpenClaw daily 03:00 schedule.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangpengle](https://clawhub.ai/user/zhangpengle)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to automate backups of configured local git workspace repositories to dedicated remote branches and to inspect backup status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automated backup can stage, commit, and push all changes from configured workspaces to their configured origins.

Mitigation: Review every configured workspace path and verify each repository origin before enabling scheduled backups.

Risk: Configured repositories may contain secrets or unintended files that would be pushed during backup.

Mitigation: Scan repositories for secrets and confirm ignore rules before the first backup and after major workspace changes.

Risk: The --force option can overwrite remote branch history.

Mitigation: Avoid --force unless the remote-history impact is understood and accepted.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zhangpengle/skills/openclaw-workspace-backup)
- [Artifact Skill Definition](artifact/SKILL.md)
- [Artifact Agent Guidance](artifact/CLAUDE.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text CLI output, log entries, and concise configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May stage, commit, and push changes from configured git repositories.]

## Skill Version(s):

0.1.5 (source: server release metadata; artifact pyproject.toml reports 0.1.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
