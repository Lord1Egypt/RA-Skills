## Description:

Queries HugMap's read-only technology knowledge graph for people, companies, technologies, products, papers, patents, articles, events, and their relationships.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jones-so](https://clawhub.ai/user/jones-so)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and external users use this skill to retrieve HugMap technology graph data, build entity briefs, explore relationships, and summarize recent industry activity with HugMap links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries and entity identifiers are sent to the configured HugMap server.

Mitigation: Use the skill only for data appropriate to share with HugMap or the configured server, and set HUGMAP_BASE_URL only to a trusted endpoint.

Risk: Responses include HugMap links and attribution by default.

Mitigation: Ask for link-free output or use --no-links when plain data is required.

## Reference(s):

- [HugMap](https://www.hugmap.com)
- [ClawHub Skill Page](https://clawhub.ai/jones-so/skills/hugmap-tech-graph)
- [HugMap Open API Reference](reference.md)
- [HugMap Use Case Examples](examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [JSON query results with Markdown-ready HugMap links and concise text guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only HugMap API queries; optional HUGMAP_BASE_URL configuration; --no-links can suppress injected HugMap links.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
