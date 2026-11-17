## Description:

Hyperliquid market and account data through the Hydromancer API: REST (POST /info) for positions, fills, funding, liquidations, oracle prices, candles, vaults, staking, builder-code fills and HIP-3 / HIP-4 markets; WebSocket streams for trades, fills, liquidations, BBO, L2 and L4 order books with session replay; and Reservoir, a requester-pays S3 archive of historical Hyperliquid data in Parquet. Use when building Hyperliquid trading apps, bots, dashboards, copy-trading, tax tools, backtests or research, or when the task mentions Hyperliquid, HyperCore, HIP-3, HIP-4, builder codes, whale tracking, order book data, liquidations, funding history, wallet trade history, or Hydromancer.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joshavenue](https://clawhub.ai/user/joshavenue)

### License/Terms of Use:

MIT

## Use Case:

Developers building Hyperliquid trading applications, dashboards, analytics, tax tools, and backtests can use this skill to retrieve account and market data through Hydromancer REST and WebSocket APIs or its historical Reservoir archive.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: REST and WebSocket access uses a Hydromancer API key, and WebSocket authentication places the key in the connection URL, where it may be captured in logs.

Mitigation: Keep WebSocket connections server-side, mask token values in logs, store keys in the environment, and rotate or revoke a key if its URL may have been logged.

Risk: Reservoir is requester-pays S3 data, so AWS bills the caller for requests and data transfer.

Mitigation: Narrow the requested date and path ranges and select only the columns needed.

Risk: The security analysis is marked partial, so some referenced paths could not be resolved and coverage is incomplete.

Mitigation: Review the skill and its dependencies before installation, especially where they access external APIs, credentials, or S3 data.

## Reference(s):

- [Hydromancer REST API documentation](https://docs.hydromancer.xyz/readme/rest-api)
- [Hydromancer WebSocket documentation](https://docs.hydromancer.xyz/readme/websocket)
- [Hydromancer Reservoir documentation](https://docs.hydromancer.xyz/reservoir)
- [Hydromancer rate limits](https://docs.hydromancer.xyz/readme/rest-api/rate-limits-and-user-limits)
- [Hydromancer API key setup](https://docs.hydromancer.xyz/readme/get-api-keys)
- [Hyperliquid API guide](https://hydromancer.xyz/blog/hyperliquid-api)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline Python, JSON, and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples can query account and market data or read historical Parquet data from Reservoir.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
