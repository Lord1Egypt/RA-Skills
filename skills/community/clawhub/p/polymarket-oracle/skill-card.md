## Description:

Multi-strategy arbitrage and trading bot for scanning Polymarket prediction markets across major categories for parity arbitrage, logical arbitrage, tail-end trading, market making, and latency opportunities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[georges91560](https://clawhub.ai/user/georges91560)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to monitor Polymarket prediction markets, identify arbitrage or market-making opportunities, receive optional Telegram alerts, and place CLOB orders when API credentials are configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A wallet private key or Polymarket API credentials could be exposed through long-lived runtime configuration.

Mitigation: Generate API credentials on a trusted local machine, remove WALLET_PRIVATE_KEY from runtime configuration, and avoid storing secrets in systemd, shell startup files, project .env files, or /etc/polymarket-oracle/credentials.env.

Risk: The skill can interact with real-money Polymarket trading when API credentials are configured.

Mitigation: Review the code's trading behavior before use, test in simulation mode first, and use a low-value wallet for testing.

Risk: Credential-generation dependencies may add supply-chain risk.

Mitigation: Pin and verify dependencies used to generate credentials before running them with wallet access.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/georges91560/skills/polymarket-oracle)
- [Polymarket Oracle homepage](https://github.com/georges91560/polymarket-oracle)
- [Polymarket documentation](https://docs.polymarket.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown documentation, Python code, shell commands, and JSONL runtime logs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May make authenticated Polymarket API requests and optional Telegram notifications when configured.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
