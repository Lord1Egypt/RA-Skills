## Description:

Complete authentication guide for Orderly Network - EIP-712 wallet signatures for EVM accounts, Ed25519 message signing for Solana accounts, and Ed25519 signatures for API requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tarnadas](https://clawhub.ai/user/tarnadas)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to implement Orderly Network account registration, API key management, authenticated API calls, and WebSocket authentication for EVM and Solana wallets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Examples include private-key handling and may expose sensitive credentials if copied directly.

Mitigation: Remove private-key logging and store keys only in a secret manager or protected local store before use.

Risk: Trading, withdrawal, and asset examples can trigger real financial actions when pointed at mainnet.

Mitigation: Use testnet first, review every request before execution, and apply minimum API key scopes.

Risk: Signing helpers can be misused if routed to unapproved origins or endpoints.

Mitigation: Restrict signing helpers to approved Orderly API origins and validate request targets before signing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tarnadas/skills/orderly-api-authentication)
- [Orderly Network API](https://api.orderly.org)
- [Orderly Network testnet API](https://testnet-api.orderly.org)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with TypeScript examples, API endpoint references, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes EVM, Solana, REST API, WebSocket, and troubleshooting guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
