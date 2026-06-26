## Description: <br>
Connect to Neo4j graph databases and execute Cypher queries for storing, querying, and managing knowledge graph data using the property graph model. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fisa712](https://clawhub.ai/user/fisa712) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to plan Neo4j-backed knowledge graph work, including Cypher queries, node and relationship modeling, indexing, transactions, and connector configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The included Python connector reports successful Neo4j operations while simulating connection, query, transaction, and index behavior. <br>
Mitigation: Replace or rewrite the connector around the official Neo4j driver and validate behavior against a test Neo4j database before using it for real workloads. <br>
Risk: Cypher examples include create, update, delete, index, and bulk operations that can change or remove graph data if run directly. <br>
Mitigation: Review each query, use least-privileged credentials, test in a non-production database, and require explicit approval before destructive operations. <br>
Risk: Neo4j credentials and connection settings are required, and sample snippets show credentials inline. <br>
Mitigation: Load credentials from a secrets manager or environment variables, avoid committing secrets, and restrict logging of connection details. <br>
Risk: Sample connection configuration includes trusting all certificates. <br>
Mitigation: Use validated TLS settings and trusted certificate authorities for encrypted connections instead of accepting all certificates. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/fisa712/neo4j-integration) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/fisa712) <br>
- [ClawHub Homepage](https://clawhub.com) <br>
- [Neo4j Integration README](README.md) <br>
- [Neo4j Design Patterns](references/neo4j-patterns.md) <br>
- [Neo4j Examples](examples/neo4j-examples.md) <br>
- [Neo4j Connector Script](scripts/neo4j_connector.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and Cypher code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Neo4j connection settings, Cypher snippets, result-shape descriptions, and implementation cautions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
