## Description:

Logs daily mood entries to an Obsidian vault using a fixed format, with mood score, tags, optional notes, and weekly mood report generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leo-zzl](https://clawhub.ai/user/leo-zzl)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to record daily mood scores, tags, and notes in Markdown, then generate weekly summaries of mood trends and tag frequency.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mood records and notes may contain sensitive personal information and are stored in a hard-coded Obsidian/iCloud path.

Mitigation: Review or change the storage path before use and avoid logging private notes in shared or synchronized vaults unless that storage is intended.

Risk: Weekly reporting and scheduled sending can expose mood summaries outside the local vault, including through the configured WeChat recipient.

Mitigation: Keep report generation manual unless recurring delivery is explicitly intended, and replace or remove the recipient before enabling scheduled sending.

Risk: Temporary report outputs under /tmp may expose private mood data to other local processes or leave residual files.

Mitigation: Write reports to a private directory with appropriate permissions or delete temporary reports immediately after use.

## Reference(s):

- [Mood Logger on ClawHub](https://clawhub.ai/leo-zzl/skills/mood-logger)
- [Weekly Report Setup](artifact/WEEKLY_REPORT_SETUP.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown mood logs and weekly reports with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local Markdown files to a configured Obsidian daily-notes directory and can print or save weekly reports.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
