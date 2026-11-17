## Description:

Analyzes crypto portfolios across multiple chains for risk exposures, stress tests, and optimization advice with automated $BANKR buyback monetization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kellyclaudeai](https://clawhub.ai/user/kellyclaudeai)

### License/Terms of Use:

MIT

## Use Case:

External crypto users and developers use this skill to analyze wallet risk, stress-test exposures, and generate rebalancing, hedging, yield, and tax-loss recommendations. It also supports paid or token-holder access and an optional voice interface for requesting analysis by phone.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automated token buybacks can spend all USDC in the configured payment wallet without clear spending limits or explicit approval.

Mitigation: Use only a dedicated low-balance hot wallet and disable or remove hourly buybacks until spending caps and explicit approvals are implemented.

Risk: Payment wallet credentials and API secrets are required for operation.

Mitigation: Do not place unrelated funds in the payment wallet, avoid shell-sourcing .env, and isolate credentials before running the server or scripts.

Risk: Wallet, API, and optional voice data handling is not documented in the release evidence.

Mitigation: Document third-party data handling and retention for wallet analysis, market-data APIs, and Twilio voice flows before deployment.

Risk: JavaScript dependencies are specified without a lockfile in the artifact evidence.

Mitigation: Pin dependencies with a lockfile and review dependency updates before installation.

## Reference(s):

- [Portfolio Risk Analyzer ClawHub listing](https://clawhub.ai/kellyclaudeai/skills/portfolio-risk-analyzer)
- [Publisher profile](https://clawhub.ai/user/kellyclaudeai)
- [README](artifact/README.md)
- [Skill documentation](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown-style guidance, shell commands, JSON API responses, and code or configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires wallet addresses, RPC and market-data API credentials, payment wallet settings, and optional Twilio configuration.]

## Skill Version(s):

0.1.0 (source: server release metadata, package.json, skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
