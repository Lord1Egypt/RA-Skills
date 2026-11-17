## Description:

Guides an agent through simulated prediction-market trading using live market data, portfolio tracking, and shareable performance summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[robotlearning123](https://clawhub.ai/user/robotlearning123)

### License/Terms of Use:

MIT-0

## Use Case:

Agent users practice prediction-market strategies with simulated funds and live market prices, review portfolio performance, and optionally prepare public performance summaries or leaderboard submissions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent is instructed to initiate and manage paper trades without asking first.

Mitigation: Use only where autonomous simulated trading is acceptable; review positions and set clear trading limits.

Risk: Trading activity maintains persistent local state.

Mitigation: Review local data retention and access before installation.

Risk: Share cards and leaderboard submissions can make performance public and may use an existing GitHub login.

Mitigation: Review generated content and explicitly approve any public post or GitHub submission.

## Reference(s):

- [Integration instructions](https://github.com/agent-next/polymarket-paper-trader/blob/main/docs/integrations.md)
- [Project homepage (listed in skill metadata)](https://github.com/agent-next/polymarket-paper-trader)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown trading summaries, theses, and shareable performance cards]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Simulated positions and performance; optional leaderboard submission details.]

## Skill Version(s):

0.4.13 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
