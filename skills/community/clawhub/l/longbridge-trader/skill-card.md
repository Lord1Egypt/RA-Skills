## Description:

Longbridge Trader helps agents use the longport Python SDK to query market data, account balances and positions, and submit, modify, or cancel brokerage orders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gavinyao](https://clawhub.ai/user/gavinyao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and trading-agent users use this skill to connect an agent to a Longbridge brokerage account for market quotes, K-line data, order book data, account balances, positions, order management, executions, and cash-flow review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent live brokerage access for trading and account operations.

Mitigation: Use isolated, least-privilege Longbridge credentials, prefer read-only or sandbox credentials where possible, and install only when brokerage access is intended.

Risk: State-changing actions such as submitting, modifying, or canceling orders can affect a real account.

Mitigation: Require explicit user confirmation for every state-changing action, including order cancellation, after showing the full order parameters.

Risk: The configured longport SDK dependency mediates access to brokerage APIs.

Mitigation: Pin and verify the longport SDK before use.

## Reference(s):

- [QuoteContext API Reference](references/quote-api.md)
- [TradeContext API Reference](references/trade-api.md)
- [Longbridge Open Platform](https://open.longbridge.cn)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with tables, status summaries, and inline Python or shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Market data, account values, quantities, prices, percentages, and order identifiers should be displayed clearly for user review.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
