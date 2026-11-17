## Description:

Set up local semantic memory search in OpenClaw using Ollama and nomic-embed-text so memory embeddings can run locally without cloud API keys.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spmzt](https://clawhub.ai/user/spmzt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure OpenClaw memory search with a local Ollama embedding model for private, offline-capable semantic retrieval. It provides setup commands, configuration examples, and troubleshooting guidance for local memory search.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional extraPaths can recursively index additional directories into memory search.

Mitigation: Review extraPaths before use and avoid secrets, private notes, unrelated team folders, or broad absolute paths unless that indexing is intentional.

Risk: Incorrect provider or baseUrl settings can prevent local Ollama routing.

Mitigation: Set provider to "ollama" and use the Ollama base URL without a /v1 suffix or trailing slash.

## Reference(s):

- [ClawHub Release Page](https://clawhub.ai/spmzt/skills/ollama-memory-with-freebsd)
- [Ollama](https://ollama.ai/)
- [README](README.md)
- [Configuration Reference](references/config-reference.md)
- [Troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only guidance for configuring OpenClaw, Ollama, model selection, and troubleshooting.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
