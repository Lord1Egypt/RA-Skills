## Description:

Audits cryptocurrency addresses and stock tickers from a local portfolio file, returning current value summaries from public read-only APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sahil1005](https://clawhub.ai/user/sahil1005)

### License/Terms of Use:

MIT

## Use Case:

Developers and ClawHub users use this skill to inspect local cryptocurrency and stock portfolio entries and receive a read-only value summary without providing private keys.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Portfolio lookup data, including coin IDs, Ethereum wallet addresses, and an optional Etherscan API key, is sent to third-party public APIs.

Mitigation: Use only public wallet addresses that are acceptable to query externally, use a limited Etherscan API key, and review API provider terms and rate limits before deployment.

Risk: Failed runs or troubleshooting output could expose sensitive portfolio lookup details or API-key related context in shared logs.

Mitigation: Avoid sharing raw logs from failed runs and redact wallet addresses, portfolio contents, and API-key material before support or review.

Risk: The pinned requests dependency and placeholder stock-pricing behavior may be unsuitable for production portfolio reporting.

Mitigation: Update the requests dependency before production use and integrate a validated stock data provider before relying on stock valuations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sahil1005/skills/local-portfolio-auditor)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Plain text portfolio summary with setup and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads portfolio.json locally, queries public market-data APIs, and prints holdings plus total estimated value.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact SKILL.md states 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
