## Description: <br>
Trades monotonicity violations in esports Total Kills O/U market ladders on Polymarket, using configurable thresholds and position limits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and trading agents use this skill to scan esports Total Kills O/U Polymarket ladders for monotonicity breaks and place simulated or explicitly enabled live trades with configurable risk limits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can place real-money USDC orders if --live is used. <br>
Mitigation: Start in paper mode and use --live only after reviewing the strategy, thresholds, and position limits. <br>
Risk: SIMMER_API_KEY grants trading authority and is a sensitive credential. <br>
Mitigation: Store the key securely, restrict access to the runtime environment, and rotate it if exposed. <br>
Risk: The simmer-sdk dependency is not pinned in the artifact. <br>
Mitigation: Review and pin an approved simmer-sdk version before running in controlled or live environments. <br>
Risk: Market parsing or strategy errors could select unintended markets or trade the wrong side. <br>
Mitigation: Inspect paper-mode logs and keep conservative tunables for max position, spread, volume, and open positions before enabling live trading. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/diagnostikon/polymarket-ladder-esports-kills-trader) <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [simmer-sdk GitHub repository](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Console text with trade decisions, skip reasons, and configuration-driven execution behavior] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SIMMER_API_KEY and simmer-sdk; defaults to paper trading unless --live is provided.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
