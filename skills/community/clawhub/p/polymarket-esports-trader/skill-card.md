## Description: <br>
Trades esports tournament, game release, and streaming milestone prediction markets on Polymarket using configurable market filters, conviction-based sizing, and paper trading by default. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run a Simmer-managed Polymarket strategy for esports, game release, and streaming milestone prediction markets. The skill is intended to start in paper trading and requires explicit live mode before real USDC trades are placed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can place real Polymarket trades using USDC. <br>
Mitigation: Keep paper trading as the default until the strategy and position limits are reviewed, and enable live mode only intentionally. <br>
Risk: SIMMER_API_KEY grants trading authority and is a sensitive credential. <br>
Mitigation: Store the key securely, use the narrowest available scope, and rotate it if exposure is suspected. <br>
Risk: The workflow depends on simmer-sdk behavior for market discovery, configuration, and trading execution. <br>
Mitigation: Review or pin simmer-sdk before relying on live trading. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/diagnostikon/polymarket-esports-trader) <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [simmer-sdk on GitHub](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, API Calls, Guidance] <br>
**Output Format:** [Markdown guidance and Python-based trading workflow output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SIMMER_API_KEY; defaults to paper trading unless live mode is explicitly enabled.] <br>

## Skill Version(s): <br>
0.0.3 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
