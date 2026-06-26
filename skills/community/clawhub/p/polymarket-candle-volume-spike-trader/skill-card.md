## Description: <br>
Detects cross-coin directional moves in Polymarket 5-minute crypto Up or Down markets and can paper-trade or live-trade lagging coins through Simmer. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and trading operators use this skill to configure an agent that monitors short-interval Polymarket crypto markets, tests the strategy in paper mode, and optionally executes live USDC trades with explicit credentials and flags. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Simmer API key that can authorize trading activity. <br>
Mitigation: Store the key securely, limit access to trusted runtimes, and rotate or revoke it if exposed. <br>
Risk: Live mode can place real USDC trades on Polymarket. <br>
Mitigation: Run in paper mode first, review position-size and max-position tunables, and enable live mode only with an explicit decision. <br>
Risk: The disclosed implementation may rely on Polymarket probability thresholds rather than independent exchange volume data despite the volume-spike framing. <br>
Mitigation: Review the strategy logic and validate it against the intended signal source before using it for live trading. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/diagnostikon/polymarket-candle-volume-spike-trader) <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [simmer-sdk GitHub repository](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown guidance with Python code and command-line usage] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses SIMMER_API_KEY and tunable risk parameters; defaults to simulated trading unless live mode is explicitly enabled.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
