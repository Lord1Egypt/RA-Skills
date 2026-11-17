## Description:

Creates rule-based reasoning systems for knowledge graphs that infer new relationships and facts from existing data using declarative logic rules, including derivation, constraint, aggregation, conditional rules, and cycle detection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fisa712](https://clawhub.ai/user/fisa712)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to design rule-based knowledge graph reasoning workflows that derive relationships, validate constraints, compute aggregations, and materialize inferred facts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled graph rule engine should not be treated as production-ready for fraud, compliance, recommendations, or other consequential decisions without additional controls.

Mitigation: Add real cycle detection, deduplication, resource limits, tests, and human review before using generated rules or engine outputs for enforcement actions.

## Reference(s):

- [Graph Rule Engine Builder Skill Page](https://clawhub.ai/fisa712/skills/graph-rule-engine-builder)
- [ClawHub Homepage](https://clawhub.com)
- [Graph Rule Engine Builder README](README.md)
- [Graph Rule Patterns](references/graph-rule-patterns.md)
- [Graph Rule Examples](examples/graph-rule-examples.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python code examples and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce inferred facts, constraint violations, materialized triples, aggregated metrics, and rule execution statistics for knowledge graph workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
