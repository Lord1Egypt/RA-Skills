## Description: <br>
Track A-share market anomalies, including limit-up streaks, unusual volume, large capital flows, and stock-level drilldowns powered by GroundAPI MCP tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qingkongzhiqian](https://clawhub.ai/user/qingkongzhiqian) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill to request A-share anomaly reports, investigate limit-up streaks, volume spikes, capital-flow changes, and drill into selected stocks through GroundAPI MCP tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a GroundAPI API key for the MCP service. <br>
Mitigation: Use a revocable, limited API key where possible and rotate it if access is no longer needed. <br>
Risk: Market-analysis requests are sent to the GroundAPI MCP service. <br>
Mitigation: Install and use the skill only when GroundAPI is trusted for the relevant market-analysis requests. <br>
Risk: Generated market analysis could be mistaken for investment advice. <br>
Mitigation: Treat reports as informational and review them before acting on any market decision. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qingkongzhiqian/groundapi-anomaly-tracker) <br>
- [GroundAPI homepage](https://groundapi.net) <br>
- [GroundAPI MCP endpoint](https://mcp.groundapi.net/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown market-analysis report with optional JSON MCP configuration snippet] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GROUNDAPI_KEY and the GroundAPI MCP service; generated market analysis is informational and not investment advice.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata; changelog: v1.1.0 Update MCP endpoint to new format) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
