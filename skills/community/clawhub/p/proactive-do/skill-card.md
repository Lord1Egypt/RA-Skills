## Description:

Proactive-Do helps an agent triage and execute a markdown todo list, maintain work journals, reconcile task states, and send concise heartbeat reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hyharry](https://clawhub.ai/user/hyharry)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to have an agent review todo/todo.md on a recurring cadence, select up to three new tasks, complete short tasks, draft plans for larger tasks, and maintain journaled status updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring todo automation can make persistent workspace changes or run repeatedly in contexts where the user does not want autonomous task handling.

Mitigation: Use only in workspaces where recurring todo automation is wanted, and require explicit approval for cron setup and any policy or memory-file changes.

Risk: External email reporting can expose sensitive todo content, private URLs, customer data, or personal details.

Mitigation: Require explicit approval for each external email destination and message body, and avoid putting secrets or sensitive details in todos that this skill may process.

## Reference(s):

- [Proactive-Do skill page](https://clawhub.ai/hyharry/skills/proactive-do)
- [Proactive-Do templates](references/templates.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown todo updates, journal files, plan files, and concise status reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce external email reports when delivery settings and user approval permit them.]

## Skill Version(s):

0.1.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
