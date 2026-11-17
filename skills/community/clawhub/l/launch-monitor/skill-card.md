## Description:

Launch Monitor helps agents verify launch instrumentation and monitor T-0 to T+30 performance signals across Hacker News, Product Hunt, app stores, news echo, and KPI snapshots while routing launch decisions to the appropriate follow-on skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaron-he-zhu](https://clawhub.ai/user/aaron-he-zhu)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing, growth, and product teams use this skill during an active launch window to verify tracking, poll launch-platform signals, compare D0/W1/M1 metrics to targets, and prepare alerts and handoff summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Launch analytics exports, platform tokens, or pasted metrics may contain sensitive operational data.

Mitigation: Provide only data and tokens appropriate for this workflow, prefer scoped or free-key access where possible, and avoid sharing unrelated analytics exports.

Risk: The skill may save launch snapshots or propose memory updates.

Mitigation: Review proposed writes and saved summaries before approval, especially when they include KPI targets or platform performance data.

Risk: Web and API results or pasted community threads may contain misleading or untrusted content.

Mitigation: Treat external content as telemetry only and review alerts before acting on launch decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aaron-he-zhu/skills/launch-monitor)
- [Project homepage](https://github.com/aaron-he-zhu/aaron-marketing-skills)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown reports and summaries with labeled metrics, alerts, and handoff notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Metrics should be labeled as Measured, User-provided, or Estimated; memory writes are proposed for review when used.]

## Skill Version(s):

19.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
