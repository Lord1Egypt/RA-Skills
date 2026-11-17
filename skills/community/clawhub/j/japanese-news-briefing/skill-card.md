## Description:

Summarizes Iran-Israel developments, U.S. and Japan economic news, and Tokyo/New York weather in Japanese four times daily.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harinezumi](https://clawhub.ai/user/harinezumi)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users use this skill to receive concise Japanese news and weather briefings on a daily schedule or by manual briefing command.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may perform web searches and weather lookups four times daily on an automated schedule.

Mitigation: Review HEARTBEAT.md before enabling the skill so the schedule, topics, and locations match the intended use.

Risk: News, market, and weather summaries depend on external live sources and may be incomplete, stale, or misleading.

Mitigation: Require source mentions in each briefing and verify important decisions against primary news, market, or weather sources.

Risk: The artifact states that severe weather alerts are not covered and that breaking-news checks may be skipped within 30 minutes.

Mitigation: Use official emergency weather channels and request a manual check for time-sensitive events.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/harinezumi/skills/japanese-news-briefing)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Japanese Markdown briefing with topic sections, bullet summaries, source mentions, weather lines, and a one-line overall summary.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scheduled four times daily with manual /briefing morning, noon, afternoon, and evening triggers; target length is 500 Japanese characters or fewer.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
