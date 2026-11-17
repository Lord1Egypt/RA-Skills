## Description:

Connect an MCP-capable coding agent to Goloco through a connection-bound credential, verify the selected agent and permissions, and use the supply-side tools without treating the credential as an account session or a wallet signer.

This skill is ready for commercial/non-commercial use.

## Publisher:

[frejusgdm](https://clawhub.ai/user/frejusgdm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to connect an MCP-capable coding agent to Goloco, verify the active agent connection, understand available marketplace tools, and interpret connection or tool refusals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A Goloco credential may be exposed if copied into checked-in configuration.

Mitigation: Store bearer credentials in the MCP client's credential store and keep them out of source control.

Risk: Users may mistake an agent credential for an account session or wallet signer.

Mitigation: Verify the connection first and rely on the console or wallet controller for account-level and money-moving approvals.

Risk: Changing credentials or retry keys after a refusal can create confusion or duplicate logical operations.

Mitigation: Read the refusal code, reconnect only when authentication has expired or been revoked, and reuse the same idempotency key for retries of the same mutation.

## Reference(s):

- [Goloco Connect Your Assistant Guide](https://1849.mintlify.app/connect-your-agent)
- [Reading a Goloco refusal](reference/failure-modes.md)

## Skill Output:

**Output Type(s):** [guidance, configuration, shell commands]

**Output Format:** [Markdown with JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance is scoped to Goloco MCP connection setup, verification, tool behavior, refusals, retries, and credential handling.]

## Skill Version(s):

1.0.0 (source: frontmatter and server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
