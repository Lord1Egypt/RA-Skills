## Description: <br>
Generate graph queries that perform multi-hop traversal and reasoning across relationships in graph databases and knowledge graphs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fisa712](https://clawhub.ai/user/fisa712) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and knowledge graph practitioners use this skill to draft Cypher and SPARQL queries for multi-hop traversal, path discovery, indirect relationship analysis, and graph reasoning across connected datasets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated graph queries may expose or over-select sensitive records when applied to healthcare, finance, fraud, account, or similar datasets. <br>
Mitigation: Review generated queries before execution and add authorization checks, masking, result limits, and audit controls for sensitive data. <br>
Risk: Unbounded or deep multi-hop traversal can cause expensive graph database queries. <br>
Mitigation: Keep traversal depth bounded, use specific starting nodes and relationship filters, and include LIMIT clauses before running queries on production data. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/fisa712/multi-hop-reasoning-query-builder) <br>
- [ClawHub](https://clawhub.com) <br>
- [Multi-Hop Reasoning Patterns](references/multi-hop-patterns.md) <br>
- [Multi-Hop Reasoning Examples](examples/multi-hop-examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown with Cypher, SPARQL, and Python code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include parameterized graph query templates, path-analysis guidance, complexity notes, and performance recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
