## Description: <br>
Real-time streaming Polymarket prediction trades on Polygon (matic) with live USD pricing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Divyn](https://clawhub.ai/user/Divyn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and trading analysts use this skill to stream live Polymarket prediction-market trades from Bitquery on Polygon, including market question, outcome, buyer, seller, USD amount, price, and transaction hash. It supports real-time order-flow monitoring, market-specific tracking, and formatted trade feeds for dashboards or terminal workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The required Bitquery API key is used in the WebSocket connection URL, which can expose the token if the URL is logged, captured, or shared. <br>
Mitigation: Store the key only in BITQUERY_API_KEY, avoid logging full WebSocket URLs, run in an isolated Python environment, and rotate the key if exposure is suspected. <br>
Risk: The live stream depends on Bitquery availability, valid credentials, and recent Polymarket activity on Polygon. <br>
Mitigation: Handle connection failures and quiet periods explicitly, validate the API key before streaming, and use timeout or retry controls for operational workflows. <br>


## Reference(s): <br>
- [Bitquery Polymarket API docs](https://docs.bitquery.io/docs/examples/polymarket-api/) <br>
- [GraphQL field reference](references/graphql-fields.md) <br>
- [ClawHub skill page](https://clawhub.ai/Divyn/polymarket-real-time-trades) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline Python and shell commands, plus formatted text output from the streaming script.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires BITQUERY_API_KEY and produces a live stream of successful Polymarket prediction trades from Polygon.] <br>

## Skill Version(s): <br>
1.0.5 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
