## Description:

Guides an execution agent through less common Hyperliquid actions, their constraints, and the desk's explicit boundaries for transfers, withdrawals, fees, and staking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[galleonlabs](https://clawhub.ai/user/galleonlabs)

### License/Terms of Use:

MIT

## Use Case:

Developers and execution traders use the skill to answer whether an approved ticket can use TWAPs, spot orders, cancellation scheduling, nonce and expiry protections, API wallet approval, sub-accounts, vaults, or HIP-3 dexs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security verdict is benign with medium confidence, but analysis was partial because four references in SKILL.md could not be resolved.

Mitigation: Review or resolve the referenced components before relying on their guidance.

Risk: The scheduleCancel dead-man's switch cancels protective stops as well as other open orders, potentially leaving an open position unprotected.

Mitigation: Use it only with the ticket's explicit acceptance and position context; if it fires with a position open, treat the position as unprotected and promptly reconcile and restore protection.

## Reference(s):

- [ClawHub release](https://clawhub.ai/galleonlabs/skills/hypergrok-hyperliquid-advanced)
- [Related project listed in artifact attribution](https://github.com/galleonlabs/hypergrok-trading-desk)

## Skill Output:

**Output Type(s):** [Guidance, Code, API Calls]

**Output Format:** [Markdown with Python, TypeScript, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Operational constraints and ticket-based execution safeguards]

## Skill Version(s):

1.9.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
