## Description:

OpenClaw-native memory maintenance, snapshots, indexing health checks, and review workflows for protecting context, troubleshooting memory search, reviewing durable learnings, safely archiving old daily notes, and inspecting provider or index health.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hazemelerefey](https://clawhub.ai/user/hazemelerefey)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to maintain OpenClaw memory without changing its memory model, including health checks, snapshots before risky work, semantic search troubleshooting, review drafts from recent daily notes, and safe archival of older daily notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact references PowerShell scripts that are not bundled with this release.

Mitigation: Treat the skill as workflow guidance unless trusted script files are supplied separately, and verify each script path before execution.

Risk: Repair or archive workflows can modify memory files or move daily notes.

Mitigation: Review the trusted script implementation and create a snapshot before repair, cleanup, provider, index, or archival operations.

Risk: Keyword fallback search can be mistaken for semantic memory search.

Mitigation: Report fallback mode clearly and avoid presenting keyword results as semantic retrieval.

## Reference(s):

- [Memory Manager v2 Workflow](references/workflow.md)
- [ClawHub Skill Page](https://clawhub.ai/hazemelerefey/skills/openclaw-memory-manager)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with inline PowerShell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces workflow guidance for existing OpenClaw memory files and may reference external PowerShell scripts that must be supplied and reviewed separately.]

## Skill Version(s):

2.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
