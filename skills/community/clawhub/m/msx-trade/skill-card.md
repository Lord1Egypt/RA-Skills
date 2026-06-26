## Description: <br>
Trade security tokens on the MSX platform by checking balances, placing and canceling orders, viewing market data, and reviewing trade history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[seineruo](https://clawhub.ai/user/seineruo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can use this skill to let an agent interact with MSX account, market, order, and history APIs for security-token trading workflows. It supports account and portfolio checks, quote and order-book lookup, order placement and cancellation, and historical trade or transaction reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an MSX API key that can expose sensitive account, balance, position, order, trade, and transaction data. <br>
Mitigation: Use the narrowest available key scope, prefer read-only credentials for reporting workflows, and never expose, log, or repeat the API key in agent responses. <br>
Risk: The skill can place and cancel security-token orders through the MSX API. <br>
Mitigation: Require explicit user confirmation before order placement or cancellation, repeat symbol, side, type, quantity, and price before execution, and add extra review for large orders. <br>
Risk: Ambiguous trading requests can result in unintended order parameters. <br>
Mitigation: Ask for missing quantity, price, side, symbol, or order type before using order-changing endpoints. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/seineruo/msx-trade) <br>
- [Publisher profile](https://clawhub.ai/user/seineruo) <br>
- [MSX API key application page](https://msx.com/api) <br>
- [Account and portfolio module](artifact/api-account.md) <br>
- [Market data module](artifact/api-market.md) <br>
- [Order execution module](artifact/api-orders.md) <br>
- [Trade history and reports module](artifact/api-history.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, configuration, guidance] <br>
**Output Format:** [Markdown responses with API request details, JSON-shaped examples, and tables for portfolio or history data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MSX_API_KEY; market data responses should include timestamps and trade-changing actions should require explicit user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
