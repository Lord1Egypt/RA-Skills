## Description:

GoldRush Streaming API helps agents produce real-time blockchain streaming guidance for GraphQL WebSocket subscriptions, SDK usage, token discovery, wallet activity monitoring, DEX pair updates, OHLCV feeds, and trader PnL queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gane5h](https://clawhub.ai/user/gane5h)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to build or troubleshoot real-time blockchain data integrations for trading bots, live dashboards, alerting workflows, copy-trading, DEX monitoring, token search, and profitability analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys may be exposed if copied directly into code or logs.

Mitigation: Use a dedicated GoldRush API key stored in a secret manager or environment variable, and avoid hardcoding credentials in generated examples.

Risk: SDK dependency behavior can change across unpinned releases.

Mitigation: Pin @covalenthq/client-sdk versions with a package lockfile and review dependency updates before deployment.

Risk: Wallet activity monitoring can expose sensitive behavioral information about real people or organizations.

Mitigation: Limit monitoring to authorized use cases, minimize retained wallet data, and apply internal privacy review before production use.

Risk: Long-lived WebSocket subscriptions can continue streaming data after the intended task is complete.

Mitigation: Call unsubscribe handlers and disconnect clients when streams are no longer needed.

## Reference(s):

- [GoldRush Streaming API Overview](artifact/references/overview.md)
- [Streaming API Endpoints](artifact/references/endpoints.md)
- [Streaming API SDK Guide](artifact/references/sdk-guide.md)
- [GraphQL over WebSocket Protocol](https://github.com/enisdenjo/graphql-ws/blob/master/PROTOCOL.md)
- [GoldRush TypeScript Client SDK](https://www.npmjs.com/package/@covalenthq/client-sdk)
- [Redstone](https://redstone.finance/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code snippets, GraphQL examples, shell commands, and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API integration steps, WebSocket connection details, SDK usage patterns, endpoint parameters, response schemas, and troubleshooting guidance.]

## Skill Version(s):

3.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
