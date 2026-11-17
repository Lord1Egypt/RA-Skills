## Description:

LanceDB long-term memory plugin with BM25 + vector hybrid search (RRF or linear reranking).

This skill is ready for commercial/non-commercial use.

## Publisher:

[joeykrug](https://clawhub.ai/user/joeykrug)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to install and configure a LanceDB-backed long-term memory plugin that combines semantic vector search with BM25 keyword search. It supports memory storage, recall, and forgetting, including optional auto-capture and auto-recall.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts or remembered text may be sent to the configured embedding provider.

Mitigation: Use a local embedding endpoint for sensitive work, or disable auto-recall and auto-capture when provider disclosure is not acceptable.

Risk: Conversation details may be persisted as long-term memory.

Mitigation: Review stored memories regularly, delete sensitive entries, and install only when long-term memory behavior matches the workspace privacy expectations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/joeykrug/skills/memory-lancedb-hybrid)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown installation guidance, configuration snippets, shell commands, and plain-text memory tool responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The plugin can persist remembered conversation details locally and can send prompts or remembered text to the configured embedding provider.]

## Skill Version(s):

1.2.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
