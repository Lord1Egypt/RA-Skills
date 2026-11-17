## Description:

Operate NEAR JSON-RPC reads through UXC with a public provider default, provider-override guidance, and read-only guardrails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jolestar](https://clawhub.ai/user/jolestar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to run safe, read-only NEAR mainnet JSON-RPC queries through UXC, including status, account state, finalized block, chunk, gas price, and validator lookups. It also guides provider overrides while avoiding deprecated public RPC endpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may create or reuse a local UXC command alias and make public network calls to the configured NEAR RPC provider and schema URL.

Mitigation: Review the provider and schema URL before use, and confirm that command alias creation is acceptable in the target environment.

Risk: Using this workflow for wallet-authenticated actions or transaction submission would exceed the reviewed read-only scope.

Mitigation: Keep usage limited to the documented read-only methods unless a separate security and workflow review approves broader NEAR operations.

Risk: Public RPC providers can differ in archival retention, rate limits, and method availability.

Mitigation: Use an official provider appropriate for the required data history and switch providers when older block or chunk lookups fail.

## Reference(s):

- [Usage patterns](references/usage-patterns.md)
- [Curated OpenRPC schema](references/near-public.openrpc.json)
- [NEAR RPC introduction](https://docs.near.org/api/rpc/introduction)
- [NEAR RPC providers](https://docs.near.org/api/rpc/providers)
- [ClawHub skill page](https://clawhub.ai/jolestar/skills/near-jsonrpc-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON-RPC request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only NEAR JSON-RPC workflows using a fixed OpenRPC schema URL and provider-aware command setup.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
