## Description:

Build atomic Polymarket combo orders by helping an agent resolve 2 or more binary market legs, preview a dry-run plan, and optionally place the combo as one signed RFQ order.

This skill is ready for commercial/non-commercial use.

## Publisher:

[simmer](https://clawhub.ai/user/simmer)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to configure, review, and run Polymarket combo slips for multi-leg binary market views. The skill supports dry-run planning by default and a live wallet-enabled placement path after user confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live mode can place real-money Polymarket combo orders from user-supplied legs, side, direction, and stake.

Mitigation: Run the dry-run path first, use a dedicated low-balance wallet, and verify every leg, side, direction, and stake before using --live.

Risk: The wallet-enabled money path depends on environment secrets, including WALLET_PRIVATE_KEY when live placement is used.

Mitigation: Keep wallet private keys out of shared environments and use only the minimum wallet balance needed for the intended trade.

Risk: Dependency versions are not fully pinned for the live trading path.

Mitigation: Pin and review dependency versions before installation or deployment.

Risk: Polymarket combos are described by the artifact as a beta product whose endpoints and behavior can change.

Mitigation: Label combo behavior as beta to users and re-check live behavior before relying on the skill for production workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/simmer/skills/polymarket-combo-builder)
- [Disclaimer](artifact/DISCLAIMER.md)
- [Example combo configuration](artifact/combo_config.example.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command snippets and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Dry-run is the default; live placement requires SIMMER_API_KEY and a configured wallet private key.]

## Skill Version(s):

0.1.1 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
