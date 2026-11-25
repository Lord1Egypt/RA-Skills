## Description:

Provides an unofficial typed Go client for the Solana Tracker REST Data API and Datastream WebSocket API, with methods for token and wallet data and real-time event subscriptions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT

## Use Case:

Developers use this skill to integrate Go applications with Solana Tracker's REST Data API and Datastream WebSocket API, including token market data, wallet analytics, and real-time event subscriptions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The API key is used in REST authentication headers and in the Datastream WebSocket URL path, so logs or errors could expose credentials.

Mitigation: Read the key from SOLANA_TRACKER_API_KEY and redact authenticated headers, WebSocket URLs, and connection paths from logs and user-facing errors.

Risk: Token metadata, URLs, and social links returned by the API are external data.

Mitigation: Treat response content as untrusted; do not execute it or fetch linked resources solely because the API returned them.

Risk: Datastream access and API requests are subject to subscription tiers, credits, and rate limits.

Mitigation: Confirm the required Datastream subscription, respect subscription limits and request credits, and avoid tight retry loops after HTTP 429 responses.

Risk: The security review reports no findings in reviewed material but notes that three references were unresolved and coverage is incomplete.

Mitigation: Use judgment before installing and review unresolved references and the skill material for the intended environment.

## Reference(s):

- [Setup and reference](references/setup.md)
- [Project repository](https://github.com/psyb0t/go-solana-tracker)
- [Go package documentation](https://pkg.go.dev/github.com/psyb0t/go-solana-tracker)
- [ClawHub skill release](https://clawhub.ai/psyb0t/skills/go-solana-tracker)

## Skill Output:

**Output Type(s):** [Go code, Shell commands, Configuration instructions, Integration guidance]

**Output Format:** [Markdown guidance with Go code and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples and guidance depend on the requested API operations and response handling.]

## Skill Version(s):

0.4.0 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
