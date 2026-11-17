## Description:

Long Task Handoff provides an ultra-light automatic handoff manager for long-running agent sessions at context-boundary moments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hollis9087](https://clawhub.ai/user/hollis9087)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to preserve restart-critical state during context compaction, session transfer, or recovery from an active handoff signal. It helps agents create, update, recover, and validate concise Markdown handoff packets without turning them into project documentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The handoff manager can follow untrusted handoff paths and may write outside the intended workspace in some cases.

Mitigation: Use only in trusted workspaces, inspect handoffs/ACTIVE.md and the handoffs directory for symlinks or external paths, and require strict workspace containment and pre-write validation before low-risk automation use.

Risk: Handoff content may accidentally include secrets or sensitive workspace details if passed into handoff fields.

Mitigation: Do not pass secrets into handoff fields; review generated handoffs and use the bundled validation behavior before relying on the handoff.

## Reference(s):

- [Long Task Handoff Protocol Reference](references/protocol.md)
- [Secret Pattern Rules](references/secret-patterns.json)
- [ClawHub Skill Page](https://clawhub.ai/hollis9087/skills/long-task-handoff)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, JSON, Guidance]

**Output Format:** [Markdown handoff files, JSON command results, and concise agent guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes restart handoff files and ACTIVE.md pointers in the workspace or configured handoff directory.]

## Skill Version(s):

0.3.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
