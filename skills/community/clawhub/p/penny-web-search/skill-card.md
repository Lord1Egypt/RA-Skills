## Description:

Penny Web Search helps agents perform paid real-time web search and structured local-business or Places lookup through PennyAPI over x402.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ayoubsalem-spec](https://clawhub.ai/user/ayoubsalem-spec)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to route current-information research, verification, fact checking, and local-business lookup through PennyAPI. It is suitable when an agent needs fresh web results or structured place data and the user accepts the per-call x402 payment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid wallet-enabled requests can spend USDC or use a higher-risk wallet.

Mitigation: Use a low-risk funded wallet, inspect endpoints before paying, and confirm each paid call.

Risk: Fresh web or Places queries may disclose secrets or private business data to the service.

Mitigation: Avoid sending secrets, credentials, or sensitive business data in queries.

Risk: The artifact examples use unpinned npx @latest commands, so CLI behavior can change over time.

Mitigation: Pin or otherwise verify AgentCash and skills CLI versions before operational use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ayoubsalem-spec/skills/penny-web-search)
- [PennyAPI Homepage](https://pennyregwatch.com)
- [Penny Web Search Endpoint](https://pennyregwatch.com/v1/search)
- [Penny Places Endpoint](https://pennyregwatch.com/web/places)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API Calls, Text, Structured data]

**Output Format:** [Markdown guidance with inline shell commands and JSON request bodies]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Paid x402 requests return web-search results or place records from PennyAPI; no API key or subscription is described.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
