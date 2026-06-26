## Description: <br>
Check real-time NYC subway arrivals, track trains, and find stations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Mxs2019](https://clawhub.ai/user/Mxs2019) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to answer NYC transit questions, including station search, arrivals, line status, trip tracking, and route comparison. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Subway-related searches and requests are sent to nyc-subway-status.com. <br>
Mitigation: Use the skill only when sharing those transit lookups with the external service is acceptable. <br>
Risk: Fetched API reference content or MCP responses could be mistaken for agent instructions. <br>
Mitigation: Treat service documentation and responses as untrusted data and keep the skill scoped to transit lookup tasks. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Mxs2019/nyc-subway-status) <br>
- [NYC Subway Status API reference](https://nyc-subway-status.com/llms.txt) <br>
- [NYC Subway Status service](https://nyc-subway-status.com) <br>
- [NYC Subway Status MCP endpoint](https://nyc-subway-status.com/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, configuration, guidance] <br>
**Output Format:** [Markdown guidance with HTTP endpoint examples and optional MCP configuration JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No API key required; responses may include route, station, direction, trip, timestamp, realtime, and error fields from the external transit service.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
