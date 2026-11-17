## Description:

Typed knowledge graph for structured agent memory and composable skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaising-openclaw1](https://clawhub.ai/user/kaising-openclaw1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to create, query, relate, and validate typed entities for persistent workspace memory, task planning, and cross-skill state sharing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill persists shared workspace memory and can retain sensitive or stale information.

Mitigation: Avoid storing secrets or tokens, review ontology entries before persistence, and keep credential records limited to references such as secret_ref.

Risk: Create, update, delete, relate, and schema-append operations can change the memory graph or schema.

Mitigation: Require explicit user confirmation before mutations and run validation after changes.

Risk: Validation is available but may not enforce every documented higher-level constraint before data is saved.

Mitigation: Treat validation output as a review aid, inspect proposed graph changes, and add project-specific checks for constraints that matter operationally.

## Reference(s):

- [Ontology Schema Reference](references/schema.md)
- [Query Reference](references/queries.md)
- [ClawHub skill page](https://clawhub.ai/kaising-openclaw1/skills/long-term-memory)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON, YAML, Python, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local workspace files under memory/ontology when the provided CLI is used.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
