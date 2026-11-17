## Description:

Application logging quality auditor that scans source files for logging anti-patterns, including production debug statements, log level mismatches, PII exposure risk, missing request or trace context, and noisy debug logging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phy041](https://clawhub.ai/user/phy041)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to audit application code for logging quality, security, and observability issues before release or CI enforcement. It reports findings with severity, file and line citations, and targeted remediation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional fix guidance can include broad shell commands that directly delete source-code lines.

Mitigation: Review generated commands before execution, run preview commands first, keep backups or version control available, and prefer reviewable patches or language-aware edits.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/phy041/skills/phy-log-smell-auditor)
- [Project homepage](https://canlah.ai)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown report with severity summaries, file and line citations, inline code examples, and optional shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Static source analysis; optional fix commands should be reviewed before execution.]

## Skill Version(s):

1.0.3 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
