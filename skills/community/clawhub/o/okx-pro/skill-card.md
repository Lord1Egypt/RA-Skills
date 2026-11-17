## Description:

Provides OKX exchange integration guidance for spot trading, futures trading, leverage, take-profit and stop-loss orders, and position management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[icenoodle](https://clawhub.ai/user/icenoodle)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and trading operators use this skill to prepare OKX V5 API requests for account queries, market data, spot and futures orders, leverage settings, cancellations, and position management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live OKX API credentials could expose account access or trading capability if stored insecurely or granted excessive permissions.

Mitigation: Use a dedicated OKX API key with minimum required permissions, no withdrawal permission, IP allowlisting where possible, and locked-down file permissions for any local credential file.

Risk: Order placement, cancellation, leverage, margin, and position-closing commands can execute financial actions.

Mitigation: Use OKX demo trading first and require explicit confirmation before any order, cancellation, leverage change, margin change, or position closure.

Risk: Leveraged futures and margin actions can amplify losses if pair, size, direction, or risk controls are wrong.

Mitigation: Verify instrument, quantity, side, and existing position before execution; keep leverage conservative and set stop-loss controls for leveraged trades.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/icenoodle/skills/okx-pro)
- [OKX V5 API Documentation](https://www.okx.com/docs-v5/)
- [OKX Demo Trading](https://www.okx.com/market/trade/demo)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, openssl, and user-provided OKX API credentials.]

## Skill Version(s):

1.1.0 (source: server release metadata; artifact frontmatter shows 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
