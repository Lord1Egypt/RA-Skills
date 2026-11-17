## Description:

Health Management helps an agent track diet, supplements, sleep, and health trends using a three-dimensional scoring model, multilingual records, and optional GitHub backup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[longerian](https://clawhub.ai/user/longerian)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to record meals, supplements, sleep, and health goals, then generate scoring feedback, daily logs, weekly or monthly analyses, and personalized improvement guidance. It can optionally back up locally stored health records to a user-provided GitHub repository after explicit configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional GitHub backup may upload sensitive health records beyond the user's intended scope.

Mitigation: Keep backup disabled unless the user has reviewed the backup scripts, selected a private repository, and confirmed the backup scope is limited to the intended user data.

Risk: Unsafe shell configuration handling and an unvalidated Git remote can make automatic backup risky.

Mitigation: Correct shell configuration sourcing and validate the Git remote before enabling automatic or scheduled backup.

Risk: Multi-user workspaces may expose or mix sensitive health data if backup scope is not fixed to one verified user.

Mitigation: Use per-user data directories and enable backup only after confirming the active user and destination repository.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/longerian/skills/health-score-pro)
- [Health Management Skill README](README.md)
- [Permissions Declaration](PERMISSIONS.md)
- [Health Management Principles](references/principles.md)
- [Diet Record Analysis Guide](references/analysis-guide.md)
- [5x5x5 Food Recognition Database](references/food-database.md)
- [Chinese Food Defense System Database](references/chinese-food-database.md)
- [Supplement Database and Analysis System](references/supplement-database.md)
- [Usage Examples](references/usage-examples.md)
- [New User Onboarding Guide](references/new-user-onboarding.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown records, health analysis summaries, configuration guidance, and optional shell command execution for backup workflows]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should follow the user's configured language and timezone; backup-related outputs apply only when the user explicitly enables and configures backup.]

## Skill Version(s):

1.6.1 (source: release evidence; artifact frontmatter is 1.6.0 and manifest is 1.5.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
