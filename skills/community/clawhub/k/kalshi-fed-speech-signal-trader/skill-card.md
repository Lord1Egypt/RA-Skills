## Description: <br>
Trades Fed rate markets on Kalshi by scoring hawkish and dovish keyword signals from market question text and comparing adjusted fair probabilities with market prices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and trading agents use this skill to analyze Kalshi Fed rate markets and identify trades from hawkish or dovish keyword signals. It defaults to dry-run analysis and can execute live trades only when explicitly run with live credentials and the live flag. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can place real Kalshi trades when credentials are provided. <br>
Mitigation: Start in dry-run mode and use the live flag only after reviewing the strategy, credentials, and position limits. <br>
Risk: Trading credentials and wallet material can authorize financial activity. <br>
Mitigation: Use a scoped SIMMER_API_KEY, avoid providing SOLANA_PRIVATE_KEY unless live trading is intended, and prefer a dedicated low-balance wallet. <br>
Risk: Automated execution can compound losses if position size, trade count, or slippage settings are too loose. <br>
Mitigation: Set conservative max position, max trades per run, entry edge, slippage, and liquidity tunables before scheduling automation. <br>
Risk: Custody and execution depend on the external simmer-sdk package. <br>
Mitigation: Review simmer-sdk and its custody behavior before providing live credentials or running the skill unattended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/diagnostikon/kalshi-fed-speech-signal-trader) <br>
- [diagnostikon publisher profile](https://clawhub.ai/user/diagnostikon) <br>
- [Simmer Markets skills](https://simmer.markets/skills) <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [simmer-sdk GitHub repository](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text with optional JSON automaton report and command/configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Dry-run by default; live mode can execute Kalshi trades when credentials and the live flag are provided.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
