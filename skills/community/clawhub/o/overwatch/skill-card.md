## Description:

Prevent agents from going dark by keeping humans informed during long-running tasks, background work, and multi-step execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tooled-app](https://clawhub.ai/user/tooled-app)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to require clear task-start, progress, error, retry, sub-agent, and completion updates during agent work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is always active and mandatory, which can conflict with workflows that require exact JSON, quiet tool execution, confidential operations, or minimal status output.

Mitigation: Scope use to user-visible long-running work and require it to yield to higher-priority safety, privacy, and formatting requirements.

Risk: Frequent progress messages can expose unnecessary operational details in sensitive workflows.

Mitigation: Keep updates concise and avoid secrets, credentials, customer data, hidden reasoning, and backend details that do not help the user understand risk or progress.

## Reference(s):

- [Overwatch ClawHub skill page](https://clawhub.ai/tooled-app/skills/overwatch)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown guidance and concise status-update templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces human-facing progress, error, retry, and completion updates; no tool calls or generated files are required by the skill itself.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact frontmatter is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
