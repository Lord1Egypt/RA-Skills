## Description:

Operates Milvus vector databases with the pymilvus Python SDK for connection, collection, vector search, indexing, partition, database, and RBAC workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhanshuyou](https://clawhub.ai/user/zhanshuyou)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to have an agent generate Milvus and pymilvus code, shell commands, and configuration guidance for vector database administration, semantic search, RAG, hybrid search, full-text search, and RBAC workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes examples for destructive database and collection operations, including drops, truncates, deletes, and RBAC changes.

Mitigation: Require explicit user confirmation before generating or executing destructive operations or access-control changes, especially in shared, staging, or production environments.

Risk: The skill includes example passwords and wildcard privilege examples that could lead to weak credentials or overly broad access if copied directly.

Mitigation: Replace example passwords with unique secret-managed values and avoid wildcard privileges unless cluster-wide access is deliberately intended.

Risk: Incorrect connection targets or credential handling could affect the wrong Milvus deployment.

Mitigation: Ask for the deployment type, URI, authentication method, and database name before writing connection code, and avoid hardcoding credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhanshuyou/skills/milvus-skill)
- [Milvus documentation](https://milvus.io/)
- [pymilvus](https://github.com/milvus-io/pymilvus)
- [Collection Management](references/collection.md)
- [Database Management](references/database.md)
- [Index Management](references/index.md)
- [Partition Management](references/partition.md)
- [Common Patterns](references/patterns.md)
- [User and Role Management](references/user-role.md)
- [Vector Operations](references/vector.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python code blocks and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-supplied Milvus deployment details and credentials before generating connection code.]

## Skill Version(s):

0.0.2 (source: ClawHub release evidence; artifact metadata reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
