## Description:

Fetch real-time and historical market data from Massive (formerly Polygon.io) for use in OpenClaw trading workflows across stocks, options, futures, indices, forex, and crypto.

This skill is ready for commercial/non-commercial use.

## Publisher:

[player-1101](https://clawhub.ai/user/player-1101)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and trading-system developers use this skill to retrieve market data for quotes, historical bars, real-time streams, backtesting datasets, and research across supported asset classes. The skill provides data access guidance and examples; it does not execute trades.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Massive API and S3 credentials could be exposed through logs, source control, or shared configuration files.

Mitigation: Store credentials in environment variables, a .env file excluded from source control, or a secret manager; rotate keys if exposure is suspected.

Risk: The setup script installs Python dependencies before using the connector.

Mitigation: Review or hash-lock the pinned dependencies before running setup in sensitive environments.

Risk: Market data availability, delay, rate limits, and WebSocket access depend on the Massive subscription plan.

Mitigation: Confirm plan limits before relying on real-time feeds, large backtests, or bulk flat-file downloads.

## Reference(s):

- [Stocks REST API Reference](references/stocks.md)
- [Options REST API Reference](references/options.md)
- [Futures REST API Reference](references/futures.md)
- [Crypto REST API Reference](references/crypto.md)
- [WebSocket API Reference](references/websocket.md)
- [Flat Files Reference](references/flat-files.md)
- [Massive API Documentation](https://massive.com/docs)
- [Massive REST API Quickstart](https://massive.com/docs/rest/quickstart)
- [Massive WebSocket Quickstart](https://massive.com/docs/websocket/quickstart)
- [Massive Flat Files Quickstart](https://massive.com/docs/flat-files/quickstart)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration, API calls]

**Output Format:** [Markdown with inline shell and Python examples; API responses are JSON objects from Massive.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Massive API key; optional S3 credentials are used only for Flat Files bulk downloads.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
