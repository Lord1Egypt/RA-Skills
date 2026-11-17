## Description:

Build and operate a unified OpenClaw memory system that combines native Markdown memory, project memory, structured event memory, migration from older PROJECTS.md/improvements.md layouts, memorySearch configuration, and upgrade-safe maintenance workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhongtw1979](https://clawhub.ai/user/zhongtw1979)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and developers use this skill to install, migrate, audit, and maintain a workspace memory layout that combines Markdown project records, structured event logs, semantic retrieval digests, and upgrade checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Rollback can delete or overwrite writable files if it is run against an untrusted or crafted manifest.

Mitigation: Inspect the rollback manifest first and use dry-run before allowing rollback to modify files.

Risk: Remote memorySearch providers may store an API key in local OpenClaw configuration when a key is supplied.

Mitigation: Prefer local retrieval when possible, avoid passing API keys unless local configuration storage is acceptable, and review configuration changes before applying them.

Risk: Optional session memory can retain conversation-derived memory.

Mitigation: Enable session memory only when conversation-derived retention is intended and acceptable for the workspace.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhongtw1979/skills/openclaw-memory-fusion-core)

## Skill Output:

**Output Type(s):** [Markdown files, JSON event records, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Mutating commands are dry-run by default and can write workspace memory files, OpenClaw configuration, manifests, checkpoints, and JSONL event records when apply flags are used.]

## Skill Version(s):

1.0.1 (source: server release metadata and script VERSION)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
