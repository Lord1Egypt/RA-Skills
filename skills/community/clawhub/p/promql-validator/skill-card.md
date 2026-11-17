## Description:

Validate, lint, audit, or fix PromQL queries and alerting rules; detects anti-patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq280948982](https://clawhub.ai/user/qq280948982)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and site reliability engineers use this skill to validate PromQL expressions, review alerting rules, explain query behavior, and identify performance or correctness issues before using queries in dashboards, alerts, or troubleshooting workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Pasting an untrusted PromQL query into the documented shell command form could allow local command execution.

Mitigation: Invoke validator scripts through a structured process call that passes the query as one argument, or pass the query through stdin; do not interpolate untrusted query text into a shell command.

Risk: Metric-type and semantic checks are heuristic and do not know the target Prometheus deployment's actual metrics or labels.

Mitigation: Confirm inferred metric types and test important queries against the intended Prometheus server before using them for production alerting or dashboards.

## Reference(s):

- [PromQL Validator Skill Page](https://clawhub.ai/qq280948982/skills/promql-validator)
- [PromQL Official Documentation](https://prometheus.io/docs/prometheus/latest/querying/basics/)
- [Prometheus Best Practices](https://prometheus.io/docs/practices/)
- [Best Practices for Naming Metrics](https://prometheus.io/docs/practices/naming/)
- [PromQL Cheat Sheet](https://promlabs.com/promql-cheat-sheet/)
- [Common Query Patterns in PromQL](https://www.robustperception.io/common-query-patterns-in-promql/)
- [Best Practices Documentation](docs/best_practices.md)
- [Anti-Patterns Documentation](docs/anti_patterns.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown with JSON validation results, PromQL code snippets, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include syntax findings, semantic warnings, optimization suggestions, output label descriptions, corrected PromQL examples, and citation line references.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
