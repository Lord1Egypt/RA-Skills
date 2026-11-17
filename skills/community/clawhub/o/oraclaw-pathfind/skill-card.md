## Description:

A* pathfinding and task sequencing for AI agents that find optimal paths through workflows, dependencies, and decision trees with K-shortest path alternatives and cost, time, and risk breakdowns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[whatsonyourmind](https://clawhub.ai/user/whatsonyourmind)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to route through task graphs, dependency networks, and decision trees when optimizing for cost, time, risk, or alternative execution paths.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires an OraClaw API key.

Mitigation: Use a revocable key, store it only in the intended environment variable, and rotate it if access is no longer needed.

Risk: Workflow graph data is sent to the external OraClaw service.

Mitigation: Minimize pathfinding inputs and avoid including unnecessary sensitive business details in nodes, edges, or labels.

Risk: Pathfinding results depend on caller-provided graph structure, non-negative edge costs, and risk values.

Mitigation: Validate graph inputs before use and review returned routes before relying on them for execution planning.

## Reference(s):

- [OraClaw Pathfind homepage](https://oraclaw.dev/pathfind)
- [ClawHub skill page](https://clawhub.ai/whatsonyourmind/skills/oraclaw-pathfind)
- [ClawHub publisher profile](https://clawhub.ai/user/whatsonyourmind)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with structured pathfinding results and cost, time, risk, and alternate-route summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ORACLAW_API_KEY and sends workflow graph inputs to the external OraClaw service.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
