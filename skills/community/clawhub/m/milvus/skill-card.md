## Description:

Operate Milvus vector databases with pymilvus for collections, vector search, hybrid search, indexes, RBAC, partitions, and related Python workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lumina2025](https://clawhub.ai/user/lumina2025)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to operate Milvus vector databases from Python, including connection setup, schema and collection management, vector CRUD, similarity and hybrid search, indexing, partitions, databases, and RBAC tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide destructive Milvus operations such as drop, delete, and RBAC changes.

Mitigation: Review and confirm destructive database or access-control changes before allowing them to run.

Risk: The examples include a default root:Milvus credential for local or standalone Milvus connections.

Mitigation: Replace default credentials with hardened secrets before using the skill against non-development systems.

Risk: Installing pymilvus adds a Python dependency to the agent environment.

Mitigation: Install only in approved environments and pin or lock the dependency when possible.

## Reference(s):

- [ClawHub Milvus Skill Page](https://clawhub.ai/lumina2025/skills/milvus)
- [pymilvus Project Homepage](https://github.com/milvus-io/pymilvus)
- [Milvus Website](https://milvus.io/)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown with Python and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include database operation examples and cautions for destructive Milvus actions.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
