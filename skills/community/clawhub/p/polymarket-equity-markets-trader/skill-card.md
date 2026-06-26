## Description: <br>
Trades Polymarket prediction markets on stock index milestones, major IPOs, earnings surprises, analyst upgrades, and company-specific financial events. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents and advanced prediction-market operators use this skill to discover equity-related Polymarket markets, size candidate trades from configured thresholds and bias logic, and execute them in paper mode by default or live mode only when explicitly enabled. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can place real Polymarket trades using USDC. <br>
Mitigation: Start in paper mode and use --live only when deliberately accepting real trading risk. <br>
Risk: SIMMER_API_KEY grants trading authority. <br>
Mitigation: Use a dedicated revocable Simmer key with the least permissions available. <br>
Risk: Automated position sizing can create larger exposure than intended if limits are loose. <br>
Mitigation: Keep position limits conservative and tune liquidity, spread, and open-position filters before live use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/diagnostikon/polymarket-equity-markets-trader) <br>
- [Simmer SDK on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [Simmer SDK GitHub repository](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, API Calls, Text] <br>
**Output Format:** [Markdown guidance, environment configuration, command-line execution, and runtime trade logs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to simulated trading unless the --live flag is provided.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
