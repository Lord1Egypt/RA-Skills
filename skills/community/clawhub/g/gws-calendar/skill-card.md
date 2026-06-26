## Description: <br>
Google Calendar: Manage calendars and events. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Google Workspace administrators use this skill to inspect Google Calendar resources and prepare gws CLI commands for calendars, events, ACLs, free/busy queries, and settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Calendar commands can modify or delete real calendar data, including events, ACLs, secondary calendars, and primary-calendar contents. <br>
Mitigation: Inspect or list the target calendar, event, or ACL first and require explicit confirmation before delete, clear, update, move, ACL-changing, or watch-creation commands. <br>
Risk: Commands may act on an unintended Google account or calendar if the active gws authentication context is unclear. <br>
Mitigation: Confirm the authenticated Google account and intended calendar before generating or executing commands that read or change calendar data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/gws-calendar) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the gws CLI and an authenticated Google Workspace account.] <br>

## Skill Version(s): <br>
1.0.13 (source: server release metadata; artifact metadata version 0.22.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
