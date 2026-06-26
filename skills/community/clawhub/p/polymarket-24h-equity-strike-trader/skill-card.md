## Description: <br>
Trades structural mispricings in equity and stock price-threshold markets by reconstructing implied probability curves across strike levels and detecting monotonicity breaks, range-sum inconsistencies, and bin-sum issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and trading automation operators use this skill to scan Polymarket equity strike-ladder markets for internally inconsistent probabilities and place simulated or explicitly enabled live trades through Simmer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can connect to a Simmer or Polymarket trading account and use a sensitive SIMMER_API_KEY. <br>
Mitigation: Keep the API key private, verify its permissions, and install only when the account connection is intended. <br>
Risk: Live mode can place real USDC trades on Polymarket. <br>
Mitigation: Start in paper mode, set conservative position limits, and use --live only after reviewing the strategy and configuration. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/diagnostikon/polymarket-24h-equity-strike-trader) <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [simmer-sdk GitHub Repository](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, API Calls, Guidance] <br>
**Output Format:** [Console text and trade API requests, with Markdown documentation for setup and risk parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to paper trading; live Polymarket trades require an explicit --live flag and SIMMER_API_KEY.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
