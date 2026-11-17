## Description:

Memory Schema helps agents manage Basic Memory Picoschema lifecycles by discovering unschemaed notes, inferring schemas, creating and editing schema definitions, validating notes, and detecting drift.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phernandez](https://clawhub.ai/user/phernandez)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and knowledge-management users use this skill to guide agents through creating, validating, and evolving Basic Memory schemas so structured notes stay consistent and queryable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Proposed schema edits can affect how Basic Memory notes are organized and validated.

Mitigation: Review schema changes before applying them, especially required fields, type changes, and edits to existing notes.

Risk: Strict validation can block or flag notes that do not yet match a schema.

Mitigation: Start with warn-mode validation and re-validate after schema evolution before using error mode.

## Reference(s):

- [Memory Schema on ClawHub](https://clawhub.ai/phernandez/skills/memory-schema)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown guidance with YAML and Python-style tool-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose schema definitions and note edits that should be reviewed before applying.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
