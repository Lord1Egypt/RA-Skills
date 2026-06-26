## Description: <br>
Memora is a self-hosted personal AI knowledge base skill for managing, retrieving, querying, and visualizing personal knowledge assets with document upload, semantic search, AI chat, web scraping, and graph exploration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zzlzzlzzl15](https://clawhub.ai/user/zzlzzlzzl15) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to connect an agent to a Memora knowledge-base backend, search and retrieve documents, upload or create knowledge assets, and ask AI-assisted questions over their personal corpus. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Documents, prompts, embeddings, reranking requests, or chat content may be sent to the configured Memora backend or external AI providers. <br>
Mitigation: Use a trusted local backend for private documents, review provider configuration before use, and avoid uploading secrets or highly sensitive files unless the deployment is local-only. <br>
Risk: The skill depends on the KB_API_BASE environment variable, so a misconfigured URL can send knowledge-base requests to the wrong service. <br>
Mitigation: Set KB_API_BASE explicitly, verify the destination before running upload or query commands, and prefer local or controlled endpoints for sensitive data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zzlzzlzzl15/skills/memora-knowledge-base) <br>
- [Memora README](https://github.com/zzlzzlzzl15/Memora/blob/main/personal_knowledge_base/README.md) <br>
- [RAG-Anything reference](https://github.com/RAG-Anything/RAG-Anything) <br>
- [Obsidian graph view](https://obsidian.md/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires KB_API_BASE to point to the selected Memora backend.] <br>

## Skill Version(s): <br>
2.0.7 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
