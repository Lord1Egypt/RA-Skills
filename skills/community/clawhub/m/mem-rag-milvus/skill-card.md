## Description: <br>
Memory management skill for AI assistants that stores, retrieves, deletes, and searches memories using SQLite by default or Milvus with optional Ollama embeddings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liushuangfa666](https://clawhub.ai/user/liushuangfa666) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to give assistants persistent memory backed by local SQLite storage or optional Milvus vector search. It supports storing memory content with metadata, searching recent or semantically similar memories, and managing memory records through a Python API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stored memories can include sensitive content and are persisted in the configured database and JSON backup files. <br>
Mitigation: Do not store secrets or regulated data unless the database and backup paths are controlled, and explicitly remove backup files when deleting memories. <br>
Risk: Milvus and Ollama configurations can send stored memory content or search text to configured local services. <br>
Mitigation: Use only trusted Milvus and Ollama endpoints under your control, and review endpoint configuration before enabling vector search. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liushuangfa666/mem-rag-milvus) <br>
- [OpenClaw RAG Memory documentation](https://docs.openclaw.ai/skills/rag-memory) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, guidance] <br>
**Output Format:** [JSON-like Python dictionaries and text status messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results include memory IDs, content, timestamps, metadata, and optional distance scores when vector search is available.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
