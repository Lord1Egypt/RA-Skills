## Description:

Mem RAG Milvus stores, retrieves, and manages AI assistant memories with SQLite by default, optional Milvus vector search, and automatic JSON backups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liushuangfa666](https://clawhub.ai/user/liushuangfa666)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent builders use this skill to persist assistant memories, retrieve recent or semantically similar items, and configure SQLite or Milvus-backed storage for memory workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stored memories and search terms may be sent to the configured or auto-detected Ollama HTTP embedding service.

Mitigation: Use a private local-only embedding endpoint, set OLLAMA_URL deliberately, and avoid storing secrets or regulated data.

Risk: Memory data is persisted locally and automatically backed up to JSON files.

Mitigation: Choose storage and backup paths deliberately, protect the backup directory, and review retention before deployment.

Risk: The security review flagged the default SQLite network behavior and backup controls as needing review.

Mitigation: Review the skill before execution and deploy only after the network and backup behavior matches the intended privacy posture.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/liushuangfa666/skills/mem-rag-milvus)
- [OpenClaw RAG Memory Documentation](https://docs.openclaw.ai/skills/rag-memory)

## Skill Output:

**Output Type(s):** [Text, Code, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python and shell snippets; runtime APIs return memory IDs and search result dictionaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores memory content, metadata, timestamps, embeddings when available, and JSON backups in configured local paths.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
