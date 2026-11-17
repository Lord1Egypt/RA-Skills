## Description:

Use when the user wants the full Groundcrew growth loop on a site: survey, fix, verify, and report as one command, or one named phase of it.

This skill is ready for commercial/non-commercial use.

## Publisher:

[trustgrowth](https://clawhub.ai/user/trustgrowth)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, site owners, and SEO operators use this skill to run a gated SEO growth cycle that surveys a site, applies safe local fixes, verifies changes, and produces a forwardable report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to run `.groundcrew/groundcrew-doctor.py` from the active skills root.

Mitigation: Install and use it only where the Groundcrew installation is trusted and controlled, and review the validator before allowing it to influence conclusions.

Risk: Some referenced guidance files are missing from the packaged artifact.

Mitigation: Treat missing guidance as unavailable context and require human review before relying on affected workflow steps.

Risk: The workflow can propose irreversible or outward-facing SEO changes.

Mitigation: Keep those changes as proposals until the site owner explicitly reviews and approves them.

## Reference(s):

- [Connectors and categories](references/connectors.md)
- [Reporting contract](references/reporting.md)
- [WHY-NOT-SLOP](https://github.com/techwright-lab/groundcrew-seo/blob/main/WHY-NOT-SLOP.md)
- [ETHICS](https://github.com/techwright-lab/groundcrew-seo/blob/main/ETHICS.md)
- [Grow skill page](https://clawhub.ai/trustgrowth/skills/grow)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown reports with prioritized findings, gated action plans, evidence references, and optional code or shell command recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs distinguish measured, user-provided, estimated, missing, applied, and unverified results.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
