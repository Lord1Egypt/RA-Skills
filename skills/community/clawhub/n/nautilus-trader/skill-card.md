## Description: <br>
NautilusTrader algorithmic trading guidance for strategy development, backtesting, and live trading deployments to Hyperliquid. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ahuserious](https://clawhub.ai/user/ahuserious) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and trading engineers use this skill to build NautilusTrader strategies, run backtests with catalog data, and configure Hyperliquid live trading examples. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Runnable live trading examples can place real orders or change leverage on mainnet. <br>
Mitigation: Before execution, review is_testnet settings, trade sizes, symbols, margin mode, and leverage; test with non-production settings first. <br>
Risk: The skill uses private keys and vault addresses for Hyperliquid access. <br>
Mitigation: Store secrets only in local environment files or secret managers, keep .env files out of version control, and rotate any exposed key. <br>
Risk: The Hyperliquid patch has documented order-management limitations. <br>
Mitigation: Review the patch and known limitations before relying on it, especially for cancel handling, reconnect behavior, and unsupported order types. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ahuserious/nautilus-trader) <br>
- [Publisher profile](https://clawhub.ai/user/ahuserious) <br>
- [Nautilus Trader Hyperfix README](references/README.md) <br>
- [Hyperliquid integration guide](references/hyperliquid.md) <br>
- [Hyperliquid patch source](references/hyperliquid_patch.py) <br>
- [Live trading example](references/live_trading.py) <br>
- [Set leverage example](references/set_leverage.py) <br>
- [Backtesting reference](references/backtesting.md) <br>
- [Data reference](references/data.md) <br>
- [Strategy patterns](references/strategies.md) <br>
- [NautilusTrader getting started](references/getting_started.md) <br>
- [NautilusTrader API reference](references/api.md) <br>
- [NautilusTrader Hyperliquid adapter issue](https://github.com/nautechsystems/nautilus_trader/issues/3152) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with Python and bash code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include runnable trading examples that require review before execution.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata; artifact frontmatter says 2.0.0 and artifact changelog says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
