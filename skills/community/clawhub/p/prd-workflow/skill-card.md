## Description:

Complete PRD workflow with integrated review, flowcharting, export, optional Wiki knowledge enhancement, and AI-assisted prototype generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gotomanutd-dot](https://clawhub.ai/user/gotomanutd-dot)

### License/Terms of Use:

MIT-0

## Use Case:

Product managers, business analysts, and developers use this skill to turn unclear product ideas into structured PRDs through interview, requirement decomposition, review, flowchart generation, prototype/design support, quality checks, and Word export.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence flags hard-coded credentials, unsafe shell command construction, and automatic dependency installation as high-risk bundled behavior.

Mitigation: Review and remove hard-coded credentials, fix shell command construction, and pin or disable automatic postinstall dependency installation before deployment.

Risk: PRDs and local wiki content may contain sensitive business information and parts of the workflow can pass document excerpts to AI or external-compatible endpoints.

Mitigation: Treat PRDs and wiki content as sensitive, review endpoint configuration, and restrict or redact sensitive content before allowing AI-assisted checks or generation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/gotomanutd-dot/skills/prd-workflow)
- [OpenClaw Documentation](https://docs.openclaw.ai)
- [Chart.js CDN](https://cdn.jsdelivr.net/npm/chart.js)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown, JSON, generated files, shell commands, and implementation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create PRD documents, review reports, flowcharts, prototype files, design-system files, quality reports, and Word exports in the workspace.]

## Skill Version(s):

5.1.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
