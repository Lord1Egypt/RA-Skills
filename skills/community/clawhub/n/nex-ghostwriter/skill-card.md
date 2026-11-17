## Description:

Nex Ghostwriter helps an agent log meeting notes, draft client follow-up emails or internal recaps in selectable tones, track draft status, manage contacts, search meeting history, and export records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nexaiguy](https://clawhub.ai/user/nexaiguy)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external professionals, and teams use this skill to turn meeting notes into follow-up emails, internal recaps, action-item records, and searchable meeting history. It is aimed at agencies, consultants, freelancers, sales teams, account managers, project managers, founders, and other users who need repeatable meeting follow-up workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The export command can overwrite user-writable files outside the skill's data folder when given unsafe output paths.

Mitigation: Use trusted export filenames and keep exports under ~/.nex-ghostwriter/exports until path validation is fixed.

Risk: CSV exports may contain spreadsheet-interpreted formulas from stored meeting content.

Mitigation: Review or neutralize CSV cells before opening exports in spreadsheet software.

Risk: Meeting notes, contacts, drafts, and exports may contain sensitive business or personal information stored on the local machine.

Mitigation: Install and use the skill only where local storage under ~/.nex-ghostwriter is acceptable, and protect or delete exported files according to the user's data-handling requirements.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nexaiguy/skills/nex-ghostwriter)
- [Publisher Profile](https://clawhub.ai/user/nexaiguy)
- [Nex AI Homepage](https://nex-ai.be)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text and Markdown-ready email or recap content with CLI command guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores meeting notes, contacts, drafts, and exports locally under ~/.nex-ghostwriter.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
