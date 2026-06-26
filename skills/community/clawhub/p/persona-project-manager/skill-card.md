## Description: <br>
Coordinate projects - track tasks, schedule meetings, and share docs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and project teams use this persona to coordinate Google Workspace projects by tracking status, scheduling meetings, sharing files, sending updates, and preparing recurring reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can help an agent make real Google Workspace changes, including emails, calendar events, file uploads, announcements, and sheet edits. <br>
Mitigation: Use dry-run or preview where available and verify recipients, attendees, files, folders, announcement channels, and sheet changes before write or outbound actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/persona-project-manager) <br>
- [Skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with inline gws shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide Google Workspace write actions such as sending email, creating calendar events, uploading files, posting announcements, and editing sheets.] <br>

## Skill Version(s): <br>
1.0.12 (source: server release metadata; artifact metadata version 0.22.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
