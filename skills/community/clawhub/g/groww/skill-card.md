## Description: <br>
Trade stocks, retrieve Indian market data, and manage portfolio and orders on Groww. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pushp1997](https://clawhub.ai/user/pushp1997) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to help an agent retrieve NSE/BSE market data, view Groww holdings, and manage brokerage orders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent live brokerage trading power without enough built-in confirmation or safety boundaries. <br>
Mitigation: Require manual confirmation with symbol, side, quantity, order type, and estimated cost before every buy, sell, or cancellation. <br>
Risk: The skill depends on a Groww brokerage API key that can expose account data and trading actions. <br>
Mitigation: Store GROWW_API_KEY as a secret and install only when the agent is intended to access a live Groww brokerage account. <br>
Risk: The artifact references a groww-mcp server for account and order actions. <br>
Mitigation: Verify the groww-mcp server separately before enabling MCP calls for portfolio, order, or market-data operations. <br>


## Reference(s): <br>
- [ClawHub Groww skill page](https://clawhub.ai/pushp1997/groww) <br>
- [Groww API base URL](https://api.groww.in/v1/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and API call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GROWW_API_KEY for live Groww brokerage account access.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
