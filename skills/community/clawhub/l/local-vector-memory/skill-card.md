## Description: <br>
Store, search, and manage local vector memories using Ollama embeddings with Qdrant, supporting Chinese and English text without cloud dependencies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jancong](https://clawhub.ai/user/jancong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to add local semantic memory backed by Ollama embeddings and Qdrant storage. It is useful for storing, searching, reindexing, and deleting local text memories without cloud APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on an external PyPI package and a local Ollama embedding model. <br>
Mitigation: Install it only after reviewing those dependencies and confirming they are appropriate for your environment. <br>
Risk: Reindexing broad local directories can make unintended files searchable in the local vector store. <br>
Mitigation: Index only deliberately approved directories and enable periodic reindexing only for paths you intend to search. <br>


## Reference(s): <br>
- [PyPI project: local-vector-memory](https://pypi.org/project/local-vector-memory/) <br>
- [GitHub repository: JanCong/local-vector-memory](https://github.com/JanCong/local-vector-memory) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration, JSON] <br>
**Output Format:** [Markdown with inline bash, Python, environment variable tables, and JSON-capable CLI examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local-only usage guidance for Ollama and Qdrant workflows; no cloud API keys are required.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
