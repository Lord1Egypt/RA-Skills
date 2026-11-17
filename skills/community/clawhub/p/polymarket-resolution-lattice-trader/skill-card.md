## Description:

Trades Polymarket markets by detecting logical inconsistencies between related contracts such as earlier-vs-later deadlines and prerequisite-vs-downstream event chains.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run or adapt a Polymarket trading agent that searches related prediction markets for temporal and prerequisite-chain inconsistencies. It is intended for supervised configuration with paper trading as the default and live trading only after explicit enablement.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live trading can place real Polymarket orders when explicitly enabled.

Mitigation: Keep live trading disabled until the strategy and safeguards have been reviewed; start with paper trading and low configured trade limits.

Risk: Position-limit controls are not reliable enough to serve as an account-wide exposure cap.

Mitigation: Set conservative per-trade limits, monitor total account exposure outside the skill, and do not rely on SIMMER_MAX_POSITIONS as the only cap.

Risk: SIMMER_API_KEY grants trading authority.

Mitigation: Use a least-privilege key if available, store it securely, and rotate it if exposed.

Risk: The skill depends on simmer-sdk behavior for market discovery, configuration, and order placement.

Mitigation: Use a pinned, reviewed simmer-sdk version before enabling live trading.

## Reference(s):

- [ClawHub Skill Release](https://clawhub.ai/diagnostikon/skills/polymarket-resolution-lattice-trader)
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk GitHub Repository](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python execution commands and console status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces paper-trading behavior by default; live trading requires an explicit flag and valid SIMMER_API_KEY.]

## Skill Version(s):

0.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
