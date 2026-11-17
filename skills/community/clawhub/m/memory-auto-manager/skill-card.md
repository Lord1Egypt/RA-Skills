## Description:

Automatic memory management based on built-in memory-lancedb-local-storage that auto-extracts key points, compresses conversation, writes to MEMORY.md, and updates the vector index after session ends.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xuchuanyu1](https://clawhub.ai/user/xuchuanyu1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to automatically distill completed conversations into durable memory entries and refresh the local vector memory index for future retrieval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conversation-derived content may be automatically persisted to MEMORY.md and indexed for later retrieval.

Mitigation: Use only in workspaces where retained chat content is appropriate, and add review-before-save, redaction, retention, and deletion controls before use with sensitive data.

Risk: Automatic session and batch triggers can process more conversation history than a user may expect.

Mitigation: Constrain trigger scope and require explicit opt-in for automated processing in environments with confidential, regulated, or untrusted content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xuchuanyu1/skills/memory-auto-manager)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown memory entries appended to MEMORY.md, log text, and OpenClaw memory index commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the current OpenClaw LLM to summarize sessions, classify entries, and update the local vector index.]

## Skill Version(s):

1.0.0 (source: release metadata and _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
