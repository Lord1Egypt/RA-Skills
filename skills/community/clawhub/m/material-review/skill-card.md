## Description:

Reviews data sharing catalog materials for field completeness, platform consistency, and traceable issue-list output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[github7265](https://clawhub.ai/user/github7265)

### License/Terms of Use:

MIT-0

## Use Case:

Employees or reviewers responsible for data-sharing catalog submissions use this skill to check material forms, identify missing or inconsistent fields, compare platform catalog status, and produce actionable issue lists for submitters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The audit workflow can persist submitted contact, database, and password-related material in local plaintext output files.

Mitigation: Use an access-controlled output directory, manage retention, and redact or replace live secrets with password-presence checks before processing operational submissions.

## Reference(s):

- [Field Completeness Checklist](references/field-completeness.md)
- [Special Field Rules](references/special-field-rules.md)
- [Platform Consistency Review](references/platform-consistency.md)
- [Issue List Template](references/issue-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Markdown guidance with optional JSON audit artifacts and Markdown audit reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [When the bundled audit script is used, it writes structured_data.json, issues.json, and audit_report.md to the selected output directory.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
