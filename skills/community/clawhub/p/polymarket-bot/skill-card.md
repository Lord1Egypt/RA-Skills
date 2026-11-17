## Description:

Automate Polymarket bot operations including fetching market data, placing trades, and implementing strategies like arbitrage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deliverydriver](https://clawhub.ai/user/deliverydriver)

### License/Terms of Use:


## Use Case:

Developers and prediction-market operators use this skill to scaffold and operate Python workflows for Polymarket market discovery, credential setup, arbitrage logic, copy-trading examples, and bot integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can handle live trading credentials unsafely, including deriving API credentials and printing derived credential data in the authentication example.

Mitigation: Use disposable or least-privilege credentials, avoid pasting private keys into prompts, keep secrets in environment variables or a secret manager, and remove credential printing before use.

Risk: The integrated bot example can enable live automated trading without clear user approval.

Mitigation: Default all workflows to dry-run mode, require explicit live-trading confirmation, and keep live funds out until the code has been reviewed and tested.

Risk: Automated arbitrage and copy-trading behavior can create unexpected exposure, fees, slippage, or rate-limit issues.

Mitigation: Add strict position, market, amount, and rate limits; include fee and slippage thresholds; and monitor API failures with backoff and alerts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/deliverydriver/skills/polymarket-bot)
- [API Guide](artifact/references/api_guide.md)
- [Challenges and Mitigations](artifact/references/challenges.md)
- [Strategy Examples](artifact/references/strategy_examples.md)
- [Prompts](artifact/references/prompts.md)
- [Polymarket Gamma API](https://gamma-api.polymarket.com)
- [Polymarket CLOB API](https://clob.polymarket.com)
- [Polymarket Data API](https://data-api.polymarket.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python code and shell-command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide authenticated API calls and live trading workflows; review generated code and configuration before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
