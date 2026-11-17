## Description:

Pg Buy guides agents through buying API access with ProxyGate, including USDC deposits, API discovery, proxied requests, streaming responses, usage checks, withdrawals, and seller ratings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jwelten](https://clawhub.ai/user/jwelten)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use this skill when they want to discover paid APIs and route requests through ProxyGate using either the CLI or SDK. It is most relevant when the workflow includes wallet balance checks, USDC deposits, paid proxy calls, usage review, settlement review, or withdrawals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide ordinary API requests into paid external ProxyGate proxy usage.

Mitigation: Require explicit user approval before every paid proxy request, and show expected cost and target service whenever available.

Risk: The workflow includes real USDC deposits, withdrawals, and withdraw-all actions.

Mitigation: Require explicit confirmation for every deposit, withdrawal, withdraw-all, and withdrawal recovery action before suggesting or executing commands.

Risk: Proxied requests may send secrets or confidential payloads to external API providers.

Mitigation: Do not send secrets, credentials, private keys, or confidential payloads through proxied APIs unless the user explicitly approves the exact data and destination.

Risk: Custom gateway or Solana RPC endpoints may redirect traffic or transaction activity to untrusted infrastructure.

Mitigation: Use default endpoints unless the user confirms that a custom gateway or RPC endpoint is trusted.

## Reference(s):

- [ProxyGate CLI Command Reference](references/commands.md)
- [ProxyGate Gateway Documentation](https://gateway.proxygate.ai/docs)
- [ClawHub Skill Page](https://clawhub.ai/jwelten/skills/pg-buy)
- [Publisher Profile](https://clawhub.ai/user/jwelten)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline bash and TypeScript code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include paid ProxyGate CLI commands, SDK usage examples, request payload examples, and wallet or gateway configuration guidance.]

## Skill Version(s):

0.2.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
