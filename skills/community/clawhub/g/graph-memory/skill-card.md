## Description:

Query the agent's knowledge graph for entities, relationships, and statistics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[space-cadet](https://clawhub.ai/user/space-cadet)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use Graph Memory to answer questions about prior session knowledge, inspect graph statistics, and explore relationships between remembered people, projects, files, tools, errors, and concepts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local memory search can reveal prior-session context, including names, files, projects, and errors.

Mitigation: Install only in workspaces where the agent is permitted to access that memory, and avoid use with shared or sensitive graph databases.

Risk: The packaged script auto-loads executable JavaScript from a workspace bridge path outside the release artifact.

Mitigation: Use only when you trust and control that local graph-memory code path, or require a release that packages or verifies the bridge before execution.

Risk: The release installs an unpinned native dependency.

Mitigation: Pin and review the better-sqlite3 dependency before deployment in controlled environments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/space-cadet/skills/graph-memory)
- [Publisher Profile](https://clawhub.ai/user/space-cadet)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown strings returned by graph_search, graph_stats, and graph_related.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads local graph memory; graph_search defaults to 20 results and graph_related traversal depth is capped at 5.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
