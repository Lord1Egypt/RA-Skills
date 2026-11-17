## Description:

Trade on Kalshi prediction markets: check portfolio, search markets, analyze orderbooks, place/cancel orders, and manage binary contract positions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ghsmc](https://clawhub.ai/user/ghsmc)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to research Kalshi prediction markets, inspect portfolio and orderbook data, and manage order workflows through a Node.js CLI. It can support real-money trading actions, so trade details should be reviewed before order placement or cancellation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI can place or cancel real-money Kalshi production orders without an enforced confirmation step or strict order limits.

Mitigation: Require manual review of ticker, side, contract count, price, total cost, and target environment before every order or cancellation.

Risk: The skill requires Kalshi API credentials and access to an RSA private key that can authorize trading actions.

Mitigation: Use demo credentials first where possible, store the private key outside the artifact, restrict file permissions, and revoke or rotate keys if exposure is suspected.

## Reference(s):

- [Kalshi API Documentation](https://kalshi.com/docs/api)
- [Setup Guide](references/setup-guide.md)
- [Trading Guide](references/trading-guide.md)
- [API Notes](references/api-notes.md)
- [ClawHub Skill Page](https://clawhub.ai/ghsmc/skills/kalshi-trading)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance, JSON data]

**Output Format:** [JSON CLI output with Markdown setup and trading guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js plus KALSHI_API_KEY_ID and KALSHI_PRIVATE_KEY_PATH; the artifact uses Kalshi production API endpoints by default.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
