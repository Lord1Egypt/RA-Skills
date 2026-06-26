## Description: <br>
Polymarket API and data access guide for connecting to Polymarket APIs, finding markets, getting real-time data via WebSocket, accessing order books, placing orders via CLOB SDK, and understanding market mechanics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nwcalvin](https://clawhub.ai/user/nwcalvin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to build agents or applications that query Polymarket market data, monitor order books, use WebSocket updates, and understand CLOB order placement mechanics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes patterns for live Polymarket order placement and private-key based credential derivation. <br>
Mitigation: Use a dedicated low-balance wallet or secret manager, keep private keys out of prompts and logs, and require explicit confirmation before enabling order placement. <br>
Risk: Trading code can place financial orders if extended or run with valid credentials. <br>
Mitigation: Default to dry-run behavior, set order-size and price limits, and keep audit logs for any execution path that posts orders. <br>
Risk: Incorrect interpretation of market data can produce misleading trading decisions. <br>
Mitigation: Use the documented reliable order book events, verify market resolution states before acting on outcomes, and review Polymarket's official order documentation before trading. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nwcalvin/innotech-polymarket-api) <br>
- [API Reference](references/API_REFERENCE.md) <br>
- [WebSocket Guide](references/WEBSOCKET_GUIDE.md) <br>
- [Polymarket create order documentation](https://docs.polymarket.com/trading/orders/create) <br>
- [Polymarket order overview documentation](https://docs.polymarket.com/trading/orders/overview) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with Python examples and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include API endpoint descriptions, WebSocket subscription examples, order book parsing guidance, and optional trading-related code patterns.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence and artifact skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
