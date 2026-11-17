## Description:

Writes Go code with go-btse (github.com/psyb0t/go-btse), an unofficial BTSE client generated from its public OpenAPI and AsyncAPI specifications. REST packages btse (spot), futures, markets, wallet, earn and otc cover spot and futures orders, account fees, positions, public markets, wallets, transfers, withdrawals, earn products and OTC quotes; auth signs private requests with HMAC-SHA384; ws/spot, ws/futures and ws/otc cover WebSocket messages. Use when Go code needs BTSE API access or already imports github.com/psyb0t/go-btse.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT

## Use Case:

Developers use this skill to write Go integrations for BTSE spot and futures trading, market data, wallets, earn products, OTC operations, and WebSocket feeds. It also helps developers find the right client methods and handle authentication and responses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: BTSE orders, transfers, withdrawals, earn operations, and accepted OTC quotes can change account balances or positions.

Mitigation: Use testnet first, grant API keys only the permissions needed, and review generated code before enabling real trades or withdrawals. Run financial actions only when explicitly requested.

## Reference(s):

- [Setup and reference guide](references/setup.md)
- [go-btse project homepage](https://github.com/psyb0t/go-btse)
- [go-btse package documentation](https://pkg.go.dev/github.com/psyb0t/go-btse)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Guidance]

**Output Format:** [Go code and concise Markdown guidance with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the Go toolchain; generated guidance and code may cover API operations that change account state.]

## Skill Version(s):

0.1.4 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
