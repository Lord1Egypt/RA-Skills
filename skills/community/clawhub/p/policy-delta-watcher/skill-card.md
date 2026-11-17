## Description:

Compares old and new policies or procedures and drafts a structured impact report covering key changes, business impacts, process impacts, documentation updates, training suggestions, and open questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external reviewers, developers, and operations teams can use this skill to turn old and new policy material plus affected-team context into a reviewable policy-change impact brief. It is intended for drafting structured analysis, not for making final legal or compliance determinations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Drafted policy-delta reports may be mistaken for legal, compliance, or operational approval.

Mitigation: Review generated reports with responsible legal, compliance, or process owners before relying on them for decisions.

Risk: Policy inputs can contain sensitive business, personal, or regulated information.

Mitigation: Provide specific policy documents or excerpts, redact sensitive material where practical, and avoid broad folders or sensitive repositories.

Risk: Incomplete source material can lead to missed affected teams, edge cases, or required documentation updates.

Mitigation: Resolve the generated open questions and validate affected teams, process changes, and document updates before execution.

Risk: The local helper script writes an output file when an output path is supplied.

Mitigation: Use dry-run or stdout for review first, and confirm the output path before writing files.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/52yuanchangxing/skills/policy-delta-watcher)
- [SKILL.md](artifact/SKILL.md)
- [README.md](artifact/README.md)
- [Specification](artifact/resources/spec.json)
- [Output Template](artifact/resources/template.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Markdown report by default; optional JSON wrapper when the local script is run with --format json.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Structured report sections include main changes, business impact, process impact, documents to update, training suggestions, and open questions.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
