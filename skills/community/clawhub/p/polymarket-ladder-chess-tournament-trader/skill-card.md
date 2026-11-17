## Description:

Trades distribution-sum violations in chess tournament winner markets on Polymarket by detecting when player winner probabilities deviate from approximately 100%.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run or adapt a paper-by-default Polymarket trading agent that groups chess tournament winner markets, checks whether their probabilities sum to approximately 100%, and proposes or places trades when configured thresholds are met.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live mode can place real USDC trades using SIMMER_API_KEY, and the security evidence reports material safety-control gaps in the live-trading path.

Mitigation: Keep paper mode as the default, review the skill before enabling --live, use limited trading credentials where possible, and validate safeguards before allowing real funds.

Risk: The security guidance says not to rely on the documented volume and open-position safeguards until they are fixed and tested.

Mitigation: Independently test trade-size, volume, spread, and open-position controls before live use, and apply external account or venue-level limits.

Risk: The skill depends on simmer-sdk for market access and trade execution.

Mitigation: Pin and review simmer-sdk before deployment, and update only after reviewing dependency changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diagnostikon/skills/polymarket-ladder-chess-tournament-trader)
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk on GitHub](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Paper trading is the default; live trading requires an explicit --live flag and SIMMER_API_KEY.]

## Skill Version(s):

0.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
