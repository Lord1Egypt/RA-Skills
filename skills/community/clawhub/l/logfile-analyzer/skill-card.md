## Description:

Analyzes application logs into actionable error digests with format auto-detection, pattern grouping, severity classification, trend analysis, and remediation recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, site reliability engineers, and incident responders use this skill to analyze log files or log directories, group recurring failures, classify severity, identify trends, and produce remediation-oriented reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads arbitrary log files or directories provided by the user, which may expose sensitive data or cover broader system logs than intended.

Mitigation: Run it only on the specific log files or directories needed for the investigation and avoid broad system log directories unless necessary.

Risk: Crafted log content may be reflected unsafely in terminal or Markdown reports.

Mitigation: Treat generated reports as untrusted when logs may contain attacker-controlled content, and prefer JSON output for safer downstream processing.

## Reference(s):

- [Error Pattern Reference](artifact/references/error-patterns.md)
- [ClawHub Skill Page](https://clawhub.ai/charlie-morrison/skills/logfile-analyzer)

## Skill Output:

**Output Type(s):** [Analysis, Text, JSON, Markdown, Shell commands, Guidance]

**Output Format:** [Plain text, JSON, or Markdown reports with remediation guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CI-friendly exit codes indicate whether no errors, warn/error entries, or fatal entries were found.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
