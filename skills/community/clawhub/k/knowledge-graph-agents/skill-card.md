## Description:

Adds a knowledge graph layer to an AI agent for relationship reasoning and multi-hop recall when flat search cannot answer relationship-based queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vnesin-sarai](https://clawhub.ai/user/vnesin-sarai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to design graph-backed agent memory and retrieval for questions about people, systems, projects, organizations, and other connected entities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Knowledge graphs built from emails, names, team data, or business documents can expose personal or sensitive relationship data.

Mitigation: Process only data the deployer is allowed to use, and apply retention limits, access controls, redaction, and opt-out choices where needed.

Risk: Co-occurrence graph construction can create noisy or excessive edges that reduce retrieval quality and increase maintenance burden.

Mitigation: Limit edges to named entity types, enforce edge-weight thresholds, and periodically prune orphan nodes and weak edges.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Configuration]

**Output Format:** [Markdown guidance with Python, SQL, and Cypher code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes architecture guidance, extraction patterns, graph storage examples, traversal queries, integration steps, and pitfalls.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
