## Description:

Builds and maintains a knowledge graph for long-term memory with concept drift detection, temporal reasoning, structured knowledge storage, and time-based queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jpengcheng523-netizen](https://clawhub.ai/user/jpengcheng523-netizen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to store structured knowledge as concepts and relationships, detect changes in concept histories, and run temporal or relationship queries over in-memory data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Caller-provided data can remain in local process memory while the skill is in use.

Mitigation: Avoid storing secrets or regulated data unless the host agent has appropriate memory handling, access control, and retention policies.

Risk: Short-term memory eviction may remove the oldest-created entry rather than the least recently used entry.

Mitigation: Configure memory size and consolidation thresholds for the workload, and explicitly recall, consolidate, or forget entries when retention behavior matters.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jpengcheng523-netizen/skills/jpeng-knowledge-graph-memory)

## Skill Output:

**Output Type(s):** [Code, JSON, Guidance]

**Output Format:** [JavaScript objects and JSON-serializable graph, memory, drift, and temporal query results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local in-memory state; no network, credential, destructive, or persistence behavior identified in server security evidence.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
