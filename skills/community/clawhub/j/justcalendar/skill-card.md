## Description: <br>
Use this skill when a user needs to install, authenticate, or operate the Just Calendar CLI against https://justcalendar.ai, including generating an agent token in the web UI and performing calendar/day-data management from terminal commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AndredAlmeida](https://clawhub.ai/user/AndredAlmeida) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, developers, and calendar operators use this skill to install and authenticate the JustCalendar CLI, manage calendars, and set, get, or delete day-level calendar data backed by Google Drive. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agent tokens grant CLI access to JustCalendar-backed Google Drive operations. <br>
Mitigation: Treat agent tokens like passwords, keep them out of prompts and source-controlled files, and rotate them by generating a new token if exposed. <br>
Risk: Calendar removal and bulk set/delete commands can change or remove many records at once. <br>
Mitigation: Confirm calendar names, IDs, dates, and date ranges before execution, and use `justcalendar data get` to verify important changes. <br>
Risk: The CLI operates on calendar data stored in Google Drive. <br>
Mitigation: Use it only with accounts and Drive data the user is authorized to manage, and reconnect Drive deliberately when permission or token errors occur. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/AndredAlmeida/justcalendar) <br>
- [Publisher Profile](https://clawhub.ai/user/AndredAlmeida) <br>
- [JustCalendar Web App](https://justcalendar.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JustCalendar CLI command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js >=18, npm, access to justcalendar.ai, an agent token, and a Google Drive-connected web session.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
