## Description:

Reuse, inspect, search, or append shared OpenClaw memory on the current machine. Use when a request depends on remembered local servers, deploy hosts, internal services, script paths, runbooks, workspace conventions, or prior user preferences that may already exist in OpenClaw memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kamiender](https://clawhub.ai/user/kamiender)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to search, inspect, and append shared OpenClaw memory for local servers, services, paths, runbooks, workspace conventions, and prior preferences before acting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically read and append shared local OpenClaw memory that may contain sensitive operational details.

Mitigation: Install it only where access to remembered hosts, paths, runbooks, preferences, and notes is acceptable; require explicit confirmation before memory search or append operations on shared or sensitive machines.

Risk: Appending memory can persist inaccurate, unintended, or overly broad operational notes.

Mitigation: Review append text before writing, use dry-run behavior when appropriate, and confirm the reported destination file after updates.

## Reference(s):

- [OpenClaw Memory on ClawHub](https://clawhub.ai/kamiender/skills/openclaw-shared-memory)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and plain-text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results include path, source, score, and snippet; append operations report the destination path.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
