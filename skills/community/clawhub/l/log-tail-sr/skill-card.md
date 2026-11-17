## Description:

Monitor log files in real-time. Filter noise, surface errors, summarize patterns, alert on anomalies. Makes logs readable.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theshadowrose](https://clawhub.ai/user/theshadowrose)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to monitor local log files, filter noisy entries, and summarize recent errors and warnings during debugging or operations work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may rely on advertised anomaly alerting, highlighting, or correlation behavior that is not fully evidenced by the scanner summary.

Mitigation: Verify required alerting, highlighting, and correlation behavior in the target environment or add that functionality before operational use.

Risk: Selected log files may contain secrets or sensitive operational data that will be processed locally by the skill.

Mitigation: Use non-sensitive logs where possible, redact secrets before monitoring, and limit file access to logs approved for local agent processing.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/theshadowrose/skills/log-tail-sr)
- [OpenClaw](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [Text, Analysis, Code]

**Output Format:** [JavaScript objects and text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processes selected local log files and keeps a bounded in-memory buffer of recent entries.]

## Skill Version(s):

1.0.0 (source: release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
