## Description:

Paper Management System helps agents index, search, rename, extract full text from, and optionally summarize local PDF research papers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crayfish-ai](https://clawhub.ai/user/crayfish-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers and developers use this skill to manage local PDF paper collections by indexing metadata into SQLite, searching records, extracting full text, renaming files, and producing optional summaries or notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Notification support can execute a configured shell command.

Mitigation: Leave notifications disabled unless the command path is fixed, reviewed, and tightly controlled.

Risk: The automated cron workflow can move, rename, and delete PDF files in configured directories.

Mitigation: Use only dedicated paper-management directories and test manual commands before enabling cron.

Risk: AI summarization behavior may not match OpenAI-related configuration and documentation in this release.

Mitigation: Confirm the actual summarization behavior before relying on external AI processing or data-transfer assumptions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/crayfish-ai/skills/paper-management-system)
- [README](README.md)
- [Skill Definition](SKILL.md)
- [Example Configuration](config.example.yaml)
- [Skill Manifest](skill.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with inline shell commands; generated artifacts include SQLite records, renamed PDF files, and optional text summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes to configured local paper, download, database, and log paths; optional notifications are disabled by default.]

## Skill Version(s):

2.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
