## Description:

Provides guidance for using the unofficial typed Go client for Interactive Brokers' Client Portal Web API to read account and market data or perform user-requested account operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT-0

## Use Case:

Go developers use this skill to integrate the go-ibkr client with an Interactive Brokers account through the Client Portal Gateway or OAuth. It helps them look up endpoints and handle account data, market data, and explicitly requested order operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Order submission, modification, cancellation, confirmation, and logout operations can affect a real brokerage account.

Mitigation: Use paper trading during development and perform an account-changing action only when the user explicitly requests that exact action.

Risk: OAuth access tokens can expose account access if disclosed.

Mitigation: Read tokens from an environment variable or the user's token code; never hardcode, commit, or log them.

Risk: Disabling certificate verification can expose requests to interception.

Mitigation: Limit disabled verification to the user's own local Client Portal Gateway; keep verification enabled for all other hosts.

Risk: The separately downloaded Go dependency was outside the artifact review.

Mitigation: Review and pin the dependency version before production use.

## Reference(s):

- [Setup and reference](references/setup.md)
- [go-ibkr package documentation](https://pkg.go.dev/github.com/psyb0t/go-ibkr)
- [go-ibkr source repository](https://github.com/psyb0t/go-ibkr)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with Go and shell code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

0.1.6 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
