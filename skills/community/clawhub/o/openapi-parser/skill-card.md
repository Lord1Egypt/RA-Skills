## Description:

Parses complex OpenAPI 3.x specs and generates Drift test cases that cover schema variants, constraints, and documented error responses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kevinrvaz](https://clawhub.ai/user/kevinrvaz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and QA engineers use this skill to analyze OpenAPI endpoints and generate Drift operations, datasets, and gap notes for schema variant and negative response coverage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted OpenAPI specs may include remote $ref URLs that fetch unreviewed schema content.

Mitigation: Keep specs local when possible and require explicit review before allowing remote reference fetches.

Risk: Generated Drift hooks or operations could affect production or privileged APIs if run without review.

Mitigation: Inspect generated Drift hooks and operations, then test first in a non-production environment with least-privileged credentials.

Risk: Broad activation could apply the skill when the user does not intend OpenAPI-to-Drift test generation.

Mitigation: Confirm the task is OpenAPI-to-Drift test generation before relying on generated outputs.

## Reference(s):

- [Schema Patterns Reference](references/schema-patterns.md)
- [Drift Mapping Reference](references/drift-mapping.md)
- [Working with Real-World Spec Collections](references/example-repos.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Drift YAML code blocks, concise analysis, dataset YAML when needed, and gap notes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated Drift hooks and operations should be reviewed before running against production or privileged APIs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
