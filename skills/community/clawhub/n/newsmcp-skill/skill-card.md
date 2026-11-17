## Description:

Real-time world news briefings with AI-clustered events, topic classification, and geographic filtering. No API key needed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pranciskus](https://clawhub.ai/user/pranciskus)

### License/Terms of Use:


## Use Case:

External users, developers, and agents use this skill to fetch and format current news briefings by importance, topic, geography, and event detail without API credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries contact newsmcp.io and may reveal requested news topics, regions, or event IDs to that service.

Mitigation: Avoid sending sensitive investigative interests or confidential context in query parameters; review the public API request before execution.

Risk: News summaries and importance signals are AI-generated and may omit context or reflect source coverage bias.

Mitigation: Include source links in briefings and verify important claims against the listed articles before relying on them.

## Reference(s):

- [newsMCP homepage](https://newsmcp.io)
- [newsMCP API base URL](https://newsmcp.io/v1)
- [ClawHub skill release page](https://clawhub.ai/pranciskus/skills/newsmcp-skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, API Calls, Guidance]

**Output Format:** [Markdown with inline bash code blocks and summarized news briefing text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill guides calls to a public news API and recommends including event summaries, source counts, source links, time windows, topics, and geography tags.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
