## Description:

Access Massive(Polygon) stock, crypto, forex, options, indices, futures, market data, and news APIs via CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bruce-shi](https://clawhub.ai/user/bruce-shi)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to look up Massive(Polygon) CLI commands for market data, reference data, technical indicators, and news across asset classes. It helps produce command guidance for calls that require MASSIVE_API_KEY.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running an unpinned npm CLI with an API key can introduce supply-chain and credential exposure risk.

Mitigation: Use a pinned and reviewed version of the massive npm package where possible, provide only the needed MASSIVE_API_KEY, and run the CLI in an environment without unrelated secrets or broad filesystem access.

## Reference(s):

- [Massive](https://massive.com)
- [Stocks Commands Reference](references/stocks_commands.md)
- [Crypto Commands Reference](references/crypto_commands.md)
- [Forex Commands Reference](references/forex_commands.md)
- [Options Commands Reference](references/options_commands.md)
- [Indices Commands Reference](references/indices_commands.md)
- [Reference Data Commands Reference](references/reference_commands.md)
- [Market Data Commands Reference](references/market_commands.md)
- [News Commands Reference](references/news_commands.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with CLI examples; referenced CLI commands return JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires npx and MASSIVE_API_KEY.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
