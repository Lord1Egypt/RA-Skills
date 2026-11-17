## Description:

Analyze server logs for error patterns, IP frequency, time-based analysis, alert generation, anomaly detection, top error messages, and frequency aggregation across syslog, custom log files, or piped input.

This skill is ready for commercial/non-commercial use.

## Publisher:

[laolaoqi](https://clawhub.ai/user/laolaoqi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and site reliability engineers use this skill to analyze selected server logs for error patterns, IP frequency, time-based trends, and spike indicators. It helps summarize local log files or piped log streams and suggests operational follow-up areas.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Log contents may include sensitive production, customer, credential, host, or IP address data.

Mitigation: Analyze only logs you are authorized to inspect and redact sensitive values before sharing output.

Risk: Running the analyzer over system logs may require elevated access in some environments.

Mitigation: Prefer user-owned or copied log files and avoid sudo unless access is explicitly authorized.

Risk: Logs from untrusted sources may contain terminal control characters that affect displayed output.

Mitigation: Review or sanitize untrusted logs before analysis and treat terminal output as untrusted text.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/laolaoqi/skills/laolaoqi-log-analyzer)
- [Publisher Profile](https://clawhub.ai/user/laolaoqi)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Terminal text with counts, ranked tables, status messages, simple bar charts, and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally over a chosen file or stdin and prints analysis results to stdout/stderr.]

## Skill Version(s):

1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
