## Description:

Trade security tokens on the MSX platform: check balances, place orders, view market data, and review trade history.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seineruo](https://clawhub.ai/user/seineruo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent retrieve MSX account, portfolio, market, order, and trade-history information and assist with trading actions through the MSX API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access sensitive financial account data through the MSX API key.

Mitigation: Install only if the MSX integration is trusted; keep MSX_API_KEY in the environment and never expose, log, or repeat it in responses.

Risk: The skill can place or cancel trading orders, and cancellation triggers may be broad.

Mitigation: Require explicit user confirmation before new orders and cancellations, repeat the exact order details, and ask for clarification whenever a request is ambiguous.

Risk: Broad account or history requests can retrieve sensitive financial records.

Mitigation: Use precise MSX-specific requests and return only the account, portfolio, order, or history data needed for the user's stated task.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/seineruo/skills/msx-trading)
- [MSX API access](https://msx.com/api)
- [MSX API base endpoint](https://api.msx.com/v1)
- [Account & Portfolio module](artifact/api-account.md)
- [Market Data module](artifact/api-market.md)
- [Order Execution module](artifact/api-orders.md)
- [Trade History & Reports module](artifact/api-history.md)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown responses with tables, confirmations, and structured API request guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses MSX_API_KEY for authenticated MSX API requests; responses may include account balances, positions, market data, orders, and history.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
