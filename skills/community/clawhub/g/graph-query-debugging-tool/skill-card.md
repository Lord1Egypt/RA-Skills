## Description: <br>
Diagnose errors in Cypher or SPARQL queries and suggest fixes for syntax issues, schema mismatches, and incorrect graph traversal patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fisa712](https://clawhub.ai/user/fisa712) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to diagnose failing or incorrect graph database queries, understand Cypher and SPARQL errors, and produce corrected query patterns with supporting explanations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Suggested corrected queries, index examples, or schema-change guidance may be unsuitable for a real graph database. <br>
Mitigation: Review suggestions against the actual graph schema and test them in a non-production environment before execution. <br>
Risk: Schema mismatch findings can be incomplete when the user does not provide accurate schema context. <br>
Mitigation: Provide current node labels, relationship types, properties, and sample records when asking the skill to validate a query. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/fisa712/graph-query-debugging-tool) <br>
- [ClawHub Homepage](https://clawhub.com) <br>
- [Debugging Patterns](references/debugging-patterns.md) <br>
- [Query Debugging Examples](examples/query-debugging-examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown with query code blocks and structured debugging reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes corrected Cypher or SPARQL snippets, issue explanations, schema validation notes, and review-before-execution guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
