## Description:

Offer Tracker helps an agent parse batches of Chinese campus recruiting or internship application updates into a searchable local HTML progress table with a restorable JSON backup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sharinchan233](https://clawhub.ai/user/sharinchan233)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to turn free-form Chinese job application updates into structured tracker records. It supports creating or updating a local HTML table, maintaining a full JSON backup, and reporting current status and upcoming deadlines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary flags unsafe data-handling and overwrite behavior around local tracker and backup files.

Mitigation: Review the HTML template before installation, and confirm before creating or overwriting Desktop tracker and backup files.

Risk: Imported JSON backups and exported CSV files can carry untrusted or formula-like user-entered content.

Mitigation: Import JSON backups only from trusted sources, and inspect exported CSV values before opening them in spreadsheet software.

## Reference(s):

- [Parsing Rules](references/parsing-rules.md)
- [ClawHub skill page](https://clawhub.ai/sharinchan233/skills/offer-tracker)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown summaries plus local HTML and JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates a browser-openable application tracker and a full JSON backup; browser-side edits are stored locally.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
