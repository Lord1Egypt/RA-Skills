## Description: <br>
Generate reusable Cypher or SPARQL query templates for common graph database operations such as finding nodes, relationships, paths, and aggregations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fisa712](https://clawhub.ai/user/fisa712) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to scaffold reusable Cypher or SPARQL templates for node lookup, relationship traversal, path discovery, aggregation, filtering, and graph exploration workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated graph queries may be unsafe or misleading if labels, properties, relationship types, predicates, operators, or IRIs come from untrusted input. <br>
Mitigation: Review generated queries before execution and use strict allowlists for graph identifiers, predicates, operators, and IRIs. <br>
Risk: Templates may expose sensitive graph data or run expensive traversals when used directly in production. <br>
Mitigation: Use least-privilege database roles, result limits, auditing, privacy controls, and bounded traversal depth. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fisa712/graph-template-query-generator) <br>
- [ClawHub project homepage](https://clawhub.com) <br>
- [Template patterns](references/template-patterns.md) <br>
- [Template examples](examples/template-examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown with Cypher, SPARQL, JSON, and Python code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs commonly include reusable query templates, parameter lists, usage examples, query explanations, performance notes, and index recommendations.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
