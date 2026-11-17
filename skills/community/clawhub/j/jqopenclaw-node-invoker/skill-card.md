## Description:

Helps an agent call JQOpenClawNode capabilities through Gateway node.invoke for remote file operations, process execution and management, system information, screenshots, notifications, clipboard access, input control, command checks, and node self-updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[188080501](https://clawhub.ai/user/188080501)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and administrators use this skill to construct valid Gateway node.invoke requests for JQOpenClawNode remote administration tasks and to interpret errors with concrete retry guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables broad remote node administration, including file changes, command execution, process termination, screenshots, clipboard access, input control, and node updates.

Mitigation: Install it only for trusted administrators, keep Gateway allowCommands narrow, and require explicit confirmation before destructive, privacy-sensitive, or state-changing actions.

Risk: The node.selfUpdate workflow can replace the node from caller-supplied HTTP or HTTPS downloads with only MD5 checking.

Mitigation: Avoid enabling node.selfUpdate unless updates are restricted to signed releases from trusted sources and integrity checks are independently controlled.

## Reference(s):

- [JQOpenClawNode call specification](artifact/references/command-spec.md)
- [ClawHub skill release page](https://clawhub.ai/188080501/skills/jqopenclaw-node-invoker)

## Skill Output:

**Output Type(s):** [Guidance, JSON, Shell commands, Configuration]

**Output Format:** [Markdown with JSON request examples and concise status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requests normally include nodeId, command, params, timeoutMs, and a fresh idempotencyKey.]

## Skill Version(s):

26.3.9 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
