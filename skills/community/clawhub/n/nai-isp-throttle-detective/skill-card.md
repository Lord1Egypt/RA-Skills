## Description:

Run speed tests to multiple endpoints, log results, detect ISP throttling patterns, and generate evidence reports for ISP complaints or plan decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[newageinvestments25-byte](https://clawhub.ai/user/newageinvestments25-byte)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and network troubleshooting staff use this skill to collect repeated connection measurements, identify peak-hour or CDN-related slowdowns, and produce reports for ISP support or plan decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled speed tests can continue every 30 minutes and consume significant bandwidth.

Mitigation: Enable launchd or cron scheduling only on networks where repeated testing is acceptable, monitor bandwidth use, and remove the schedule when testing is complete.

Risk: Active tests contact Cloudflare, npm/Fastly, GitHub/Fastly, and optionally CloudFront endpoints.

Mitigation: Review and customize endpoints before running tests, especially on capped, mobile, enterprise, or sensitive networks.

Risk: Logs and reports can include timestamps, endpoint URLs, speed measurements, and connection-performance history.

Mitigation: Review generated logs and reports before sharing them with ISP support or other third parties.

## Reference(s):

- [ISP Throttle Detective Setup Guide](references/setup-guide.md)
- [ClawHub Skill Page](https://clawhub.ai/newageinvestments25-byte/skills/nai-isp-throttle-detective)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash commands, JSON analysis, JSONL logs, and Markdown evidence reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes logs and generated reports under ~/.isp-throttle-detective by default.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
