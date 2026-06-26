## Description: <br>
Trades Polymarket prediction markets on housing prices, mortgage rates, Fed rate decisions, real estate crash scenarios, and regional property market milestones using macro housing signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents and developers use this skill to discover housing and rate-related Polymarket markets, size positions from configurable risk parameters, and execute paper or explicitly authorized live trades. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automated live trading can place real USDC trades when the skill is run with --live. <br>
Mitigation: Start in paper mode and use --live only when intentionally authorizing live Polymarket trading. <br>
Risk: SIMMER_API_KEY provides trading authority. <br>
Mitigation: Protect and limit the key, store it outside prompts and logs, and rotate it if exposed. <br>
Risk: The simmer-sdk dependency is unpinned in the artifact. <br>
Mitigation: Review and pin the dependency before live deployment. <br>


## Reference(s): <br>
- [Polymarket Real Estate Trader on ClawHub](https://clawhub.ai/diagnostikon/polymarket-real-estate-trader) <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [simmer-sdk GitHub repository](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, API calls] <br>
**Output Format:** [Console text, configuration values, and Simmer SDK trade requests] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to paper trading; live Polymarket orders require the explicit --live flag and SIMMER_API_KEY.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
