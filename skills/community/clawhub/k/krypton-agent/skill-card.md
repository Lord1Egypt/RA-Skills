## Description:

Register as buyer or seller, create and manage USDC escrow trades on Kryptone/PrivacyEscrow via HTTP API using agent API key or human JWT auth.

This skill is ready for commercial/non-commercial use.

## Publisher:

[webcraft3r](https://clawhub.ai/user/webcraft3r)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and operators use this skill to let an agent register as a buyer or seller and manage Kryptone/PrivacyEscrow USDC escrow workflows through an authenticated HTTP API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an agent sensitive financial API authority through AGENT_API_KEY and can send that shared key to the configured HTTP endpoint.

Mitigation: Install only when the Kryptone API server is trusted, use HTTPS for non-local endpoints, keep HTTP limited to localhost, and rotate AGENT_API_KEY if it may have crossed an untrusted connection.

Risk: Trade creation and settlement commands can affect USDC escrow state.

Mitigation: Require explicit user approval before allowing an agent to run trade-creation, deposit, or settlement commands.

## Reference(s):

- [Krypton Agent ClawHub page](https://clawhub.ai/webcraft3r/skills/krypton-agent)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code]

**Output Format:** [Markdown instructions with inline shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Node.js CLI helpers that print API responses as formatted JSON.]

## Skill Version(s):

1.0.0 (source: package.json and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
