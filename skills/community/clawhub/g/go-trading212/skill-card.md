## Description:

Unofficial Go client for the Trading 212 Public API, generated with oapi-codegen from the OpenAPI document Trading 212 publishes. Package `trading212` (`github.com/psyb0t/go-trading212`) has a typed `...WithResponse` method for every endpoint: account summary, positions, open orders, limit, market, stop and stop-limit orders, order, dividend and transaction history, CSV report exports, exchange and instrument metadata, and pies. Prices and amounts are `float64`. Use when Go code needs to read a Trading 212 account or place Trading 212 orders, or already imports go-trading212.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to integrate Go applications with the Trading 212 Public API, read account data and history, or make account changes when explicitly requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live orders and pie changes can affect real investments.

Mitigation: Start with demo credentials, use the live environment only when explicitly requested, and authorize each account change explicitly.

Risk: API credentials could expose account access if disclosed.

Mitigation: Read credentials from environment variables and never hardcode, commit, or log them.

## Reference(s):

- [Setup and API reference](artifact/references/setup.md)
- [Go Trading212 project](https://github.com/psyb0t/go-trading212)
- [Go package documentation](https://pkg.go.dev/github.com/psyb0t/go-trading212)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration instructions]

**Output Format:** [Go source code, shell commands, and concise Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Go integration examples; account changes require an explicit user request.]

## Skill Version(s):

0.1.5 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
