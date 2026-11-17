## Description:

Interact with the Nerve Kanban board API to create and manage tasks, run workflow actions, handle proposals, and configure the board under /api/kanban.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seanford](https://clawhub.ai/user/seanford)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to manage a Nerve Kanban board through REST API calls, including task lifecycle operations, proposal review, and board configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can permanently delete Kanban tasks.

Mitigation: Require explicit human approval before deletion and verify the target task ID before issuing DELETE requests.

Risk: The skill can execute tasks, approve work, complete runs, and change workflow state.

Mitigation: Require human review before execution, approval, completion, abort, or rejection actions, especially when an agent-generated result is involved.

Risk: Board configuration can enable automatic proposal approval or bypass normal review controls.

Mitigation: Keep proposalPolicy set to confirm unless auto-approval is intentional, and review configuration changes before applying them.

Risk: The skill acts against the configured local Nerve server.

Mitigation: Use it only with a trusted Nerve server and trusted board data.

## Reference(s):

- [Nerve Kanban API Reference](references/api.md)
- [ClawHub Skill Page](https://clawhub.ai/seanford/skills/nerve-kanban)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with REST paths, JSON request bodies, and curl or JavaScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill can guide direct API calls that create, update, delete, execute, approve, reject, abort, complete, and configure Kanban tasks.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
