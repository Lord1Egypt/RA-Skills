## Description: <br>
Micro-trades altcoin 5-minute Up/Down markets when BTC leads with strong directional bias and ETH, SOL, or XRP have not caught up yet. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and trading agents use this skill to monitor Polymarket 5-minute crypto Up/Down markets and act on BTC lead-lag signals for ETH, SOL, and XRP. It defaults to simulated trading and can place live Polymarket trades only when explicitly run with the live flag. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can place real Polymarket trades and expose funds to USDC loss. <br>
Mitigation: Start in paper mode, keep the live flag disabled until limits and strategy behavior are reviewed, and use small position tunables. <br>
Risk: SIMMER_API_KEY is a sensitive credential with trading authority. <br>
Mitigation: Use a least-privileged or disposable key when available and keep it out of source control, logs, and shared prompts. <br>
Risk: The skill depends on simmer-sdk for market access and trade execution. <br>
Mitigation: Review the installed simmer-sdk package before deployment and pin dependency versions in controlled environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/diagnostikon/polymarket-micro-coin-lag-trader) <br>
- [Simmer SDK on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [Simmer SDK GitHub repository](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python command examples and runtime console output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SIMMER_API_KEY and supports configurable trading limits through environment tunables.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
