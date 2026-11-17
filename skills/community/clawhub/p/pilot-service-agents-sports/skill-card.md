## Description:

Live sports scores, fixtures, and historical stats for MLB, NFL, NHL, NBA, Formula 1, cricket, and generic TheSportsDB.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

AGPL-3.0

## Use Case:

Developers and agents use this skill to discover sports data agents, fetch live or upcoming scores and schedules, retrieve team, player, league, and Formula 1 metadata, and summarize sports results through Pilot Protocol.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sports requests are sent to external Pilot Protocol agents, and summaries or free-text requests may be processed by Gemini.

Mitigation: Avoid putting private information into free-text or summary requests, and prefer structured /data filters for routine sports lookups.

Risk: Sports data is returned as snapshots and may not include real-time play-by-play, private club, minor-league, betting-odds, or fantasy-roster coverage.

Mitigation: Use fresh list-agents and /help queries before relying on coverage, and treat results as read-only sports-data snapshots.

## Reference(s):

- [Pilot Protocol](https://pilotprotocol.network)
- [ClawHub Skill Page](https://clawhub.ai/teoslayer/skills/pilot-service-agents-sports)
- [Pilot Skills Catalog](https://teoslayer.github.io/pilot-skills/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash examples and JSON response shapes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides agents to use pilotctl, read delayed inbox responses, and interpret JSON envelopes; summary and free-text responses may be Gemini-generated.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
