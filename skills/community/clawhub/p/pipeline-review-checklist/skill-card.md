## Description:

Provides a weekly US pipeline review checklist and a limited local text checker for selected required fields and phrases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rapidworker1](https://clawhub.ai/user/rapidworker1)

### License/Terms of Use:

MIT-0

## Use Case:

US sales managers and RevOps leads use the checklist to structure weekly pipeline reviews. Treat the included checker as a limited text linter, not a complete deal or forecast review.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: The checker is a limited text linter and does not perform the full pipeline review described by the skill.

Mitigation: Manually verify deal dates, amounts, and next steps; use the report as a checklist rather than a complete review.

Risk: The script replaces lint-report.md in its output folder, and the optional publisher Windows application is a separate download.

Mitigation: Choose an output folder where replacing the report is acceptable. The Windows app is unnecessary for this workflow; assess it separately before running it.

## Reference(s):

- [Pipeline review rules](references/pipeline-review-rules.md)
- [ClawHub release](https://clawhub.ai/rapidworker1/skills/pipeline-review-checklist)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown lint report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [A local report identifies selected missing terms, overlong lines, and banned phrases; it does not perform a full sales pipeline review.]

## Skill Version(s):

1.0.7 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
