## Description:

Unofficial Go client for Kalshi, generated from the API specs Kalshi publishes, with typed REST, WebSocket, and request-signing packages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT

## Use Case:

Developers use this skill to add the unofficial go-kalshi client to Go projects for reading Kalshi markets and account data, streaming market or account updates, and building integrations that manage a Kalshi account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review was partial because two local references could not be resolved, leaving some uncertainty despite no specific scanner findings.

Mitigation: Review the skill and its references before installation or use, taking the unresolved references into account.

Risk: Signed requests and account-management operations can expose private credentials or affect a real Kalshi account.

Mitigation: Keep private keys out of source control and logs, use the demo environment while developing, and perform account-changing operations only when explicitly requested.

## Reference(s):

- [Setup and reference](references/setup.md)
- [go-kalshi on GitHub](https://github.com/psyb0t/go-kalshi)
- [go-kalshi on pkg.go.dev](https://pkg.go.dev/github.com/psyb0t/go-kalshi)

## Skill Output:

**Output Type(s):** [Code, Configuration instructions, Guidance]

**Output Format:** [Go code and Markdown guidance with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

0.12.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
