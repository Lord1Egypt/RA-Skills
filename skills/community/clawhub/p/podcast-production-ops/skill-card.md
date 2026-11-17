## Description:

Organizes podcast production workflows from topic selection through publishing and drafts show notes, title options, editing points, publishing checklists, and reusable materials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

Content teams, podcast producers, and publishing operators use this skill to turn episode topics, guest summaries, and recording notes into a reviewable production package. It is intended for drafting and planning, not for inventing guest statements or publishing unauthorized segments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated podcast drafts may contain incomplete, misleading, or unverified production guidance if the input material is sparse.

Mitigation: Review the generated production package and resolve any listed confirmation items before editing, publishing, or sharing.

Risk: Inputs may include personal information, guest details, or unreleased episode material.

Mitigation: Use only project-appropriate local files, redact sensitive content when possible, and avoid sharing generated drafts until they have been reviewed.

Risk: The local script may write or overwrite the output path supplied by the user.

Mitigation: Use a dedicated output file or dry-run mode and inspect results before moving them into production workflows.

Risk: The bundled script contains inactive generic audit code that is not central to podcast drafting.

Mitigation: Document or remove the inactive audit code in a future release to reduce reviewer confusion.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/52yuanchangxing/skills/podcast-production-ops)
- [README](artifact/README.md)
- [Skill Definition](artifact/SKILL.md)
- [Specification](artifact/resources/spec.json)
- [Output Template](artifact/resources/template.md)
- [Smoke Test](artifact/tests/smoke-test.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or JSON, with optional local shell command usage.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated drafts should be reviewed before publishing or sharing.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
