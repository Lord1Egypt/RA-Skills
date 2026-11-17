## Description:

知识本体 helps agents model typed knowledge graphs with entity relationships, constraint validation, schema evolution, and graph traversal planning for structured, verifiable memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to structure agent memory as a typed ontology, validate entity and relationship changes, plan graph operations, and preserve schema history during evolution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad file and command access.

Mitigation: Install and run it only in workspaces where broad read, write, and command execution are acceptable, and review proposed commands before execution.

Risk: The evidence reports inconsistent statements about API keys and network use.

Mitigation: Avoid providing real API keys unless the publisher clarifies the network behavior and credential requirements.

Risk: Ontology graph content may include sensitive operational knowledge or credential references.

Mitigation: Do not store raw secrets in the graph; use external secret references and keep graph files access-controlled.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/knowledge-ontology)
- [Publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with JSON examples and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe append-only JSONL graph operations, schema migration steps, validation results, and credential-reference patterns.]

## Skill Version(s):

1.0.4 (source: server release evidence; artifact frontmatter lists 2.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
