## Description:

Context-aware daily assistant — weather, packages, IP, tax calculator, calendar, fuel prices, traffic restrictions, and daily briefing. Powered by GroundAPI MCP tools (7 life + 2 info tools).

This skill is ready for commercial/non-commercial use.

## Publisher:

[qingkongzhiqian](https://clawhub.ai/user/qingkongzhiqian)

### License/Terms of Use:

MIT-0

## Use Case:

External users and assistant builders use this skill to answer everyday life queries through GroundAPI, including weather, package tracking, IP location, tax calculations, calendar information, fuel prices, traffic restrictions, trending topics, and daily briefings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Casual greetings or unspecified city requests can trigger approximate IP-based location lookup and multiple GroundAPI requests without explicit consent.

Mitigation: Configure the agent to ask for confirmation before running location, weather, traffic, trends, or news tools from a greeting or ambiguous location request.

Risk: GroundAPI receives requests for daily assistant features, including approximate city-level IP lookup.

Mitigation: Install only after confirming the deployment is comfortable sharing these request details with GroundAPI and has a valid GROUNDAPI_KEY configuration.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qingkongzhiqian/skills/groundapi-context-aware)
- [GroundAPI homepage](https://groundapi.net)
- [GroundAPI MCP endpoint](https://mcp.groundapi.net/mcp)
- [Publisher profile](https://clawhub.ai/user/qingkongzhiqian)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Configuration]

**Output Format:** [Markdown responses with tables and concise natural-language guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs follow the user's language and may include city-level location, weather, logistics, tax, calendar, fuel price, traffic, trending, or bulletin information.]

## Skill Version(s):

1.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
