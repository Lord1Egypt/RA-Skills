## Description:

Trade security tokens on the MSX platform by checking balances, placing orders, viewing market data, and reviewing trade history.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seineruo](https://clawhub.ai/user/seineruo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent retrieve MSX account, portfolio, market, order, and trade-history information. It can also guide live order placement and cancellation when the user provides explicit confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use an MSX API key to retrieve sensitive balances, holdings, orders, and transaction history.

Mitigation: Install only after review, use a restricted API key where possible, and avoid exposing account data in shared conversations or logs.

Risk: The skill can place or cancel live MSX orders.

Mitigation: Require manual confirmation for every order and cancellation, including symbol, side, order type, quantity, and price when applicable.

Risk: Broad or ambiguous trading requests could trigger unintended order workflows.

Mitigation: Ask clarifying questions for vague requests and proceed only when the user clearly intends an MSX trading action.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/seineruo/skills/msx-trade)
- [MSX API access](https://msx.com/api)
- [MSX API base endpoint](https://api.msx.com/v1)
- [Account and portfolio module](artifact/api-account.md)
- [Market data module](artifact/api-market.md)
- [Order execution module](artifact/api-orders.md)
- [Trade history module](artifact/api-history.md)

## Skill Output:

**Output Type(s):** [API Calls, Markdown, Guidance]

**Output Format:** [Markdown responses with API request details, tables, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include sensitive account, position, order, and transaction details returned by the MSX API.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
