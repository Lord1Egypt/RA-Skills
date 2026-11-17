## Description:

Memora Kb helps an agent work with a self-hosted personal knowledge base for document upload, semantic search, AI-assisted Q&A, and knowledge graph exploration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zzlzzlzzl15](https://clawhub.ai/user/zzlzzlzzl15)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to connect an agent to a Memora backend, search personal knowledge assets, retrieve source-backed answers, upload or create documents, and inspect document details. It is suited for personal or team knowledge-management workflows where the backend endpoint and provider configuration are trusted.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Manual installation instructions point to unpinned remote installer code.

Mitigation: Prefer the ClawHub package path or a pinned, reviewed Memora commit; inspect installer code before running manual setup.

Risk: Uploaded documents and user questions may be sent to the configured backend and, depending on backend settings, to external LLM, embedding, or rerank providers.

Mitigation: Keep KB_API_BASE on localhost or a trusted HTTPS service, review provider configuration, and avoid sensitive documents unless the backend and providers are approved for that data.

Risk: API keys and provider credentials may appear in local environment files or troubleshooting output.

Mitigation: Do not paste full API keys into prompts, logs, or shared outputs; redact secrets when debugging.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zzlzzlzzl15/skills/memora-kb)
- [Publisher Profile](https://clawhub.ai/user/zzlzzlzzl15)
- [Memora README](https://github.com/zzlzzlzzl15/Memora/blob/main/personal_knowledge_base/README.md)
- [Memora Repository](https://github.com/zzlzzlzzl15/Memora)
- [Memora Issues](https://github.com/zzlzzlzzl15/Memora/issues)
- [RAG-Anything](https://github.com/RAG-Anything/RAG-Anything)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, API calls]

**Output Format:** [Markdown guidance with shell commands and JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires KB_API_BASE and may use backend LLM, embedding, or rerank provider credentials depending on deployment.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 2.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
