## Description: <br>
Create PMS tasks (bugs or features) on GitHub and sync to Google Sheets. Use when user says 'PMS Bug addition' for bugs or 'PMS Feature addition' for features. Creates GitHub issue with appropriate labels, assigns to roshanasingh4, updates PMS Task Tracker sheet and Team Daily Update sheet. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tarasinghrajput](https://clawhub.ai/user/tarasinghrajput) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Project and operations contributors use this skill to turn PMS bug or feature requests into GitHub issues and synchronized Google Sheets task records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create records in a specific GitHub repository and two Google Sheets. <br>
Mitigation: Confirm the active GitHub and Google accounts before execution and review the generated issue and sheet content before allowing writes. <br>
Risk: Task details may include sensitive internal project information. <br>
Mitigation: Review titles, descriptions, reproduction steps, and sheet entries for sensitive details before syncing them. <br>
Risk: The workflow uses fixed reporter, assignee, and destination fields. <br>
Mitigation: Verify that the hard-coded reporter, assignee, repository, and sheet destinations are appropriate for the organization before use. <br>


## Reference(s): <br>
- [PMS Domain Overview](references/pms-overview.md) <br>
- [PMS Sheet Schemas](references/sheet-schemas.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with GitHub CLI and Google Sheets command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create records in a configured GitHub repository and Google Sheets when the user authorizes execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
