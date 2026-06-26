## Description: <br>
Operate Helius Wallet API reads through UXC with a curated OpenAPI schema, API-key auth, and read-first guardrails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jolestar](https://clawhub.ai/user/jolestar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to inspect and run read-only Helius Wallet API operations for Solana wallet identity, balances, history, transfers, and funding-source lookups through UXC. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet addresses and lookup details may be sent to Helius and could be logged by that provider. <br>
Mitigation: Avoid querying sensitive targets from identifiable environments, minimize query size and frequency, and review Helius data-handling terms or use a local or self-hosted alternative when operational privacy is critical. <br>
Risk: The Helius Wallet API is documented by the artifact as beta, so response shapes may drift. <br>
Mitigation: Keep automation focused on stable JSON envelope fields, inspect operation schemas before use, and start with narrow reads before paginating larger histories or transfers. <br>


## Reference(s): <br>
- [Usage patterns](references/usage-patterns.md) <br>
- [Curated OpenAPI schema](references/helius-wallet.openapi.json) <br>
- [Helius authentication docs](https://www.helius.dev/docs/api-reference/authentication) <br>
- [Helius Wallet API docs](https://www.helius.dev/docs/api-reference/wallet-api) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls, JSON] <br>
**Output Format:** [Markdown instructions with bash examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires HELIUS_API_KEY and network access to https://api.helius.xyz; the documented operations are read-only.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
