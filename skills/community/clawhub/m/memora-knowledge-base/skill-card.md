## Description:

Memora Knowledge Base helps agents connect to a self-hosted personal knowledge base for document management, semantic search, AI Q&A, and knowledge graph exploration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zzlzzlzzl15](https://clawhub.ai/user/zzlzzlzzl15)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to manage personal documents, query a Memora backend, retrieve AI-organized answers, upload or create knowledge assets, and inspect document details through an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send private documents, embeddings, and chat prompts to the configured Memora backend or downstream AI providers.

Mitigation: Use only a backend you control, prefer localhost or HTTPS, and avoid uploading sensitive files unless you understand where retrieval, embeddings, and chat prompts are processed.

Risk: Manual setup instructions include running mutable installer code.

Mitigation: Pin or inspect the upstream installer before running ./install.sh, and review the skill before installation.

Risk: Troubleshooting commands can expose API keys if .env output is shared.

Mitigation: Do not paste secret-bearing .env output into support channels or logs.

## Reference(s):

- [Memora ClawHub Skill Page](https://clawhub.ai/zzlzzlzzl15/skills/memora-knowledge-base)
- [Memora GitHub Repository](https://github.com/zzlzzlzzl15/Memora)
- [Memora Personal Knowledge Base README](https://github.com/zzlzzlzzl15/Memora/blob/main/personal_knowledge_base/README.md)
- [RAG-Anything Reference](https://github.com/RAG-Anything/RAG-Anything)
- [Obsidian](https://obsidian.md/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON API responses and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires KB_API_BASE to point at the Memora backend; API helper commands can list, search, upload, create, and retrieve documents.]

## Skill Version(s):

2.1.0 (source: release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
