## Description:

Writes Go code with go-deribit, an unofficial client for Deribit crypto options and futures generated from Deribit's public specs, covering REST endpoints and WebSocket subscription channels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT

## Use Case:

Developers use this skill to write Go applications that call Deribit REST APIs or consume Deribit WebSocket subscriptions for market data, trading, account information, and administration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private REST calls require an OAuth token, and order, transfer, withdrawal, and account administration operations can affect a live account.

Mitigation: Keep credentials in environment or secret storage and never hardcode, commit, or log them. Use testnet during development and perform account-changing actions only when the user requested that exact action.

Risk: The benign security verdict has medium confidence because scanner coverage was partial.

Mitigation: Review the skill and its dependencies before providing credentials or using it against a production account.

## Reference(s):

- [Setup and API reference](references/setup.md)
- [go-deribit project](https://github.com/psyb0t/go-deribit)
- [go-deribit Go package documentation](https://pkg.go.dev/github.com/psyb0t/go-deribit)

## Skill Output:

**Output Type(s):** [Code, API Calls, Configuration instructions, Guidance]

**Output Format:** [Go code and Markdown guidance with shell commands where needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tailored to the requested REST or WebSocket task; may include public or authenticated account operations.]

## Skill Version(s):

0.4.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
