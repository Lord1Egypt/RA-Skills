## Description:

Create PMS tasks (bugs or features) on GitHub and sync to Google Sheets. Use when user says 'PMS Bug addition' for bugs or 'PMS Feature addition' for features. Creates GitHub issue with appropriate labels, assigns to roshanasingh4, updates PMS Task Tracker sheet and Team Daily Update sheet.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tarasinghrajput](https://clawhub.ai/user/tarasinghrajput)

### License/Terms of Use:


## Use Case:

Employees and project maintainers use this skill to collect PMS bug or feature details, create a matching GitHub issue, and record the task in PMS tracking and daily update sheets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill writes to a named GitHub repository and two named Google Sheets using fixed identities and assignments.

Mitigation: Install only for the stated PMS workflow and confirm the repository, sheets, assignee, reporter name, and assigned email before use.

Risk: The release evidence flags unsafe shell command templates for GitHub and Sheets writes.

Mitigation: Add a final confirmation step and implement writes with safe argument handling and JSON serialization.

## Reference(s):

- [PMS Domain Overview](references/pms-overview.md)
- [PMS Sheet Schemas](references/sheet-schemas.md)
- [ClawHub Skill Page](https://clawhub.ai/tarasinghrajput/skills/pms-task)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and structured issue and sheet fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces task details, GitHub issue commands, Google Sheets updates, and confirmation guidance for a fixed PMS workflow.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
