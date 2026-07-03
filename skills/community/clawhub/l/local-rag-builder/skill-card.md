## Description: <br>
Builds and manages a local RAG system with environment setup, embedding model downloads, document chunking, vector knowledge bases, prompt configuration, and a local web configuration UI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ldxs001](https://clawhub.ai/user/ldxs001) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and technical users use this skill to set up local retrieval workflows, ingest supported text documents into Chroma-backed knowledge bases, and query them from an agent or a standalone local LLM workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install Python packages, download embedding models, and write persistent local RAG data. <br>
Mitigation: Run it in an isolated virtual environment and review package mirrors, model IDs, and persistent data paths before use. <br>
Risk: The local web control panel exposes configuration and file/model management controls. <br>
Mitigation: Keep the web UI bound to localhost or place it behind a trusted firewall; do not expose its port to an untrusted network. <br>
Risk: Standalone mode can send retrieved context to a configured local or remote LLM endpoint. <br>
Mitigation: Review the configured LLM base URL and avoid sending sensitive knowledge base content to untrusted endpoints. <br>
Risk: Knowledge base and model deletion actions can remove local data. <br>
Mitigation: Confirm deletion targets and maintain backups of important knowledge base directories. <br>


## Reference(s): <br>
- [Skill page](https://clawhub.ai/ldxs001/skills/local-rag-builder) <br>
- [Architecture](references/architecture.md) <br>
- [Command reference](references/commands.md) <br>
- [Usage guide](references/guide.md) <br>
- [LLM setup](references/llm-setup.md) <br>
- [Permissions](references/permissions.md) <br>
- [Data directory](references/data-directory.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON configuration examples, and optional JSON query output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Integrated mode returns retrieved context for an agent to answer from; standalone mode can return retrieved answers through a configured LLM service.] <br>

## Skill Version(s): <br>
1.1.3 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
