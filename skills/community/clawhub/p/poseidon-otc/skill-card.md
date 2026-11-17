## Description:

Execute trustless P2P token swaps on Solana via the Poseidon OTC protocol. Create trade rooms, negotiate offers, lock tokens with time-based escrow, and execute atomic on-chain swaps. Supports agent-to-agent trading with real-time WebSocket updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[romovow](https://clawhub.ai/user/romovow)

### License/Terms of Use:

MIT

## Use Case:

Developers and external agents use this skill to create and manage Solana OTC trade rooms, negotiate token offers, coordinate escrow confirmations, and execute atomic swaps. It supports manual link-based signing and autonomous operation with a dedicated burner wallet.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Autonomous mode can move real Solana funds from a hot wallet.

Mitigation: Use a dedicated low-balance burner wallet and require approval or spending controls around offer updates, confirmations, claims, cancellations, and execution.

Risk: Secrets used for autonomous signing may be exposed if valuable keys are placed in environment files or logs.

Mitigation: Avoid storing valuable private keys in environment files or logs, and restrict POSEIDON_BURNER_KEY to a purpose-limited wallet.

Risk: The Poseidon API is part of the trade coordination trust boundary.

Mitigation: Review the Poseidon API trust boundary before using the skill for valuable trades.

## Reference(s):

- [Poseidon Cash](https://poseidon.cash)
- [Poseidon Cash Docs](https://docs.poseidon.cash)
- [ClawHub Skill Page](https://clawhub.ai/romovow/skills/poseidon-otc)

## Skill Output:

**Output Type(s):** [text, configuration, guidance]

**Output Format:** [Markdown or structured JSON-style results with room links, trade status, and transaction signatures]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Solana transaction signatures, trade room links, WebSocket connection information, and wallet balance or status data.]

## Skill Version(s):

1.0.0 (source: evidence release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
