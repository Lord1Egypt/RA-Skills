## Description: <br>
Memo helps agents record work notes, search stored history, generate work summary reports, and manage to-do items with local JSON persistence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[QU8](https://clawhub.ai/user/QU8) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and agent users use this skill as a private work-memory assistant for capturing spoken work updates, finding prior records, exporting Markdown reports, and tracking unfinished to-do items. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores long-term work notes locally, which may include sensitive personal or business details. <br>
Mitigation: Confirm the records.json and export locations before use, and avoid storing secrets or private work details unless local storage is acceptable. <br>
Risk: The skill can create, update, and delete recurring reminders when to-do items are added or marked complete. <br>
Mitigation: Require explicit confirmation before reminder creation, update, or deletion, and review the reminder date, recurrence, prompt, and working directory. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/QU8/i) <br>
- [Field recognition rules](references/field-rules.md) <br>
- [Report format](references/report-format.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Text responses, local JSON records, and Markdown work reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read and write local records.json data and exported Markdown reports; documented reminder behavior can create, update, or delete dated work reminders.] <br>

## Skill Version(s): <br>
1.2.0 (source: server-resolved release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
