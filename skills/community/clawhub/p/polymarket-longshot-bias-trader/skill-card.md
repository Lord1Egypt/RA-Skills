## Description: <br>
Trades Polymarket prediction markets by using price thresholds to fade low-probability longshots and back high-probability near-certainties, with paper trading by default and live trading only when explicitly enabled. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents and developers use this skill to configure and run a Simmer-based prediction-market trading strategy that scans broad Polymarket categories, proposes or places bounded paper trades by default, and can place live trades only when --live is used. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Simmer trading API key with trading authority. <br>
Mitigation: Treat SIMMER_API_KEY as a high-value credential and install only when comfortable granting that access. <br>
Risk: Running with --live can place real Polymarket trades and create financial loss. <br>
Mitigation: Start in paper mode, keep position limits low, and enable --live only after reviewing the strategy and accepting the financial risk. <br>
Risk: The strategy scans a broad market scope across categories. <br>
Mitigation: Review the configured keywords, thresholds, spread limits, volume limits, position caps, and minimum days-to-resolution before live use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/diagnostikon/polymarket-longshot-bias-trader) <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [simmer-sdk on GitHub](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Console text with trade, skip, warning, and completion status lines] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SIMMER_API_KEY. Defaults to paper trading on the sim venue; live Polymarket trading requires the explicit --live flag.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
