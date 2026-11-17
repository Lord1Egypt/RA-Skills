## Description:

Unofficial Go client for the dYdX v4 Indexer HTTP API, generated with oapi-codegen. `dydxindexer.NewClientWithResponses(baseURL)` from `github.com/psyb0t/go-dydx-indexer` gives a typed method for every endpoint in the indexer's OpenAPI spec (block height and time, perpetual markets, orderbooks, candles, trades, historical funding, sparklines, subaccounts, positions, orders, fills, transfers, PnL, rewards, affiliates, vaults, compliance screening), with decoded `JSON200` response fields. The API is public and needs no key. Use when Go code needs dYdX v4 market or account data from the indexer, or already imports go-dydx-indexer.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

AGPL-3.0-only

## Use Case:

Developers use this skill to add the Go client to a project and make typed requests to the dYdX v4 Indexer for public market data or account data associated with an address. It provides setup instructions, endpoint guidance, and examples for handling typed responses and errors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Go dependency is fetched from an external module source.

Mitigation: Review and pin the dependency version before adding it to a project.

Risk: Registration, sign-in, notification, and affiliate endpoints can change or act on the caller's identity.

Mitigation: Use these endpoints only when the user explicitly requests the corresponding identity-related action.

Risk: Account data requests send wallet addresses to the selected indexer.

Mitigation: Send only the address supplied for the task and use the intended mainnet or testnet indexer URL.

## Reference(s):

- [Setup and API reference](references/setup.md)
- [Go package documentation](https://pkg.go.dev/github.com/psyb0t/go-dydx-indexer)
- [Project homepage](https://github.com/psyb0t/go-dydx-indexer)
- [ClawHub skill page](https://clawhub.ai/psyb0t/skills/go-dydx-indexer)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Guidance]

**Output Format:** [Markdown guidance with Go code examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

0.1.3 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
