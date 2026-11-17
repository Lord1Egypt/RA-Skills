## Description:

Quick-scans raw PostgreSQL migration files for ten common risk patterns and reports findings without rewriting migrations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hehuiwudai63-bit](https://clawhub.ai/user/hehuiwudai63-bit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to check raw PostgreSQL migration files for common destructive, locking, or compatibility risks before deployment. It reports matching patterns and recommendations as a quick review aid.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saved reports can overwrite existing files and may contain sensitive SQL values.

Mitigation: Use a new report filename or keep the default terminal output, and protect saved reports from unintended access.

Risk: A clean scan can be mistaken for deployment approval.

Mitigation: Treat results as a limited pattern check and review the migration before deployment.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/hehuiwudai63-bit/skills/migration-risk-quick-scan)
- [Server-resolved source repository](https://github.com/hehuiwudai63-bit/migration-risk-quick-scan)
- [Publisher profile](https://clawhub.ai/user/hehuiwudai63-bit)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown]

**Output Format:** [JSON scan report and concise Markdown summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Per-file pattern findings with severity, location, explanation, and recommendation. Detection only; a clean result is limited pattern evidence, not deployment approval.]

## Skill Version(s):

0.1.0 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
