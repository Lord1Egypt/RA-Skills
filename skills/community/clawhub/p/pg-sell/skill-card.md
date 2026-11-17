## Description:

Helps agents guide ProxyGate sellers through creating and managing API listings, exposing services through tunnels, rotating credentials, uploading documentation, managing headers, and checking earnings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jwelten](https://clawhub.ai/user/jwelten)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and engineers use this skill to sell API capacity on ProxyGate by preparing listings, configuring tunnels, managing service metadata and credentials, and monitoring seller earnings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential-handling examples include API keys, OAuth tokens, wallet keypairs, uploaded docs, and custom headers.

Mitigation: Confirm credential-related commands with the user, avoid placing real secrets directly in shell commands, and review docs and headers for secrets before upload.

Risk: The included command reference covers broader financial, buyer proxy, and job-marketplace workflows beyond the seller listing task.

Mitigation: Use the skill only for intended seller listing and tunnel workflows unless the user explicitly requests those separate actions.

Risk: Tunnel and gateway commands can expose local services or route traffic through a custom gateway.

Mitigation: Verify the local service, selected tunnel configuration, and gateway URL before starting development or production tunnels.

## Reference(s):

- [ProxyGate CLI Command Reference](references/commands.md)
- [ProxyGate Gateway Docs](https://gateway.proxygate.ai/docs)
- [Pg Sell on ClawHub](https://clawhub.ai/jwelten/skills/pg-sell)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, YAML configuration, and TypeScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may affect ProxyGate listings, tunnels, credentials, documentation, headers, balances, and seller earnings.]

## Skill Version(s):

0.2.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
