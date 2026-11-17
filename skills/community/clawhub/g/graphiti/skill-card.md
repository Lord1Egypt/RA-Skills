## Description:

Knowledge graph operations via Graphiti API. Search facts, add episodes, and extract entities/relationships.

This skill is ready for commercial/non-commercial use.

## Publisher:

[emasoudy](https://clawhub.ai/user/emasoudy)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill to search a Graphiti-backed knowledge graph for relevant facts and add new episodes or memories through the Graphiti REST API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documented shell command templates can execute unintended local commands when user-supplied query or memory text contains shell syntax.

Mitigation: Review generated commands before execution and replace hand-written JSON curl payloads with jq-generated JSON or another structured request method.

Risk: Search terms and added memories are sent to the configured Graphiti server, and added memories are persisted there.

Mitigation: Use only a trusted Graphiti server and avoid submitting secrets or sensitive data unless the deployment is approved for that data.

## Reference(s):

- [Graphiti project](https://github.com/getzep/graphiti)
- [Graphiti Skill on ClawHub](https://clawhub.ai/emasoudy/skills/graphiti)
- [env-check.sh](references/env-check.sh)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with shell command templates and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a reachable Graphiti service plus Neo4j and Qdrant backing services.]

## Skill Version(s):

1.0.1 (source: server release metadata and manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
