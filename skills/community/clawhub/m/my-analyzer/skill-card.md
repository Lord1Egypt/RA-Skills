## Description:

基于 Chroma、Ollama 与 MCP 的本地 RAG 检索技能，用于 OpenClaw 查询私有知识库与 PDF 文档。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xjw163](https://clawhub.ai/user/xjw163)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users, local RAG developers, and teams with private knowledge bases use this skill to query local PDFs, project documents, meeting notes, technical materials, and Chroma-backed document collections through an MCP tool.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is intended to query a private local Chroma knowledge base.

Mitigation: Install it only for agents that should access that knowledge base, and limit indexed documents to material the agent is allowed to retrieve.

Risk: Installation uses unpinned Python dependencies.

Mitigation: Use a virtual environment or container, pin dependency versions, and review package versions before deployment.

Risk: The skill depends on a referenced local MCP server script.

Mitigation: Inspect rag_mcp_server.py before connecting it to private documents.

Risk: The embedding model source affects retrieval behavior and trust.

Mitigation: Verify the Ollama model source where possible before using it with private data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xjw163/skills/my-analyzer)
- [Publisher profile](https://clawhub.ai/user/xjw163)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON configuration examples, and JSON retrieval-result examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The MCP tool returns retrieved document snippets with source metadata and optional page metadata.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
