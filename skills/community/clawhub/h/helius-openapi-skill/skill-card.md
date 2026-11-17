## Description:

Operate Helius Wallet API reads through UXC with a curated OpenAPI schema, API-key auth, and read-first guardrails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jolestar](https://clawhub.ai/user/jolestar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure UXC and run read-only Helius Wallet API lookups for wallet identity, balances, activity, transfers, and funding source data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends wallet addresses, balance and history filters, and related lookup parameters to Helius.

Mitigation: Use the skill only when sharing those lookup parameters with Helius is acceptable for the intended workflow.

Risk: The skill requires a Helius API key configured for UXC.

Mitigation: Store the key in the documented HELIUS_API_KEY environment variable and bind it only to api.helius.xyz with the X-Api-Key header.

Risk: The Helius Wallet API surface is documented by the artifact as beta and response shapes may drift.

Mitigation: Keep automation focused on stable JSON envelope fields and start with small limits before broader history or transfer reads.

Risk: Strict change-control environments may need confidence in the remote OpenAPI schema source.

Mitigation: Review or pin the curated OpenAPI schema before deployment when remote schema changes would affect approval requirements.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jolestar/skills/helius-openapi-skill)
- [Usage patterns](references/usage-patterns.md)
- [Curated OpenAPI schema](references/helius-wallet.openapi.json)
- [Helius authentication docs](https://www.helius.dev/docs/api-reference/authentication)
- [Helius Wallet API docs](https://www.helius.dev/docs/api-reference/wallet-api)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API calls]

**Output Format:** [Markdown with inline bash commands and JSON-oriented API guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill guides read-only operations and recommends parsing stable JSON envelope fields such as ok, kind, protocol, data, and error.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
