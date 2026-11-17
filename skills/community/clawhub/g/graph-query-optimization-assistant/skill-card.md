## Description:

Analyze graph queries and suggest optimizations to improve performance, reduce execution time, and ensure efficient traversal in graph databases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fisa712](https://clawhub.ai/user/fisa712)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to analyze Cypher and SPARQL queries, identify bottlenecks, and receive query rewrites, index recommendations, cost estimates, and benchmarking guidance for graph databases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Suggested CREATE INDEX, CREATE CONSTRAINT, PROFILE, or benchmarking steps can affect graph database schema, performance, or workload when applied to real systems.

Mitigation: Review and test recommendations before applying them, especially in production environments; the skill evidence indicates these actions are advisory and user-directed.

Risk: Optimization advice may be based on estimated costs and example assumptions rather than the user's actual graph data distribution.

Mitigation: Validate recommendations with EXPLAIN, PROFILE, or representative benchmarks against the target database before rollout.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/fisa712/skills/graph-query-optimization-assistant)
- [ClawHub Homepage](https://clawhub.com)
- [Optimization Patterns](references/optimization-patterns.md)
- [Optimization Examples](examples/optimization-examples.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline query examples, Python code snippets, and shell-style database commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include optimized Cypher or SPARQL queries, index suggestions, cost estimates, traversal recommendations, cardinality analysis, and benchmark comparisons.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
