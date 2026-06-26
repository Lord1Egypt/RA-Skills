## Description: <br>
Converts documents to Markdown, classifies them, extracts keywords, and enables local keyword and vector search in a private knowledge base. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[michealxie001](https://clawhub.ai/user/michealxie001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to build a local, searchable private knowledge base from documents such as PDFs, Office files, web documents, text files, images, archives, and Feishu-downloaded files. It supports document ingestion, classification, keyword search, semantic search, listing, retrieval, deletion, and category management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Imported documents may include private or sensitive content that is converted, stored, indexed, and searched locally. <br>
Mitigation: Use an isolated OpenClaw workspace, review files before ingestion, and avoid shared /tmp auto-ingest directories for sensitive documents. <br>
Risk: Setup and vector search can install Python dependencies into the active environment. <br>
Mitigation: Run initialization and vector-index commands in a dedicated Python environment and review dependency versions before enabling automation. <br>
Risk: Document deletion removes the Markdown file and JSON index entry, while vector-index deletion behavior needs manual verification. <br>
Mitigation: Verify vector-search results after deleting sensitive documents and rebuild or clear the ChromaDB index when necessary. <br>
Risk: Feishu or cron-driven auto-ingest can import newly downloaded files without manual review. <br>
Mitigation: Enable auto-ingest only for trusted directories and review Feishu or cron integrations before continuous scanning. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/michealxie001/knowledge-base-001) <br>
- [Publisher profile](https://clawhub.ai/user/michealxie001) <br>
- [Microsoft MarkItDown documentation](https://github.com/microsoft/markitdown) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with CLI commands, plus text and JSON status output from the bundled scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local Markdown files, JSON indexes, and optional ChromaDB vector data under ~/.openclaw/workspace/knowledge-base.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
