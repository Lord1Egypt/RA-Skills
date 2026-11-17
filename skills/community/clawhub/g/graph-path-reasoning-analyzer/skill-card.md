## Description:

Analyze and discover paths between entities in knowledge graphs to explain relationships, identify indirect connections, and provide reasoning over traversal patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fisa712](https://clawhub.ai/user/fisa712)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and knowledge-graph practitioners use this skill to find, rank, filter, and explain paths between graph entities for relationship discovery, recommendations, investigations, supply-chain analysis, and other multi-hop reasoning workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: All-path enumeration can grow quickly on large or highly connected graphs.

Mitigation: Use explicit maximum path length and result limits, and prefer shortest-path or K-shortest-path modes for large or user-supplied graphs.

Risk: Generated path explanations may be treated as decision evidence even when graph data or relationship confidence is incomplete.

Mitigation: Validate explanations and source graph data before relying on results for investigations, recommendations, or operational decisions.

## Reference(s):

- [Graph Path Reasoning Patterns](references/graph-path-patterns.md)
- [Graph Path Reasoning Examples](examples/graph-path-examples.md)
- [ClawHub Skill Page](https://clawhub.ai/fisa712/skills/graph-path-reasoning-analyzer)
- [Publisher Profile](https://clawhub.ai/user/fisa712)
- [ClawHub Homepage](https://clawhub.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with Python code examples and structured path-analysis results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include graph traversal explanations, path rankings, statistics, and JSON-like result examples.]

## Skill Version(s):

1.0.0 (source: server release and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
