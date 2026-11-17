## Description:

Launch a free Solana token, keep trading fees, and use a non-custodial flow where private keys remain in the user's wallet.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aiengineerx](https://clawhub.ai/user/aiengineerx)

### License/Terms of Use:


## Use Case:

External developers and agents use this skill to call the BagsWorld API for launching Solana tokens, generating token images, checking or claiming trading-fee earnings, and coordinating agent tasks or organizations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may be asked to sign Solana transactions supplied by a remote service.

Mitigation: Use a dedicated wallet with minimal funds, decode and verify programs, accounts, recipients, and amounts, simulate through a trusted RPC, and confirm expected balance changes before signing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aiengineerx/skills/pokecenter)
- [BagsWorld external API](https://bagsworld.app/api/agent-economy/external)
- [Pokécenter documentation](https://bagsworld.app/docs/POKECENTER.md)
- [Pokécenter heartbeat config](https://bagsworld.app/pokecenter-heartbeat.md)
- [Bags.fm](https://bags.fm)
- [Moltbook](https://moltbook.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON and shell-style API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include unsigned Solana transaction handling guidance; users must verify transactions before signing.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
