## Description:

Typed knowledge graph for structured agent memory and composable skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lovefromio](https://clawhub.ai/user/lovefromio)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to create, update, link, query, and validate workspace-local ontology entities for structured memory and cross-skill state sharing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill writes persistent workspace-local ontology data that other skills may later rely on.

Mitigation: Review memory/ontology contents before sharing or allowing other skills to depend on the stored graph.

Risk: Sensitive values could be stored in ontology memory if users place raw secrets in entity properties.

Mitigation: Do not store raw passwords, tokens, API keys, or other secrets; use secret references instead.

Risk: Validation and rollback protections may be overstated relative to implemented checks.

Mitigation: Treat validation as a manual review aid and inspect proposed ontology changes before relying on them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lovefromio/skills/lovefromio-ontology)
- [Ontology Schema Reference](artifact/references/schema.md)
- [Query Reference](artifact/references/queries.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON/YAML examples and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces or updates workspace-local ontology data under memory/ontology when its CLI operations are used.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
