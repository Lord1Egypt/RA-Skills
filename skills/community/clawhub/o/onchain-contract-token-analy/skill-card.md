## Description:

Analyzes smart contracts, token mechanics, permissions, fee flows, upgradeability, market risks, and likely attack surfaces for ERC-20s, launchpads, vaults, staking systems, LP fee routing, ownership controls, proxy setups, and suspicious token behavior.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xrowan](https://clawhub.ai/user/0xrowan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, auditors, and analysts use this skill to structure reviews of smart contracts, tokens, protocol modules, and onchain economic flows for permissions, value movement, upgradeability, attack surface, and market-facing risks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conclusions can be stale or incomplete when live chain state, explorer data, ABI, deployment details, or offchain dependencies are missing.

Mitigation: Verify current chain or explorer data for live deployments and list missing source, ABI, deployment, or offchain dependency evidence as open questions.

Risk: Token reviews can overstate maliciousness when they rely on heuristic indicators without code-based support.

Mitigation: Distinguish confirmed code behavior from dangerous centralization, poor design, and conditional market-behavior signals.

Risk: Administrative powers can create user loss scenarios through upgrades, fee changes, pauses, blacklists, minting, rescue functions, or withdrawals.

Mitigation: Identify each privileged actor, whether the power is bounded or mutable, and the economic effect before ranking severity.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/0xrowan/skills/onchain-contract-token-analy)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with structured analysis sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings are ordered by severity and include trust model, token and fee flow, and open questions when evidence is missing.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
