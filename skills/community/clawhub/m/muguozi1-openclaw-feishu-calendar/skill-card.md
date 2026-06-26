## Description: <br>
Manage Feishu (Lark) calendars by listing and searching calendars, checking schedules, syncing events, creating reminders, and setting up shared project calendars. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[muguozi1](https://clawhub.ai/user/muguozi1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers connected to Feishu use this skill to inspect calendars, create task reminders, sync routine events, and maintain local schedule state. It is intended for environments where Feishu app credentials and calendar permissions are available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Calendar permissions can allow event creation, deletion, attendee invites, shared-calendar membership changes, and local persistence of calendar data. <br>
Mitigation: Use a least-privilege Feishu app with a dedicated calendar, review scripts before execution, and grant only the calendar scopes required for the intended workflow. <br>
Risk: Cleanup, setup, and routine-sync scripts may make calendar changes that are difficult to notice before execution. <br>
Mitigation: Run those scripts only after confirming the exact calendar, event range, recurrence, invitees, and shared-calendar members they will affect. <br>
Risk: Task-marking and reminder flows can invite attendees or create recurring events based on parsed user requests. <br>
Mitigation: Require explicit user confirmation before event deletion, recurring event creation, attendee invites, or shared-calendar membership changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/muguozi1/muguozi1-openclaw-feishu-calendar) <br>
- [Publisher profile](https://clawhub.ai/user/muguozi1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal output with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call Feishu calendar APIs and may write local calendar state files when sync routines are executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence, package.json, _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
