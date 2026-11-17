## Description:

Complete DEX architecture guide including project structure, provider hierarchy, network configuration, TradingView setup, and provider configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tarnadas](https://clawhub.ai/user/tarnadas)

### License/Terms of Use:


## Use Case:

Developers building an Orderly Network DEX use this skill to plan project structure, provider setup, network configuration, chart integration, and runtime configuration for a React and TypeScript application.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Incorrect broker ID, network selection, or wallet connector configuration could point a DEX at the wrong trading environment.

Mitigation: Review broker ID, mainnet versus testnet defaults, chain handling, and wallet connector behavior before production deployment.

Risk: Manually downloaded TradingView files or npm packages may introduce supply-chain or versioning risk.

Mitigation: Download TradingView assets from the official source, review package provenance, and scan dependencies before deployment.

Risk: Financial applications can be harmed by otherwise normal example configuration when copied directly into production.

Mitigation: Treat generated configuration as implementation guidance and validate it against production security, compliance, and operational requirements.

## Reference(s):

- [TradingView Advanced Charts](https://www.tradingview.com/HTML5-stock-forex-bitcoin-charting-library/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with TypeScript, JavaScript, CSS, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
