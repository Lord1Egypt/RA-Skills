## Description: <br>
Use this skill to help agents fetch cryptocurrency prices, stream real-time market data, list exchanges or markets, and retrieve historical OHLCV candlestick data through the Luzia API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hvasconcelos](https://clawhub.ai/user/hvasconcelos) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to integrate Luzia as a cryptocurrency market-data source for price lookups, exchange and market discovery, historical candles, streaming dashboards, trading bots, portfolio trackers, and price alerts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Luzia API keys could be exposed if copied into source code, logs, prompts, or shared configuration. <br>
Mitigation: Store the API key in environment variables or a secrets manager, avoid hardcoding it, and redact it from logs and shared outputs. <br>
Risk: WebSocket access and API usage are constrained by plan limits and rate limits. <br>
Mitigation: Check the active Luzia plan before using streaming features, monitor usage, and handle rate-limit or subscription-limit errors explicitly. <br>
Risk: Users may provide unrelated secrets such as exchange trading keys or wallet credentials. <br>
Mitigation: Request only the Luzia API key needed for market data and reject exchange trading keys, wallet secrets, and unrelated credentials. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/hvasconcelos/luzia-crypto-api) <br>
- [Luzia Homepage](https://luzia.dev) <br>
- [Luzia Documentation](https://luzia.dev/docs) <br>
- [Luzia API Documentation](https://api.luzia.dev/docs) <br>
- [Luzia WebSocket Documentation](https://luzia.dev/docs/websocket) <br>
- [Luzia TypeScript SDK](https://luzia.dev/docs/sdk) <br>
- [Luzia Python SDK](https://luzia.dev/docs/python-sdk) <br>
- [Luzia MCP Server](https://luzia.dev/docs/mcp-server) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration] <br>
**Output Format:** [Markdown with endpoint references, code blocks, JSON examples, and command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include REST and WebSocket request patterns, SDK usage examples, authentication guidance, rate-limit notes, and error-handling guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
