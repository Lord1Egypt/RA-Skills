## Description:

Monitor cryptocurrency prices and send alerts when thresholds are crossed. No API key required - uses Binance public API. Supports BTC, ETH, SOL, and 10+ tokens.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jimmyclanker](https://clawhub.ai/user/jimmyclanker)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to check cryptocurrency prices, configure local threshold alerts, and optionally send alert notifications through Telegram.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The alert-setting workflow has a code-injection risk when untrusted alert text is passed into set-alert.sh.

Mitigation: Review before installing and allow only trusted alert inputs until the heredoc and JSON construction are fixed.

Risk: Service documentation is inconsistent because the skill uses both Binance and CoinGecko public APIs.

Mitigation: Expect outbound requests to both Binance and CoinGecko, and review network access policies before deployment.

Risk: Telegram bot tokens and chat IDs may be stored in local configuration.

Mitigation: Protect Telegram credentials and exclude local configuration files from sharing or source control.

## Reference(s):

- [Binance Public API](https://api.binance.com/api/v3)
- [CoinGecko Public API](https://api.coingecko.com/api/v3)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and concise configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local alert state in ~/.crypto-alert-state.json when the provided shell scripts are run.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
