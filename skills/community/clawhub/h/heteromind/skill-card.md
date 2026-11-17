## Description:

HeteroMind routes natural language questions to SQL databases, knowledge graphs, or table files and generates answers through multi-stage source detection and query generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bahuia](https://clawhub.ai/user/bahuia)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data teams use this skill to answer structured-data questions across relational databases, knowledge graphs, and tabular files. It helps agents choose the likely data source, generate SQL, SPARQL, or Pandas code, and summarize the result.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated SQL, SPARQL, and table-analysis code may run with broader access than the documented safety controls justify.

Mitigation: Use isolated runtimes, nonprivileged credentials, read-only database copies, trusted SPARQL endpoints, and non-sensitive table files.

Risk: Documented sandboxing, read-only query validation, endpoint restrictions, and dependency controls should not be assumed complete.

Mitigation: Keep execution disabled or gated by review until exec-based code execution, SQL validation, endpoint allowlisting, and dependency pinning are fixed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bahuia/skills/heteromind)
- [README](README.md)
- [Usage guide](USAGE.md)
- [Security documentation](SECURITY.md)
- [Source detection configuration](config/source_detection.yaml)
- [Comprehensive test report](tests/comprehensive_test_report.md)
- [DBpedia SPARQL endpoint](https://dbpedia.org/sparql)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Text and Markdown guidance with generated SQL, SPARQL, Pandas code, configuration snippets, and answer summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include selected sources, confidence values, generated queries, execution results, and review guidance.]

## Skill Version(s):

0.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
