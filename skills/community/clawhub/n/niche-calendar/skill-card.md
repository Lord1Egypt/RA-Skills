## Description:

Provides specialized calendars for WHL Saskatoon Blades schedules, npm and ClawHub release timelines, Saskatchewan events, and developer planning or publish schedules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skunnyo](https://clawhub.ai/user/skunnyo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and ClawHub users use this skill to find niche event, sports, release, and publishing timelines, then receive date-focused summaries, tables, links, and planning milestones.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may ask an agent to run ClawHub CLI commands with user-provided search terms, creating avoidable local command execution risk.

Mitigation: Limit CLI use to fixed read-only commands or argument-array invocation, and require explicit user confirmation before any publish-related action.

Risk: Calendar, event, sports, and release data can become stale or misleading when copied from search results.

Mitigation: Include source links where available and verify date-sensitive results against authoritative sources before acting on them.

## Reference(s):

- [Niche Calendar on ClawHub](https://clawhub.ai/skunnyo/skills/niche-calendar)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with tables, links, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include current or future dates, source links, release summaries, and planning milestones.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
