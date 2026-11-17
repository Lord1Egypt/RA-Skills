## Description:

Omni News aggregates public news, social trend, finance, technology, AI, and international feeds into concise news digests with source summaries and sentiment analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zain1299999-create](https://clawhub.ai/user/zain1299999-create)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to request daily news briefings, quick headlines, topic-focused reports, and public sentiment summaries across Chinese and international sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill fetches broad public-source news and trend data from many external services.

Mitigation: Review enabled sources before use and disable feeds that are not needed for the user's briefing.

Risk: The skill may create local news archives and retain high-heat events for longer periods.

Mitigation: Use the documented retention controls and clear local workspace archives when they are no longer needed.

Risk: Push channels, scheduled runs, X/Twitter cookies, Playwright deep fetching, and Docker self-hosting expand operational and data-flow exposure.

Mitigation: Leave those options disabled unless explicitly required, configured by the user, and reviewed in the deployment environment.

## Reference(s):

- [Omni News ClawHub skill page](https://clawhub.ai/zain1299999-create/skills/omni-news)
- [60s API documentation](https://docs.60s-api.viki.moe)
- [NewsMCP API](https://newsmcp.io/v1/news/)
- [The Hear country headlines API](https://www.thehear.org/api/country-view/us)
- [DailyHotApi public instance](https://api-hot.imsyy.top)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports with optional tables, links, shell command examples, configuration snippets, HTML, JSON, PDF, image, and RSS output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local report archives and sentiment or trend summaries when the user requests them.]

## Skill Version(s):

1.0.1 (source: server release evidence and artifact version history, released 2026-09-17)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
