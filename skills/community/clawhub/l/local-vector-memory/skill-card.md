## Description:

Store, search, and manage local vector memories using Ollama embeddings with Qdrant, supporting Chinese and English text without cloud dependencies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jancong](https://clawhub.ai/user/jancong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to install and operate a local semantic memory layer backed by Ollama embeddings and Qdrant. It supports adding memories, searching them, reindexing local Markdown directories, and integrating local recall into OpenClaw workflows without cloud APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs an unpinned PyPI package.

Mitigation: Install in an isolated virtual environment and pin or review the local-vector-memory package before use.

Risk: Reindexing local directories can store private notes or OpenClaw memory in a local vector database.

Mitigation: Only reindex directories approved for local vector storage and review retention expectations for the Qdrant database path.

Risk: Optional cron or HEARTBEAT.md reindexing creates persistent refresh behavior for indexed content.

Mitigation: Enable periodic reindexing only when ongoing local content refresh is intended and documented for the operator.

## Reference(s):

- [Local Vector Memory skill page](https://clawhub.ai/jancong/skills/local-vector-memory)
- [PyPI: local-vector-memory](https://pypi.org/project/local-vector-memory/)
- [GitHub: JanCong/local-vector-memory](https://github.com/JanCong/local-vector-memory)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell commands, Python examples, configuration tables, and CLI output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce JSON-formatted search results when using the documented lvm search --json command.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
