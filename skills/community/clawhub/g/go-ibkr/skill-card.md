## Description:

Provides an unofficial typed Go client for the Interactive Brokers Web API, covering account and market data access as well as order operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT-0

## Use Case:

Go developers use this client to access Interactive Brokers account, position, contract, and market data APIs, or to submit and manage orders when requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Order submission, modification, cancellation, confirmations, model order actions, and logout can affect a real brokerage account.

Mitigation: Perform account actions only when the user requested that specific action, and prefer a paper trading account during development.

Risk: OAuth access tokens can expose account access if they are mishandled.

Mitigation: Read tokens from the user's secure token source; never hardcode, commit, or log them.

Risk: The security assessment is benign with medium confidence, but analysis is incomplete because two local references were unresolved.

Mitigation: Review the unresolved references and use credentials only for account actions the user intends.

## Reference(s):

- [Setup and API reference](references/setup.md)
- [Project homepage](https://github.com/psyb0t/go-ibkr)
- [Go package documentation](https://pkg.go.dev/github.com/psyb0t/go-ibkr)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with Go code examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

0.2.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
