## Description:

Executes Polymarket (pmbuysell) trade/balance via CLI or Python API. Use when the user or model needs to trade or query balances/positions. Auto-redeem is a separate paid addon (pmbuysell_redeem).

This skill is ready for commercial/non-commercial use.

## Publisher:

[yutou123](https://clawhub.ai/user/yutou123)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to initialize pmbuysell configuration, validate account settings, place Polymarket buy/sell orders, and query USDC balances or market positions through CLI or Python calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place real-money Polymarket orders.

Mitigation: Use a dedicated wallet with limited funds and require explicit human confirmation before every trade.

Risk: Transaction amount handling includes automatic or sentinel behavior for zero, negative, or large values.

Mitigation: Require explicit positive trade amounts, set conservative maximums, and review automatic amount calculation before use.

Risk: Credential and API key handling relies on local environment files and cached API credentials.

Mitigation: Protect local config and cache files, avoid shared environments, and delete or disable plaintext credential caches where possible.

Risk: Dependencies and the separate redeem add-on require additional trust review.

Mitigation: Pin and audit dependencies, and review the pmbuysell_redeem package independently before installing it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yutou123/skills/pmbuysell)
- [Publisher profile](https://clawhub.ai/user/yutou123)
- [Polymarket CLOB endpoint](https://clob.polymarket.com)
- [Polymarket relayer endpoint](https://relayer-v2.polymarket.com/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with shell and Python examples; runtime commands return JSON objects.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Trade and balance commands emit an ok flag, message, balances or positions, and order details when available.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
