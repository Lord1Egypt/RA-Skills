## Description:

Query and summarize the MarsEdge probability board for BTC, ETH, SOL, and XRP 5-minute up/down signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[akgod](https://clawhub.ai/user/akgod)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to fetch the live MarsEdge probability board and produce short, trading-style summaries of symbol strength, model probabilities, market bid/ask context, and stale-data caveats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The fetch script can be pointed at arbitrary base URLs.

Mitigation: Use the default MarsEdge endpoint and review any custom base URL before execution.

Risk: Trading-style probability summaries may be mistaken for financial advice.

Mitigation: Treat summaries as informational only and avoid presenting model-market gaps as certainty or recommendations.

Risk: Live board data can be stale or unavailable.

Mitigation: Check updatedAt, ts, ttl, and rem_secs before interpreting the board, and say plainly when data is stale or missing.

## Reference(s):

- [Edge Rules](references/edge-rules.md)
- [MarsEdge](https://marsedge.vip)
- [MarsEdge ProbBoard on ClawHub](https://clawhub.ai/akgod/skills/marsedge-probboard)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Concise Markdown bullets with numeric probability, bid/ask, edge, freshness, and caveat details.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include compact JSON from the fetch script; summaries are informational and should identify stale or missing live data.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
