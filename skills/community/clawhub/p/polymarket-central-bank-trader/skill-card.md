## Description: <br>
Trades Polymarket prediction markets on central bank decisions, interest rates, inflation prints, and Fed/ECB/Riksbank policy moves using keyword-based discovery, conviction sizing, and paper trading by default. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to discover monetary-policy prediction markets, evaluate central-bank and macroeconomic timing signals, and place simulated or explicitly enabled live Polymarket trades through Simmer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automated trading can risk real funds when live mode is explicitly enabled. <br>
Mitigation: Keep the skill in paper mode until tested, use --live only when willing to risk funds, and set conservative position limits. <br>
Risk: SIMMER_API_KEY grants trading authority and is a sensitive credential. <br>
Mitigation: Use the least-privileged available key and keep the credential out of logs, prompts, and shared configuration. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/diagnostikon/polymarket-central-bank-trader) <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [simmer-sdk on GitHub](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Text, Configuration] <br>
**Output Format:** [Console text and Simmer SDK trade requests] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to paper trading; live Polymarket trades require the explicit --live flag and SIMMER_API_KEY.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
