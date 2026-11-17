## Description:

Semantic memory plugin using m3e-large embeddings with SQLite storage, supporting storage, retrieval, and deletion via cosine similarity search in pure JavaScript.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kalalxy](https://clawhub.ai/user/kalalxy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to give an OpenClaw agent persistent semantic memory backed by an external m3e-large embedding service and local SQLite storage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private memory text, search/delete queries, and embedding API credentials may be sent to the configured embedding service, including over unsecured HTTP if configured that way.

Mitigation: Use only an HTTPS or trusted localhost embedding endpoint, avoid storing secrets or regulated data, and treat embedding provider access as access to memory contents.

Risk: Deleting by semantic query can remove the top matching memory without confirmation.

Mitigation: Prefer deletion by exact memory ID and review query-based deletion behavior before enabling it for sensitive memories.

Risk: Automatic capture and recall can broaden when conversation content is stored or injected.

Mitigation: Disable or tightly scope autoCapture and autoRecall unless their triggers are understood and acceptable for the deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kalalxy/skills/memory-m3e)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)
- [OpenClaw plugin manifest](artifact/openclaw.plugin.json)

## Skill Output:

**Output Type(s):** [text, configuration]

**Output Format:** [Text responses with structured details for stored, recalled, and deleted memories]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses an external embedding endpoint and local SQLite database; retrieval returns ranked semantic matches with similarity scores.]

## Skill Version(s):

1.0.0 (source: server release metadata, package.json, openclaw.plugin.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
