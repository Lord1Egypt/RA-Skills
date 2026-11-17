## Description:

Manage HoneyDew Kanban boards, cards, and labels via the REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smartify-dot-ai](https://clawhub.ai/user/smartify-dot-ai)

### License/Terms of Use:

MIT

## Use Case:

Developers, teams, and external users use this skill to let an OpenClaw agent create, update, move, delete, label, transfer, and summarize HoneyDew Kanban tasks through a running local or trusted-network HoneyDew REST API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can direct an agent to modify or delete HoneyDew boards, columns, cards, comments, and labels through an unauthenticated API.

Mitigation: Install it only for trusted HoneyDew instances and require explicit user confirmation before destructive actions such as deleting boards, columns, or cards.

Risk: Exposing the HoneyDew API outside localhost or a trusted network could allow unintended task-board changes.

Mitigation: Keep the HoneyDew API bound to localhost or a genuinely trusted network, and avoid broad network exposure.

## Reference(s):

- [ClawHub HoneyDew skill page](https://clawhub.ai/smartify-dot-ai/skills/honeydew)
- [HoneyDew repository](https://github.com/smartify-inc/Honeydew)
- [HoneyDew API documentation](https://github.com/smartify-inc/Honeydew#api-endpoints)
- [HoneyDew Python agent tools reference](https://github.com/smartify-inc/Honeydew#agent-integration)
- [HoneyDew support issues](https://github.com/smartify-inc/honeydew/issues)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Code, Configuration instructions, Guidance]

**Output Format:** [Markdown with REST API examples, shell commands, and optional Python code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent actions can modify or delete HoneyDew boards, columns, cards, comments, and labels.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata and clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
