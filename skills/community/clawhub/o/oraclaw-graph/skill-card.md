## Description:

Network intelligence for AI agents. PageRank, community detection (Louvain), critical path, and bottleneck analysis for any graph of connected things.

This skill is ready for commercial/non-commercial use.

## Publisher:

[whatsonyourmind](https://clawhub.ai/user/whatsonyourmind)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and AI agents use this skill to analyze graph-shaped data such as task dependencies, org charts, knowledge graphs, and connected decision data. It helps identify influential nodes, communities, critical paths, and bottlenecks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Graph data may contain sensitive private relationships or business information when sent to an external analysis service.

Mitigation: Review OraClaw's data handling terms before use and avoid submitting sensitive private graph data unless those terms meet the deployment requirements.

Risk: Use may incur per-analysis charges after the disclosed free tier.

Mitigation: Configure ORACLAW_API_KEY only for approved deployments and monitor usage against the published pricing model.

## Reference(s):

- [OraClaw Graph Homepage](https://oraclaw.dev/graph)
- [ClawHub Skill Page](https://clawhub.ai/whatsonyourmind/skills/oraclaw-graph)

## Skill Output:

**Output Type(s):** [Text, Guidance, Configuration]

**Output Format:** [Markdown or structured text summarizing PageRank scores, community assignments, bottlenecks, and critical paths.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ORACLAW_API_KEY and uses a paid external graph-analysis service after the free tier.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
