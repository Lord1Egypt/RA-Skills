## Description:

NOFX AI Trading OS integration provides crypto market data, AI trading signals, strategy management, trader control, automated reporting, backtesting, and AI debate workflows for the NOFX platform.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tinkle-community](https://clawhub.ai/user/tinkle-community)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to query NOFX crypto-market APIs, configure strategies and exchange connections, manage traders, run backtests, and generate market reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live-trading controls and exchange API permission changes can affect real funds.

Mitigation: Require explicit confirmation before strategy activation, trader start or stop actions, exchange API permission changes, or fund transfers; start with testnet or isolated sub-accounts with limited funds and withdrawal permissions disabled.

Risk: Deployment and update instructions fetch remote installers or container definitions.

Mitigation: Review the deployment source before installation, pin installers and images to immutable releases or checksums, and use HTTPS end to end.

Risk: API keys and exchange credentials are needed for normal operation.

Mitigation: Store secrets outside shared workspace files, prefer environment variables or a secret manager, enable IP whitelists, rotate keys, and grant only the minimum permissions required.

## Reference(s):

- [NOFX Skill on ClawHub](https://clawhub.ai/tinkle-community/skills/nofx)
- [NOFX Web Dashboard](https://nofxai.com)
- [NOFX Data API](https://nofxos.ai)
- [NOFX API Docs](https://nofxos.ai/api-docs)
- [NOFX GitHub Repository](https://github.com/NoFxAiOS/nofx)
- [NOFX API Response Examples](references/api-examples.md)
- [NOFX Browser Automation Guide](references/browser-automation.md)
- [NOFX Deployment Guide](references/deployment.md)
- [NOFX Supported Exchanges](references/exchanges.md)
- [NOFX Strategy Configuration Schema](references/strategy-schema.md)
- [NOFX Webhook Notification Integration](references/webhooks.md)
- [NOFX Multi-Account Management](references/multi-account.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration examples, shell command snippets, and API call instructions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require a NOFX API key, exchange credentials, and an authenticated browser profile; some workflows can affect live trading accounts.]

## Skill Version(s):

1.1.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
