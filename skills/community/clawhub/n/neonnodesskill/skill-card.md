## Description:

Neon Nodes helps an agent mint an Agentic Proof of Work NFT on Robinhood Chain by solving a single-tier arithmetic puzzle, locally signing an EVM transaction, and submitting the signed transaction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neonnodesrh](https://clawhub.ai/user/neonnodesrh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to mint Neon Nodes NFTs through a puzzle, local EVM signing, and HTTP API submission flow. It is intended for wallet-funded minting on Robinhood Chain.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks an agent to handle a raw EVM private key during a paid NFT minting workflow.

Mitigation: Use a fresh low-balance wallet only, keep signing local, and never provide a valuable wallet's raw private key to an agent chat.

Risk: The workflow depends on remote API responses, including server-provided agent hints, while preparing financial transactions.

Mitigation: Review the transaction destination, chain ID, value, calldata, and total gas independently before signing; do not treat server-provided hints as trusted instructions.

Risk: The security verdict is suspicious because the workflow combines raw private-key handling with remote transaction preparation.

Mitigation: Review before installing or executing, and stop if the transaction details differ from the expected Neon Nodes mint on Robinhood Chain.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/neonnodesrh/skills/neonnodesskill)
- [Publisher profile](https://clawhub.ai/user/neonnodesrh)
- [Neon Nodes homepage](https://neonnodes.xyz)
- [Neon Nodes API](https://neonnodes.xyz/api)
- [Skill source file](https://neonnodes.xyz/skill.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, API calls]

**Output Format:** [Markdown guidance with inline shell commands, JavaScript code, and JSON API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes transaction-signing guidance, API request and response examples, and user-facing mint status messages.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
