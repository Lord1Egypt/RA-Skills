## Description: <br>
Automate Polymarket bot operations including fetching market data, placing trades, and implementing strategies like arbitrage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deliverydriver](https://clawhub.ai/user/deliverydriver) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and trading automation builders use this skill to create or adapt Polymarket bots that fetch market data, authenticate with trading APIs, monitor prices, and prototype arbitrage or copy-trading strategies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles real trading credentials and private keys. <br>
Mitigation: Use a dedicated low-value wallet, avoid shared or logged environments, and store API keys, secrets, passphrases, and private keys in secure secret storage. <br>
Risk: Example bot flows can execute live automated trades without sufficient safeguards. <br>
Mitigation: Default examples to dry-run mode, require explicit confirmation before live trading, and set position and loss limits before connecting funded credentials. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/deliverydriver/polymarket-bot) <br>
- [API Guide](references/api_guide.md) <br>
- [Challenges and Mitigations](references/challenges.md) <br>
- [Prompts](references/prompts.md) <br>
- [Strategy Examples](references/strategy_examples.md) <br>
- [Polymarket Gamma API](https://gamma-api.polymarket.com) <br>
- [Polymarket CLOB API](https://clob.polymarket.com) <br>
- [Polymarket Data API](https://data-api.polymarket.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python code and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include API usage patterns and trading bot configuration guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
