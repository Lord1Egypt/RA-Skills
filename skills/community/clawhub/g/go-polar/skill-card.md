## Description:

An unofficial typed Go client for the Polar API, covering products, customers, subscriptions, checkouts, orders, payments, benefits, usage events, meters, refunds, and webhooks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to add or work with Go code that calls Polar's API, including reading account data and carrying out requested account changes. It is intended for Go projects using github.com/psyb0t/go-polar; the client is unofficial and not maintained by Polar.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Polar bearer tokens can authorize access to account data and operations.

Mitigation: Use a token with only the required scopes, keep it in POLAR_ACCESS_TOKEN, and never hardcode, commit, or log it.

Risk: Create, update, delete, refund, and revoke operations change Polar account data.

Mitigation: Run these operations only when requested, and use the environment selected by the user.

Risk: The security assessment is benign but partial; credential-related setup and unresolved path-like references leave some uncertainty.

Mitigation: Review the setup guidance and use an appropriately scoped token before installation or use.

## Reference(s):

- [Setup and API usage reference](artifact/references/setup.md)
- [go-polar source repository](https://github.com/psyb0t/go-polar)
- [go-polar package documentation](https://pkg.go.dev/github.com/psyb0t/go-polar)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Go code and Markdown guidance with shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples and client calls depend on the requested Polar operation and Go project.]

## Skill Version(s):

0.4.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
