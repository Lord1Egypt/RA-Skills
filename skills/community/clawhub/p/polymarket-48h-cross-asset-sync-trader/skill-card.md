## Description: <br>
Trades cross-asset correlation divergences in 5-minute crypto "Up or Down" markets on Polymarket by grouping overlapping crypto market windows, identifying outliers, and sizing consensus-reversion trades by conviction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and trading agents use this skill to monitor short-duration Polymarket crypto markets, detect cross-asset divergences across synchronized time windows, and propose or place simulated trades by default. Live Polymarket trading requires explicit user action and exposes real USDC to loss. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review flags the skill as suspicious because live-trading safeguards and trade behavior may not fully match user-facing claims. <br>
Mitigation: Review the trading logic before use, run in paper mode first, and enable --live only when accepting the possibility of losing real funds. <br>
Risk: The skill requires a high-value trading credential and can place real Polymarket orders when live mode is enabled. <br>
Mitigation: Use a limited dedicated trading key where possible, keep position limits conservative, and restrict access to SIMMER_API_KEY. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/diagnostikon/polymarket-48h-cross-asset-sync-trader) <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [simmer-sdk GitHub repository](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text output and trade execution requests through simmer-sdk] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SIMMER_API_KEY; defaults to simulated trading unless run with --live.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
