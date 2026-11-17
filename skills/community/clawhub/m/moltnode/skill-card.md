## Description:

Helps agents read blockchain data through MoltNode and obtain Chord swap quotes, simulations, and unsigned transactions for user-approved EVM trades.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tuantqse90](https://clawhub.ai/user/tuantqse90)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use this skill to look up on-chain data and prepare EVM token swap quotes and unsigned transactions for a user to review and approve.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Blockchain queries, token interests, wallet addresses, and swap intent are shared with MoltNode and Chord.

Mitigation: Use the services only when comfortable sharing this information; never provide private keys or seed phrases.

Risk: Signing a stale or incorrect approval or swap transaction can move funds unexpectedly.

Mitigation: Review the exact quote, approval, recipient, value, and simulation status; obtain explicit user confirmation before signing or broadcasting.

## Reference(s):

- [MoltNode chain reference](references/chains.md)
- [MoltNode agents](https://moltnode.ag/agents)
- [MoltNode chain catalog](https://moltnode.ag/api/chains)
- [ClawHub skill release](https://clawhub.ai/tuantqse90/skills/moltnode)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Markdown with JSON request and response details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Swap guidance may include a quote, simulation result, approval details, and unsigned transaction for user review.]

## Skill Version(s):

1.1.2 (source: ClawHub release record)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
