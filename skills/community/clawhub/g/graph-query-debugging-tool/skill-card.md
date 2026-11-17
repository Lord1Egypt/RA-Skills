## Description:

Diagnose errors in Cypher or SPARQL queries and suggest fixes for syntax issues, schema mismatches, and incorrect graph traversal patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fisa712](https://clawhub.ai/user/fisa712)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to debug Cypher and SPARQL graph queries, identify syntax and schema issues, and produce corrected query versions with practical explanations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Suggested database changes such as index creation can affect database performance or schema state if run unreviewed.

Mitigation: Review proposed database changes before running them, especially on production systems.

Risk: Corrected query suggestions may be incomplete when the user does not provide an accurate graph schema.

Mitigation: Validate suggested queries against the target database schema and test on representative data before relying on results.

## Reference(s):

- [Skill Definition](artifact/SKILL.md)
- [Query Debugging Patterns](artifact/references/debugging-patterns.md)
- [Query Debugging Examples](artifact/examples/query-debugging-examples.md)
- [ClawHub Skill Page](https://clawhub.ai/fisa712/skills/graph-query-debugging-tool)
- [ClawHub Metadata Homepage](https://clawhub.com)
- [Publisher Profile](https://clawhub.ai/user/fisa712)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown explanations with corrected query snippets, diagnostic steps, and optional structured analysis summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include schema validation notes, relationship analysis, performance observations, and alternative queries.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
