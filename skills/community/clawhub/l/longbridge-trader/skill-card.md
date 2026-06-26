## Description: <br>
Longbridge Trader helps agents use the longport Python SDK to query market data, review account balances and positions, and submit, modify, or cancel brokerage orders with user confirmation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gavinyao](https://clawhub.ai/user/gavinyao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent assist with Longbridge/Longport market-data lookup, account review, and brokerage order workflows for Hong Kong, U.S., Shanghai, and Shenzhen securities. Trading actions should be treated as user-confirmed execution assistance, not investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent live brokerage-account authority when Longport credentials include trade permissions. <br>
Mitigation: Use quote-only or read-only credentials where possible, grant trade permissions only when needed, and require explicit confirmation before any order placement, modification, or cancellation. <br>
Risk: Order workflows may be unsafe if the agent does not present complete execution details before acting. <br>
Mitigation: Before execution, show the symbol, side, order type, quantity, price, and account context, then wait for the user's confirmation. <br>


## Reference(s): <br>
- [QuoteContext API Reference](references/quote-api.md) <br>
- [TradeContext API Reference](references/trade-api.md) <br>
- [Longbridge Open Platform](https://open.longbridge.cn) <br>
- [ClawHub release page](https://clawhub.ai/gavinyao/longbridge-trader) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with tables and inline Python or Bash snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May make Longport API calls when configured with user credentials; trading actions require explicit user confirmation before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
