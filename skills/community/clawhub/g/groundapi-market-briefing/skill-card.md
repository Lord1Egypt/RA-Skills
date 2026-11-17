## Description:

Generate A-share market briefings with indices, limit-up/down pools, sector rotation, IPO calendar, anomaly signals, gold and forex macro data, trending topics, and daily news digest using GroundAPI MCP tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qingkongzhiqian](https://clawhub.ai/user/qingkongzhiqian)

### License/Terms of Use:

MIT-0

## Use Case:

External users and market analysts use this skill to ask an agent for concise A-share market briefings, including market overview, sector movement, hot stocks, macro references, trending topics, and finance news. It is intended for informational briefing workflows and should not be treated as investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Market and news lookup requests are sent to GroundAPI using a configured API key.

Mitigation: Install only when the operator accepts that service dependency and is comfortable configuring GROUNDAPI_KEY for the agent environment.

Risk: Financial briefing content can be mistaken for investment advice or may be incomplete if a lookup fails.

Mitigation: Present the output as informational, skip failed data sources with a clear note, and retain the skill's instruction not to fabricate missing data.

Risk: Broad finance-related prompts may trigger the skill when a user only wants a narrow answer.

Mitigation: Use clear trigger wording and let the agent tailor the briefing scope to the user's request.

## Reference(s):

- [GroundAPI homepage](https://groundapi.net)
- [GroundAPI MCP endpoint](https://mcp.groundapi.net/mcp)
- [ClawHub skill page](https://clawhub.ai/qingkongzhiqian/skills/groundapi-market-briefing)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown market briefing with tables, bullet lists, and concise explanatory text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a configured GroundAPI key for live market, news, calendar, gold price, and forex lookups; output language follows the user.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
