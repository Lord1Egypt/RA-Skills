## Description: <br>
Mcdonald helps an agent query and claim McDonald's coupons, check campaign calendars, and look up nutrition information through the mcp.mcd.cn service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hi-yu](https://clawhub.ai/user/hi-yu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and OpenClaw agents use this skill to retrieve McDonald's coupon, campaign, time, and nutrition data, and to present coupon or nutrition results in readable tables or lists. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an MCD_TOKEN bearer credential to call an external MCP service. <br>
Mitigation: Store MCD_TOKEN as a private secret, verify the endpoint before sending it, and avoid exposing tokens in prompts, logs, or shared command output. <br>
Risk: The skill can claim coupons or otherwise change coupon state on a user's account. <br>
Mitigation: Ask for explicit user approval before executing coupon-claiming actions such as auto-bind-coupons. <br>
Risk: Coupon, campaign, and nutrition data can change over time or be rate limited by the service. <br>
Mitigation: Query fresh data before presenting time-sensitive offers and handle expired-token, unauthorized, and rate-limit errors clearly. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hi-yu/mcdonald) <br>
- [Publisher profile](https://clawhub.ai/user/hi-yu) <br>
- [McDonald's MCP service](https://mcp.mcd.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, configuration, guidance] <br>
**Output Format:** [Markdown and plain-text guidance with curl commands, JSON-RPC examples, and tables or lists for coupon and nutrition results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an MCD_TOKEN bearer credential and may use MCD_MCP_URL to target the MCP endpoint.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
