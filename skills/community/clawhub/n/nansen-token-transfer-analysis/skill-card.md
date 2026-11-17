## Description:

Where is this token moving and why? Large transfers, flow trends over time, and breakdown by wallet label.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nansen-devops](https://clawhub.ai/user/nansen-devops)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and token researchers use this skill to inspect a token's large transfers, flow trends, and activity grouped by wallet labels. It helps summarize movement across supported chains and highlight possible patterns such as exchange inflows or fresh-wallet activity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Supported x402 research calls can spend funds from the configured wallet, and repeated calls or loops can multiply charges.

Mitigation: Use an explicitly selected authenticated key or browser session, review wallet authorization and spending limits, and avoid unattended repeated calls. Stop if authentication or renewal fails.

Risk: Transfer and wallet-label patterns can be misread as evidence of market intent; the skill describes exchange inflows as potential sell pressure and fresh-wallet inflows as possible interest or wash trading.

Mitigation: Treat these patterns as signals for further research, not proof of intent or a standalone investment decision.

## Reference(s):

- [Nansen browser login platform scope](https://github.com/nansen-ai/nansen-cli/blob/main/docs/browser-login.md#preview-platform-scope)

## Skill Output:

**Output Type(s):** [Analysis, Shell commands, Guidance]

**Output Format:** [Markdown analysis with token transfer and flow summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected token, chain, time range, available account entitlements, and wallet labels. Token flows does not support stablecoins.]

## Skill Version(s):

0.1.3 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
