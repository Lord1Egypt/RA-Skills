## Description:

Provides CLI and Python helpers for creating, listing, cancelling, retrying, and running priority-based background tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[michealxie001](https://clawhub.ai/user/michealxie001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to queue and monitor background jobs such as code analysis, document generation, backups, and multi-step workflows from CLI or Python integrations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad write, command execution, and cron authority.

Mitigation: Grant only the minimum tools needed for the intended task and avoid cron access until scheduled execution is fully implemented and scoped.

Risk: Security evidence says key advertised scheduler features are missing or under-scoped.

Mitigation: Review and test behavior in an isolated environment before relying on it for production task automation.

Risk: Future WebSocket exposure could create network risk if exposed beyond the local machine.

Mitigation: Keep any WebSocket service bound to localhost unless authentication and network controls are added.

Risk: Dependency evidence includes optional or unused packages.

Mitigation: Pin required dependencies and remove unused optional dependencies before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/michealxie001/skills/oc-task-scheduler)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command snippets; CLI commands emit plain text task status.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Task creation accepts JSON parameters and returns task identifiers, status, priority, timing, result, and error fields when available.]

## Skill Version(s):

1.0.0 (source: release evidence, SKILL.md, lib/__init__.py)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
