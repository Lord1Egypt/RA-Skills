## Description: <br>
Trades Polymarket markets about OnlyFans by classifying join, ban, and earnings markets, applying keyword-based trading signals, and optionally placing simulated or live orders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers can use this skill to run a supervised Polymarket trading bot focused on OnlyFans-related markets. It is intended for paper trading by default, with live trading only when explicitly enabled and funded. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can spend real funds on prediction-market trades. <br>
Mitigation: Start in paper mode, enable --live only after review, and use limited funding or a limited trading key. <br>
Risk: Market discovery may include broader or unknown OnlyFans-related markets beyond the stated strategy. <br>
Mitigation: Review candidate markets and keep conservative limits for maximum position size, open positions, spread, and minimum trade size. <br>
Risk: The SIMMER_API_KEY grants trading authority. <br>
Mitigation: Store the key securely, rotate it if exposed, and avoid using credentials with more trading authority or balance than needed. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/diagnostikon/polymarket-onlyfans-trader) <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [simmer-sdk GitHub repository](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Console logs and trading API calls controlled by environment configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Paper trading is the default; live trading requires the --live flag and a SIMMER_API_KEY.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
