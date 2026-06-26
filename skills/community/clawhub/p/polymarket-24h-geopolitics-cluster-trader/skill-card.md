## Description: <br>
Trades logical inconsistencies in geopolitical event clusters on Polymarket by detecting probability constraint violations and sizing correction trades by conviction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and trading agents use this skill to scan Polymarket geopolitical markets for logical probability inconsistencies and run paper or explicitly enabled live correction trades through Simmer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running with --live can place real USDC trades on Polymarket. <br>
Mitigation: Use paper mode first, require explicit live execution, and keep conservative position limits. <br>
Risk: SIMMER_API_KEY grants trading authority and is a high-value credential. <br>
Mitigation: Protect the key, avoid exposing it in logs or shared environments, and rotate it if disclosure is suspected. <br>
Risk: The skill depends on simmer-sdk for market access and trade execution. <br>
Mitigation: Review or pin simmer-sdk when supply-chain assurance matters. <br>
Risk: The advertised minimum-volume filter does not appear to be implemented in the code according to the security evidence. <br>
Mitigation: Do not rely on SIMMER_MIN_VOLUME alone; review candidate markets and use conservative sizing before live trading. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/diagnostikon/polymarket-24h-geopolitics-cluster-trader) <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [simmer-sdk GitHub repository](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, API calls] <br>
**Output Format:** [Console text from Python execution, configuration tunables, and Simmer trading requests] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to paper trading; live Polymarket orders require --live and SIMMER_API_KEY.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
