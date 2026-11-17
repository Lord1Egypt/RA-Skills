## Description:

Use when a recruiter wants to batch-evaluate resumes, run general resume quality checks, optionally match resumes to a JD and company background, and produce evidence-backed Markdown and CSV review reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[debtvc2022](https://clawhub.ai/user/debtvc2022)

### License/Terms of Use:

MIT-0

## Use Case:

Recruiters and hiring teams use this skill to batch review resumes, run resume-quality checks, optionally compare candidates against a job description and company context, and generate human-review materials. The reports are advisory and require recruiter review before any hiring workflow action.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Candidate resumes, optional job descriptions, and company background can be sent to the configured model provider.

Mitigation: Use only an approved HTTPS model endpoint, bind the configuration to the intended API key, and avoid processing resumes unless that provider is authorized for the data.

Risk: Generated scores and screening buckets may be mistaken for final hiring decisions.

Mitigation: Treat all reports as advisory recruiter-review material and require human review before any hiring, rejection, or screening action.

Risk: Untrusted replacement configuration files can change the model endpoint or credential environment variable.

Mitigation: Protect and review model and evaluation configuration files before running the skill.

## Reference(s):

- [Compliance Policy](references/compliance-policy.md)
- [Output Schema](references/output-schema.md)
- [Role Family Taxonomy](references/role-family-taxonomy.md)
- [Scoring Rubric](references/scoring-rubric.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown reports, CSV summary files, JSON model outputs, and command-line guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces one candidate report per successfully evaluated resume, one batch summary report, one CSV summary, and failure records for unreadable or invalid files.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
