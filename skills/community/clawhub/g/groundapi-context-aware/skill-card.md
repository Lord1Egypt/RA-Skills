## Description: <br>
Context-aware daily assistant — weather, packages, IP, tax calculator, calendar, fuel prices, traffic restrictions, and daily briefing. Powered by GroundAPI MCP tools (7 life + 2 info tools). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qingkongzhiqian](https://clawhub.ai/user/qingkongzhiqian) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to answer daily-life requests through GroundAPI-backed weather, package tracking, IP location, China tax, calendar, fuel price, traffic restriction, trending-topic, and news briefing lookups. It is suited for concise personal-assistant responses that combine current conditions with practical reminders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: GroundAPI-backed lookups can disclose user context such as IP-derived location, shipment numbers, recipient phone verification digits, or requested cities to the configured service. <br>
Mitigation: Install only when the user trusts GroundAPI for those requests, prefer explicit city input over IP-based location, and avoid shipment or phone verification details unless the user is comfortable sending them. <br>
Risk: The skill requires a GroundAPI credential for MCP access. <br>
Mitigation: Store GROUNDAPI_KEY as a configured secret or environment variable and do not paste the key into conversation content. <br>


## Reference(s): <br>
- [GroundAPI homepage](https://groundapi.net) <br>
- [GroundAPI MCP endpoint](https://mcp.groundapi.net/mcp) <br>
- [ClawHub skill page](https://clawhub.ai/qingkongzhiqian/groundapi-context-aware) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown responses with tables, concise summaries, and configuration snippets where setup is needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use GroundAPI MCP tools that require GROUNDAPI_KEY; responses follow the user's language.] <br>

## Skill Version(s): <br>
1.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
