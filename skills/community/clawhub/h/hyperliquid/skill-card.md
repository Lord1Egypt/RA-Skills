## Description: <br>
Read-only Hyperliquid market data assistant (perps + spot optional) with support for natural-language requests and deterministic command parsing (terminal-style `hl ...` and slash-style `/hl ...`). Use to fetch quotes (mark/mid/oracle/funding/OI/volume), top movers, funding rankings, L2 order book, and candle snapshots via https://api.hyperliquid.xyz/info, and to format results for chat. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[k0nkupa](https://clawhub.ai/user/k0nkupa) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to query Hyperliquid market data and read-only account views from chat or terminal-style prompts. It helps inspect quotes, movers, funding, order books, candles, positions, balances, open orders, fills, and locally saved account aliases without trading or private-key handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet addresses, positions, balances, orders, and fills can appear in chat when account views are requested. <br>
Mitigation: Use the skill only in trusted chat contexts and avoid requesting account views on shared or logged sessions unless that disclosure is acceptable. <br>
Risk: Saved account aliases are stored locally in `~/.clawdbot/hyperliquid/config.json` and may reveal sensitive labels or addresses on shared machines. <br>
Mitigation: Review saved aliases regularly, avoid sensitive labels, and remove entries that should not persist locally. <br>
Risk: Setting `HYPERLIQUID_INFO_URL` can redirect API requests to a replacement endpoint. <br>
Mitigation: Leave `HYPERLIQUID_INFO_URL` unset unless the replacement endpoint is intentionally trusted. <br>


## Reference(s): <br>
- [Hyperliquid Skill on ClawHub](https://clawhub.ai/k0nkupa/hyperliquid) <br>
- [Hyperliquid Info API reference](references/hyperliquid-api.md) <br>
- [Hyperliquid Info endpoint documentation](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint) <br>
- [Hyperliquid Perpetuals API documentation](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint/perpetuals) <br>
- [Hyperliquid Spot API documentation](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint/spot) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Concise chat-friendly Markdown text with terminal-style command examples and formatted market or account data.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only outputs may include wallet addresses, balances, positions, orders, fills, funding data, order book levels, and candle snapshots when requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
