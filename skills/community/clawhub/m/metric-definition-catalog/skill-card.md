## Description:

Organizes scattered metric definitions into a reviewable catalog of definitions, formulas, ownership, exceptions, common misuses, and maintenance notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

Analytics, data, and governance users use this skill to turn metric lists, definition fragments, and calculation notes into a structured metric catalog for review and alignment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Inputs may include sensitive metric definitions or business context.

Mitigation: Keep inputs limited to the files and excerpts intended for review, and remove sensitive material before processing when needed.

Risk: The bundled script contains unused audit modes that could scan broader local content if the specification is modified.

Mitigation: Review configuration changes and run the script only against intended paths.

Risk: Conflicting metric definitions could be merged into a misleading single definition.

Mitigation: List conflicting definitions side by side and mark missing source, ownership, or formula details as items to confirm.

## Reference(s):

- [Metric Definition Catalog release page](https://clawhub.ai/52yuanchangxing/skills/metric-definition-catalog)
- [52yuanchangxing publisher profile](https://clawhub.ai/user/52yuanchangxing)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Structured Markdown or JSON with optional local command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Emphasizes reviewable drafts, explicit open questions, and next-step recommendations.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
