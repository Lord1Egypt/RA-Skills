## Description: <br>
Map GraphQL queries and schemas to underlying graph database operations, enabling applications to access knowledge graph data through GraphQL APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fisa712](https://clawhub.ai/user/fisa712) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to design GraphQL API mappings for graph databases and to translate schema/query patterns into Cypher, Gremlin, SPARQL, and GraphQL-shaped responses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated graph database queries may be unsafe or misleading if run directly against live databases, especially when based on untrusted GraphQL input. <br>
Mitigation: Review generated queries before execution, use read-only or least-privilege database credentials by default, and avoid exposing the translator directly to untrusted input. <br>
Risk: The release presents production-ready query generation while the security evidence notes unparameterized query construction and limited live-use safety guidance. <br>
Mitigation: Add strict schema-based validation and parameterized query construction before production use. <br>


## Reference(s): <br>
- [GraphQL Mapping Patterns](references/graphql-mapping-patterns.md) <br>
- [GraphQL Mapping Examples](examples/graphql-mapping-examples.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/fisa712/graphql-graph-mapping) <br>
- [ClawHub Homepage](https://clawhub.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown with query examples, Python snippets, and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include generated Cypher, Gremlin, SPARQL, GraphQL schema mappings, execution plans, and performance guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
