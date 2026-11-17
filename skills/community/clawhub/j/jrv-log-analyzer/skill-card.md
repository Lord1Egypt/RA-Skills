## Description:

Analyze log files to detect error patterns, aggregate by severity, group repeated errors by fingerprint, and flag anomaly time windows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnnywang2001](https://clawhub.ai/user/johnnywang2001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect text-based application, server, syslog, nginx, and Apache logs for severity trends, recurring error fingerprints, and anomaly time windows. It supports debugging incidents, summarizing log output, and producing structured results for downstream reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Human-readable output can print raw log text, including attacker-controlled or sensitive content.

Mitigation: Treat logs as untrusted input; prefer JSON output or sanitize reports before sharing results.

Risk: Severity and since filters are imperfect and may not provide strict filtering.

Mitigation: Do not rely on --severity or --since as enforcement controls until those issues are fixed; verify important findings manually.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/johnnywang2001/skills/jrv-log-analyzer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with shell commands and optional JSON analyzer output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Human-readable reports may include raw log text; JSON output is available for piping or safer downstream handling.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
