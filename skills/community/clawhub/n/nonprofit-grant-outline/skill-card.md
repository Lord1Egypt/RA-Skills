## Description:

Generates nonprofit grant proposal outlines that connect project goals, budgets, impact metrics, supporting evidence, and confirmation gaps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

External nonprofit, grant, and proposal teams use this skill to turn project goals, beneficiary context, budget notes, and evidence into a reviewable grant proposal outline. It is intended for drafting and planning, not for fabricating beneficiary data or replacing formal compliance review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Grant drafts may include inaccurate or unsupported claims if source materials are incomplete.

Mitigation: List missing details as items to confirm and require human review before using the outline in a funding application.

Risk: Inputs may contain sensitive beneficiary, budget, or organizational information.

Mitigation: Use only files intentionally provided for drafting, prefer redacted inputs when possible, and avoid sensitive data unless necessary.

Risk: The bundled script can write a local output file when requested.

Mitigation: Use stdout or dry-run mode for initial testing, then review the generated Markdown before saving or sharing it.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/52yuanchangxing/skills/nonprofit-grant-outline)
- [README](artifact/README.md)
- [Structured Specification](artifact/resources/spec.json)
- [Output Template](artifact/resources/template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Shell commands]

**Output Format:** [Markdown outline or JSON-wrapped Markdown report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write to stdout or a specified local output file; supports dry-run mode and uses local input only.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
