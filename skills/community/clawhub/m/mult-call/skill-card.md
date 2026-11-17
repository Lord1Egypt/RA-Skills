## Description:

Mult Call analyzes metric and dimension output from intent recognition, recalls similar question-and-SQL examples from a vector knowledge base, and retrieves table DDL from a graph database.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lovenervermore](https://clawhub.ai/user/lovenervermore)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data application teams use this skill in a SQL-generation workflow to enrich an interpreted user query with table schema, metric context, and relevant question-and-SQL examples before generating SQL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read broad environment files and pass the process environment into a Python subprocess.

Mitigation: Install it with a dedicated, minimal .env containing only the required Neo4j, Milvus, and embedding variables.

Risk: Standalone execution can contact configured Neo4j, Milvus, and embedding services and can write or clean workflow JSON files.

Mitigation: Review service endpoints and credentials before running, and execute it only in a workspace where the workflow JSON files are expected to be modified.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lovenervermore/skills/mult-call)
- [Publisher Profile](https://clawhub.ai/user/lovenervermore)

## Skill Output:

**Output Type(s):** [text, code, configuration]

**Output Format:** [JSON object containing table DDL text, metric context, similar question-and-SQL pairs, and workflow metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill can degrade independently when the graph database or vector retrieval service is unavailable.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter lists 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
