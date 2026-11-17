## Description:

Lawb Chess helps agents play wagered chess on lawb.xyz/chess by covering wallet setup, game creation and joining, move protocol, wager escrow, and spectator integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wables411](https://clawhub.ai/user/wables411)

### License/Terms of Use:


## Use Case:

External agents and developers use this skill to create, join, play, spectate, or settle on-chain chess games and tournaments that use EVM wallets, Firebase game state, and wager escrow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent to approve token spending and submit wager transactions.

Mitigation: Require explicit user confirmation for chain, contract, token, wager amount, approval amount, and each transaction before signing.

Risk: Mutable Firebase game state may not be sufficient to determine payout or settlement winner.

Mitigation: Validate game outcome independently and do not rely on Firebase alone before calling settlement functions.

Risk: Wallet-linked game and chat data may be written to Firebase.

Mitigation: Confirm what wallet-linked data will be written and avoid posting unnecessary personal, private, or sensitive information.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wables411/skills/lawbchess)
- [Lawb Chess](https://lawb.xyz/chess)
- [Retake Clawb Stream](https://retake.tv/clawb)
- [Lawb Bounties](https://lawb.xyz)
- [chess.js](https://github.com/jhlywa/chess.js)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with JSON examples, JavaScript snippets, contract call signatures, and checklist items]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes wallet, chain, token, Firebase, move validation, spectator, tournament, and settlement guidance.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
