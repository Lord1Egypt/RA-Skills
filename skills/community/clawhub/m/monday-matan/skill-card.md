## Description:

Access the Monday.com API via Maton Gateway to manage boards, items, columns, groups, users, and workspaces using GraphQL with OAuth authentication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[otman-ai](https://clawhub.ai/user/otman-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to query and manage Monday.com workspaces through Maton Gateway using OAuth-backed GraphQL requests. It supports common board, item, column, group, user, workspace, and connection-management workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes commands that can create, update, or delete Monday.com boards, items, columns, groups, and Maton OAuth connections.

Mitigation: Require explicit user confirmation before any create, update, delete, or connection-management command, and test first on non-production boards.

Risk: MATON_API_KEY exposure could grant access to connected Monday.com data.

Mitigation: Store MATON_API_KEY as a secret, avoid printing or pasting it, and do not use the documented echo pattern in shared logs or terminals.

Risk: Use depends on a third-party Maton Gateway between the agent and Monday.com.

Mitigation: Install only if the user trusts Maton for this access path and uses the least-privileged OAuth scopes available.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/otman-ai/skills/monday-matan)
- [Maton sign-in](https://maton.ai)
- [Maton connection control plane](https://ctrl.maton.ai)
- [Maton Monday GraphQL endpoint](https://gateway.maton.ai/monday/v2)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown-style operational guidance with curl and GraphQL examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses MATON_API_KEY and optional Maton-Connection headers; examples may read, create, update, or delete Monday.com resources.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
