## Description: <br>
Google Power Tools helps agents operate Google Workspace services through the gws CLI, including Gmail, Drive, Calendar, Docs, Sheets, Slides, Forms, Tasks, People, Meet, and Classroom. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cyrushuang1995-cmyk](https://clawhub.ai/user/cyrushuang1995-cmyk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, operators, and developers use this skill to perform Google Workspace tasks from an agent, including Gmail triage and sending, Drive file management, Calendar scheduling, and updates to Docs, Sheets, Slides, Forms, Tasks, contacts, Meet, and Classroom resources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can help operate a real Google Workspace account with broad OAuth access. <br>
Mitigation: Use the narrowest OAuth scopes available, protect ~/.config/gws, and install only when account-level Workspace automation is intended. <br>
Risk: Examples include high-impact actions such as sending email, changing sharing, deleting files or events, clearing tasks, and bulk edits. <br>
Mitigation: Require explicit user confirmation before destructive, sharing, sending, or bulk-modification commands are executed. <br>
Risk: The required gws CLI is installed from npm and runs with the user's local credentials. <br>
Mitigation: Verify the npm package source and keep local credentials and configuration files access-controlled. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/cyrushuang1995-cmyk/gws-google-workspace) <br>
- [Google Workspace CLI](https://github.com/googleworkspace/cli) <br>
- [GWS Installation and Authorization Guide](references/setup.md) <br>
- [Gmail Reference](references/gmail.md) <br>
- [Drive Reference](references/drive.md) <br>
- [Calendar Reference](references/calendar.md) <br>
- [Sheets Reference](references/sheets.md) <br>
- [Docs, Slides, and Forms Reference](references/docs-slides-forms.md) <br>
- [Tasks, People, Meet, and Classroom Reference](references/tasks-people-other.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose commands that operate on live Google Workspace data and require OAuth authorization.] <br>

## Skill Version(s): <br>
2.1.9 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
