## Description: <br>
Trades crypto "Up or Down" 5-minute interval markets on Polymarket by detecting Morning Star and Evening Star candlestick reversal patterns, with conviction scaled by lag distance from the expected reversal price. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and trading operators can use this skill to run a paper-by-default Polymarket strategy that scans crypto 5-minute interval markets for Morning Star and Evening Star reversal patterns. Live trading is available only when explicitly enabled and requires careful limit setting because it can place real-money trades. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can place real-money Polymarket trades using a Simmer trading API key. <br>
Mitigation: Run in paper mode first, keep limits small, and enable --live only after reviewing trader.py and the configured trading parameters. <br>
Risk: The evidence security summary says some advertised volume and concurrent-position safeguards are not fully enforced by the visible code. <br>
Mitigation: Treat configured limits as controls that need manual verification, monitor orders, and avoid unattended scheduling until safeguards are confirmed. <br>
Risk: SIMMER_API_KEY grants trading authority and is a high-value credential. <br>
Mitigation: Store the key securely, scope or rotate it where supported, and avoid exposing it in logs or shared environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/diagnostikon/polymarket-candle-morning-star-trader) <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [simmer-sdk GitHub repository](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, API calls] <br>
**Output Format:** [Console logs and Simmer trading API calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SIMMER_API_KEY; defaults to paper trading unless --live is used.] <br>

## Skill Version(s): <br>
0.0.3 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
