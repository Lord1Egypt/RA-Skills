## Description:

Gets today's NBA schedule, live scores, final results, team records, and current season standings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[goog](https://clawhub.ai/user/goog)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to answer NBA schedule, live score, final result, and standings questions with current basketball data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes outbound requests to NBA and StatMuse public endpoints when live scores or standings are requested.

Mitigation: Use the skill only in environments where those public network requests are acceptable.

Risk: Live sports data can be delayed, temporarily unavailable, or affected by upstream page and endpoint changes.

Mitigation: Present results with source context and fall back to the linked NBA or StatMuse pages when fetching fails.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/goog/skills/nba)
- [NBA live scoreboard JSON](https://cdn.nba.com/static/json/liveData/scoreboard/todaysScoreboard_00.json)
- [NBA schedule](https://www.nba.com/schedule)
- [StatMuse NBA](https://www.statmuse.com/nba)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown summaries with optional inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include current game status, scores, records, standings, leaders, and source links.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
