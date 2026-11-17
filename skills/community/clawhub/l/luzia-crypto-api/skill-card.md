## Description:

Guides agents in using the Luzia REST and WebSocket APIs to fetch cryptocurrency prices, list exchanges and markets, retrieve historical OHLCV candlestick data, and build market-data integrations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hvasconcelos](https://clawhub.ai/user/hvasconcelos)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to integrate with Luzia as a third-party cryptocurrency market-data provider for spot price lookup, exchange and market discovery, OHLCV history, WebSocket streaming, trading bots, portfolio trackers, and price alerts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires calls to Luzia as a third-party cryptocurrency market-data provider and uses Luzia API credentials.

Mitigation: Install only when Luzia is the intended data source, keep API keys in secure secret storage, and avoid hardcoding or logging credentials.

Risk: Trading bots, portfolio trackers, or alerting tools built from the guidance could act on stale, rate-limited, or plan-restricted market data.

Mitigation: Respect documented rate limits and plan requirements, use maxAge or equivalent freshness checks, handle API and WebSocket errors explicitly, and review outputs before connecting them to automated trading actions.

Risk: Requests, symbols, logs, or generated code can expose unnecessary sensitive information when integrating with external services.

Mitigation: Send only required market-data parameters, minimize request and error logging, and avoid including unrelated sensitive information in prompts or generated integration code.

## Reference(s):

- [Luzia homepage](https://luzia.dev)
- [Luzia documentation](https://luzia.dev/docs)
- [Luzia Swagger UI](https://api.luzia.dev/docs)
- [Luzia WebSocket documentation](https://luzia.dev/docs/websocket)
- [Luzia TypeScript SDK documentation](https://luzia.dev/docs/sdk)
- [Luzia Python SDK documentation](https://luzia.dev/docs/python-sdk)
- [Luzia MCP Server documentation](https://luzia.dev/docs/mcp-server)
- [ClawHub skill page](https://clawhub.ai/hvasconcelos/skills/luzia-crypto-api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code examples and API request patterns]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces integration guidance for REST and WebSocket API usage, including authentication, rate-limit handling, symbol formatting, and error handling.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
