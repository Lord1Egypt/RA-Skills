## Description:

Interact with the Nerve Kanban board API. CRUD tasks, manage workflow (execute, approve, reject, abort), handle proposals, configure the board. All endpoints are under /api/kanban on the Nerve server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blueworldmarketing](https://clawhub.ai/user/blueworldmarketing)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and agents use this skill to manage Nerve Kanban tasks through the local REST API, including task CRUD, workflow transitions, proposal handling, and board configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can mutate live Kanban board data, including task creation, updates, reordering, workflow state changes, and permanent deletion.

Mitigation: Use it only with a trusted Nerve API and require explicit operator confirmation before delete, execute, approve, reject, complete, or configuration update requests.

Risk: Proposal auto-approval can allow autonomous agent changes to be applied without human review.

Mitigation: Keep proposalPolicy set to confirm unless the board is intentionally configured for autonomous agent changes.

Risk: Task execution can spawn agent sessions and move work into review based on run completion.

Mitigation: Review execution requests and resulting task output before approval, especially when the board contains important work data.

## Reference(s):

- [Nerve Kanban API Reference](references/api.md)
- [ClawHub Skill Page](https://clawhub.ai/blueworldmarketing/skills/nerve-kanban-bwm)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, code, configuration]

**Output Format:** [Markdown with REST endpoint descriptions, JSON request and response shapes, curl commands, and JavaScript fetch examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires access to a trusted Nerve server origin; mutating endpoints should be used with explicit operator approval.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
