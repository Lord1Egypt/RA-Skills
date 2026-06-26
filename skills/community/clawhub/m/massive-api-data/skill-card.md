## Description: <br>
Fetch real-time and historical market data from Massive, formerly Polygon.io, for OpenClaw across stocks, options, futures, indices, forex, and crypto. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[player-1101](https://clawhub.ai/user/player-1101) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw agents use this skill to retrieve market data for quotes, OHLCV bars, options chains, futures prices, crypto prices, real-time streaming, and historical datasets used in analysis, backtesting, and trading decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup script installs a package name that security evidence flags as questionable. <br>
Mitigation: Review or replace the setup dependency with the official Massive Python client package before installation. <br>
Risk: The skill requires a sensitive Massive API key and may use optional S3 credentials for Flat Files. <br>
Mitigation: Provide only the credentials needed for the chosen access method, store them in a secret manager or uncommitted .env file, and monitor API usage and billing. <br>
Risk: Market-data subscription limits, delayed data, rate limits, and WebSocket connection limits can affect downstream decisions. <br>
Mitigation: Confirm the Massive plan, check response status before using results, handle rate limits, and distinguish delayed data from real-time data in agent workflows. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/player-1101/massive-api-data) <br>
- [Publisher profile](https://clawhub.ai/user/player-1101) <br>
- [Massive documentation](https://massive.com/docs) <br>
- [Massive REST API quickstart](https://massive.com/docs/rest/quickstart) <br>
- [Massive WebSocket quickstart](https://massive.com/docs/websocket/quickstart) <br>
- [Massive Flat Files quickstart](https://massive.com/docs/flat-files/quickstart) <br>
- [Stocks reference](references/stocks.md) <br>
- [Options reference](references/options.md) <br>
- [Futures reference](references/futures.md) <br>
- [Crypto reference](references/crypto.md) <br>
- [WebSocket reference](references/websocket.md) <br>
- [Flat Files reference](references/flat-files.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, Python examples, configuration snippets, and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide REST API calls, WebSocket subscriptions, and Flat Files downloads; requires Massive API credentials for live use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
