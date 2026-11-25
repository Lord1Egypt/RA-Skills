## Description:

Guides Go developers in using the unofficial go-dydx-indexer client to query dYdX v4 Indexer endpoints through typed responses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

AGPL-3.0-only

## Use Case:

Developers use this skill to integrate Go applications with the dYdX v4 Indexer for market and account data. It guides installation and typed endpoint usage, including response and error handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet addresses and account queries are sent to the configured indexer URL.

Mitigation: Use the intended mainnet or testnet HTTPS indexer URL and send only wallet addresses authorized for that destination.

Risk: Some POST endpoints affect the caller's identity, including push-token registration, Turnkey sign-in, and affiliate referral codes.

Mitigation: Call these endpoints only when the user requested the identity-related action and verify the target and request data.

## Reference(s):

- [Setup and reference](references/setup.md)
- [Go package documentation](https://pkg.go.dev/github.com/psyb0t/go-dydx-indexer)
- [Source repository](https://github.com/psyb0t/go-dydx-indexer)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown with Go code examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Endpoint-specific examples and typed Go usage guidance.]

## Skill Version(s):

0.3.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
