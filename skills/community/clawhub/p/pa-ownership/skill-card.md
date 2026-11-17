## Description:

Autonomous task tracking with retry loops and proactive updates. Use when Heleni takes ownership of a task that needs to be tracked, retried on failure, and reported when complete or stuck. Integrates with heartbeat to surface stale tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[netanel-abergel](https://clawhub.ai/user/netanel-abergel)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and personal-agent operators use this skill to have Heleni persist owned tasks, retry blocked work, surface stale tasks through heartbeat checks, and report completion or failure to the task initiator.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad automatic execution, retry, messaging, memory-writing, and heartbeat persistence authority may act on unintended or untrusted task requests.

Mitigation: Install only for trusted task initiators, gate group-triggered tasks, and require confirmation before sensitive actions.

Risk: Task content may be written to memory files or outbound reports, exposing sensitive details.

Mitigation: Minimize or redact sensitive task content before writing memory or sending status reports.

Risk: Shell-sourcing the local .context file can execute unintended content if the file is modified or untrusted.

Mitigation: Do not shell-source .context unless it is controlled and reviewed; prefer a parsed configuration format for deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/netanel-abergel/skills/pa-ownership)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline JSON, Python, shell, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces task status records, retry guidance, heartbeat snippets, and human-facing progress or failure reports.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
