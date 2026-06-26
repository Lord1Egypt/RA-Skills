## Description: <br>
Operate NEAR JSON-RPC reads through UXC with a public provider default, provider-override guidance, and read-only guardrails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jolestar](https://clawhub.ai/user/jolestar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect NEAR mainnet JSON-RPC state through UXC while staying on a documented read-only method surface. It helps link a local CLI command, run status and query operations, and switch providers without using deprecated public RPC endpoints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates a local UXC CLI link and sends read-only NEAR RPC requests to the configured provider. <br>
Mitigation: Install only when that local command creation and provider network use are acceptable for the deployment environment. <br>
Risk: A moving schema URL can change after release. <br>
Mitigation: For stricter supply-chain control, use the bundled schema or a pinned schema URL instead of relying on a main-branch URL. <br>
Risk: Public RPC providers can vary in archival retention and rate limits. <br>
Mitigation: Switch to a provider that explicitly supports the needed history or rate profile when older block, chunk, or high-volume reads fail. <br>


## Reference(s): <br>
- [Usage patterns](references/usage-patterns.md) <br>
- [Curated OpenRPC schema](references/near-public.openrpc.json) <br>
- [NEAR RPC introduction](https://docs.near.org/api/rpc/introduction) <br>
- [NEAR RPC providers](https://docs.near.org/api/rpc/providers) <br>
- [ClawHub skill page](https://clawhub.ai/jolestar/near-jsonrpc-skill) <br>
- [Publisher profile](https://clawhub.ai/user/jolestar) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance, JSON examples] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only NEAR JSON-RPC workflows using a public provider default and provider override guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
