## Description:

Polymarket prediction-market arbitrage tool that scans for pricing deviations and can automatically execute trades with per-call billing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bob-z-pro](https://clawhub.ai/user/bob-z-pro)

### License/Terms of Use:

MIT

## Use Case:

External users and developers can use this skill to scan Polymarket markets for apparent Yes/No price deviations and, when configured with wallet credentials, submit live Polygon trades.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live trading can submit recurring orders using configured wallet credentials.

Mitigation: Use a dedicated low-balance wallet, test only with small amounts, and avoid scan/start workflows unless live trading is intended.

Risk: The skill asks for wallet private-key and billing credentials.

Mitigation: Do not use a primary wallet private key; keep credentials scoped to the session and rotate any key that may have been exposed.

Risk: Security evidence reports no clear confirmations, limits, or reliable arbitrage safeguards.

Mitigation: Review the workflow before installation and add explicit confirmations, order-size limits, and stop conditions before relying on automated execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bob-z-pro/skills/polymarket-arbitrage-pro)
- [Polymarket Gamma API endpoint](https://gamma-api.polymarket.com)
- [Polymarket CLOB API endpoint](https://clob.polymarket.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Console text and Markdown guidance with command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May execute network calls and live trading actions when wallet and billing environment variables are configured.]

## Skill Version(s):

7.1.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
