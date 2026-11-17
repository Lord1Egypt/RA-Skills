## Description:

Trades Polymarket prediction markets on Bitcoin, Ethereum, Solana price milestones, ETF inflows, halving events, and DeFi protocol milestones using heuristic conviction sizing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to discover crypto-related Polymarket markets, size simulated or live trade candidates, and execute them through the Simmer SDK. It is intended for users who understand prediction-market trading risk and can review heuristic strategy behavior before using live mode.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place real Polymarket trades when live mode is enabled.

Mitigation: Keep the skill in paper mode until the strategy, SDK behavior, and account limits have been independently reviewed.

Risk: SIMMER_API_KEY is a high-value trading credential.

Mitigation: Use a restricted key where possible, store it securely, and rotate it if exposure is suspected.

Risk: The strategy is a heuristic trading template, not a verified on-chain or ETF-flow model.

Mitigation: Validate signals independently and treat generated trades as proposals before committing capital.

Risk: Security evidence notes incomplete controls around liquidity, order size, and aggregate exposure.

Mitigation: Set conservative tunables for position size, spread, volume, and maximum open positions, and apply external portfolio limits before live use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diagnostikon/skills/polymarket-crypto-onchain-trader)
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk GitHub repository](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions, Python execution commands, configuration values, and runtime trade logs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SIMMER_API_KEY and simmer-sdk; defaults to simulated trading unless live mode is explicitly enabled.]

## Skill Version(s):

0.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
