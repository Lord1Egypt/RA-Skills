## Description:

MemCore 记忆核心 helps OpenClaw agents retrieve, summarize, and maintain local memory through SQLite-backed trace, pattern, world-model, feedback, and startup-brief workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adchina2025](https://clawhub.ai/user/adchina2025)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to replace full-memory startup loading with concise memory briefs, search historical memory on demand, index recent session state, and run maintenance or diagnostic memory workflows. It is intended for local memory management where the operator can review generated context before it influences future sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Past conversation logs and session state can become persistent local memory and later influence startup context.

Mitigation: Review MEMORY_BRIEF.md before using it as startup context, and manually control first-run indexing and scheduled maintenance until the operator is comfortable with the retained content.

Risk: Sensitive information in OpenClaw memory, session state, or search queries may be indexed or logged locally.

Mitigation: Avoid indexing secrets, review the local SQLite memory layer, and disable or manually control query logging where secret exposure is a concern.

Risk: Server-resolved provenance is unavailable for this release.

Mitigation: Treat the ClawHub publisher profile and local artifact contents as the release evidence, and perform source review before deploying in sensitive environments.

## Reference(s):

- [MemCore Architecture](references/architecture.md)
- [MemCore Usage Guide](references/使用说明.md)
- [EXO1 Upgrade Guide](references/upgrade-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and local generated files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can generate MEMORY_BRIEF.md under the OpenClaw workspace and maintain local SQLite indexes for traces, patterns, feedback, searches, and retrieval state.]

## Skill Version(s):

2.1.0 (source: server release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
