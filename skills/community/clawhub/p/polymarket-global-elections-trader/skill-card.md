## Description: <br>
Trades Polymarket prediction markets on elections, referendums, and democratic events worldwide using election-system heuristics, regional information-lag signals, and configurable trading safeguards. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to discover global election-related Polymarket opportunities, size positions from configurable thresholds, and run trades in paper mode by default or live mode when explicitly enabled. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can place real Polymarket trades and create financial loss. <br>
Mitigation: Start in paper mode, keep position limits low, and enable --live only after accepting the real-money trading risk. <br>
Risk: SIMMER_API_KEY grants trading authority and is a sensitive credential. <br>
Mitigation: Use a revocable or scoped key where possible, store it securely, and rotate it if exposure is suspected. <br>
Risk: The skill depends on the external simmer-sdk package for market and trade operations. <br>
Mitigation: Verify the simmer-sdk package source before installation and review updates before running live trades. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/diagnostikon/polymarket-global-elections-trader) <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [simmer-sdk source repository](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, API calls] <br>
**Output Format:** [Console text plus Simmer/Polymarket trading actions configured through environment variables.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to paper trading; live Polymarket trading requires the --live flag, SIMMER_API_KEY, and user-controlled position, liquidity, spread, and timing limits.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
