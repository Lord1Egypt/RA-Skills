## Description:

NautilusTrader algorithmic trading platform for strategy development and live trading, including guidance for backtesting and Hyperliquid deployment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ahuserious](https://clawhub.ai/user/ahuserious)

### License/Terms of Use:

MIT

## Use Case:

Developers and trading engineers use this skill to build NautilusTrader strategies, run backtests with catalog data, and prepare Hyperliquid live trading workflows. It can also help debug adapter issues and configure multi-timeframe indicator strategies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Example code can place real Hyperliquid mainnet orders or change leverage when wallet credentials are present.

Mitigation: Use testnet or paper trading first, require explicit mainnet opt-in, and add wallet, vault, order-size, and leverage confirmations before running live workflows.

Risk: Live trading behavior depends on environment-provided private keys and a monkey patch that bypasses the NautilusTrader Rust HTTP client.

Mitigation: Review the patch before use, keep private keys outside source control, pin dependencies, and run with minimal account permissions and limited funds.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ahuserious/skills/nautilus-trader)
- [NautilusTrader Hyperliquid Integration](https://nautilustrader.io/docs/latest/integrations/hyperliquid)
- [NautilusTrader API Reference](https://nautilustrader.io/docs/latest/api_reference/)
- [NautilusTrader Trading API](https://nautilustrader.io/docs/latest/api_reference/trading)
- [NautilusTrader Persistence API](https://nautilustrader.io/docs/latest/api_reference/persistence)
- [NautilusTrader Issue #3152](https://github.com/nautechsystems/nautilus_trader/issues/3152)
- [Artifact Reference: Hyperliquid Guide](references/hyperliquid.md)
- [Artifact Reference: Backtesting](references/backtesting.md)
- [Artifact Reference: Strategy Patterns](references/strategies.md)
- [Artifact Reference: Data Handling](references/data.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include trading strategy templates, environment configuration, dependency installation commands, and operational cautions.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
