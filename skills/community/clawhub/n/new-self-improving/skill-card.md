## Description:

Logs corrections, errors, feature requests, and recurring patterns into structured workspace learning files, then promotes stable patterns into tiered memory and OpenClaw workspace files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[muhamadbasim](https://clawhub.ai/user/muhamadbasim)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to capture feedback, command failures, feature requests, and recurring work patterns as local workspace memory. They can review and promote validated lessons into persistent agent guidance files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can turn conversation-derived patterns into persistent local agent behavior without clear owner approval.

Mitigation: Audit .learnings, .self-improving/HOT.md, AGENTS.md, SOUL.md, TOOLS.md, and MEMORY.md before relying on promoted behavior.

Risk: Persistent memory may retain sensitive or inappropriate context if used in shared or untrusted conversations.

Mitigation: Use the skill only in private local workspaces, add an approval step before promotion, and sanitize logged context beyond credentials and secrets.

## Reference(s):

- [Logging Format](references/logging-format.md)
- [Promotion and Demotion Rules](references/promotion-rules.md)
- [Heartbeat Review Procedure](references/heartbeat-review.md)
- [Workspace Layout](references/workspace-layout.md)
- [OpenClaw Homepage](https://github.com/muhamadbasim/oktoclaw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and workspace file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates persistent local workspace memory files when the agent applies the workflow.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
