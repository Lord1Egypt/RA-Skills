## Description:

Provides Go developers with a typed client for reading Trading 212 account data and managing orders and pies through the Trading 212 Public API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT-0

## Use Case:

Go developers use this client to read account, position, order, and history data, or to place and manage orders and pies when requested. It supports projects that already use github.com/psyb0t/go-trading212.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Order and pie operations can change a Trading 212 account, including a live account.

Mitigation: Use the demo environment by default; perform only the exact account action the user requested, and use the live environment only when the user explicitly asks for it.

Risk: Security review coverage is incomplete because two local references were unresolved.

Mitigation: Review the installation steps and setup guidance, including the documented order and pie deletion operations, before installing or using the client.

## Reference(s):

- [Setup and API reference](references/setup.md)
- [go-trading212 project homepage](https://github.com/psyb0t/go-trading212)
- [go-trading212 package documentation](https://pkg.go.dev/github.com/psyb0t/go-trading212)
- [ClawHub skill release](https://clawhub.ai/psyb0t/skills/go-trading212)

## Skill Output:

**Output Type(s):** [Code, Configuration instructions]

**Output Format:** [Go code with setup and API usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses API credentials supplied through environment variables; account-changing operations require explicit user direction.]

## Skill Version(s):

0.1.6 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
