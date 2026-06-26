## Description: <br>
Operate Milvus vector database with pymilvus - collections, vector search, hybrid search, indexes, RBAC, partitions, and more via Python code. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Lumina2025](https://clawhub.ai/user/Lumina2025) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to work with Milvus vector databases through pymilvus for collection design, vector CRUD, similarity and hybrid search, indexing, partitions, databases, RBAC, RAG pipelines, semantic search, and recommendation systems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Milvus credentials or broad privileges could allow unintended database access or administrative actions. <br>
Mitigation: Use least-privilege Milvus credentials and avoid default admin credentials in production. <br>
Risk: Delete, drop, and RBAC operations can remove data or change access controls. <br>
Mitigation: Confirm destructive and permission-changing actions before execution. <br>
Risk: Vector collections may store sensitive or untrusted content. <br>
Mitigation: Review data sensitivity before ingestion and avoid storing content that should not be persisted or searched. <br>


## Reference(s): <br>
- [pymilvus GitHub Repository](https://github.com/milvus-io/pymilvus) <br>
- [Milvus](https://milvus.io/) <br>
- [ClawHub Skill Page](https://clawhub.ai/Lumina2025/milvus) <br>
- [Publisher Profile](https://clawhub.ai/user/Lumina2025) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python and shell command code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3.8+, pymilvus, and a Milvus URI or local Milvus Lite database path.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
