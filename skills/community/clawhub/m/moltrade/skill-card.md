## Description: <br>
Operate the Moltrade trading bot (config, backtest, test-mode runs, Nostr signal broadcast, exchange adapters, strategy integration) in OpenClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ai-chen2050](https://clawhub.ai/user/ai-chen2050) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and trading operators use this skill to configure, backtest, and run Moltrade strategies, including test-mode and live trading workflows. It also supports exchange adapter setup, Nostr signal broadcast, and related Binance posting or API-call guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live trading, order cancellation, DEX swaps, and copy-trading actions can move real funds. <br>
Mitigation: Start with testnet or test mode, verify strategy settings and symbols, set risk limits, and require explicit human approval before any live action. <br>
Risk: The skill depends on sensitive API keys, wallet private keys, Nostr keys, and related trading credentials. <br>
Mitigation: Use environment variables or a trusted secret manager, keep withdrawal permissions disabled where possible, do not ask the agent to handle private keys directly, and redact secrets from output. <br>
Risk: Binance Square and Nostr workflows can publish public trading signals or posts. <br>
Mitigation: Show the exact content before publication, require user confirmation, and use platform limits and moderation errors to stop unsafe or unsupported posts. <br>
Risk: Server evidence does not provide resolved GitHub import provenance for this version. <br>
Mitigation: Inspect and pin the external Moltrade repository before running it, and treat the configured homepage as a reference link rather than proof of provenance. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ai-chen2050/moltrade) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/ai-chen2050) <br>
- [Configured homepage](https://github.com/hetu-project/moltrade.git) <br>
- [Moltrade website](https://www.moltrade.ai/) <br>
- [Binance authentication reference](binance/spot/references/authentication.md) <br>
- [Binance Square posting README](binance/square-post/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, JSON configuration examples, and operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include redacted command output, backtest metrics, generated configuration changes, and public post URLs.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
