## Description: <br>
Trades mean reversion on geopolitical prediction markets pushed to probability extremes by breaking news, using time-to-resolution staleness to size conviction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and trading agents use this skill to find geopolitical prediction markets at extreme probabilities and run paper or live mean-reversion trades through Simmer/Polymarket with configurable risk limits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can place real-money Polymarket trades using a high-value SIMMER_API_KEY. <br>
Mitigation: Start in paper mode, use dedicated low-balance credentials where possible, set external position and spend limits, and enable --live only after reviewing the strategy. <br>
Risk: Automated trading may act on incorrect market signals or stale geopolitical assumptions. <br>
Mitigation: Review candidate trades and tune position size, spread, volume, days-to-resolution, and open-position limits before production use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/diagnostikon/polymarket-geopolitics-sentiment-reversal-trader) <br>
- [Artifact skill documentation](artifact/SKILL.md) <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [simmer-sdk on GitHub](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance, API calls] <br>
**Output Format:** [Markdown guidance with Python command examples and runtime trade/log output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SIMMER_API_KEY; defaults to paper trading unless --live is used; tunables constrain trade size, spread, volume, and open positions.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release evidence; artifact metadata reports 1.0.0 and clawhub.json reports 0.0.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
