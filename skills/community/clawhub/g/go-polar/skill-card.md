## Description:

Unofficial Go client for the Polar API, generated with oapi-codegen from Polar's published OpenAPI document. Package polar (github.com/psyb0t/go-polar) provides typed REST methods for products, customers, subscriptions, checkouts, orders, payments, benefits, usage events, meters, refunds and webhook management. Use when Go code needs the Polar API or already imports go-polar.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT-0

## Use Case:

Go developers use this skill to add and work with a typed Polar API client in a Go project, including reading data and carrying out requested account operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Polar access tokens grant access according to their scopes, and create, update, delete, refund, or revoke operations can change account data.

Mitigation: Use a token type and scopes appropriate to the requested operation, keep the token out of source control and logs, and perform account-changing operations only when requested.

Risk: The security scan was partial with medium confidence because two local references were unresolved.

Mitigation: Review the available setup reference and verify any details that depend on the unresolved material before use.

## Reference(s):

- [Setup and reference](artifact/references/setup.md)
- [go-polar repository](https://github.com/psyb0t/go-polar)
- [go-polar package documentation](https://pkg.go.dev/github.com/psyb0t/go-polar)
- [go-polar on ClawHub](https://clawhub.ai/psyb0t/skills/go-polar)

## Skill Output:

**Output Type(s):** [Code, API Calls, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline Go and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples and integration guidance for the Go Polar client.]

## Skill Version(s):

0.3.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
