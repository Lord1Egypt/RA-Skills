## Description:

Trades Bitcoin price bin markets on Kalshi by comparing market-implied volatility to BTC historical 60% annualized volatility with a lognormal model.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to scan Kalshi Bitcoin price-bin markets, compare market prices with a historical-volatility lognormal model, and produce dry-run or live trading actions when explicitly configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live trading mode can spend real USDC and requires high-value trading credentials.

Mitigation: Use paper mode first, provide live credentials only in an isolated account or wallet with limited funds, and avoid --live until the skill has been reviewed.

Risk: Security evidence reports that exit logic can sell BTC positions the skill did not create.

Mitigation: Do not run live exit logic until it is fixed to sell only positions positively tagged as created by this skill.

Risk: The simmer-sdk dependency receives trading authority when credentials are supplied.

Mitigation: Pin and review simmer-sdk before using production credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diagnostikon/skills/kalshi-crypto-volatility-skew-trader)
- [Simmer Markets skills](https://simmer.markets/skills)
- [simmer-sdk repository](https://github.com/SpartanLabsXyz/simmer-sdk)
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, API calls]

**Output Format:** [Plain text CLI output and JSON automaton status.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Dry-run by default; live execution requires --live, SIMMER_API_KEY, and SOLANA_PRIVATE_KEY.]

## Skill Version(s):

1.0.5 (source: server release evidence; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
