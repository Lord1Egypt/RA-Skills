## Description: <br>
Operate Milvus vector database with pymilvus Python SDK for connection setup, collection management, vector search, hybrid search, full-text search, indexing, partitions, databases, and RBAC via Python code. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhanshuyou](https://clawhub.ai/user/zhanshuyou) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to have an agent draft Milvus and pymilvus workflows for vector database administration, semantic search, RAG, indexing, and access control tasks. It is intended for environments where users can supply their own Milvus connection details and review database-changing operations before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes examples for delete, drop, truncate, password, role, and privilege operations that can change or remove Milvus resources. <br>
Mitigation: Use least-privilege credentials, verify the target database or collection, and require explicit user confirmation before destructive or administrative operations. <br>
Risk: Generated connection code could expose or misuse database credentials if connection details are assumed or hardcoded. <br>
Mitigation: Ask for the deployment type, URI, authentication method, and database name at runtime, and avoid embedding secrets in reusable files or examples. <br>


## Reference(s): <br>
- [Milvus documentation](https://milvus.io/) <br>
- [pymilvus Python SDK](https://github.com/milvus-io/pymilvus) <br>
- [Collection Management](references/collection.md) <br>
- [Vector Operations](references/vector.md) <br>
- [Index Management](references/index.md) <br>
- [Partition Management](references/partition.md) <br>
- [Database Management](references/database.md) <br>
- [User and Role Management](references/user-role.md) <br>
- [Common Patterns](references/patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with Python and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include pymilvus API examples, connection placeholders, schema definitions, index parameters, search filters, and operational cautions.] <br>

## Skill Version(s): <br>
0.0.2 (source: ClawHub release metadata; artifact metadata lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
