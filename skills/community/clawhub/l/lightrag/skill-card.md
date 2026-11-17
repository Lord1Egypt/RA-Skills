## Description:

Search and manage knowledge bases using LightRAG API. Supports multiple servers, context-aware writing, and direct information retrieval. Use when the user wants to query a LightRAG-powered knowledge base or use it as context for tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ruslanlanket](https://clawhub.ai/user/ruslanlanket)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to configure LightRAG API servers, query knowledge bases in supported retrieval modes, and pass retrieved context into writing or analysis tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configured API keys and knowledge-base queries may expose credentials or sensitive query content.

Mitigation: Use only trusted LightRAG endpoints, avoid API keys on HTTP URLs, and treat ~/.lightrag_config.json as sensitive.

Risk: Broad use is risky while TLS verification and credential storage controls remain unresolved.

Mitigation: Re-enable normal TLS verification and store API keys with restrictive file permissions or a credential store before broader deployment.

Risk: The security verdict is suspicious.

Mitigation: Review the skill before installation and deployment, following the server-provided security guidance.

## Reference(s):

- [LightRAG API Reference](references/API_DOCS.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Plain text or Markdown guidance, with command-line usage and LightRAG query responses or retrieved context.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include retrieved knowledge-base context from configured LightRAG endpoints.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
