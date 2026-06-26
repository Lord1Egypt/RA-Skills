## Description: <br>
Trades the lag between geopolitical escalation markets and crypto price threshold markets on Polymarket, using paper trading by default and live trading only when explicitly enabled. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and trading workflow operators use this skill to evaluate and optionally execute a Polymarket strategy that compares geopolitical escalation market probabilities with crypto threshold market probabilities. It is intended for agent-assisted market discovery, signal calculation, risk-parameter tuning, and controlled paper or live execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires SIMMER_API_KEY, which grants trading authority. <br>
Mitigation: Keep the credential private, scope access where possible, and install the skill only for intentional agent-assisted trading workflows. <br>
Risk: Live mode can place real Polymarket orders and risk USDC. <br>
Mitigation: Use paper mode first, review position-size and spread tunables, and enable --live only after accepting the financial risk. <br>
Risk: The strategy depends on a market-lag thesis that may be wrong or may stop working. <br>
Mitigation: Review the signal assumptions, monitor skipped and placed orders, and keep conservative trade-size, spread, and max-position settings. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/diagnostikon/polymarket-macro-crypto-geopolitics-trader) <br>
- [Simmer SDK on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [Simmer SDK GitHub repository](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, configuration tables, and runtime console status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can place simulated trades by default; live Polymarket orders require explicit live mode and SIMMER_API_KEY.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
