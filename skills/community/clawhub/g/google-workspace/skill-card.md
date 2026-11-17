## Description:

Plan, audit, and safely execute Google Workspace admin, Gmail, Calendar, Drive, Groups, and user lifecycle work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[patrick-erichsen-2](https://clawhub.ai/user/patrick-erichsen-2)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, IT administrators, and Workspace operators use this skill to plan and review Google Workspace administration, migration, account lifecycle, permission audit, group, mailbox, calendar, Drive, and API command work before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated commands or API calls could affect users, groups, mailboxes, calendars, Drive permissions, ownership, or sharing state.

Mitigation: Require explicit human approval before write, deletion, ownership transfer, suspension, archive, or sharing-change operations.

Risk: Overbroad OAuth scopes could grant more Workspace access than the task requires.

Mitigation: Prefer read-only discovery scopes first and escalate to write scopes only after the exact change plan is approved.

Risk: Bulk changes can be hard to reverse without current state evidence.

Mitigation: Export affected users, groups, permissions, or settings and define a rollback path before applying writes.

## Reference(s):

- [Google Workspace OAuth Scopes](references/scopes.md)
- [ClawHub Skill Page](https://clawhub.ai/patrick-erichsen-2/skills/google-workspace)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with command examples, API call descriptions, change plans, and rollout checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses placeholders for domains, users, groups, and file IDs until real values are supplied; generated write operations require explicit human approval.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
