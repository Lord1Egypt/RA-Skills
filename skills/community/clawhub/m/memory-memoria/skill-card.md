## Description:

Use Memoria as OpenClaw's durable memory slot for cross-session recall, storage, correction, deletion, snapshots, rollback, branches, merge, and long-term memory workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[randomradio](https://clawhub.ai/user/randomradio)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to configure and operate Memoria as durable external memory, including storing reusable facts, retrieving prior context, repairing incorrect memories, and managing snapshots or branches for reversible memory changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow installs and enables an unpinned third-party plugin.

Mitigation: Review the plugin before installation and prefer a pinned, verified version.

Risk: The setup example includes weak root database credentials.

Mitigation: Do not copy the root:111 example; create a dedicated least-privilege database account with a strong secret.

Risk: Durable memory can retain credentials or other sensitive data if deliberately stored.

Mitigation: Avoid storing secrets or sensitive data in durable memory unless the user explicitly accepts the persistence risk.

Risk: Forget, purge, rollback, and merge operations can remove or alter stored memory.

Mitigation: Preview target records and confirm before applying destructive or broad memory changes.

## Reference(s):

- [Memoria homepage](https://github.com/matrixorigin/Memoria)
- [OpenClaw Setup](references/setup.md)
- [Tool Surface](references/tool-surface.md)
- [Memory Slot Operations](references/operations.md)
- [Usage Patterns](references/patterns.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, text]

**Output Format:** [Markdown with inline shell commands and tool-selection guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides explicit durable-memory operations; outputs may include setup commands, memory workflow recommendations, and verification steps.]

## Skill Version(s):

0.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
