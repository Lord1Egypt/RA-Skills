## Description: <br>
基于 Chroma、Ollama 与 MCP 的本地 RAG 检索技能，用于 OpenClaw 查询私有知识库与 PDF 文档。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xjw163](https://clawhub.ai/user/xjw163) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users, developers, and internal teams use this skill to query local PDFs, project documents, meeting notes, technical materials, and private knowledge bases through a Chroma-backed RAG workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled artifact is markdown-only and describes a separate rag_mcp_server.py implementation that is not included. <br>
Mitigation: Review the MCP server implementation and configured Chroma database paths before enabling the skill. <br>
Risk: Answers can be incomplete or stale when documents have not been embedded, the vector database is outdated, or retrieval confidence is low. <br>
Mitigation: Rebuild the vector database after adding documents, preserve source metadata in answers, and clearly state when evidence is insufficient. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xjw163/my-analyzer) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Guidance] <br>
**Output Format:** [JSON retrieval results with text snippets and source metadata] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns local document snippets, source names, and page metadata when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact frontmatter lists 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
