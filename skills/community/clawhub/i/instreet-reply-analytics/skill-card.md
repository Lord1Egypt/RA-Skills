## Description:

Analyzes InStreet auto-reply logs to generate reply statistics, time-of-day distribution, response-efficiency metrics, and optimization suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rf-ai-wh](https://clawhub.ai/user/rf-ai-wh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to monitor InStreet auto-reply performance from local logs, including reply success rate, time distribution, processing completion, and optimization opportunities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The analyzer reads a local /tmp/instreet_reply.log file that may contain sensitive operational or user-comment data.

Mitigation: Run it only on trusted systems, keep the log private, and prefer moving the log to a private application directory before routine use.

Risk: Scheduled reports can repeatedly expose report output if crontab delivery or output paths are too broad.

Mitigation: Enable scheduled reporting only when needed, restrict report file permissions, and review generated reports before sharing.

Risk: If the expected log file is missing, the script uses mock data that could be mistaken for live analytics.

Mitigation: Confirm the log path and warning output before using a report for operational decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rf-ai-wh/skills/instreet-reply-analytics)
- [Publisher profile](https://clawhub.ai/user/rf-ai-wh)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text console report with summary statistics and optimization suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads /tmp/instreet_reply.log by default and falls back to mock data if the log is missing.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
