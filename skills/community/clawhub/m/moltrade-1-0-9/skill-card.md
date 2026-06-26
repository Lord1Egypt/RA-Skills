## Description: <br>
Operate the Moltrade trading bot for configuration, backtesting, test-mode runs, Nostr signal broadcasting, exchange adapters, and strategy integration in OpenClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhouhuihui008](https://clawhub.ai/user/zhouhuihui008) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and trading operators use this skill to configure Moltrade, run backtests and test-mode trading, integrate exchange adapters and strategies, and prepare live or copy-trading workflows with explicit human approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live trading, copy-trading runs, cancel-all operations, and decentralized swaps can move real funds. <br>
Mitigation: Use backtests and test mode first, keep withdrawal permissions disabled, confirm symbols, limits, and keys, and require explicit human approval before any live execution. <br>
Risk: The skill discusses API keys, wallet private keys, Nostr keys, and exchange credentials. <br>
Mitigation: Use least-privilege keys from environment variables or a secret store, never print or commit secrets, and have users enter private keys outside agent-managed scripts. <br>
Risk: Binance Square posting and Nostr broadcasting can publish public or subscriber-visible content. <br>
Mitigation: Preview the exact content, verify credentials and recipient scope, and require explicit confirmation before publishing or broadcasting. <br>
Risk: External dependencies and the referenced Moltrade repository are not covered by server-resolved provenance for this release. <br>
Mitigation: Review the external repository and dependency set before installation or operational use. <br>


## Reference(s): <br>
- [Moltrade ClawHub listing](https://clawhub.ai/zhouhuihui008/moltrade-1-0-9) <br>
- [Moltrade homepage](https://github.com/hetu-project/moltrade.git) <br>
- [Moltrade website](https://www.moltrade.ai/) <br>
- [Binance authentication reference](binance/spot/references/authentication.md) <br>
- [Binance testnet](https://testnet.binance.vision) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown with inline shell commands, JSON configuration snippets, and operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include redacted configuration guidance, command examples, API call guidance, and risk checks before live trading or public posting.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; ClawHub display/artifact label: Moltrade 1.0.9) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
