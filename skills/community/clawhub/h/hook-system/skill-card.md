## Description:

Hook System lets agents run configured PreToolUse and PostToolUse hooks to validate inputs, log activity, block selected tool calls, or process tool outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xhmqq616](https://clawhub.ai/user/xhmqq616)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to add hook-based pre-processing and post-processing around tool execution, including validation, logging, denial decisions, and output handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configured hooks can execute shell commands with access to the agent environment and tool data.

Mitigation: Install only when local hook execution is intentional, and allow only reviewed hook commands from trusted sources.

Risk: Hook commands can observe tool inputs, outputs, private files, command output, and environment secrets.

Mitigation: Avoid sensitive contexts unless strict allowlists, redaction, sandboxing, and review controls are in place.

## Reference(s):

- [Hook System on ClawHub](https://clawhub.ai/xhmqq616/skills/hook-system)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JavaScript, shell, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 18 or newer.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
