## Description:

Device-level network log analysis using raw syslog data without SIEM platforms, covering forensic timeline construction, syslog pattern recognition, multi-device event correlation, anomaly detection, and NTP-aware timestamp normalization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vahagn-madatyan](https://clawhub.ai/user/vahagn-madatyan)

### License/Terms of Use:

MIT-0

## Use Case:

Network engineers, security analysts, and incident responders use this skill to investigate raw device syslog data, audit syslog collection health, correlate events across devices, detect anomalies, and produce a structured forensic report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Timestamp-conversion examples may pass log text through shell commands when used on attacker-controlled logs.

Mitigation: Use safer parsing tools or scripts that avoid shell interpolation of log text before applying examples to untrusted logs.

Risk: Intermediate timeline and baseline files may expose sensitive log data or collide on shared systems.

Mitigation: Use private temporary directories, restrict file permissions, and run analysis under an unprivileged read-only account.

Risk: Incomplete syslog collection, retention gaps, or unsynchronized clocks can make forensic conclusions unreliable.

Mitigation: Verify collector coverage, retention, and NTP status before correlation, and document evidence gaps in the final report.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/vahagn-madatyan/skills/network-log-analysis)
- [CLI Reference](references/cli-reference.md)
- [Syslog Patterns Reference](references/syslog-patterns.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, configuration examples, tables, and report templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces analyst-facing procedures and report structure; it does not execute log analysis directly.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
