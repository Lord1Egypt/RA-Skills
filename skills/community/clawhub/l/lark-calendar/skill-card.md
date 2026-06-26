## Description: <br>
Create, update, and delete calendar events and tasks in Lark (Feishu), with employee directory support for name-to-user_id resolution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[boyangwang](https://clawhub.ai/user/boyangwang) <br>

### License/Terms of Use: <br>
ISC <br>


## Use Case: <br>
Developers and operators use this skill to manage Lark calendar events, attendees, tasks, and task members from an agent workflow. It is suited for teams that want automated scheduling and task updates while resolving known employee names to Lark user IDs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses Lark app credentials and requested scopes to read or write calendar, task, contact, and potentially messaging data. <br>
Mitigation: Use a least-privileged Lark app, review granted scopes before installation, and avoid IM/message scopes unless they are required. <br>
Risk: Delete commands can remove Lark events or tasks when provided an event ID or task ID. <br>
Mitigation: Confirm target event and task IDs before running delete operations. <br>
Risk: Employee directory data may be loaded, cached, or resolved from a static fallback list. <br>
Mitigation: Review contact access, keep the fallback directory current, and avoid exposing cached employee data beyond the intended workspace. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/boyangwang/lark-calendar) <br>
- [Lark Calendar Events API](https://open.larksuite.com/document/server-docs/calendar-v4/calendar-event/create) <br>
- [Lark Calendar Attendees API](https://open.larksuite.com/document/server-docs/calendar-v4/calendar-event-attendee/create) <br>
- [Lark Tasks API](https://open.larksuite.com/document/server-docs/task-v2/task/create) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with command examples, JavaScript module usage, and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Lark app credentials from environment variables and may call Lark Calendar, Task, Contact, and messaging APIs depending on granted scopes.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence, frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
