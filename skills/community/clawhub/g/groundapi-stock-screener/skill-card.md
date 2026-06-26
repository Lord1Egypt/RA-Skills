## Description: <br>
Screens A-share stocks by PE, PB, market cap, dividend yield, industry, and concept, with preset filters, macro context, and GroundAPI-powered result deep dives. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qingkongzhiqian](https://clawhub.ai/user/qingkongzhiqian) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to convert stock-screening requests into GroundAPI queries, macro context checks, and concise stock-selection reports. It is intended for informational screening workflows, not investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: GroundAPI receives the user's API key and stock-screening queries. <br>
Mitigation: Use a dedicated, revocable GroundAPI key, monitor usage or billing, and rotate the key if exposure is suspected. <br>
Risk: Generated stock reports may be mistaken for investment advice. <br>
Mitigation: Treat reports as informational screening output and review conclusions independently before making financial decisions. <br>
Risk: Screening data may come from database snapshots rather than real-time market data. <br>
Mitigation: Verify current market conditions and prices before relying on a report for time-sensitive decisions. <br>


## Reference(s): <br>
- [GroundAPI](https://groundapi.net) <br>
- [GroundAPI MCP endpoint](https://mcp.groundapi.net/mcp) <br>
- [ClawHub skill page](https://clawhub.ai/qingkongzhiqian/groundapi-stock-screener) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, API calls, Configuration guidance] <br>
**Output Format:** [Markdown stock-screening report with tables and concise commentary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses GroundAPI MCP tools and requires a GROUNDAPI_KEY.] <br>

## Skill Version(s): <br>
1.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
