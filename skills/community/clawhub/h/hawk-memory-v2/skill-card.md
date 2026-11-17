## Description:

Pure Python memory management with four-layer decay, context compression, extraction, vector retrieval, and self-improving features for AI agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[relunctance](https://clawhub.ai/user/relunctance)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to add persistent memory, task-state recall, context compression, and memory extraction to Python-based AI agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist conversation-derived data and imported markdown memories locally.

Mitigation: Avoid storing secrets or regulated data, and regularly review and purge the local ~/.hawk memory files.

Risk: Recalled memory may be injected into future prompts as high-priority context.

Mitigation: Review stored memories before use in sensitive workflows and remove stale or untrusted memories.

Risk: Configured AI providers or custom endpoints may receive prompts, recalled memories, markdown memory files, or API credentials.

Mitigation: Use local or keyword modes where possible, and only configure AI providers or endpoints that are explicitly trusted.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/relunctance/skills/hawk-memory-v2)
- [README](artifact/README.md)
- [Four-Tier Memory Architecture](artifact/references/memory-system.md)
- [Task State Memory](artifact/references/task-state.md)
- [Structured Memory Format](artifact/references/structured-memory.md)
- [Context Injection Strategies](artifact/references/injection-strategies.md)
- [Compression Strategies](artifact/references/compression-strategies.md)
- [CLI Reference](artifact/references/cli.md)
- [LanceDB Integration](artifact/references/lancedb-integration.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
