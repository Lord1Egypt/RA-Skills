## Description:

Pay-per-call access to the Nansen API via MPP (Tempo). Use when a user wants anonymous Nansen access without an API key and without managing their own Base/Solana wallet — they install the tempo CLI separately and call the API through `tempo request`.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nansen-devops](https://clawhub.ai/user/nansen-devops)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use the skill to make paid Nansen API requests through Tempo MPP when they want to avoid an API key or managing a Base or Solana wallet.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup instructions pipe a downloaded Tempo installer directly into a shell without verifying its signature or checksum, creating supply-chain and code-execution risk.

Mitigation: Consider avoiding installation until the CLI installer can be verified through a trusted signature or checksum, or install the CLI separately from the skill. The scan was partial because a referenced local path was missing, so related behavior may not have been fully inspected.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/nansen-devops/skills/nansen-mpp-payment)
- [Tempo documentation](https://docs.tempo.xyz)
- [MPP protocol](https://mpp.dev/protocol)
- [Nansen CLI package](https://www.npmjs.com/package/nansen-cli)
- [Nansen CLI source repository (linked in the skill)](https://github.com/nansen-ai/nansen-cli)
- [Nansen paid endpoint discovery](https://api.nansen.ai/.well-known/x402)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Endpoint paths and request bodies depend on the selected Nansen API operation; paid requests incur per-request charges.]

## Skill Version(s):

1.0.1 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
