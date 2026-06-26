## Description: <br>
LightRAG-based semantic memory system for AI agents that provides long-term knowledge storage and retrieval using vector embeddings and knowledge graphs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ogi98rus](https://clawhub.ai/user/ogi98rus) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to index and query long-term agent memory with LightRAG, reducing repeated full-file reads and enabling semantic retrieval across memory documents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Indexed files and query text may be sent to the configured OpenAI-compatible provider for embeddings and language-model processing. <br>
Mitigation: Only index content suitable for that provider, use a dedicated API key, and verify OPENAI_BASE_URL before indexing or querying. <br>
Risk: Python dependencies are installed from package indexes and may change over time if left unpinned. <br>
Mitigation: Install in a virtual environment and review or pin the dependencies before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ogi98rus/lightrag-memory) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Plain text query results and Markdown command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports naive, local, global, and hybrid query modes; stores LightRAG data locally by default.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
