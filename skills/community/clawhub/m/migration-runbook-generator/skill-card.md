## Description:

Generates reviewable migration runbooks that organize scope, cutover windows, pre-checks, rollback plans, validation signals, and responsibilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, SREs, and migration owners use this skill to turn migration plans into structured, auditable runbooks for system migrations, data migrations, and platform cutovers. It is intended for documentation, review, and dry-run planning, not direct execution of database or infrastructure changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated runbooks may echo migration plans, rollback details, hostnames, or other operational data supplied as input.

Mitigation: Review and sanitize sensitive inputs before use, and treat generated reports as operational documents with the same handling requirements as the source material.

Risk: A migration runbook draft may be incomplete or misleading if the source plan omits dependencies, switch windows, rollback conditions, or acceptance criteria.

Mitigation: Use the skill's待确认项 output to collect missing details and require human review before any execution or system change.

Risk: Changing script configuration or scanning broad directories can expose unrelated local files in generated summaries.

Mitigation: Use the documented structured_brief flow with explicit input files or text, and avoid broad directory inputs unless the contents are intended for review.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/52yuanchangxing/skills/migration-runbook-generator)
- [README](README.md)
- [Output Template](resources/template.md)
- [Structured Specification](resources/spec.json)
- [Smoke Test](tests/smoke-test.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown runbook or JSON payload containing the generated report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are read-only drafts that may include待确认项 for missing migration details; the bundled script can write the generated report to a user-specified local output path.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
