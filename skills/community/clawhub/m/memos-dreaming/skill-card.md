## Description:

Automatically consolidates daily memories by scoring and filtering entries from MemOS SQLite and daily logs, writing top insights to MEMORY.md each morning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rongtianhua](https://clawhub.ai/user/rongtianhua)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to review and consolidate useful memories from MemOS records and daily logs into persistent workspace memory. It also supports periodic memory quality audits for duplicate, outdated, noisy, or orphaned entries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically change persistent agent memory.

Mitigation: Keep cron and apply modes disabled until DREAMS.md or AUDIT.md output has been reviewed and MEMORY.md has been backed up.

Risk: Local notes or MemOS records may be copied into persistent agent memory.

Mitigation: Install only when the user intends this skill to manage OpenClaw memory files and has reviewed the type of content selected for promotion.

Risk: Cleanup scope is not fully disclosed.

Mitigation: Review AUDIT.md before enabling apply mode; rely on backup behavior before accepting automatic cleanup.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/rongtianhua/skills/memos-dreaming)
- [Publisher Profile](https://clawhub.ai/user/rongtianhua)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown files and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Dry-run writes DREAMS.md for review; apply mode can append selected entries to MEMORY.md; audit mode writes AUDIT.md and can clean high-confidence noise after creating a backup.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
