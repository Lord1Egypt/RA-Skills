## Description:

Personal knowledge base skill for saving notes, indexing local documents, and searching them with natural-language queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[54lynnn](https://clawhub.ai/user/54lynnn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, agents, and individual users use this skill to create a local searchable knowledge base from notes and documents, then retrieve relevant source text through chat-style prompts or CLI commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private document search and admin APIs may be exposed too broadly.

Mitigation: Run only on a trusted single-user machine and do not expose ports 5777 or 8768 to a LAN or untrusted browser context.

Risk: The skill can browse or index outside the intended knowledge folder.

Mitigation: Avoid placing sensitive documents in reachable paths until API binding, authentication, and path limits are fixed.

Risk: Installation depends on external Ollama and package installation steps.

Mitigation: Use verified Ollama and package sources before installing or pulling embedding models.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/54lynnn/skills/knowledge-rag)
- [Ollama Download](https://ollama.com/download)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and local API or CLI outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local search guidance and retrieval results backed by a local SQLite index and Ollama embeddings.]

## Skill Version(s):

1.6.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
