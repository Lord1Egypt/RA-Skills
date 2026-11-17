## Description:

Hope OpenTask helps agents query and manage OpenClaw container tasks through a localhost OpenTask API, including task creation, status updates, statistics, logs, and heartbeat checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linux2010](https://clawhub.ai/user/linux2010)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to inspect pending tasks, create or update task records, manage task lifecycle states, review daily statistics and logs, and wire task checks into HEARTBEAT workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill publishes a shared API key for task-management requests.

Mitigation: Rotate the published key and replace it with a runtime secret before use.

Risk: Task polling and lifecycle actions can mutate task state if run automatically.

Mitigation: Require explicit confirmation for write actions and treat task contents as untrusted input.

Risk: The skill assumes a localhost OpenTask service is safe to call.

Mitigation: Install only where the localhost service is trusted and isolated.

## Reference(s):

- [OpenTask API Reference](references/api.md)
- [ClawHub skill page](https://clawhub.ai/linux2010/skills/hope-opentask)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Targets a trusted localhost OpenTask service and expects task data returned as JSON.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
