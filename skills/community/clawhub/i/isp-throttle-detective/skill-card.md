## Description:

Runs multi-endpoint download and upload speed tests, logs timestamped results, and produces analyses and Markdown evidence reports for ISP throttling patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[newageinvestments25-byte](https://clawhub.ai/user/newageinvestments25-byte)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to collect repeated internet speed measurements, compare peak and off-peak behavior, detect CDN or endpoint-specific slowdowns, and prepare evidence for ISP support conversations or plan decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled tests create recurring third-party network traffic and can consume bandwidth through repeated downloads and uploads.

Mitigation: Review the configured endpoints, byte limits, timeout settings, and cron or launchd schedule before enabling recurring runs, especially on metered, enterprise, or sensitive networks.

Risk: Timestamped local speed-test history may reveal usage patterns or network performance details.

Mitigation: Store logs only where appropriate, review generated reports before sharing them, and delete ~/.isp-throttle-detective when the history is no longer needed.

Risk: Throttling conclusions depend on sufficient samples across multiple hours or days and may be misleading with sparse data.

Mitigation: Collect enough measurements across peak and off-peak periods before relying on the generated analysis or report.

## Reference(s):

- [Setup Guide](references/setup-guide.md)
- [ClawHub Skill Page](https://clawhub.ai/newageinvestments25-byte/skills/isp-throttle-detective)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON test results, JSONL logs, human-readable analysis text, and Markdown reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local history under ~/.isp-throttle-detective and reports under ~/.isp-throttle-detective/reports.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
