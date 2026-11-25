## Description:

Helps developers write Go code with go-btse, an unofficial typed client for BTSE REST and WebSocket APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to write Go applications that access BTSE public market data and account APIs through REST or WebSocket clients.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan was partial because two local references could not be resolved, leaving their contents unassessed.

Mitigation: Review the unresolved references before relying on their contents or deploying the skill.

Risk: Private API credentials or signed request headers could be exposed if included in source code, logs, or output.

Mitigation: Read credentials from BTSE_API_KEY and BTSE_API_SECRET, and never hardcode, commit, or log credentials or signed headers.

Risk: Orders, withdrawals, transfers, and other account operations can change a user's exchange account.

Mitigation: Perform only the specific account action requested by the user; default to the test environment and use production only when requested.

## Reference(s):

- [go-btse setup and reference](artifact/references/setup.md)
- [go-btse source repository](https://github.com/psyb0t/go-btse)
- [go-btse Go package documentation](https://pkg.go.dev/github.com/psyb0t/go-btse)
- [BTSE REST API specifications](https://docs.btse.com/specs/{product}-rest.openapi.yaml)
- [BTSE WebSocket API specifications](https://docs.btse.com/specs/{spot,futures,otc}-websocket.asyncapi.yaml)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Go source code and concise Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

0.1.5 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
