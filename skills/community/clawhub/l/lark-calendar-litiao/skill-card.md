## Description: <br>
Create, update, and delete calendar events and tasks in Lark (Feishu), including employee directory support for automatic name-to-user_id resolution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[litiao1224](https://clawhub.ai/user/litiao1224) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and workplace automation agents use this skill to schedule Lark calendar events, manage attendees, and create or maintain Lark tasks with name-to-user-ID resolution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill has broad authority over business calendar and task data. <br>
Mitigation: Install only when the publisher and Feishu tenant app credentials are trusted, and restrict Lark app scopes to the minimum needed. <br>
Risk: Calendar actions may target the wrong default calendar or always include a specific attendee. <br>
Mitigation: Before use, verify the default calendar ID and confirm that every created event should include Boyang. <br>
Risk: Extra messaging helpers and employee fields may exceed the stated calendar and task workflow. <br>
Mitigation: Review whether IM messaging helpers and excess employee fields are needed, and remove them if they are outside the deployment scope. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/litiao1224/lark-calendar-litiao) <br>
- [Lark Calendar Events API](https://open.larksuite.com/document/server-docs/calendar-v4/calendar-event/create) <br>
- [Lark Calendar Attendees API](https://open.larksuite.com/document/server-docs/calendar-v4/calendar-event-attendee/create) <br>
- [Lark Tasks API](https://open.larksuite.com/document/server-docs/task-v2/task/create) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, API calls, JSON, configuration guidance] <br>
**Output Format:** [Command-line output and optional JSON responses from Lark API operations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Feishu app credentials and Lark app scopes for calendar, task, and contact operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, package.json, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
