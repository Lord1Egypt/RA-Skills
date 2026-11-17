## Description:

OpenTelemetry instrumentation coverage auditor that scans Node.js, Python, Go, and Java source code for missing or misconfigured telemetry and returns findings with actionable fix snippets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phy041](https://clawhub.ai/user/phy041)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to audit OpenTelemetry coverage in application source code before release or during CI review. It helps identify missing spans, weak trace context propagation, incomplete error reporting, and other observability gaps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads the source tree selected by the user and may print short matching source snippets to stdout.

Mitigation: Run it only on repositories or directories that are appropriate for local code review, and use a narrower target directory for very large or sensitive projects.

## Reference(s):

- [Canlah AI Homepage](https://canlah.ai)
- [ClawHub Skill Page](https://clawhub.ai/phy041/skills/phy-otel-audit)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown or plain text audit report with inline code snippets and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings may include file paths, line references, severity labels, and short matched source snippets.]

## Skill Version(s):

1.0.3 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
