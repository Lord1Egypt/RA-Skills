## Description:

Track A-share market anomalies, including limit-up streaks, unusual volume, and large capital flows, and drill into individual stocks using GroundAPI MCP tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qingkongzhiqian](https://clawhub.ai/user/qingkongzhiqian)

### License/Terms of Use:

MIT-0

## Use Case:

External users and market analysts use this skill to summarize A-share market anomaly signals, inspect limit-up activity, compare unusual volume and capital-flow indicators, and produce an informational anomaly report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Market anomaly reports may be mistaken for investment advice.

Mitigation: Present outputs as informational market data, preserve the non-advice caveat, and avoid recommendation language.

Risk: The skill sends market-analysis queries to the GroundAPI MCP endpoint.

Mitigation: Use it only when sharing those queries with GroundAPI is acceptable.

Risk: A real GroundAPI key could be exposed if copied into files or chat transcripts.

Mitigation: Configure the key through environment or secret management and do not commit real credentials.

Risk: Third-party market data calls can fail or return incomplete data.

Mitigation: Skip failed retrieval steps, clearly state missing data, and avoid filling gaps with assumptions.

## Reference(s):

- [GroundAPI homepage](https://groundapi.net)
- [GroundAPI MCP endpoint](https://mcp.groundapi.net/mcp)
- [ClawHub skill page](https://clawhub.ai/qingkongzhiqian/skills/groundapi-anomaly-tracker)

## Skill Output:

**Output Type(s):** [markdown, text, guidance, configuration]

**Output Format:** [Markdown report with tables, bullet summaries, and informational caveats]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output language follows the user; failed data retrieval steps should be skipped and disclosed.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
