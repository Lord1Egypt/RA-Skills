## Description:

Audits OpenClaw scheduler token usage for cron jobs, scheduled tasks, and heartbeat sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yueeli](https://clawhub.ai/user/yueeli)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and workspace administrators use this skill to audit OpenClaw cron jobs, scheduled tasks, and heartbeat sessions for expensive token usage. It helps compare authoritative usage records against explicit thresholds and explain supported causes without treating transcripts as billing meters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Auditing scheduler usage may require listing sessions or reading relevant session transcripts, which can expose private conversation content.

Mitigation: Prefer cron usage totals first, ask for confirmation before transcript access, limit review to the specific job or recent turns needed, and avoid including raw transcript content in reports.

Risk: Heartbeat sessions without explicit usage fields can be overstated as exact token measurements.

Mitigation: Use bounded or inconclusive conclusions unless authoritative usage data is present, and always state the threshold used.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yueeli/skills/openclaw-scheduler-token-auditor)
- [Publisher profile](https://clawhub.ai/user/yueeli)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown audit report with threshold, target type, evidence class, token finding, verdict, and concise cause analysis.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports classify findings as Exact, Bounded, or Inconclusive and state the token threshold used.]

## Skill Version(s):

1.0.2 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
