## Description:

Guides Go developers in using unofficial, typed eToro REST and WebSocket clients for account data, market data, and account updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT-0

## Use Case:

Go developers use this skill to add and call eToro's REST client or consume WebSocket streams for account and market data. It explains authentication, response handling, and safeguards for operations that can transfer funds or publish content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API credentials could be exposed if hardcoded, logged, committed, or sent to an unintended host.

Mitigation: Read keys from environment variables, never hardcode, commit, or log them, and use them only with the documented eToro endpoints.

Risk: Some API operations can transfer funds or publish or delete content.

Mitigation: Use read-only endpoints by default and call transfer or publishing operations only when the user requested that exact action.

## Reference(s):

- [Setup and reference](references/setup.md)
- [Go package documentation](https://pkg.go.dev/github.com/psyb0t/go-etoro)
- [Project documentation](https://github.com/psyb0t/go-etoro)
- [ClawHub skill release](https://clawhub.ai/psyb0t/skills/go-etoro)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with Go and shell code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Go-only client usage; includes REST and WebSocket examples.]

## Skill Version(s):

0.6.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
