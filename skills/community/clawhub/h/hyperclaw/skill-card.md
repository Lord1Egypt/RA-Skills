## Description: <br>
Trade on Hyperliquid with commands for account status, market data, funding rates, order books, trading, HIP-3 assets, market scanning, sentiment analysis, Grok web/X search, and prediction market data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zoan37](https://clawhub.ai/user/zoan37) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and agents use HyperClaw to inspect Hyperliquid markets, monitor account and position health, place or manage trades, and gather market intelligence from Hyperliquid, Grok-powered web/X research, and Polymarket data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent live financial authority over a Hyperliquid account. <br>
Mitigation: Start on testnet, use a separate low-balance API wallet, and manually verify asset, side, size, leverage, collateral, and cancellation effects before any mutating command. <br>
Risk: The skill requires wallet credentials for account and trading operations. <br>
Mitigation: Keep the .env file private and use API wallet credentials rather than a main wallet private key. <br>
Risk: The caching proxy may be reachable beyond the local machine if exposed on a network. <br>
Mitigation: Run the proxy only on a trusted local network and do not point HL_PROXY_URL at untrusted services. <br>


## Reference(s): <br>
- [HyperClaw on ClawHub](https://clawhub.ai/zoan37/hyperclaw) <br>
- [Hyperliquid](https://hyperliquid.xyz) <br>
- [Hyperliquid API](https://app.hyperliquid.xyz/API) <br>
- [AgentSkills](https://agentskills.io) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with shell command examples; CLI commands return terminal text and optional raw JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only market commands can run without credentials; account and trading commands require Hyperliquid wallet credentials.] <br>

## Skill Version(s): <br>
0.1.15 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
