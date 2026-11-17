## Description:

Create, update, and delete calendar events and tasks in Lark (Feishu), including employee directory name-to-user_id resolution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[boyangwang](https://clawhub.ai/user/boyangwang)

### License/Terms of Use:

ISC

## Use Case:

Employees and operations teams use this skill to manage Lark calendar events, task assignments, attendee lists, and due dates from agent-guided commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad employee-directory access may expose more employee data than the scheduling workflow needs.

Mitigation: Use the narrowest Lark scopes available and minimize employee fields returned, cached, or displayed.

Risk: Calendar events automatically include a fixed attendee.

Mitigation: Confirm that this business rule is acceptable for the tenant before enabling event creation.

Risk: Delete and membership-management commands can make destructive calendar or task changes.

Mitigation: Require explicit confirmation before deleting events or tasks or changing attendees and task members.

Risk: Secrets are loaded from a shared relative secrets file.

Mitigation: Use a dedicated Lark app and ensure the secrets file contains only credentials intended for this skill.

Risk: Generic messaging helpers are present but not part of the documented calendar and task workflow.

Mitigation: Remove or restrict those helpers unless messaging behavior is intentionally reviewed and enabled.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/boyangwang/skills/lark-calendar)
- [Lark Calendar Events API](https://open.larksuite.com/document/server-docs/calendar-v4/calendar-event/create)
- [Lark Calendar Attendees API](https://open.larksuite.com/document/server-docs/calendar-v4/calendar-event-attendee/create)
- [Lark Tasks API](https://open.larksuite.com/document/server-docs/task-v2/task/create)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance, JSON]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Lark app credentials and tenant permissions before commands can modify events or tasks.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
