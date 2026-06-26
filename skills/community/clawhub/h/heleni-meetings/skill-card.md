## Description: <br>
Helps agents coordinate meetings, create calendar invites, and turn pasted meeting notes or transcripts into summaries and action items. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[netanel-abergel](https://clawhub.ai/user/netanel-abergel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, assistants, and agents use this skill to schedule meetings, coordinate availability with another PA, create calendar invites, and convert meeting notes or transcripts into summaries, decisions, and owner-tagged action items. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Meeting notes or transcripts may include confidential, legal, HR, customer, or credential-related content and may be saved locally. <br>
Mitigation: Use only in approved workspaces, avoid saving raw transcripts unless users explicitly request local retention, and redact sensitive content before storage. <br>
Risk: Calendar events may be created or deleted without consistently requiring explicit user approval. <br>
Mitigation: Require user confirmation before creating, rescheduling, or deleting calendar events, and use only an approved calendar account. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with optional shell command blocks and local Markdown files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create meeting-notes/*.md and update todo.md when the notes workflow is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
