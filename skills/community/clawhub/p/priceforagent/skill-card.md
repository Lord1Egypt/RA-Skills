## Description: <br>
Get real-time prices for crypto, stocks, and commodities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edibez](https://clawhub.ai/user/edibez) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agents and developers use this skill to retrieve current market prices for crypto assets, stocks, and commodities through natural-language queries or direct lookup calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Natural-language market queries may include sensitive portfolio holdings, trading plans, account details, or other personal information sent to the price API. <br>
Mitigation: Keep the generated API key private and avoid including sensitive personal or financial details in queries. <br>
Risk: Market price lookups can be stale, unavailable, or unsuitable as the sole basis for trading decisions. <br>
Mitigation: Treat returned prices as informational market data and verify important decisions against authoritative financial sources. <br>


## Reference(s): <br>
- [Price for Agent on ClawHub](https://clawhub.ai/edibez/priceforagent) <br>
- [Price for Agent API](https://p4ai.bitharga.com) <br>
- [OpenAPI specification](https://p4ai.bitharga.com/v1/openapi.yaml) <br>
- [Function schema](https://p4ai.bitharga.com/v1/function-schema) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an API key; documented rate limit is 2 requests per second per API key.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
