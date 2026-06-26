## Description: <br>
Trade security tokens on the MSX platform by checking balances, placing and canceling orders, viewing market data, and reviewing trade history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[seineruo](https://clawhub.ai/user/seineruo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to interact with MSX trading APIs for account, portfolio, market data, order management, and trade-history workflows. Order placement and cancellation require explicit confirmation before requests are sent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access private account, portfolio, balance, transaction, and trading-history data. <br>
Mitigation: Use a dedicated least-privilege MSX_API_KEY, avoid unnecessary account-history requests, and verify the MSX endpoint and publisher independently before installation. <br>
Risk: The skill can place or cancel security-token orders, which may affect a real trading account. <br>
Mitigation: Require explicit user confirmation for every order or cancellation, review symbol, side, type, quantity, and price, and add extra confirmation for large orders. <br>
Risk: A leaked or over-permissive API key could expose financial data or trading permissions. <br>
Mitigation: Store the API key only in the environment, do not log or repeat it, scope permissions narrowly, rotate it regularly, and disable trading permissions unless needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/seineruo/msx-trading) <br>
- [MSX API key application](https://msx.com/api) <br>
- [MSX API base URL](https://api.msx.com/v1) <br>
- [Account and portfolio module](artifact/api-account.md) <br>
- [Market data module](artifact/api-market.md) <br>
- [Order execution module](artifact/api-orders.md) <br>
- [Trade history module](artifact/api-history.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, configuration, guidance] <br>
**Output Format:** [Markdown responses with tables, timestamps, and API request details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MSX_API_KEY; responses should match the user's language and confirm order details before trading actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
