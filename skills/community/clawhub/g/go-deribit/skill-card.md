## Description:

Writes Go code with go-deribit, an unofficial client for Deribit crypto options and futures generated from Deribit's public specs. Root package `deribit` (`github.com/psyb0t/go-deribit`) covers all 186 REST paths for instruments, market data, accounts, positions, orders, transfers and account administration. Package `deribitws` (`/ws`) covers all 43 JSON-RPC subscription channels for order books, tickers, trades and account updates. Use when Go code needs Deribit REST calls or WebSocket subscriptions, or already imports go-deribit.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to write Go integrations with Deribit's REST API and WebSocket subscription channels for market data and account operations. Private calls require an OAuth token, and account-changing actions should be made only when the user requests the specific action.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private REST calls use an OAuth bearer token, and the security review says its assessment is partial because some local references could not be resolved.

Mitigation: Review the referenced material before installing; keep tokens in environment configuration such as DERIBIT_ACCESS_TOKEN, and never hardcode, commit, or log credentials.

Risk: The client exposes order, transfer, withdrawal, and account or API key operations that can affect an account.

Mitigation: Use testnet during development, select production only when requested, and make account-changing calls only when the user requested that exact action.

## Reference(s):

- [Setup and reference](artifact/references/setup.md)
- [Go package documentation](https://pkg.go.dev/github.com/psyb0t/go-deribit)
- [Project repository](https://github.com/psyb0t/go-deribit)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Go examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Go integration code and usage guidance; dependency installation commands may be included.]

## Skill Version(s):

0.3.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
