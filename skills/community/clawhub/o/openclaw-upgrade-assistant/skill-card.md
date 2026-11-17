## Description:

Analyzes OpenClaw version updates against local configuration, generates compatibility reports, and backs up affected files before upgrade.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adgai115](https://clawhub.ai/user/adgai115)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill before upgrading OpenClaw to compare release notes with local configuration, identify affected files, generate an advisory Markdown report, and create backups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests command execution and documents a global OpenClaw update command despite positioning itself as a pre-upgrade assessment tool.

Mitigation: Constrain the skill to workspace reads and writes plus GitHub release fetching; require separate human approval before any update command is executed.

Risk: The generated compatibility report is advisory and may be based on fallback release data when GitHub release fetching fails.

Mitigation: Verify the release notes and review the report before using it to make upgrade decisions.

Risk: Backup behavior may not prove that every important configuration file was copied.

Mitigation: Confirm the backup directory and manifest contain the expected files before proceeding with an upgrade.

## Reference(s):

- [OpenClaw Official Documentation](https://docs.openclaw.ai)
- [OpenClaw GitHub Releases](https://github.com/openclaw/openclaw/releases)
- [OpenClaw Backup Best Practices](https://docs.openclaw.ai/gateway/backup)
- [ClawHub Skill Page](https://clawhub.ai/adgai115/skills/openclaw-upgrade-assistant)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report, console text, and workspace backup files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write an advisory report, backup files, and a backup manifest in the workspace.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
