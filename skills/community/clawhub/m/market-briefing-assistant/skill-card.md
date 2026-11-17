## Description:

AirnodeHub market skill for current briefings, prices, news, earnings, fundamentals, indicators, portfolio checks, and company snapshots via attested Airnode POSTs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[metobom](https://clawhub.ai/user/metobom)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to request compact, timestamped market briefings and company snapshots from documented AirnodeHub market-data providers. It is intended for informational market research with clear source attribution, approval before paid calls, and separation of facts, estimates, and inference.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can direct an agent to send requests to external AirnodeHub market-data providers.

Mitigation: Use only documented POST operations and report exact blockers when provider data is unavailable.

Risk: Some market-data calls may be paid, credentialed, subscription-based, or uncertain in cost.

Mitigation: State the planned calls and costs and obtain explicit approval before making those requests.

Risk: Market data may be delayed, revised, estimated, or computed from incomplete context.

Mitigation: Validate symbols, exchanges, intervals, units, timestamps, and data status, then separate facts from inference and estimates from actuals.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/metobom/skills/market-briefing-assistant)
- [AirnodeHub Benzinga provider documentation](https://airnode-benzinga.fly.dev/)
- [AirnodeHub Twelve Data provider documentation](https://airnode-twelvedata.fly.dev/)
- [AirnodeHub TickerLayer provider documentation](https://airnode-tickerlayer.fly.dev/)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown briefing with attributed market facts, concise analysis, and explicit blockers.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes timestamps, provider attribution, data-limit notes, and a non-advice market-data disclaimer.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
