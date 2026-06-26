## Description: <br>
Schema-aware graph database query assistant that detects Neo4j-style schema, generates Cypher from natural language, reviews query safety, executes through HTTP, and formats results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jeffRao](https://clawhub.ai/user/jeffRao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data practitioners use this skill to inspect graph database schemas, generate read-oriented Cypher queries from natural language, execute them against a configured graph database, and present results as tables, graph paths, statistics, or JSON. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent can inspect configured graph database schema and sampled fields using supplied database credentials. <br>
Mitigation: Use a dedicated read-only database account, connect only to databases the user is comfortable letting an agent inspect, and clear cached schema memory if labels, properties, or sampled fields are sensitive. <br>
Risk: Generated Cypher may be incorrect, too broad, or expensive on large graphs. <br>
Mitigation: Review generated Cypher before execution, keep default LIMIT and path-depth controls enabled, and prefer narrow labels, filters, and HTTPS/TLS endpoints. <br>
Risk: Database credentials and endpoint configuration are required for execution. <br>
Mitigation: Avoid admin or production credentials, store credentials outside shared transcripts, and rotate credentials if they are exposed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jeffRao/neo4j-cypher-query-analyze) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Cypher, shell commands, tables, graph-path descriptions, statistics, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include generated Cypher, curl-based Neo4j HTTP API calls, formatted query results, schema-cache guidance, and troubleshooting notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
