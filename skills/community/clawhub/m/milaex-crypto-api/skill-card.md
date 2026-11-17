## Description:

Unified crypto market data API and scripts for exchanges, markets, tickers, OHLCV, and orderbooks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kmasterrr](https://clawhub.ai/user/kmasterrr)

### License/Terms of Use:


## Use Case:

Developers, analysts, traders, and support teams use this skill to query normalized cryptocurrency market data from the Milaex REST API, including exchange lists, markets, tickers, OHLCV candles, and orderbook snapshots.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An undocumented endpoint override can send the user's Milaex API key to a non-Milaex host.

Mitigation: Use only the official Milaex endpoint, avoid setting MILAEX_BASE_URL unless the destination is fully trusted, and avoid HTTP endpoints.

Risk: The skill requires a live API key for market data access.

Mitigation: Use a restricted or easily rotated Milaex API key and store it through the intended environment configuration.

Risk: Runtime dependency installation is not pinned by an artifact dependency file.

Mitigation: Install dependencies in a controlled virtual environment or add a pinned dependency file before deployment.

## Reference(s):

- [Milaex API Documentation](https://api.milaex.com/api-docs/index.html)
- [Milaex Website](https://milaex.com)
- [ClawHub Skill Page](https://clawhub.ai/kmasterrr/skills/milaex-crypto-api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scripts print JSON to stdout and may print rate-limit headers or error details to stderr.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
