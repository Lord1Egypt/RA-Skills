## Description:

Create, update, and delete calendar events and tasks in Lark (Feishu), with employee directory support for name-to-user_id resolution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[litiao1224](https://clawhub.ai/user/litiao1224)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and agents use this skill to manage Lark calendar events and tasks from command-line workflows, including attendee and assignee resolution from names. It is intended for a specific Lark tenant where the documented calendar, permissions, and employee directory behavior are acceptable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change real Lark calendar events, tasks, attendees, and task members.

Mitigation: Require explicit user confirmation before deletes, attendee or member changes, and other write operations.

Risk: Created calendar events automatically add a fixed attendee.

Mitigation: Install only where the organization policy requires that attendee behavior, and verify the default calendar ID before use.

Risk: The skill may access broad employee directory data for name resolution.

Mitigation: Grant only the required calendar, task, and contact scopes, and avoid unrelated messaging scopes.

Risk: Lark app credentials are required for operation.

Mitigation: Protect .secrets.env and store FEISHU_APP_ID and FEISHU_APP_SECRET using the workspace's approved secret-handling process.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/litiao1224/skills/lark-calendar-litiao)
- [Lark Calendar Events API](https://open.larksuite.com/document/server-docs/calendar-v4/calendar-event/create)
- [Lark Calendar Attendees API](https://open.larksuite.com/document/server-docs/calendar-v4/calendar-event-attendee/create)
- [Lark Tasks API](https://open.larksuite.com/document/server-docs/task-v2/task/create)

## Skill Output:

**Output Type(s):** [Shell commands, API calls, JSON, Text]

**Output Format:** [Markdown usage guidance with command-line examples and optional JSON responses from scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Lark app credentials and tenant-specific calendar, task, contact, and employee directory configuration.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
