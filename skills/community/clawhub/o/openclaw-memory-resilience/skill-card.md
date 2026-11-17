## Description:

Configure OpenClaw agent memory to survive compaction and session restarts, including gateway compaction defaults, file-based memory architecture, archival patterns, diagnostics, and context-footer monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ferosin](https://clawhub.ai/user/ferosin)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to configure OpenClaw workspaces so important instructions, preferences, and decisions are preserved across compaction and session restarts. It is also useful for diagnosing memory loss, tuning compaction headroom, and organizing searchable long-term memory files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Long-lived memory files and indexed archives can persist sensitive information if used for secrets or full connection details.

Mitigation: Use the memory pattern only for non-sensitive notes, preferences, decisions, and references; store secret-manager names or retrieval procedures instead of plaintext secrets.

Risk: Silent memory flushes can write conversation content to disk without a visible user-facing turn.

Mitigation: Enable silent memory flushes only in workspaces where automatic disk persistence is acceptable and review saved memory files before sharing or indexing them.

## Reference(s):

- [Compaction Config - Field Reference](references/config-explained.md)
- [Context Footer - Why It Matters](references/context-footer.md)
- [File Architecture for Memory Durability](references/file-architecture.md)
- [ClawHub skill page](https://clawhub.ai/ferosin/skills/openclaw-memory-resilience)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration, shell commands]

**Output Format:** [Markdown guidance with JSON configuration, Markdown snippets, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes OpenClaw compaction defaults, context-footer thresholds, memory file architecture guidance, and archive/indexing patterns.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
