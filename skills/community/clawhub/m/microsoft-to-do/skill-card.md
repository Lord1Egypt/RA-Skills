## Description:

Helps agents manage Microsoft To Do task lists, tasks, checklist items, and linked resources through a user-authorized Maton connection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

People and teams use this skill to find, create, update, and delete Microsoft To Do lists and tasks. With separate approval, they can also set up hosted functions and triggers for ongoing automations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Writes or deletions could change the wrong account or task.

Mitigation: Confirm the account, target resource, and payload before approving each change.

Risk: Hosted functions or triggers can keep running after the immediate task is complete.

Mitigation: Approve each deployment or trigger separately, check its scope and frequency, and remove it when no longer needed.

Risk: A trigger destination can continuously forward event data.

Mitigation: Confirm the exact destination and data flow before approving persistent delivery.

## Reference(s):

- [Microsoft To Do API overview](https://learn.microsoft.com/en-us/graph/api/resources/todo-overview)
- [Maton documentation](https://docs.maton.ai)
- [Maton homepage](https://maton.ai)
- [Microsoft To Do skill on ClawHub](https://clawhub.ai/byungkyu/skills/microsoft-to-do)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code]

**Output Format:** [Markdown with command and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may retrieve or change data in the authorized Microsoft To Do account; optional automation requires separate approval.]

## Skill Version(s):

1.2.5 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
