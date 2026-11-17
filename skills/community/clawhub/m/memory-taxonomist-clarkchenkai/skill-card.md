## Description:

Memory Taxonomist turns raw notes into typed, retrievable memory by classifying facts, preferences, procedures, unresolved questions, and exceptions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clarkchenkai](https://clawhub.ai/user/clarkchenkai)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and developers use this skill to turn raw notes, transcripts, and memory cleanup inputs into classified knowledge items with recommended storage actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may unintentionally choose to persist secrets or sensitive personal data while acting on storage recommendations.

Mitigation: Review every recommended storage action and avoid saving secrets or sensitive personal data unless that persistence is explicitly intended.

Risk: Provisional, contradicted, or context-specific information may be stored as durable memory.

Mitigation: Use the skill's hold, update, deprecate, conflict, and exception checks before accepting a memory item as stable.

## Reference(s):

- [Memory Taxonomy](references/taxonomy.md)
- [Storage Rules](references/storage-rules.md)
- [Conflict Signals](references/conflict-signals.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with six fixed sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable code; includes recommended storage actions for classified memory items.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
