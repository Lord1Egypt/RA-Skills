## Description:

Integrates ChromaDB with Ollama embeddings for long-term memory and auto-recalls relevant context to enhance conversations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[broedkrummen](https://clawhub.ai/user/broedkrummen)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to connect an agent to a configured ChromaDB collection and Ollama embedding service for searchable long-term memory and optional automatic context recall.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts may be sent to configured ChromaDB and embedding endpoints.

Mitigation: Use trusted endpoints, keep them local unless remote services are intentional, and avoid sending secrets or private transcripts.

Risk: Stored memories can be injected into future turns through auto-recall.

Mitigation: Review whether autoRecall should be disabled and apply controls for reviewing, filtering, and deleting indexed content.

Risk: Untrusted indexed documents may influence future agent context.

Mitigation: Index only trusted sources or review retrieved memory content before relying on it.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/broedkrummen/skills/memory-chromadb)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown-formatted text responses and prepended context snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Configurable ChromaDB URL, collection ID or name, Ollama URL, embedding model, auto-recall behavior, result count, and minimum similarity score.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
