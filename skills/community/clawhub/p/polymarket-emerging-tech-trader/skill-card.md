## Description:

Trades Polymarket prediction markets on Web3/DeFi milestones, NFT market recovery, metaverse adoption, humanoid robotics deployments, quantum computing breakthroughs, and synthetic biology commercialization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and traders use this skill to discover and place Polymarket trades for emerging technology markets using keyword discovery, conviction-based sizing, and configurable risk parameters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live execution can place real Polymarket trades when a live-capable SIMMER_API_KEY is used.

Mitigation: Use paper mode by default, require explicit approval before --live execution, and use a narrowly scoped key with strict spending limits.

Risk: Some advertised financial safeguards are not enforced.

Mitigation: Review market volume and open-position exposure outside the skill before allowing live trading.

Risk: Mode handling can be unsafe in reused sessions.

Mitigation: Run the trader in a fresh process for each mode and avoid importing or reusing trader.py in long-lived processes.

## Reference(s):

- [Polymarket Emerging Tech Trader on ClawHub](https://clawhub.ai/diagnostikon/skills/polymarket-emerging-tech-trader)
- [DeFiLlama](https://defillama.com/)
- [GitHub API](https://api.github.com/)
- [IBM Quantum Network](https://quantum.ibm.com/)
- [The Good Food Institute](https://gfi.org/)
- [CoinGlass NFT](https://www.coinglass.com/nft)
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk GitHub repository](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, API Calls]

**Output Format:** [Console logs, configuration values, and trade execution requests]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to paper trading; live Polymarket trades require an explicit --live flag and a SIMMER_API_KEY.]

## Skill Version(s):

0.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
